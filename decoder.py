import random
import numpy as np
from encoder_hamming import number_of_parity_bits, enter_parity_bit, calcularFila, define_partity_bits

def enter_error_bit(code, probabilidad):
    newCode = ""
    for i in range(len(code)):
        n = random.uniform(0.0, 100.0)
        bit = code[i]
        if(n <= float(probabilidad)):
            if(bit=="0"):
                newCode += "1"
            else:
                newCode += "0"
            
            #print(f"(X) Error generado en la posición {i+1}")
        else:
            newCode += code[i]
    
    return newCode

def generate_identityMatrix(cantBits_code):
    Istring = []
    Imatrix = []
    for i in range(cantBits_code):
        rowString = ""
        row = []
        for j in range(cantBits_code):
            if i == j:
                rowString+= "1"
                row.append(1)
            else: 
                rowString+= "0"
                row.append(0)
        Imatrix.append(row)
        Istring.append(rowString)

    return Imatrix, Istring

def generator_matrix(cantBits_code):
    matrixTemp = []
    matrix = []
    bits = []
    temp = "0"*cantBits_code
    identity_matrix, identity_matrix_code = generate_identityMatrix(cantBits_code)
    n = number_of_parity_bits(identity_matrix[1])
    for i in range(n):
        bits.append(2**i)
        
    for i in range(cantBits_code):
        code = enter_parity_bit(identity_matrix_code[i], n)
        define_partity_bits(code, n)
        matrixTemp.append(code)
    
    for i in range(len(matrixTemp)):
        parityBits = []
        for j in range(len(bits)):
            parityBits.append(matrixTemp[i][bits[j]-1])

        matrix.append(np.hstack((identity_matrix[i], parityBits)))

    return matrix
            
def ordenate_code_and_cantityDataBits(code):
    p = 0
    d = 0
    paritybits = []
    data = []

    for i in range(len(code)):
        if 2**p == i+1:
            paritybits.append(code[i])
            p+=1
        else:
            data.append(code[i]) 
            d+=0

    code = np.hstack((data, paritybits))
    return code, (len(code)-p)

def get_parity_matrix(matrixG, cantityDataBits, cantityParityBits):
    P = []
    H = []
    I = np.identity(cantityParityBits)
    # G = [ I | P ]
    # H = [ P**T | I ]
    for i in range(len(matrixG)):
        temp = []
        for j in range(cantityDataBits, cantityDataBits+cantityParityBits):
            temp.append(matrixG[i][j])
        P.append(temp)
    

    P = np.array(P).transpose()
    H = np.hstack((P, I))
    return H

def validate_syndrome(word_received, H, G, syndrome):
    #word received : r
    #parity matrix: H
    # H*r = s
    # s*G = patron de error
    # patron de error + 
    word_received = np.array(word_received,dtype='float64' ).transpose()
    H = np.array(H,dtype='float64')
    syndrome = np.array(syndrome,dtype='float64')
    s = np.matmul(H, word_received.transpose())

    bit_error = 0
    for i in range(len(s)):
        if s[i]%2 != 0:
            s[i] = 1
            bit_error += 2**i
        else:
            s[i] = 0
    #print("s", s)
    return bit_error

def parity_isCorrect(H, code):
    Ht = np.array(H).transpose()
    Ht = np.array(Ht,dtype='float64')
    code = np.array(code,dtype='int64')
    code_check = np.matmul(code, Ht)
    for i in range(int(code_check.shape[0])):
        if int(code_check[i])%2 != 0:
            return False
    
    return True
        
def generate_syndrome(cantParityBits):
    return generator_matrix(cantParityBits)

def main():
    c=0
    total =0
    probabilidad = input("Ingrese error (%): ")
    for k in range(30):
        file_input = open("word_encoded", "r")
        code = file_input.read()
        code_separed = code.split()
        parityisOkMatrix = []
        
        for i in range(len(code_separed)):
            total+=1
            #print(f"-------------Proceso para palabra {code_separed[i]}-------------")
            codewithError = enter_error_bit(code_separed[i],probabilidad)
            code,cantBits_code = ordenate_code_and_cantityDataBits(codewithError)
            generatorMatrix = generator_matrix(cantBits_code)
            parityMatrix = get_parity_matrix(generatorMatrix, cantBits_code, len(codewithError)-cantBits_code)
            parityIsOk_before= parity_isCorrect(parityMatrix, code)
            
            parityisOkMatrix.append(parityIsOk_before)
            # print(f"G[{i}] = ")
            # print(np.array(generatorMatrix))
            # if(parityisOkMatrix[i] == True):
            #     print(f"(V) Paridad de {code_separed[i]} esta Ok")
            # else:
            #     print(f"(X) Paridad de {code_separed[i]} esta mal")
            
            
            sy = generate_syndrome(len(codewithError)-cantBits_code)
            
            bit_error = validate_syndrome(code, parityMatrix, generatorMatrix, sy)
            code_after=codewithError
            for i in range(len(codewithError)):
                if i == bit_error-1:
                    if codewithError[i]=="1" or codewithError[i]==1:
                        code_after = code_after[0:i] + "0" + code_after[i+1:]
                    else:
                        code_after = code_after[0:i] + "1" + code_after[i+1:]
            # print("-------------------------------------------------")
            # print(f"Palabra antes de error      {code_separed[i]}")
            # print(f"Palabra despues de error    {codewithError}")
            # print(f"Palabra despues de sindrome {code_after}")

            if(code_after == code_separed[i]):
                c+=1
                
        #print("------------------------------------END------------------------------------")
    print(f"corregidas: {c/total} con probabilidad {probabilidad}")


if __name__ == "__main__":
    main()

