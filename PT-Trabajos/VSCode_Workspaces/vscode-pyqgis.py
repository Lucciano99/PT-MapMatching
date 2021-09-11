import sys

from qgis.core import (
 QgsProject,
 QgsApplication
)

from qgis.core import*
from PyQt5.QtGui import*

from processing.core import Processing

from qgis.utils import iface 

QgsApplication.setPrefixPath(".local/share/QGIS/QGIS3", True)

capPunto='/home/lucciano/Trabajo PT/CapaPrueba/Capa_T434_34.shp'
capLinea= '/home/lucciano/Trabajo PT/Cargas_de_Capas/Redvial/RedVialComunasSantiago.shp'
capOut='/home/lucciano/Trabajo PT/Carpeta_Temporal_Prueba_ProcesoHerramienta/resultado.shp'
capOutSnap='/home/lucciano/Trabajo PT/Carpeta_Temporal_Prueba_ProcesoHerramienta/resultado_snap.shp'
capSegmento='/home/lucciano/Trabajo PT/Carpeta_Temporal_Prueba_ProcesoHerramienta/segmento_snap.shp'

#capa1=QgsVectorLayer(capResultado, "Capa_Punto", "ogr")
#capa2=QgsVectorLayer(capOutput, "Red_vial", "ogr")

#if not capa1.isValid():
    #print("Layer failed to load!")
#else:
    #QgsProject.instance().addMapLayer([capa1,capa2])

Processing.run("native:joinbynearest",\
{'INPUT':capPunto,\
'INPUT_2':capLinea,\
'FIELDS_TO_COPY':[],\
'DISCARD_NONMATCHING':False,\
'PREFIX':'',\
'NEIGHBORS':1,\
'MAX_DISTANCE':200,\
'OUTPUT':capOut})

linea= iface.addVectorLayer(capLinea, '' , 'ogr')
Punto= iface.addVectorLayer(capPunto, '', 'ogr')
Salida= iface.addVectorLayer(capOut, '', 'ogr')

    
Processing.run("saga:snappointstolines",\
{'INPUT': capPunto,\
'SNAP': capLinea,\
'OUTPUT': capOutSnap,\
'MOVES': capSegmento,\
'DISTANCE':200})

Salida_snap= iface.addVectorLayer(capOutSnap, '', 'ogr')
linea_segmento=iface.addVectorLayer(capSegmento, '', 'ogr')


#for Punto in QgsProject.instance().mapLayers().values():
    #Punto.setCrs(QgsCoordinateReferenceSystem('EPSG:32719'))