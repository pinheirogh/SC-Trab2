## Fluxo de Execução
- Lado A (Emissor)
    - Gerar chaves RSA
        - Checar primalidade dos número p e q cada um com 1024 bits
            - Miller-Rabin
    - Gerar chave de sessão (128 ou 256 bits)
    - Cifrar simetricamente documento com chave de sessão 
    - Cifrar assimetricamente (c/ chave pública do receptor) a chave de sessão usando OAEP
    - Calcular o hash do documento não cifrado 
    - Cifrar o hash do documento (c/ chave privada do emissor)
    - Enviar:
        - Chave de sessão cifrada assimetricamente + IV
        - Documento cifrado simetricamente
        - Hash cifrado (Assinatura) assimetricamente
- Lado B (Receptor)
    - Decifrar a chave de sessão (c/ chave privada do receptor)
    - Decifrar o documento c/ chave de sessão decifrada
    - Calcular o hash do documento decifrado
    - Decifrar a assinatura (Hash cifrado) (c/ chave pública do emissor)
    - Fazer comparação dos hashes


## Bibliografia
- Miller-Rabin
    - Faster Primality Test - Applied Cryptography: https://youtu.be/p5S0C8oKpsM
- RSA
    - RSA Digital Signature Scheme using Python - GeeksforGeeks: https://www.geeksforgeeks.org/rsa-digital-signature-scheme-using-python/
    - RSA (sistema criptográfico) – Wikipédia, a enciclopédia livre (wikipedia.org): https://pt.wikipedia.org/wiki/RSA_(sistema_criptogr%C3%A1fico)#Gera%C3%A7%C3%A3o_das_chaves
- OAEP
    - Optimal asymmetric encryption padding - Wikipedia: https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding
    - Improving the security of RSA with OAEP | by Prakhash Sivakumar | Blue Space | Medium: https://medium.com/blue-space/improving-the-security-of-rsa-with-oaep-e854a5084918
    - public key - How does OAEP improve the security of RSA? - Cryptography Stack Exchange: https://crypto.stackexchange.com/questions/8383/how-does-oaep-improve-the-security-of-rsa
    - OAEP - Applied Cryptography: https://youtu.be/ZwPGE5GgG_E
    - Oaep Solution - Applied Cryptography: https://youtu.be/bU4so01qMP4
    - Udacity/challenge 5.py at master · corylstewart/Udacity (github.com): https://github.com/corylstewart/Udacity/blob/master/cs%20387/challenge%205.py
    - Mask generation function - Wikipedia: https://en.wikipedia.org/wiki/Mask_generation_function
- Hash
    - Python hash() method - GeeksforGeeks: https://www.geeksforgeeks.org/python-hash-method/#:~:text=Python%20hash()%20function%20is,while%20looking%20at%20a%20dictionary.
    - Mask generation function - Wikipedia: https://en.wikipedia.org/wiki/Mask_generation_function
- AES
    - rdomanski/AES-CTR: Python implementation of AES encryption algorithm in counter mode. (github.com): https://github.com/rdomanski/AES-CTR
    - Using AES for Encryption and Decryption in Python Pycrypto | Novixys Software Dev Blog: https://www.novixys.com/blog/using-aes-encryption-decryption-python-pycrypto/
- BASE64
    - Encoding and Decoding Base64 Strings in Python (stackabuse.com): https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/ 
