import hashlib

def main():
    print('GERAÇÃO DE HASH SHA3-256')
    # Receber do terminal nome do arquivo para leitura
    raiz_arquivo = input('Digite o nome do arquivo de mensagem: ')
    nome_arquivo_mensagem = f'arquivos_texto/{raiz_arquivo}.txt'
    hash_gerado = gerar_hash(nome_arquivo_mensagem)
    print('Hash gerado com sucesso!')

    # Gravar hash gerado em arquivo
    nome_arquivo_hash = f'arquivos_texto/hash_{raiz_arquivo}.txt'
    with open(nome_arquivo_hash, 'w') as arquivo:
        arquivo.write(hash_gerado.hexdigest())
    arquivo.close()
    print('Hash gravado com sucesso!')


def gerar_hash(nome_arquivo_mensagem):
    # Abrir arquivo para leitura de texto
    with open(nome_arquivo_mensagem, 'r') as arquivo:
        mensagem = arquivo.read()
    # Fechar arquivo
    arquivo.close()

    mensagem_encoded = mensagem.encode()

    return hashlib.sha3_256(mensagem_encoded)

if __name__ == '__main__':
   main()