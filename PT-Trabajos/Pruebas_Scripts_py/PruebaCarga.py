
import os

from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsApplication
)

#from .Funcion import recorre_dic
#from qgis.utils import iface

from qgis.core import QgsApplication
#from qgis.utils import QgsGeometryAnalyzer
from qgis.utils import iface #Por siacaso en caso de 


qgs = QgsApplication([], False) #Se especifica que no se trabajara con la GUI
QgsApplication.setPrefixPath(".local/share/QGIS/QGIS3", True)
QgsApplication.initQgis()
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), "->", alg.displayName())


dir_Archivo_Vectores = '/home/lucciano/git_Proyecto/CapaPrueba/Capa_T434_34.shp' #Hay que cambiarlo
dir_Archivo_Vectores_temporal='/home/lucciano/git_Proyecto/CapaPrueba/Capa_Temporal_2'
vlayer = QgsVectorLayer(dir_Archivo_Vectores, "Capa_Prueba1", "ogr")


if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer,False)

#Obtiene el arbol de capas del grupoo de nivel en el proyecto
layerTree= iface.layerTreeCanvasBridge().rootGroup()
layerTree.insertChildNode(-1, QgsLayerTreeLayer(vlayer))


features= vlayer.getFeatures()

for feat in features:
    
    #print("OBJECTID: ", feat['OBJECTID']) Modo de ejemplo muestra todo los OBJECTID de la capa
    #print(feat) Muestra los atributos del objeto
    #attr= feat.attributes() #Muestra todos los atributos en una lista
    #print(attr)
    geo= feat.geometry() #Para acceder a las coordenadas del verctor
    #print(geo.asPoint()) #Muestra la coordenadas del objeto geo
    #print(geo.asPoint().x()) #Muestra la coordenada del elemento X como ejemplo
    dic_vect={}
    dic_vect[feat['OBJECTID']]={'X':geo.asPoint().x(), 'Y': geo.asPoint().y()
    , 'Velocidad':feat['VELOCIDAD']}

    print(dic_vect)








        









