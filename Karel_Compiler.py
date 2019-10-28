import re

#Tener un input que nos reciba el nombre del archivo
archivo = open("prueba2.txt","r") # Input


text = archivo.readlines() #Texto en formato lista, cada item es una linea 

 
tokens = (#PALABTAS RESERVADAS
          "BEGINNING-OF-PROGRAM","END-OF-PROGRAM",
          "BEGINNING-OF-EXECUTION","END-OF-EXECUTION",
          "DEFINE-NEW-INSTRUCTION","BEGIN","AS","TIMES",
          "WHILE","DO","ITERATE","IF","THEN", 
          
          #DICCIONARIO DE PROPOSICIONES
          "front-is-clear", "front-is-blocked",
          "left-is-clear", "left-is-blocked",
          "right-is-clear", "right-is-blocked",
          "next-to-a-beeper", "not-next-to-a-beeper",
          "facing-north", "not-facing-north",
          "facing-south", "not-facing-south",
          "facing-east", "not-facing-east",
          "facing-west", "not-facing-west",
          
          #DICCIONARIO INSTRUCCIONES
          "move","turnleft","turnoff",
          "pickbeeper","putbeeper")


#Tomar todas las palabras en cada linea del texto para analizarla
palabras = [] #Sin (;)
palabras_con_PuntoYComa = []


#Contador de ocurrencias del patron DEFINE...
contador_de_nuevas_instrucciones = 0


for line in text:

    lista_palabras = re.compile(r"\b[a-zA-Z-]+").findall(line)
    palabras.append(lista_palabras)
    match = re.compile(r"\bDEFINE-NEW-INSTRUCTION\s+[a-zA-Z-]+\s+AS").findall(line)
    if len(match) != 0:
        contador_de_nuevas_instrucciones += 1
        print(contador_de_nuevas_instrucciones)



indice_palabra_final = len(palabras)-1


#for range(contador_de_nuevas_instrucciones):
#    token+= ( ,)


#Recorrer todas las palabras y verificar si es una palabra conocida o no (sin ;)
#Numero de linea sera el indice del elemento mas 1
for lista_palabras in palabras:
    for palabra in lista_palabras:
        if palabra not in tokens:
            myError = NameError("{0} no esta definida".format(palabra))
            raise myError


#Toma todas las palabras en cada linea de texto con ;
for line in text:
    lista_palabras = re.compile(r"\b[a-zA-Z-;]+").findall(line)
    palabras_con_PuntoYComa.append(lista_palabras)


#Errores de Sintaxis
            
if palabras_con_PuntoYComa[0][0] != "BEGINNING-OF-PROGRAM":
    myError = SyntaxError("Error de sintaxis".format(palabra))
    raise myError


if palabras_con_PuntoYComa[1][0] != "BEGINNING-OF-EXECUTION":
    myError = SyntaxError("Error de sintaxis".format(palabra))
    raise myError


#Recorre cada linea y revisa si al final existe un punto y coma 
for words_in_line in palabras_con_PuntoYComa[2:len(palabras_con_PuntoYComa) - 3]: #aQUI TOCA AGREGAR EL TURNOFF DE ALGUNA MANERA
    for palabra_in_line in words_in_line:
        print(words_in_line)
        if palabra_in_line[len(palabra_in_line)-1] != ";":
            myError = SyntaxError("Error de sintaxis, hace falta ;".format(palabra))
            raise myError
            
            
if palabras_con_PuntoYComa[indice_palabra_final-2][0] != "turnoff":
    myError = SyntaxError("Error shutoff".format(palabra))
    raise myError
   
    
if palabras_con_PuntoYComa[indice_palabra_final-1][0] != "END-OF-EXECUTION":
    myError = SyntaxError("Error de sintaxis".format(palabra))
    raise myError


if palabras_con_PuntoYComa[indice_palabra_final][0] != "END-OF-PROGRAM":
    myError = SyntaxError("Error de sintaxis".format(palabra))
    raise myError    

print(text)
archivo.close()
