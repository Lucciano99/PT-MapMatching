
capMuestra='/home/lucciano/Trabajo PT/CapasResultante_UAP/Capa_T434_34.shp'
capLine= '/home/lucciano/Trabajo PT/Cargas_de_Capas/Redvial/RedVialComunasSantiago.shp'

capa1=QgsVectorLayer(capMuestra, "Capa_Punto", "ogr")
capa2=QgsVectorLayer(capLine, "Capa_Linea", "org")

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

