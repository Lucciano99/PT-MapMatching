
import os

from qgis.core import (
 QgsVectorLayer,
 QgsProject,
 QgsApplication,
 QgsField
)

#from .Funcion import recorre_dic
#from qgis.utils import iface
#from qgis.utils import QgsGeometryAnalyzer
from qgis.utils import iface #Por siacaso en caso de 
from qgis.PyQt.QtCore import QVariant



qgs = QgsApplication([], True) #Se especifica que no se trabajara con la GUI
QgsApplication.setPrefixPath(".local/share/QGIS/QGIS3", False)
QgsApplication.initQgis()
for alg in QgsApplication.processingRegistry().algorithms():
    print(alg.id(), "->", alg.displayName())


capResultado='/home/lucciano/git_Proyecto/CapasResultante_UAP/Test1.shp'
capOutput= '/home/lucciano/git_Proyecto/CapasResultante_UAP'
capa1=QgsVectorLayer(capResultado, "Capa_Punto", "ogr")
capa2=QgsVectorLayer(capOutput, "Capa_Out", "memory")

if not capa1.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(capa1,False)
    QgsProject.instance().addMapLayer(capa2,False)


features= capa1.getFeatures()

temp=capa2.dataProvider()


temp.addAttributes([QgsField("nearest_x", QVariant.String),
QgsField("nearest_y", QVariant.String)])

capa2.updateFields()


for features in features:
    print("Nearest X: ", features['nearest_x'])
    print("Nearest Y: ", features['nearest_y'])



