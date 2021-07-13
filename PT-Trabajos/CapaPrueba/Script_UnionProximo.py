import processing
import os
from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsApplication,
 QgsProcessing
)


CapPoint='/home/lucciano/git_Proyecto/CapaPrueba/Capa_T434_34_X_Y.shp'
CapLine='/home/lucciano/git_Proyecto/Cargas_de_Capas/Redvial/RedVialComunasSantiago.shp'
#CapOut='/home/lucciano/git_Proyecto/CapaPrueba/Resultado2.shp'
CapOut2='/home/lucciano/git_Proyecto/CapasResultante_UAP/Test1.shp'

processing.run("native:joinbynearest",\
{'INPUT':CapPoint,\
'INPUT_2': CapLine, \
'FIELDS_TO_COPY':['Recorrido'], \
'DISCARD_NONMATCHING':False, \
'PREFIX':'joined_', \
'NEIGHBORS':1, \
'MAX_DISTANCE':7, \
'OUTPUT': CapOut2})

iface.addVectorLayer(CapOut2, 'Test1' ,'org')

