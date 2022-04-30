from Crypto.Cipher import AES
from Crypto.Util import Counter
import random


key = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])


counter = Counter.new(128, initial_value=int(iv,16))


cipher=AES.new(key, AES.MODE_CTR, counter=counter)

mensagem = 'Teste de mensagem'

mensagem_enc = cipher.encrypt(mensagem)