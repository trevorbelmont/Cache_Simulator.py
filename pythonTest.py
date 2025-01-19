import sys

def hex2bin(hex):
    """
    Converte um número hexadecimal (string) em uma string de bits de 32 bits.
    """

    #converte a string hex para binário.
    binn = bin(int(hex, 16)) # converte de hex pra inteiro (decimal) e de inteiro pra binário (com o prefixo '0b')
    binn = binn[2:] # remove os dois primeiros caracteres por slicing (o prefixo '0b').
    binn = binn.zfill(32) # completa com zeros a esquerda até que a string binário tenha 32 caracteres (32 dígitos binários)
    
    return binn

def process_file(input_file, output_file):
    """
    Lê números hexadecimais de um arquivo de entrada, converte para binário
    em blocos de 4 bits e escreve no arquivo de saída.
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                hex_number = line.strip()
                # Ignorar linhas vazias
                if hex_number:
                    binary_representation = hex2bin(hex_number)
                    outfile.write(binary_representation + '\n')
        print(f"Conversão concluída. Resultados salvos em '{output_file}'.")
    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_file}' não foi encontrado.")
    except ValueError as e:
        print(f"Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <arquivo_de_entrada>")
    else:
        input_filename = sys.argv[1]
        output_filename = "out.txt"
        process_file(input_filename, output_filename)
