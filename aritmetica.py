def mdc(a, b):
    # Retorna o MDC de 'a' e 'b' usando o algoritmo de Euclides
    while a != 0:
        a, b = b % a, a
    return b


def inverso_modular(a, m):
    # Retorna o inverso modular de 'a' em 'm' equivalente a a*x % m = 1

    if mdc(a, m) != 1:
        return None 

    # Algoritmo de Euclides Estendido
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m