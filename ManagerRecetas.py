def addReceta(nombre, prolog):
    file = open("recetas.pl", 'a')
    file.write("\nreceta("+ nombre +").")
    file.close()
