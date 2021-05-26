
import os

from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsApplication
)

from qgis.core import QgsApplication
  
################
###Parametros###
################

#Buffer
searchRadius_list= []
#Rango de tolerancia de velocidad
tolerancia_V= [15,20,35,45,55]
#frecuencia de muestreo(Lo que emite en cada intervalo de tiempo?)
samp_freq_List = [10]


qgs = QgsApplication([], False) #Se especifica que no se trabajara con la GUI
QgsApplication.setPrefixPath(".local/share/QGIS/QGIS3", True)
QgsApplication.initQgis()
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), "->", alg.displayName())


dir_Archivo_Vectores = '/home/lucciano/git_Proyecto/CapaPrueba/Capa_T434_34.shp' #Hay que cambiarlo # Carga de capas GPS a probar
dir_redVial= '/home/lucciano/git_Proyecto/Cargas_de_Capas/Redvial/RedVialComunasSantiago.shp' # Carga redVial

vlayer = QgsVectorLayer(dir_Archivo_Vectores, "Capa_Prueba1", "ogr")
roadway = QgsVectorLayer(dir_redVial, "RedVial", "ogr")


if vlayer.isValid() == False and roadway.isValid() == False:       #not vlayer.isValid() || 
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)
    QgsProject.instance().addMapLayer(roadway)


#######################################################################
## Obtiene toda la informacion (atributos) de los objeto capas creados#
#######################################################################

features= vlayer.getFeatures() 
rw = roadway.getFeatures()


def gpsDataCapa(features):
    for aux_dic in features:
        geo_coordenada = aux_dic.geometry()
        atributos= aux_dic.attributes()
        
        dic_gps={}


        key_list= ['X', 'Y', 'Distancia', 'Velocidad', 'NeaFID']  
        value_list = [geo_coordenada.asPoint().x(), geo_coordenada.asPoint().y(), atributos[11], atributos[14], atributos[18]] #0, X, Y, 11 , 14, 18
        
        dic_gps[atributos[0]]=dict(zip(key_list, value_list))

        #diccionario_gps = dic_gps.keys() Me muestra las llaves del diccionario dic_gps

        print(dic_gps.keys())
        return dic_gps 




def near_segments(index,tempData, rw, tempTable, searchRadius, dic_gps, snapDict):
    nearList= []


for samp_freq in samp_freq_List:
    #Como crear el objeto geoprocesamiento o como ocupar sus herramientas para el analisis

    serie_List= range(1, samp_freq/10 + 1) # Crea una lista correspondiente al rango de 1 a 


gpsDataCapa(features)





