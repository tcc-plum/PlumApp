import os
import glob
import pyrebase
import datetime
import json
#from PlumApp.sky_biometry import SkyBiometry

class WorkFiles:
        
        RAIZ = './PlumApp/cluster'
        #biometry = SkyBiometry()
        
        FIREBASE_KEY = "AIzaSyBYZqhEllq8-vN0XN_yBpav54CCVGRHq9E"
        FIREBASE_AUTH = "teste-tcc-2c7b3.firebaseapp.com"
        FIREBASE_DATABASE = "https://teste-tcc-2c7b3.firebaseio.com/"
        FIREBASE_STORAGE = "teste-tcc-2c7b3.appspot.com"
        
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

        def loadAllImagesToFirebase(self, biometry):
                ## apagar todos os dados do firebase
                self.f_db.child("cluster").remove()
                self.f_db.child("sky").remove()
                
                if not os.path.exists(self.RAIZ):
                        return False
                else:
                        ## sobe todos os dados de cada cluster para o firebase
                        for pasta in os.listdir(self.RAIZ):
                                diretorio = self.RAIZ + '/' + pasta
                                dataNome = self.getCurrentDateAsId()
                                arquivos = glob.glob(diretorio + '/*.jpg')
                                print('[INFO]: Cluster: ' + pasta)
                                count = 5
                                for arquivo in arquivos:
                                        if count > 0 and count <= 5:
                                        
                                                log = str(arquivos.index(arquivo) + 1) + '/' + str(len(arquivos))
                                                
                                                arquivo_local = arquivo.replace(os.sep,'/')
                                                list_arquivo = arquivo_local.split(sep='/')
                                                arquivo_firebase = list_arquivo[1] + '/' + list_arquivo[3]
                                                path_id = list_arquivo[2] + '_' + dataNome
                                                resultado = self.storage.child(arquivo_firebase).put(arquivo_local, self.FIREBASE_KEY)
                                                url_imagem = self.storage.child(arquivo_firebase).get_url(self.FIREBASE_KEY)
                                                resultado['img_url'] = url_imagem
                                                resultado['path_local'] = arquivo_local
                                                resultado['path_cloud'] = arquivo_firebase
                                                resultado['path_id'] = path_id
                                                caminho_json = 'cluster' + '/' + path_id
                                                ## consulta sky
                                                biometry = biometry.skyBiometry(arquivo_local, url_imagem, path_id, log)
                                                ## salva no banco de dados
                                                if biometry:
                                                        resultado_banco = self.f_db.child(caminho_json).push(resultado)
                                                        count -= 1
                                        else:
                                             break   
                        return True
        
        def listAllClusters(self):
                resposta = self.f_db.child("cluster").get().val()
                return dict(resposta)
        
        def listImagesFromCluster(self, cluster):
                resposta = dict(self.f_db.child("cluster/" + cluster.lower()).get().val())
                urls = []
                for k, v in resposta.items():
                        urls.append(v['img_url'])
                return urls
        
        def listAllImages(self):
                urls = []
                resposta = dict(self.f_db.child("cluster").get().val())
                for k,v in resposta.items():
                        lista = self.listImagesFromCluster(k)
                        for item in lista:
                                urls.append(item)
                return urls