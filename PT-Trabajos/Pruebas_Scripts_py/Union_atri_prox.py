
import os
import PyQt5.QtCore
import sys


from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsApplication,
 QgsProcessingFeedback
)

from qgis.utils import iface #Por siacaso en caso de 
from qgis.analysis import QgsNativeAlgorithms

qgs = QgsApplication([], False) #Se especifica que no se trabajara con la GUI
qgs.setPrefixPath(".local/share/QGIS/QGIS3", True)
qgs.initQgis()
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), "->", alg.displayName())


capPoint= '/home/lucciano/git_Proyecto/CapaPrueba/Capa_T434_34_X_Y.shp'
capLine= '/home/lucciano/git_Proyecto/CapaPrueba/RedVialPrueba.shp' #Capa temporal prueba de buffer punto creados
capOut='home/lucciano/git_Proyecto/CapaPrueba/ResultadoSinGUI.shp'

vlayer = QgsVectorLayer(capPoint, "Capa_Punto", "ogr")
temporal= QgsVectorLayer(capLine, "Capa_Linea", "org")


if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer,False)
    QgsProject.instance().addMapLayer(temporal,False)

features= vlayer.getFeatures()
features_temp= temporal.getFeatures()

#sys.path.append('home/lucciano/.local/share/QGIS/QGIS3/profiles/default/python/plugins')
sys.path.append('home/lucciano/.local/share/QGIS/QGIS3/profiles/default/python/expressions')
import processing
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

processing.run("native:joinbynearest",\
{'INPUT':capPoint,\
'INPUT_2': capLine,\
'FIELDS_TO_COPY':[''],\
'DISCARD_NONMATCHING':False,\
'PREFIX':'joined_',\
'NEIGHBORS':1,\
'MAX_DISTANCE':7,\
'OUTPUT': capOut})

iface.addVectorLayer(capOut, '' ,'org')







        









