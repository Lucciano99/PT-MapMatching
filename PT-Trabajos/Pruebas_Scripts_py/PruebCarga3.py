import os

from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsApplication,
)

from qgis.core import QgsApplication
from qgis.utils import iface #Por siacaso en caso de 
#from qgis.analysis import QgsGeometryAnalyzer PARA LAS VERSIONES 3.X NO SIRVE
from qgis import processing 


################
###Parametros###
################

#Buffer
#searchRadius_list= []
#Rango de tolerancia de velocidad
#tolerancia_V= [15,20,35,45,55]
#frecuencia de muestreo(Lo que emite en cada intervalo de tiempo?)
#samp_freq_List = [10]

################
###Diccionarios#
################

#Diccionario de resultados
d_res={}
#Diccionario con cantidad de puntos gps
d_gps={}

qgs = QgsApplication([], False) #Se especifica que no se trabajara con la GUI
QgsApplication.setPrefixPath(".local/share/QGIS/QGIS3", True)
QgsApplication.initQgis()
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), "->", alg.displayName())


dir_Archivo_Vectores = '/home/lucciano/git_Proyecto/CapaPrueba/Capa_T434_34.shp' #Hay que cambiarlo # Carga de capas GPS a probar
Cap_temporal= '/home/lucciano/git_Proyecto/CapaPrueba/Capa_temporal.shp' #Capa temporal para utilizar los buffer
dir_redVial= '/home/lucciano/git_Proyecto/Cargas_de_Capas/Redvial/RedVialComunasSantiago.shp' # Carga redVial

vlayer = QgsVectorLayer(dir_Archivo_Vectores, "Capa_Prueba1", "ogr")
roadway = QgsVectorLayer(dir_redVial, "RedVial", "ogr")
temporal= QgsVectorLayer(Cap_temporal, "Capa_temporal", "org")


if vlayer.isValid() == False and roadway.isValid() == False:       #not vlayer.isValid() || 
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)
    QgsProject.instance().addMapLayer(roadway)
    QgsProject.instance().addMapLayer(temporal)



#Se crea la capa vacia, ahora ver como ingresar los puntos

#Prepara la capa temporal para editar
#temporal.startEditing()
vlayer.startEditing()


features= vlayer.getFeatures() 
rw = roadway.getFeatures()


def gpsDataCapa(features):
    for aux_dic in features:
        geo_coordenada = aux_dic.geometry()
        atributos= aux_dic.attributes()
        
    
        #atri_list=[]

        #for aux_list in atributos:
            #atri_list=[aux_list]
            #print(atri_list)            

       
        #for aux_list in atri_list:

            #aux_list=atri_list[atributos]

        #print(atributos)
        #print(atributos[0][1])
        
        dic_gps={}

        key_list= ['X', 'Y', 'Velocidad']  #Por mientras almacenar NeaFID pero sin ocupar 
        value_list = [geo_coordenada.asPoint().x(), geo_coordenada.asPoint().y(), atributos[14]] #0, X, Y , 14, 18
        
        dic_gps[atributos[0]]=dict(zip(key_list, value_list))
        
        #diccionario_gps = dic_gps.keys() Me muestra las llaves del diccionario dic_gps

        print (dic_gps)

        

        #return dic_gps

#gpsDataCapa(features)

dic_resultadoBuff={}

dic_resultadoBuff= processing.run("native:buffer", {'INPUT': 'Capa_Prueba1',
    'DISTANCE': 100.0,
    'SEGMENTS': 5,
    'DISSOLVE': True,
    'END_CAP_STYLE': 0,
    'JOIN_STYLE': 0,
    'MITER_LIMIT': 10,
    'OUTPUT': 'Capa_temporal'
    })



