from math import log
from os import pardir
import random
import string

def txt_to_binary(txt):
    return ''.join(format(ord(i), '08b') for i in txt)

def number_of_parity_bits(word):
    p=0
    while True: 
        if(2**p >= (len(word) + p + 1)):
            return p
            break

        p+=1

def enter_parity_bit(word, numberParityBits):
    code = []
    for t in range(len(word)+numberParityBits):
        code.append('0')   
    j=0
    p=0
    for i in range(len(word)+numberParityBits):
        if 2**p == i+1:
            code[i] = f'P'
            p+=1
        else:
            code[i] = word[j]
            j+=1
    # print(code)
    return code

def calcularFila(palabra, salto, cadenaTemporal=""):
	originalCadenaAuto = palabra

	# recortamos la cadena para que empiece en ese elemento
	palabra = palabra[salto-1:]
	# agregamos una varible apoyo para conservar las "coordenadas"
	n = "N"*(salto-1)
	cadenaTemporal += n 

	n = "N"*salto
	nsalto = salto * 2
	while len(palabra) > 0:
		# tomamos los elementos segun la paridad
		cadenaTemporal += palabra[:salto]
		# brincamos los elementos segun la paridad
		palabra = palabra[nsalto:]
		# agregamos una varible apoyo para conservar las coordenadas
		cadenaTemporal += n
		
	# truncamos hasta el largo de la cadena con paridad
	cadenaTemporal = cadenaTemporal[:len(originalCadenaAuto)]
	return cadenaTemporal

def define_partity_bits(code, numberParityBits):
    bits = []
    filas_paridad = []
    length = len(code)
    for i in range(numberParityBits):
        bits.append(2**i)
        filas_paridad.append(i)
        
    stringCode = ""
    for i in code:
        stringCode+=i

    for j in range(numberParityBits):
        filas_paridad[j] = calcularFila(stringCode,bits[j])
        # print(filas_paridad[j])


    for j in range(numberParityBits):
        paridad=0
        toOr = []
        for i in range(len(filas_paridad[j])):
            if filas_paridad[j][i] == "1" or filas_paridad[j][i] == 1:
                paridad+=1
            if filas_paridad[j][i] == "1" or filas_paridad[j][i] == 1 or filas_paridad[j][i] == "0" or filas_paridad[j][i] == 0:
                toOr.append(filas_paridad[j][i])
        
        if(paridad%2==0): 
            # print(f"{j}) Paridad %2=0, cantidad de 1s={paridad}")
            code[bits[j]-1] = "0"
        else:  
            # print(f"{j}) Paridad %2!=0, cantidad de 1s={paridad}")
            code[bits[j]-1] = "1"



def main():
    for i in range(30):
        f = open(f"./words/word_{i}", "w")
        letters = string.ascii_lowercase
        f.write(''.join(random.choice(letters) for i in range(10)))
        f.close()

    for k in range(30):
        file_input= open(f"./words/word_{k}", "r")
        word=file_input.read()
        char_of_word = []
        code_of_char = []
        for i in range(len(word)):
            char_of_word.append(word[i])
        
        for i in range(len(char_of_word)):
            #word_bin = txt_to_binary(char_of_word[i])
            word_bin = "0101"
            #print(f"Palabra en bin: {word_bin}")
            n = number_of_parity_bits(word_bin)
            code = enter_parity_bit(word_bin, n)
            define_partity_bits(code, n)
            stringCode = ""
            for i in code:
                stringCode+=i
            code_of_char.append(stringCode)
        
            

        
        # define_partity_bits(code, n)
        stringCodeComplete = ""
        for i in range(len(code_of_char)):
            stringCodeComplete+=code_of_char[i] + " "
        
        
        # print("------------------------------------START------------------------------------")
        # print(f">> palabra: {char_of_word}")
        # print("---------------------------------------------------------------------------")
        # print(f">> palabra en binario codificada con hamming: {code_of_char}")
        # print("------------------------------------END------------------------------------")
        print(k)
        fileout = open(f"./wordsEncoded/word_encoded_{k}","w")
        fileout.write(stringCodeComplete)
        file_input.close()
        fileout.close()
if __name__ == "__main__":
    main()


