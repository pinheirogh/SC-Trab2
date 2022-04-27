import random


def miller_rabin(num):
    # Retorna True se num é primo, False se não é primo.
    if num % 2 == 0 or num < 2:
        return False  
    if num == 3:
        return True

    s = num - 1
    t = 0

    while s % 2 == 0:
        s = s // 2
        t += 1

    for tentativa in range(5):  # Tenta falsificar a primalidade 5 vezes.
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)

        if v != 1:  # Se o v = 1 o teste não se aplica
            i = 0

            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num

    return True


def gerar_n_primo_grande(tam_chave=1024):
    # Retorna um número primo de tamanho definido por tam_chave.
    while True:
        num = random.randrange(2**(tam_chave-1), 2**(tam_chave))
        if (num >= 2) and miller_rabin(num):
            return num
