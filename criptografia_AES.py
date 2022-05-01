from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Random import get_random_bytes
import random
import base64
from criptografia_RSA import codificar_base64, decodificar_base64

def main():    
    opcao = input('''ALGORITMO AES\n1 - Cifrar\n2 - Decifrar\nOpção: ''')

    if opcao == '1':
        nome_arquivo_mensagem = 'arquivos_texto/' + input('Digite o nome do arquivo de mensagem: ') + '.txt'

        # Abrir arquivo para leitura de texto
        with open(nome_arquivo_mensagem, 'r') as arquivo:
            mensagem = arquivo.read()
        # Fechar arquivo
        arquivo.close()

        mensagem_enc, chave_sessao, iv = encrypt(mensagem)

        nome_arquivo_cifrado = 'arquivos_texto/msg_cifrada_AES.txt'
        conteudo_cifrado = base64.b64encode(mensagem_enc)

        file_object = open(nome_arquivo_cifrado, 'wb')
        file_object.write(conteudo_cifrado)
        file_object.close()

        nome_arquivo_chavesessao = 'arquivos_texto/chave_sessao_AES.txt'
        chave_64 = base64.b64encode(chave_sessao)

        conteudo_cifrado = chave_64
        file_object = open(nome_arquivo_chavesessao, 'wb')
        file_object.write(conteudo_cifrado)
        file_object.close()

        nome_arquivo_iv = 'arquivos_texto/iv_AES.txt'
        conteudo_cifrado = iv
        file_object = open(nome_arquivo_iv, 'w')
        file_object.write(conteudo_cifrado)
        file_object.close()
        
        print('Mensagem cifrada com sucesso! Arquivos gerados com sucesso!')

    elif opcao == '2':
        nome_arquivo_cifrado = 'arquivos_texto/' + input('Digite o nome do arquivo de mensagem cifrada: ') + '.txt'
        nome_arquivo_chavesessao = 'arquivos_texto/' + input('Digite o nome do arquivo de chave: ') + '.txt'
        nome_arquivo_iv = 'arquivos_texto/' + input('Digite o nome do arquivo de iv: ') + '.txt'

        # Abrir arquivo para leitura de texto
        with open(nome_arquivo_cifrado, 'r') as arquivo:
            mensagem_cifrada = arquivo.read()
        # Fechar arquivo
        arquivo.close()

        mensagem_cifrada = base64.b64decode(mensagem_cifrada)

        # Abrir arquivo para leitura de texto
        with open(nome_arquivo_chavesessao, 'r') as arquivo:
            chave_sessao = arquivo.read()
        # Fechar arquivo
        arquivo.close()

        chave_sessao = base64.b64decode(chave_sessao)

        # Abrir arquivo para leitura de texto
        with open(nome_arquivo_iv, 'r') as arquivo:
            iv = arquivo.read()
        # Fechar arquivo
        arquivo.close()


        texto_decifrado = decrypt(mensagem_cifrada, chave_sessao, iv)

        nome_arquivo_decifrado = 'arquivos_texto/msg_decifrada_AES.txt'
        conteudo_cifrado = texto_decifrado
        file_object = open(nome_arquivo_decifrado, 'w')
        file_object.write(conteudo_cifrado)
        file_object.close()

        print()
        print('MENSAGEM DECIFRADA:')
        print(texto_decifrado)

def encrypt(mensagem):
    chave_sessao = get_random_bytes(16)
    iv = ''.join([str(random.randint(0, 0xFF)) for i in range(16)])
    counter = Counter.new(128, initial_value=int(iv, 16))

    cifracao = AES.new(chave_sessao, AES.MODE_CTR, counter=counter)

    mensagem_enc = cifracao.encrypt(mensagem)

    return mensagem_enc, chave_sessao, iv

def decrypt(mensagem_enc, chave_sessao, iv):

    counter = Counter.new(128, initial_value=int(iv, 16))
    decifracao = AES.new(chave_sessao, AES.MODE_CTR, counter=counter)
    mensagem_dec = str(decifracao.decrypt(mensagem_enc)).replace('b\'', '').replace('\'', '')

    return mensagem_dec

if __name__ == '__main__':
    main()