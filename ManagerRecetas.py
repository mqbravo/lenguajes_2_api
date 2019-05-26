def addReceta(nombre, tipo, listaInstrucciones, listaIngredientes, listaImagenes, prolog):
    file = open("recetas.pl", 'a')

    auxIngredientes = "['"
    for ingrediente in listaIngredientes:
        if(ingrediente == ","):
            auxIngredientes += "'" + ingrediente + "'"
        else:
            auxIngredientes += ingrediente
    auxIngredientes += "']"

    auxImagenes = "['"
    for url in listaImagenes:
        if(url == ","):
            auxImagenes += "'" + url + "'"
        else:
            auxImagenes += url
    auxImagenes += "']"

    auxInstrucciones = "['"
    for instruccion in listaInstrucciones:
        if(instruccion == ","):
            auxInstrucciones += "'" + instruccion + "'"
        else:
            auxInstrucciones += instruccion
    auxInstrucciones += "']"

    file.write("\nreceta('"+ nombre + "','" + tipo + "'," + auxInstrucciones + "," + auxIngredientes + "," + auxImagenes + ").")
    file.close()
