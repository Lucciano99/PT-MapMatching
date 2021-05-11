
import os 

from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsRasterLayer
)

#from qgis.utils import iface

from qgis.core import *

qgs = QgsApplication([], False) #Se especifica que no se trabajara con la GUI
QgsApplication.setPrefixPath(".local/share/QGIS/QGIS3", True)
QgsApplication.initQgis()
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), "->", alg.displayName())


dir_Archivo_Vectores = "/home/pt2021/PT-Trabajos/CapasPruebas"



vlayer = QgsVectorLayer(dir_Archivo_Vectores, "Capa_Prueba1", "ogr")

if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)


#for field in vlayer.fields():  #Muestra toda la informacion del objeto vlayer
#   print(field.name(), field.typeName())

dic_vect={} #Diccionario de vectores
dic_ejes={} #Diccionario de posiciones o coordenadas

#vlayer= iface.activeLayer()
features= vlayer.getFeatures()

for feat in features:
    
    #print("OBJECTID: ", feat['OBJECTID']) Modo de ejemplo muestra todo los OBJECTID de la capa
    #print(feat) Muestra los atributos del objeto
    attr= feat.attributes() #Muestra todos los atributos en una lista
    print(attr)
    geo= feat.geometry() #Para acceder a las coordenadas del verctor
    #print(geo.asPoint()) #Muestra la coordenadas del objeto geo
    #print(geo.asPoint().x()) #Muestra la coordenada del elemento X como ejemplo
    dic_vect={'ObjectID':feat['OBJECTID'], 'X':geo.asPoint().x()}
    #print(dic_vect)












