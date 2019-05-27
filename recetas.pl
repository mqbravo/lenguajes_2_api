receta('Ensalada Verde', 'Ensalada', ['1. Picar Ensalada', '2. Exprimir limon', '3. Picar tomate', '4. Revolver'], ['Lechuga', 'Limon', 'Tomate', 'Sal'],[]).
receta('Hamburguesa', 'Comida rapida', ['1. Cortar pan', '2. Cocinar carne', '3. Picar tomate', '4. Combinar'], ['Torta Carne', 'Pan', 'Tomate', 'Lechuga'], []).
receta('Arroz con camarones', 'Mariscos', ['1. Hacer arroz', '2. Hacer camarones', '3. Combinar'], ['Arroz', 'Camarones', 'Cebolla', 'Achiote'], []).
receta('Camarones al ajillo', 'Mariscos', ['1. Picar ajos', '2. Freir camarones en mantequilla'], ['Camarones', 'Ajo', 'Cebolla', 'Mantequilla'], []).
receta('Ensalada rusa','Ensalada',['1. Cocinar huevos','2. Cocinar remolacha','3. Combinar'],['Huevo','Papa','Remolacha'],['http']).
receta('Pina Colada','Bebida',['1. Pelar pina','2. Agregar alcohol','3. Combinar'],['Pina','Alcohol'],[]).
receta('Pacha con Jet','Bebida',['1. Agregar pacha','2. Agregar jet','3. Combinar'],['Pacha','Alcohol'],[]).

buscarNombre(X, Y):-receta(X,_,_,_,_), Y = X.
buscarTipo(X, Y):-receta(R,X,_,_,_), Y = R.

buscarIngrediente(Ingrediente, X):-receta(R,_,_,Lista,_),aux(Lista, Ingrediente, R, X).
aux([],Elemento,Temp,X):-fail.
aux([H|T],Elemento,Temp,X):-H==Elemento,X=Temp.
aux([H|T],Elemento,Temp,X):-aux(T,Elemento,Temp,X).


receta('Pacha con vainilla','Bebida',['1. Agregar Pacha','2 Agregar Vainilla','3. Combinar'],['Pacha','Vainilla'],['http']).
