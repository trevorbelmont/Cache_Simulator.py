import sys

def indexDecimal(hex :str, nIgnore : int):
    """ Converte um índce de memória, hex, de hex2Binário e ignora os nIgnore bits menos significativos. Depois converte o resultado pra decimal"""
    binn = bin(int(hex, 16)) # converte de hex pra inteiro (decimal) e de inteiro pra binário (com o prefixo '0b')
    binn = binn[2:-nIgnore] # remove os dois primeiros caracteres (o prefixo '0b') e os nIgnore menos significativos dígitos por slicing
    binn = binn.zfill(32) # completa com zeros a esquerda até que a string binário tenha 32 caracteres (32 dígitos binários)    
    return int(binn,2) #converte o índice binário ajustado para decimal

def hexaDoeu(hex : str, nDigits : int):
    """ Formata uma string contendo um valor hexadecimal com menos de 8 dígitos num hexadecimal de 8 dígitos (adicionanado zeros à esquerda) máisuculos"""
    if len(hex) >= nDigits+2:
        return hex # retorna a string sem formatação para que não haja perda de dados
    else:
        hex = hex[2:].zfill(nDigits)
        hex = "0x"+hex.upper()
    return hex

def testConversion():
    print(f"cs = {cs}\nls = {ls}\nss = {ss}\nnLines = {nLines}\nnSets = {nSets}\ninFile = {inFile}")
    
    print(f"0xDEADBEEF ({int("0xDEADBEEF",16)}) -> {hexaDoeu(hex(indexDecimal("0xDEADBEEF",10)),8)} ({indexDecimal("0xDEADBEEF",10)})")

def printCacheState(nEntries, validList, addressList):
    ''' Este método imprime o estado da cache em um dado momento.'''
    print("================")
    print("IDX V ** ADDR **")
    for i in range(nEntries):
        address = hexaDoeu(addressList[i],8) if (validList[i]== True) else "" # condiciona a impressão da tag se o dado é válido na cache
        print (f"{str(i).zfill(3)} {int(validList[i])} {address}")
    

def main():
    vList = [False] * nLines
    vList[2] = vList[0] = 1
    addressList = ["0x456ef"] * nLines
    printCacheState(nLines,vList,addressList)
    

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso do script: python3 simulador.py <Cache_byte_size> <Entry_byte_size> <Cache_set_size> <Input_reading_file.txt>")
    else:
        cs = int (sys.argv[1]) # cs (cache size, em bytes)
        ls = int (sys.argv[2]) # ls (line size, em bytes)
        nLines = int(cs / ls)
        ss = int (sys.argv[3]) # ss (set size (tamanho do conjunto), em linhas)
        nSets = int(nLines/ss)      # número de sets = nLinhas / tamanho do conjunto (linhas)
        inFile = sys.argv[4]   # Arquivo de entrada com os endereços dos blocos (de memória) a serem carregados
        main()