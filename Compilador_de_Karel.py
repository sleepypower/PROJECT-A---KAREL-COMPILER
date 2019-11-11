import re

#Tener un input que nos reciba el nombre del archivo
nombre = input("Escriba el nombre del archivo a analizar: ")
nombre += ".txt"
archivo = open(nombre,"r") # Input


text = archivo.readlines() #Texto en formato lista, cada item es una linea 

 
tokens = (#PALABTAS RESERVADAS
          "BEGINNING-OF-PROGRAM","END-OF-PROGRAM",
          "BEGINNING-OF-EXECUTION","END-OF-EXECUTION",
          "DEFINE-NEW-INSTRUCTION","BEGIN","AS","TIMES",
          "WHILE","DO","ITERATE","IF","THEN", "END",
          
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
contador_if = 0
contador_while=0
contador_iterate=0
indice = 0
indice_nueva = []


for line in text:
    lista_palabras = re.compile(r"\b[a-zA-Z-]+").findall(line)
    palabras.append(lista_palabras)
    instruccion_nueva = re.compile(r"\bDEFINE-NEW-INSTRUCTION\s+[a-zA-Z-]+\s+AS").findall(line)
    condicional_if =  re.compile(r"\bIF\s+[a-zA-Z-]+\s+THEN").findall(line)
    iterate =  re.compile(r"\bITERATE\s+[0-9]+\s+TIMES").findall(line)
    condicional_while =  re.compile(r"\bWHILE\s+[a-zA-Z-]+\s+THEN").findall(line)
    if len(instruccion_nueva) != 0:
        contador_de_nuevas_instrucciones += 1
        indice_nueva.append(indice)
    if len(condicional_if) != 0:
        contador_if += 1
    if len(condicional_while) != 0:
        contador_while += 1
    if len(iterate) != 0:
        contador_iterate += 1

        
    indice +=1
#Se guardan los indices en los cuales estan definidas las nuevas instrucciones
indice_palabra_final = len(palabras)-1

#Se agregan las nuevas instrucciones a los tokens
for instruccion in indice_nueva:
    if palabras[instruccion][1] not in tokens:    
        tokens += (palabras[instruccion][1],)
    else:
        myError = NameError("{0} ya esta definida".format(palabras[instruccion][1]))
        raise myError
    
 
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
    if len(lista_palabras)!=0:
        palabras_con_PuntoYComa.append(lista_palabras)

indice_recorrido = 1
#Errores de Sintaxis
            
if palabras_con_PuntoYComa[0][0] != "BEGINNING-OF-PROGRAM":
    myError = SyntaxError("Error de sintaxis")
    raise myError

# Se recorre el bloque entre Beginning-of-program y Beginning-of-execution para 
    # las nuevas instrucciones

value = False # Esta Variable me permite saber si existe BEGINNING-OF-EXECUTION
valor_condicional = False #Esta Variable me permite saber si existen condicionales
contador_end = 0

for token in palabras_con_PuntoYComa:
    for string in token:
        if string == "BEGINNING-OF-EXECUTION":
            while palabras_con_PuntoYComa[indice_recorrido][0] != "BEGINNING-OF-EXECUTION" :
                if palabras_con_PuntoYComa[indice_recorrido][0] == "DEFINE-NEW-INSTRUCTION":
                    valor_define = True
                    contador_end +=1
                    if palabras_con_PuntoYComa[indice_recorrido+1][0] != "BEGIN":
                        myError = SyntaxError("Error de sintaxis")
                        raise myError       
                elif palabras_con_PuntoYComa[indice_recorrido][0] == "BEGIN":
                        if palabras_con_PuntoYComa[indice_recorrido+1][0] == "END":
                            myError = SyntaxError("Error de sintaxis")
                            raise myError
                elif (palabras_con_PuntoYComa[indice_recorrido][0] == "ITERATE" and contador_iterate>0) or (palabras_con_PuntoYComa[indice_recorrido][0] == "IF" and contador_if>0) or  (palabras_con_PuntoYComa[indice_recorrido][0] == "WHILE" and contador_while>0):
                    contador_end +=1
                
                    if palabras_con_PuntoYComa[indice_recorrido+1][0] != "BEGIN":
                        myError = SyntaxError("Error de sintaxis")
                        raise myError
                    valor_condicional = True #Si existe un condicional se cambia el valor de la variable

                else:
                    tamano_instruccion = len(palabras_con_PuntoYComa[indice_recorrido][0])
                    instruccion = palabras_con_PuntoYComa[indice_recorrido][0]
                    sig_instr = palabras_con_PuntoYComa[indice_recorrido+1][0]
                    if valor_condicional: # Si existe , se verifica la sintaxis teniendo en cuenta unos patrones
                        if instruccion[tamano_instruccion-1] != ";" and instruccion != "END" and (sig_instr !="END" and sig_instr !="END;"):
                            myError = SyntaxError("Error de sintaxis en la linea {0}".format(indice_recorrido+1))
                            raise myError       
                        elif instruccion[tamano_instruccion-1] == ";" and (sig_instr == "END" or sig_instr =="END;"):
                            myError = SyntaxError("Error de sintaxis en la linea {0}".format(indice_recorrido+1))
                            raise myError
                        elif (instruccion == "END" and sig_instr == "END") or (instruccion == "END;" and sig_instr == "END;"):
                            myError = SyntaxError("Error de sintaxis END")
                            raise myError                            
                        
                    else:
                        if instruccion[tamano_instruccion-1] != ";" and sig_instr !="END;":
                            myError = SyntaxError("Error de sintaxis, en la linea {0}".format(indice_recorrido+1))
                            raise myError
                        if instruccion[tamano_instruccion-1] == ";" and sig_instr == "END;":
                            myError = SyntaxError("Error de sintaxis en la linea {0}".format(indice_recorrido+1))
                            raise myError
                    
                        
                indice_recorrido += 1  
            value = True   #Si se cumple la condicion de la existencia del BEG-OF-EXE me cambia el valor


#Se verifica que si existe un DEFINE , este debe ir antes del bloque de ejecucion
if valor_define == False and contador_de_nuevas_instrucciones>0:
    myError = SyntaxError("Error de sintaxis. DEFINE-NEW-INSTRUCTION debe ir antes de BEG-OF-EXE".format(indice_recorrido+1))
    raise myError

#
if value==False:
    myError = SyntaxError("Error de sintaxis, hace falta BEG-OF-EXE ")
    raise myError
if palabras_con_PuntoYComa[indice_recorrido][0] != "BEGINNING-OF-EXECUTION":
    myError = SyntaxError("Error de sintaxis".format(palabra))
    raise myError
else:
    indice_recorrido += 1
  
valor_condicional1 = False # La siguiente variable se crea para indicar si aparece un condicional o no
valor_end = False # Se utiliza para verificar que ya se halla pasado el end , lo anterior para permitir tener mas de un condicional en la ejecución
#
#Recorre cada linea y revisa si al final existe un punto y coma 
for words_in_line in palabras_con_PuntoYComa[indice_recorrido:len(palabras_con_PuntoYComa) - 3]: #aQUI TOCA AGREGAR EL TURNOFF DE ALGUNA MANERA
    if (palabras_con_PuntoYComa[indice_recorrido][0] == "ITERATE" and contador_iterate>0) or (palabras_con_PuntoYComa[indice_recorrido][0] == "IF" and contador_if>0) or  (palabras_con_PuntoYComa[indice_recorrido][0] == "WHILE" and contador_while>0):  
        if palabras_con_PuntoYComa[indice_recorrido+1][0] != "BEGIN":
            myError = SyntaxError("Error de sintaxis , hace falta BEGIN")
            raise myError
        valor_condicional1 = True # Si existe un condicional entonces se verifica la sintaxis dentro de la estructura
        valor_end = False
        
    elif palabras_con_PuntoYComa[indice_recorrido][0] == "END;":
        valor_end = True
        valor_condicional1 = False
    
    elif palabras_con_PuntoYComa[indice_recorrido][0] == "BEGIN":
        contador_end += 1
        
        
    elif valor_condicional1: # Se verifica la sintaxis dentro del condicional 
        tamano_instruccion = len(palabras_con_PuntoYComa[indice_recorrido][0])
        instruccion = palabras_con_PuntoYComa[indice_recorrido][0]
        sig_instr = palabras_con_PuntoYComa[indice_recorrido+1][0]  
 
        if instruccion[tamano_instruccion-1] != ";" and sig_instr !="END;":
            myError = SyntaxError("Error de sintaxis, en la linea {0}".format(indice_recorrido+1))
            raise myError
        elif instruccion[tamano_instruccion-1] == ";" and sig_instr == "END;":
            myError = SyntaxError("Error de sintaxis en la linea {0}".format(indice_recorrido+1))
            raise myError
            
    elif valor_end: # Una vez pase la palabra END; pueden haber mas instrucciones que se verifican de manera diferente
        tamano_instruccion = len(palabras_con_PuntoYComa[indice_recorrido][0])
        instruccion = palabras_con_PuntoYComa[indice_recorrido][0]
        sig_instr = palabras_con_PuntoYComa[indice_recorrido+1][0]
        if instruccion[tamano_instruccion-1] != ";":
            myError = SyntaxError("Error de sintaxis, hace falta ; en la linea {0}".format(indice_recorrido+1))
            raise myError
    indice_recorrido += 1

#La ultima instruccion debe corresponder a un turnoff
if palabras_con_PuntoYComa[indice_recorrido][0] != "turnoff":
    myError = SyntaxError("Error shutoff".format(palabra))
    raise myError
indice_recorrido +=1

#Luego de la ultima instruccion debe ir END-OF-EXECUTION
if palabras_con_PuntoYComa[indice_recorrido][0] != "END-OF-EXECUTION":
    myError = SyntaxError("Error de sintaxis END-OF-EXECUTION".format(palabra))
    raise myError
indice_recorrido +=1

#La ultima linea del programa debe ser END-OF-PROGRAM
if palabras_con_PuntoYComa[indice_recorrido][0] != "END-OF-PROGRAM":
    myError = SyntaxError("Error de sintaxis END-OF-PROGRAM".format(palabra))
    raise myError    

print("El archivo {0} no cuenta con errores de lexico o sintaxis.".format(nombre)) 
archivo.close()
                
