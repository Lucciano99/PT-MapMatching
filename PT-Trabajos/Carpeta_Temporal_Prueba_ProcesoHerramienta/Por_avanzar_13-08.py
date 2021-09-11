import sys
import processing
import qgis

from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsCoordinateReferenceSystem
)

from qgis.utils import iface 

capaMuestra='/home/lucciano/Trabajo PT/CapaPrueba/Capa_T434_34.shp'
capaP=QgsVectorLayer(capaMuestra,"Capa_Punto","ogr")
capaLinea='/home/lucciano/Trabajo PT/Cargas_de_Capas/Redvial/RedVialComunasSantiago.shp'
capaL=QgsVectorLayer(capaLinea, "Redvial", "ogr")

#capaSnap='/home/lucciano/Trabajo PT/Carpeta_Temporal_Prueba_ProcesoHerramienta/aca/line.shp'


if not capaP.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayers([capaP,capaL])

for capaP in QgsProject.instance().mapLayers().values():
    capaP.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))

capaSalida='/home/lucciano/Trabajo PT/CapaPrueba/hola.shp'

processing.run("saga:snappointstolines",\
{'INPUT': capaP,\
'SNAP': capaL,\
'OUTPUT':capaSalida,\
'DISTANCE':100000})

iface.addVectorLayer(capaSalida, 'hola', 'org')

