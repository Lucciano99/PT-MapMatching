
import os

from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsApplication
)

from qgis.core import QgsApplication

qgs = QgsApplication([], False) #Se especifica que no se trabajara con la GUI
QgsApplication.setPrefixPath(".local/share/QGIS/QGIS3", True)
QgsApplication.initQgis()
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), "->", alg.displayName())


dir_Archivo_Vectores = '/home/lucciano/git_Proyecto/CapaPrueba/Capa_T434_34.shp' #Hay que cambiarlo
vlayer = QgsVectorLayer(dir_Archivo_Vectores, "Capa_Prueba1", "ogr")

if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)




dic_vect={} #Diccionario de vectores


features= vlayer.getFeatures()

#####################################################################################

def gpsDataCapa(features):
    for aux_dic in features:
        geo_coordenada = aux_dic.geometry()
        attr= aux_dic.attributes()
        
        dic_gps={}


        key_list= ['X', 'Y', 'Distancia', 'Velocidad', 'NeaFID']  
        value_list = [geo_coordenada.asPoint().x(), geo_coordenada.asPoint().y(), attr[11], attr[14], attr[18]] #0, X, Y, 11 , 14, 18
        
        dic_gps[attr[0]]=dict(zip(key_list, value_list))

        diccionario_gps = dic_gps.keys()

        #dic_vect={'ObjectID':aux_dic['OBJECTID'], 'X':geo_coordenada.asPoint().x(), 'Y': geo_coordenada.asPoint().y()
    #, 'Distancia':aux_dic['DISTANCIA'], 'Velocidad':aux_dic['VELOCIDAD'], 'NeaFID': aux_dic['Near_FID']}
        print(diccionario_gps)
      



#def recorre_dic(dic_vect):
	#for i in dic_vect:
		#print(i, ":", dic_vect[i])

gpsDataCapa(features)






