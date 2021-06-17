
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


dir_Archivo_Vectores = '/home/lucciano/git_Proyecto/CapaPrueba/Capa_T434_34.shp'
Cap_temporal= '/home/lucciano/git_Proyecto/CapaPrueba/Prueba_Punto_Buffer.shp' #Capa temporal prueba de buffer punto creados

vlayer = QgsVectorLayer(dir_Archivo_Vectores, "Capa_Prueba1", "ogr")
temporal= QgsVectorLayer(Cap_temporal, "Prueba_Punto", "org")


if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer,False)
    QgsProject.instance().addMapLayer(temporal,False)




features= vlayer.getFeatures()
features_temp= temporal.getFeatures()

for aux_feat in features_temp:

    print(aux_feat)
    geo_temp=aux_feat.geometry()
    print(geo_temp)

    buffer_distance=100
    bf_geoTemp= geo_temp.buffer(buffer_distance, -1)
    firstpoint= geo_temp.interpolat(0)
    print(bf_geoTemp)  



for feat in features:
    
    #print("OBJECTID: ", feat['OBJECTID']) Modo de ejemplo muestra todo los OBJECTID de la capa
    #print(feat) Muestra los atributos del objeto
    #attr= feat.attributes() #Muestra todos los atributos en una lista
    #print(attr)
    geo= feat.geometry() #Para acceder a las coordenadas del vector
    #print(geo.asPoint()) #Muestra la coordenadas del objeto geo
    #print(geo.asPoint().x()) #Muestra la coordenada del elemento X como ejemplo
    #print(geo.asPoint().y()) #Muestra la coordenada del elemento Y como ejemplo

    buffer_distance=100
    bf_geom=geo.buffer(buffer_distance, -1)
    firstpoint= geo.interpolate(0)
    #print(bf_geom)

    dic_vect={}
    dic_vect[feat['OBJECTID']]={'X':geo.asPoint().x(), 'Y': geo.asPoint().y()
    , 'Velocidad':feat['VELOCIDAD']}

    #print(dic_vect)







'''
for i in coor:
    coor_XY= coor['X']['Y']

print(coor_XY)
'''


'''
buffer_distance=100
bf_geo=.buffer(buffer_distance, -1)
firstpoint= .interpolate(0)
print(bf_geo)
'''

'''
buffer_distance=100

bf_geom=gpsDataCapa(features).buffer(buffer_distance, -1)
firstpoint= gpsDataCapa(features).interpolate(0)
print(bf_geom)
'''









        









