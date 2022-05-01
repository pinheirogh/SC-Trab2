import sys
import math
import base64

SIMBOLOS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.,+/=-'

def main():
    opcao = input('''ALGORITMO RSA\n1 - Cifrar\n2 - Decifrar\nOpção: ''')

    if opcao == '1':
        print()
        nome_arquivo_mensagem = 'arquivos_texto/' + input('Nome do arquivo em claro: ') + '.txt'
        
        
        # Abrir arquivo para leitura de texto
        with open(nome_arquivo_mensagem, 'r') as arquivo:
            mensagem = arquivo.read()
        # Fechar arquivo
        arquivo.close()

        nome_arquivo_chave = 'arquivos_texto/' + input('Nome do arquivo de chave pública: ') + '.txt'

        nome_arquivo_cifrado = 'arquivos_texto/' + input('Nome p/ arquivo de saída: ') + '.txt'
                
        texto_cifrado = str(cifrar_para_arquivo(nome_arquivo_cifrado, nome_arquivo_chave, mensagem)).replace('b\'', '').replace('\'', '')    

        print()
        print('TEXTO CIFRADO:')
        print(texto_cifrado)        
    elif opcao == '2':
        print()
        nome_arquivo_mensagem = 'arquivos_texto/' + input('Nome do arquivo cifrado: ') + '.txt'
        nome_arquivo_chave = 'arquivos_texto/' + input('Nome do arquivo de chave privada: ') + '.txt'
        
        texto_decifrado = arquivo_para_decifrar(nome_arquivo_mensagem, nome_arquivo_chave)

        nome_arquivo_decifrado = 'arquivos_texto/' + input('Nome p/ arquivo de saída: ') + '.txt'

        # Escrever texto decifrado no arquivo
        with open(nome_arquivo_decifrado, 'w') as arquivo:
            arquivo.write(texto_decifrado)
        # Fechar arquivo
        arquivo.close()

        print()
        print('TEXTO DECIFRADO:')
        print(texto_decifrado)

def codificar_base64(conteudo):
    # Codifica conteudo em base64
    return base64.b64encode(bytes(conteudo, 'utf-8'))
    

def decodificar_base64(conteudo):
    # Decodifica um arquivo base64 e retorna string
    return str(base64.b64decode(conteudo).decode('utf-8'))


def converter_texto_em_blocos(mensagem, tam_bloco):
    # Converts a string mensagem to a list of block integers.

    # Verificar se há algum simbolo não permitido
    for simbolo in mensagem:
        if simbolo not in SIMBOLOS:
            print(f'ERRO: O texto contém simbolos não permitidos: {str(simbolo)}')
            sys.exit()

    blocos_int = []
    for bloco in range(0, len(mensagem), tam_bloco):
        # Calcular o numero inteiro de cada bloco:
        bloco_int = 0
        for i in range(bloco, min(bloco + tam_bloco, len(mensagem))):
            bloco_int += (SIMBOLOS.index(mensagem[i])) * \
                (len(SIMBOLOS) ** (i % tam_bloco))
        blocos_int.append(bloco_int)
    return blocos_int


def converter_blocos_em_texto(blocos_cifrados, tam_mensagem, tam_bloco):
    # Converte uma lista de blocos cifrados em uma mensagem
    mensagem = []
    for bloco_int in blocos_cifrados:
        bloco_mensagem = []
        for i in range(tam_bloco - 1, -1, -1):
            if len(mensagem) + i < tam_mensagem:
                # Decodificar o bloco de texto de acordo com o tamanho do alfabeto utilizado
                indice = bloco_int // (len(SIMBOLOS) ** i)
                bloco_int = bloco_int % (len(SIMBOLOS) ** i)
                bloco_mensagem.insert(0, SIMBOLOS[indice])
        mensagem.extend(bloco_mensagem)
    return ''.join(mensagem)


def cifrar_mensagem(mensagem, chave, tam_bloco):
    # Criptografa a mensagem com a chave publica e retorna uma lista de blocos cifrados

    blocos_cifrados = []
    n, e = chave

    for bloco in converter_texto_em_blocos(mensagem, tam_bloco):
        # C = m ^ e mod n
        blocos_cifrados.append(pow(bloco, e, n))

    # Aplicar OAEP aos blocos
          
    return blocos_cifrados


def decifrar_mensagem(blocos_cifrados, tam_mensagem, chave, tam_bloco):
    # Descriptografa a mensagem com a chave privada e retorna uma lista de blocos decifrados

    blocos_decifrados = []
    n, d = chave

    # Reverter OAEP dos blocos

    for bloco in blocos_cifrados:
        # M = C ^ d mod n
        blocos_decifrados.append(pow(bloco, d, n))
    return converter_blocos_em_texto(blocos_decifrados, tam_mensagem, tam_bloco)


def ler_arquivo_chave(arquivo_chave):
    # Procura o arquivo de chave e retorna uma tupla com os valores tamanho da chave, 'n' e 'e'/'d'

    file_object = open(arquivo_chave)
    conteudo = file_object.read()
    file_object.close()
    conteudo = decodificar_base64(conteudo)    
    tam_chave, n, EorD = conteudo.split(',')
    return (int(tam_chave), int(n), int(EorD))


def cifrar_para_arquivo(nome_arquivo_decifrado, arquivo_chave, mensagem, tam_bloco=None):
    # Cifra o conteudo e salva o resultado em um arquivo

    tam_chave, n, e = ler_arquivo_chave(arquivo_chave)

    if tam_bloco == None:
        # Definir o tamanho do bloco para o maior valor possivel de acordo com o tamanho da chave
        tam_bloco = int(math.log(2 ** tam_chave, len(SIMBOLOS)))

    # Checar se o tamanho da chave é suficiente para o tamanho do bloco:
    if not (math.log(2 ** tam_chave, len(SIMBOLOS)) >= tam_bloco):
        sys.exit('ERRO: Tamanho do bloco é muito grande para a chave e o alfabeto. Os arquivos indicados estão corretos?')
    
    # Cifrar mensagem:
    blocos_cifrados = cifrar_mensagem(mensagem, (n, e), tam_bloco)

    # Converter os blocos cifrados para string:
    for i in range(len(blocos_cifrados)):
        blocos_cifrados[i] = str(blocos_cifrados[i])
    conteudo_cifrado = ','.join(blocos_cifrados)
    
    # Gravação do arquivo de criptografia e codificação em base64
    conteudo_cifrado = f'{len(mensagem)}_{tam_bloco}_{conteudo_cifrado}'
    conteudo_cifrado = codificar_base64(conteudo_cifrado)
    file_object = open(nome_arquivo_decifrado, 'wb')
    file_object.write(conteudo_cifrado)
    file_object.close()

    return conteudo_cifrado


def arquivo_para_decifrar(nome_arquivo_cifrado, arquivo_chave):
    # Decifra o conteudo de um arquivo e retorna o conteudo decifrado

    tam_chave, n, d = ler_arquivo_chave(arquivo_chave)

    # Ler o arquivo de criptografia, decodificar e extrair o conteudo cifrado:
    file_object = open(nome_arquivo_cifrado)
    conteudo = decodificar_base64(file_object.read())
    file_object.close()
    tam_mensagem, tam_bloco, mensagem_cifrada = conteudo.split('_')
    tam_mensagem = int(tam_mensagem)
    tam_bloco = int(tam_bloco)

    # Checar se o tamanho da chave é suficiente para o tamanho do bloco:
    if not (math.log(2 ** tam_chave, len(SIMBOLOS)) >= tam_bloco):
        sys.exit('ERRO: Tamanho do bloco é muito grande para a chave e o alfabeto. Os arquivos indicados estão corretos?')

    # Converter o conteudo cifrado em blocos de inteiros:
    blocos_cifrados = []
    for bloco in mensagem_cifrada.split(','):
        blocos_cifrados.append(int(bloco))

    return decifrar_mensagem(blocos_cifrados, tam_mensagem, (n, d), tam_bloco)


if __name__ == '__main__':
    main()
