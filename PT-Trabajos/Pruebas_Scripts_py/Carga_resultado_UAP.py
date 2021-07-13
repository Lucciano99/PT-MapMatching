
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


capResultado='/home/lucciano/git_Proyecto/CapasResultante_UAP/Test1.shp'

capa1=QgsVectorLayer(capResultado, "Capa_Punto", "ogr")

if not capa1.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(capa1,False)


features= capa1.getFeatures()

for features in features:
    print("nearst_X: ", features['nearest_xs'])