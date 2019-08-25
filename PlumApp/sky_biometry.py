# libraries
from PIL import Image
import requests
from io import BytesIO
import pyrebase
import datetime
import json
import os

class SkyBiometry(object):
	# constants
		## chave do William
		SKY_API_KEY = "7spe2on6kr9bva7b7m5hrokc31"
		# SKY_API_SECRET = "1s00ucu8ijg98flecmaqnhpi8g"
		## chave do Kaue
		# SKY_API_SECRET = "1s00ucu8ijg98flecmaqnhpi8g" # SKY_API_SECRET =
		# "l9kus97mjm2cs0d5jup2ird06m"
		
		## chave do projeto
		# SKY_API_KEY = "cqm6psmc935f0svh5igl162kc9"
		# SKY_API_SECRET = "vj06aa6179mffof6h9mfvkrhcm"
		FIREBASE_KEY = "AIzaSyBYZqhEllq8-vN0XN_yBpav54CCVGRHq9E"
		FIREBASE_AUTH = "teste-tcc-2c7b3.firebaseapp.com"
		FIREBASE_DATABASE = "https://teste-tcc-2c7b3.firebaseio.com/"
		FIREBASE_STORAGE = "teste-tcc-2c7b3.appspot.com"

		# def __init__(self, url_image):
		#			self.url_image = url_image
				
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

		# load image to Firebase storage
		def loadToFirebaseStorage(self, image, filename, f_key, f_storage):
				# load image to Firebase storage
				l_storage_file = filename + ".jpg"
				f_storage_path = "sky/" + l_storage_file

				if not os.path.exists('./img'):
						os.makedirs('./img')

				l_storage_path = './img/' + l_storage_file

				image.save(l_storage_path, "JPEG")

				result = f_storage.child(f_storage_path).put(l_storage_path, f_key)

				# remove picture from the local storage
				os.remove(l_storage_path)

				return result

		# load json to Firebase database
		def loadToFirebaseDatabase(self, f_db, json_file):
				result_db = f_db.child("sky").push(json_file)
				return result_db

		def skyBiometry(self, url_image, f_url_image, cluster_id, log):
				# read image from url
				# image_http = requests.get(url_image)
				# image = Image.open(BytesIO(image_http.content))

				# using Sky Biometry API for face detect
				# url_sky_biometry = [
				#			"https://api.skybiometry.com/fc/faces/detect.json?api_key=" +
				#			self.SKY_API_KEY +
				#			"&api_secret=" + self.SKY_API_SECRET +
				#			"&urls=" + url_image + "&attributes=all"]
				url_sky_biometry = ["https://api.skybiometry.com/fc/faces/detect.json?api_key=" + self.SKY_API_KEY + "&api_secret=" + self.SKY_API_SECRET + "&attributes=all"]
				
				# sky_biometry = requests.get(url_sky_biometry[0]).json()
				sky_biometry = requests.post(url_sky_biometry[0], files = {'media': open(url_image, 'rb')}).json()

				sky_biometry['current_date'] = self.getCurrentDateAsId()
				sky_biometry['dev_type'] = 'entrance'
				sky_biometry['img_url'] = url_image
				sky_biometry['f_url_img'] = f_url_image
				sky_biometry['cluster_id'] = cluster_id

				# pid = sky_biometry['operation_id']

				# self.loadToFirebaseStorage(image, pid, self.FIREBASE_KEY, self.storage)
				try:
						if sky_biometry['status'] == 'success' and len(sky_biometry['photos'][0]['tags']) > 0:
								self.loadToFirebaseDatabase(self.f_db, sky_biometry)
								print('[INFO]: ' + log + ' Inserido OK')
						else:
								print('[WARNING]: ' + log + ' Falta tag ou não é sucesso')
								return False
				except:
						print('[ERROR]: ' + log + ' Documento não inserido')
				# print(sky_biometry)
				return sky_biometry

		def listAllData(self):
			try:
				resposta = self.f_db.child("sky").get().val()
				print(dict(resposta))
			except:
				print('Não foi possível capturar imagem do Firebase')
			return dict(resposta) 

		def listData(self, document_id):
			try:
				resposta = self.f_db.child("sky" + '/' + document_id).get().val()
			except:
				print('Não foi possível capturar imagem do Firebase')
			return dict(resposta) 