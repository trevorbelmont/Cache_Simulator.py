import sys
import math

def isHexadecimal(line : str):
    """ Retorna true se a string for um número hexadecimal"""
    hexDigits = "0123456789ABCDEF" #Todos os possíveis dígitos de um número hexadecimal no padrão adotado (letras maiúsculas).
    return (all(c in hexDigits for c in line[2:]) and  line.startswith("0x") )
    # retorna true se todos dígitos válidos, c, na string line está presente (previsto) na string hexDigits e line começa com o prefixo "0x".

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
    print(f"cs = {cs}\nls = {ls}\nss = {ss}\nnLines = {nLines}\nnSets = {nSets}\ninFile = {InFile}")
    print(f"0xDEADBEEF ({int("0xDEADBEEF",16)}) -> {hexaDoeu(hex(indexDecimal("0xDEADBEEF",10)),8)} ({indexDecimal("0xDEADBEEF",10)})")

def cacheAllocate(index, addressList, vList,FIFO):
    """"Essa função aloca um bloco de memória na cache. 
    Ela retorna True, se um novo bloco foi carregado pra cache (MISS), ou False, caso o bloco buscado já estiver na cache (HIT).
    Em outras palavras: a função retorna False se não houve necessidade de uma busca da memória (HIT)
    e True quando uma nova busca da memória teve que ser executada para acessar o dado (MISS)."""
    wSet = index%nSets # wSet (which Set) indica em qual set/conjunto da cache o bloco será inserido/buscado
    wLine = wSet * ss # wLine (which Line) aponta para a primeira linha do set
    
    if index in addressList[wLine: wLine + ss]: #checa se o bloco de memória já está carregado na cache
        if DBG: print("+1 um HIT, Muleque!!!")
        return False # Retorna False. Nenhum bloco de memória precisou ser carregado da cache (ou seja: deu HIT).
    
    if(DBG): print(f"index = {index} ({hex(index)}) nSets={nSets} lines = {nLines} wSet = {wSet} wLine = {wLine} wLine+FIFO = {wLine+FIFO[wSet]}")
    
    wLine += FIFO[wSet] # wLine agora aponta para a entrada mais antiga no set (FIFO)
    addressList[wLine] = index
    vList[wLine] = True
    FIFO[wSet] = (FIFO[wSet] + 1) % ss #atualiza o FIFO do set correspondente
    return True # Retorna True. Ou seja: um novo bloco de memória foi carregado da memória RAM pra cache (MISS).

    
    

def printCacheState(nEntries, validList, addressList, FIFO, dbg):
    ''' Este método retorna uma string formatada com o estado atual da cache.'''
    cache = "================\n"
    cache += "IDX V ** ADDR **\n"
    for i in range(nEntries):
        address = " "+hexaDoeu(hex(addressList[i]),8) if (validList[i]== True) else "" # condiciona a impressão da tag/index se o dado é válido na cache
        cache += f"{str(i).zfill(3)} {int(validList[i])}{address}" # adiciona cada linha da cache à string cache
        wSet = i//nSets if nSets > 1 else 0
        fifoMark =  "\n"#" !\n" if (dbg and FIFO[wSet] == i%nSets) else "\n"
        cache += fifoMark
    if dbg:
        print(cache)
    return cache
 
def memoryLoading(InputFile : str, OutputFile : str):
    """ Essa função lê os endereços de memória buscados do arquivo "InputFile" e carrega-os na cache.\n 
        Cada estado da cache após cada load(leitura de cada linha) é impresso no arquivo "OutputFile". """
    
    vList = [False] * nLines # array de dígitos de validade
    addressList = [""] * nLines # array de tags de indereços
    fifo = [0] * nSets
    
    hits = miss = 0
    
    printCacheState(nLines,vList,addressList,fifo,DBG)
    
    #try : similar ao excepetion handler (try-throw-catch) do C++.
    try: 
        #with <expression> as <variable> : gerenciador automático de recursos. Neste caso ele fecha o arquivo automaticamente.
        with open(InputFile, 'r') as inFile, open(OutputFile, 'w') as outFile:
            for linha in inFile: #loop que lê todas as linhas no arquivo
                if linha: # linha = true -> linha não é uma string vazia
                    memBlock = linha.strip() # memBlock (str) recebe o conteúdo da linha com os espaços em branco removidos
                    if isHexadecimal(memBlock):
                        index = indexDecimal(memBlock,offset)
                        newAlloc = cacheAllocate(index,addressList, vList, fifo)
                        if newAlloc :
                            miss += 1
                        else: 
                            hits += 1
                        outFile.write(printCacheState(nLines,vList,addressList,fifo,DBG))
            
            outFile.write(f"\n#hits: {hits}\n#miss: {miss}")
                        
    # Lança as exceções do bloco try (relativas à leitura de arquivos)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{InputFile}' não foi encontrado.")
    except ValueError as e:
        print(f"Erro ao processar o arquivo: {e}")


def main():
    ''' Uma função main de lei porque tô acostumado é com c++ e c# ;-p '''
    memoryLoading(InFile, OutFile)
       

if __name__ == "__main__":
    if (len(sys.argv) < 5 or len(sys.argv) > 7) :
        print("Uso do script: python3 simulador.py <Cache_byte_size> <Entry_byte_size> <Cache_set_size> <Input_reading_file.txt>")
    else:
        cs = int (sys.argv[1]) # cs (cache size, em bytes)
        ls = int (sys.argv[2]) # ls (line size, em bytes)
        offset = int(math.log2(ls))
        nLines = int(cs / ls)
        ss = int (sys.argv[3]) # ss (set size (tamanho do conjunto), em linhas)
        nSets = int(nLines/ss)      # número de sets = nLinhas / tamanho do conjunto (linhas)
        InFile = sys.argv[4]   # Arquivo de entrada com os endereços dos blocos (de memória) a serem carregados
        DBG = True if len(sys.argv) >= 6 and sys.argv[5] == "debug" else False
        OutFile = "out.txt" if len(sys.argv) != 7 else sys.argv[6]
        #print(f"{isHexadecimal("0x00023FD")}")
        #print(offset)
        #hexa = "0x0CB886CA"
        #print(f"{hexa} -> {hexaDoeu(hex(indexDecimal(hexa,offset)),8)} :: {int(hexaDoeu(hex(indexDecimal(hexa,offset)),8),16)} % {nSets} = ({int(hexaDoeu(hex(indexDecimal(hexa,offset)),8),16)%nSets})")
        main()