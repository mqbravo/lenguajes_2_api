def addReceta(nombre, tipo, listaInstrucciones, listaIngredientes, listaImagenes, prolog):
    file = open("recetas.pl", 'a')

    ingredientes = "["
    for ingrediente in listaIngredientes['ingredients']:
        ingredientes += "'" + ingrediente + "',"
    ingredientes = ingredientes[:-1] + "]"

    imagenes = "["
    for url in listaImagenes['imageURLs']:
        imagenes += "'" + url + "',"
    imagenes = imagenes[:-1] + "]"

    instrucciones = "["
    for instruccion in listaInstrucciones['preparation']:
        instrucciones += "'" + instruccion + "',"
    instrucciones = instrucciones[:-1] + "]"

    file.write("\nreceta('"+
                nombre['name'] +
                 "','" +
                tipo['type'] +
                "'," +
                instrucciones +
                "," +
                ingredientes +
                "," +
                imagenes +
                ").")
    file.close()
