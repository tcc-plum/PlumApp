from pkg_resources import resource_filename


def shape_predictor_5():
    return resource_filename(__name__, "dlib_models/shape_predictor_5_face_landmarks.dat")

def dlib_face_recognition():
    return resource_filename(__name__, "dlib_models/dlib_face_recognition_resnet_model_v1.dat")

def human_face_detector():
    return resource_filename(__name__, "dlib_models/mmod_human_face_detector.dat")