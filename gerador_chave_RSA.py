import random
import sys
import os
import gerador_num_primo
import aritmetica
import base64


def main():
    nome_arquivo = input('Digite o nome do arquivo: ')
    print('Gerando arquivos de chaves...')
    gravar_em_arquivo(nome_arquivo, 1024)
    print('Arquivos de chaves gerados com sucesso!')

def codificar_base64(conteudo):
    # Codifica conteudo em base64
    return base64.b64encode(bytes(conteudo, 'utf-8'))

def gerar_chave(tam_chave):
    # Cria uma chave publica e privada de tam_chave bits
    p = 0
    q = 0

    # Criação de números primos p e q e calculo de n
    while p == q:
        p = gerador_num_primo.gerar_n_primo_grande(tam_chave)
        q = gerador_num_primo.gerar_n_primo_grande(tam_chave)

    n = p * q

    # Criação de numero 'e' relativamente primo a (p-1)*(q-1)
    while True:
        e = random.randrange(2 ** (tam_chave - 1), 2 ** (tam_chave))
        if aritmetica.mdc(e, (p - 1) * (q - 1)) == 1:
            break

    # Cálculo de 'd' ou inverso modular de 'e'
    d = aritmetica.inverso_modular(e, (p - 1) * (q - 1))

    chave_publica = (n, e)
    chave_privada = (n, d)

    print('Chave pública:', chave_publica)
    print('Chave privada:', chave_privada)

    return (chave_publica, chave_privada)


def gravar_em_arquivo(nome_arquivo, tam_chave):
    # Cria arquivos contendo as chaves publica e privada 
    # Em cada arquivo há: tamanho da chave, 'n', 'e' ou 'd' separados por virgula

    # Checagem de segurança para evitar sobrescrita de arquivos
    if os.path.exists(f'arquivos_texto/{nome_arquivo}_chavepub.txt') or os.path.exists(f'arquivos_texto/{nome_arquivo}_chavepriv.txt'):
        sys.exit(f'PERIGO: O arquivo arquivos_texto/{nome_arquivo}_chavepub.txt ou arquivos_texto/{nome_arquivo}_chavepriv.txt ja existem! Use outro nome ou delete os arquivos.')

    chave_publica, chave_privada = gerar_chave(tam_chave)

    print(f'Gravando as chaves no arquivo {nome_arquivo}')

    file_object = open(f'arquivos_texto/{nome_arquivo}_chavepub.txt', 'wb')
    file_object.write(codificar_base64(f'{tam_chave},{chave_publica[0]},{chave_publica[1]}'))
    file_object.close()

    file_object = open(f'arquivos_texto/{nome_arquivo}_chavepriv.txt', 'wb')
    file_object.write(codificar_base64(f'{tam_chave},{chave_privada[0]},{chave_privada[1]}'))
    file_object.close()


if __name__ == '__main__':
    main()
