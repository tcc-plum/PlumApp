# libraries
import cv2
import datetime
import json
import os
import pyrebase
#from PlumApp.clusterization import FaceClusterization

class FaceStreaming:

    # constants
    FIREBASE_KEY = "AIzaSyBYZqhEllq8-vN0XN_yBpav54CCVGRHq9E"
    FIREBASE_AUTH = "teste-tcc-2c7b3.firebaseapp.com"
    FIREBASE_DATABASE = "https://teste-tcc-2c7b3.firebaseio.com/"
    FIREBASE_STORAGE = "teste-tcc-2c7b3.appspot.com"

    # constructor
    def __init__(self):
        __self__ = self

    # setting up Firebase application
    k_fields = ["apiKey", "authDomain", "databaseURL", "storageBucket"]
    v_fields = [FIREBASE_KEY, FIREBASE_AUTH, FIREBASE_DATABASE, FIREBASE_STORAGE]

    config = dict(zip(k_fields, v_fields))

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    f_db = firebase.database()

    def getCurrentDateAsId(self):
        cur_date_str = json.dumps(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
        cur_date_str = cur_date_str.replace('"', '')
        return cur_date_str

    def getCurrentDateAsFolderName(self):
        cur_date_str_1 = json.dumps(datetime.datetime.now().strftime('%Y%m%d'))
        cur_date_str_1 = cur_date_str_1.replace('"', '')
        return cur_date_str_1

    # load image to Firebase storage
    def loadToFirebaseStorage(self, filename, f_key, f_storage):
        f_storage_path = "frames/" + str(self.getCurrentDateAsFolderName()) + "/" + filename
        l_filepath = './frames/' + filename
        result = f_storage.child(f_storage_path).put(l_filepath, f_key)
        os.remove(l_filepath)
        return result

    # using realtime video
    def faceFromStreamingVideo(self, fc):
        classifier_1 = cv2.CascadeClassifier('./PlumApp/train_data/haarcascade_frontalface_default.xml')

        video_capture = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = classifier_1.detectMultiScale(gray, flags=cv2.CASCADE_SCALE_IMAGE)

            for face in faces:
                # detect the vertices and the size of the rectangle in which the face lies.
                x_axis, y_axis, width, height = [vertice for vertice in face]

                # draw a rectangle in the face using the RGB (255,0,222)
                cv2.rectangle(frame, (x_axis, y_axis), (x_axis + width, y_axis + height), (255, 0, 222), 2)

                # get the sub faces for the entire image
                sub_face = frame[y_axis:y_axis + height, x_axis:x_axis + width]

                # indicates the file name and store in the indicated path
                if not os.path.exists('./PlumApp/frames'):
                    os.makedirs('./PlumApp/frames')

                frame_name = "face_" + self.getCurrentDateAsId() + ".jpg"
                sub_face_f_name = "./PlumApp/frames/" + frame_name

                # saves the detected face locally
                cv2.imwrite(sub_face_f_name, sub_face)

                # push frame to Firebase and remove from local device
                # self.loadToFirebaseStorage(frame_name, FIREBASE_KEY, storage)

            # Display the resulting frame
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                #fc = FaceClusterization()
                resultado = fc.cluster('./PlumApp/frames', './PlumApp/cluster')
                break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()
        return resultado