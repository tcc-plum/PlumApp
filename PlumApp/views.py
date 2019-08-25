"""
Routes and views for the flask application.
"""

from flask import render_template
from PlumApp import app
## owned packages
from PlumApp.work_files import WorkFiles
from PlumApp.sky_biometry import SkyBiometry
from PlumApp.face_streaming import FaceStreaming
from PlumApp.clusterization import FaceClusterization

biometry = SkyBiometry()

@app.route('/')
@app.route('/index')
def index():
		#biometry = SkyBiometry()
		try:
				sky_resultados = biometry.listAllData().decode('utf-8')
		except:
				sky_resultados = []

		if len(sky_resultados) == 0:
				return render_template('vazia.html', title='Home', label='Perfis', texto='Sem dados sobre os perfis')
		else:
				return render_template('index.html', title='Home', dados=sky_resultados)

@app.route('/cluster')
def cluster():
		wf = WorkFiles()
		try:
				clusters = wf.listAllClusters()
				pastas = []
				total_frames = 0
				for k, v in clusters.items():
						pastas.append(k)
						total_frames += len(v)
		except:
				clusters = []
				
		if len(clusters) == 0:
				return render_template('vazia.html', title='Cluster', label='Clusters', texto='Sem dados sobre os clusters')
		else:
				return render_template('cluster.html', title='Cluster', clusters=clusters, quantidade=len(pastas), total_frames=total_frames)

@app.route('/cluster/<pasta>')
def cluster_pasta(pasta):
		wf = WorkFiles()
		imagens = wf.listImagesFromCluster(pasta)
		return render_template('pasta.html', title='Pasta', imagens=imagens, pasta=pasta)


@app.route('/camera/', methods=['POST'])
def camera():
		streaming = FaceStreaming()

		if streaming.faceFromStreamingVideo(FaceClusterization()):
				return render_template('resultado.html', title='Camera', label='Camera', texto='Frames capturados e clusterizados com sucesso')
		else:
				return render_template('resultado.html', title='Erro', label='Camera', texto='Não foi possível capturar os frames')
				
@app.route('/push', methods=['POST'])
def push_firebase():
		wf = WorkFiles()

		if wf.loadAllImagesToFirebase(biometry):
				return cluster()
		else:
				return render_template('resultado.html', title='Erro', label='Clusters', texto='Clusters não identificados')
	