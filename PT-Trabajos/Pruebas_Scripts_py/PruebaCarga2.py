import os
#import qgis
#import sys

from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsApplication,
)



from qgis.core import QgsApplication
#from qgis.utils import iface #Por siacaso 
#from qgis.analysis import QgsGeometryAnalyzer PARA LAS VERSIONES 3.X NO SIRVE
#from qgis import processing 
#from qgis import utils



qgs = QgsApplication([], False) #Se especifica que no se trabajara con la GUI
QgsApplication.setPrefixPath(".local/share/QGIS/QGIS3", True)
QgsApplication.initQgis()
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), "->", alg.displayName())


dir_Archivo_Vectores = '/home/lucciano/git_Proyecto/CapaPrueba/Capa_T434_34.shp' #Hay que cambiarlo # Carga de capas GPS a probar
Cap_temporal= '/home/lucciano/git_Proyecto/CapaPrueba/Prueba_Punto_Buffer.shp' #Capa temporal prueba de buffer punto creados
dir_redVial= '/home/lucciano/git_Proyecto/Cargas_de_Capas/Redvial/RedVialComunasSantiago.shp' # Carga redVial

vlayer = QgsVectorLayer(dir_Archivo_Vectores, "Capa_Prueba1", "ogr")
roadway = QgsVectorLayer(dir_redVial, "RedVial", "ogr")
temporal= QgsVectorLayer(Cap_temporal, "Prueba_Punto", "org")


if vlayer.isValid() == False:       #not vlayer.isValid() || 
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)
    #QgsProject.instance().addMapLayer(roadway)
    #QgsProject.instance().addMapLayer(temporal)



features= vlayer.getFeatures() 

def gpsDataCapa(features):
    dic_gps={}
    for aux_dic in features:
        geo_coordenada = aux_dic.geometry()
        atributos= aux_dic.attributes()       

        
        key_list= ['X', 'Y', 'Velocidad']  #Por mientras almacenar NeaFID pero sin ocupar 
        value_list = [geo_coordenada.asPoint().x(), geo_coordenada.asPoint().y(), atributos[14]] #0, X, Y , 14, 18
        dic_gps[atributos[0]]=dict(zip(key_list, value_list))
        #diccionario_gps = dic_gps.keys() Me muestra las llaves del diccionario dic_gps

    return dic_gps

