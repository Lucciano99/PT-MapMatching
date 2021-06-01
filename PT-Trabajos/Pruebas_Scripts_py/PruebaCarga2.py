import os

from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsApplication
)


from qgis.core import QgsApplication

qgs = QgsApplication([], True) 
QgsApplication.setPrefixPath(".local/share/QGIS/QGIS3", True)
QgsApplication.initQgis()
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), "->", alg.displayName())


dir_Archivo_Vectores = "/home/lucciano/git_Proyecto/Cargas_de_Capas/Packages Layers/433/commondata/433/433_24Proj.shp" 
vlayer = QgsVectorLayer(dir_Archivo_Vectores, "Capa_Prueba1", "ogr")

if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)


vlayer= QgsProject.instance().mapLayers()

#print(vlayer)


lista = [vlayer.name() for vlayer in QgsProject.instance().mapLayers().values()]

dic_list = {}

for lista in QgsProject.instance().mapLayers().values():
    dic_list[lista.name()]= lista

print(dic_list)

Capa_Prueba1_layer=QgsProject.instance().mapLayersByName("Capa_Prueba1")[0]

print(Capa_Prueba1_layer)
