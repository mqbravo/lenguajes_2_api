
receta('Cerdo en Salsa de PiNa').
receta('Cerdo al ajillo').
receta('Cerdo en Salsa de PiNa').
receta('Cerdo en Salsa de Hongos').

buscarNombre(X,Y):-receta(X), Y = X.
