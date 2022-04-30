import hashlib

def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return ''.join(str(x) for x in m)

def toDecimal(a):
    resultado = []
    for x in range(len(a), 8, -8):
        teste = a[x-8:x]
        if(teste != ''):
            decimal = int(teste, 2)
            resultado.append(decimal)
        
    resultado = resultado[::-1]
    return ''.join(str(x) for x in resultado)
    


## Importado da wikipedia
def i2osp(integer: int, size: int = 4) -> str:
    teste = [str((integer >> (8 * i)) & 0xFF) for i in reversed(range(size))]
    teste = [toBinary(x) for x in teste]
    return ''.join(x for x in teste)

def mgf1(input_str: bytes, length: int, hash_func=hashlib.sha1) -> str:
    """Mask generation function."""
    counter = 0
    output = ''

    # Converter input_str para string
    # semente_str = input_str.decode('utf-8')

    while len(output) < length:
        C = i2osp(counter, 4)

        # Concatenar C e input_str
        convertido = input_str + C    
        output += toBinary(str(int(hash_func(convertido.encode('utf-8')).hexdigest(), 16)))

        counter += 1
    return output[:length]
## Importado da wikipedia


def xor(a, b):
    assert len(a) == len(b)
    a, b = int(a), int(b)
    string = str(a^b)    
    return string
    #return [aa^bb for aa, bb in zip(a, b)]

def final_xor(L, R):
    # while (len(L) != len(R)):
    #     L = '0' + L
    ans = ""
    for i in range(len(L)):
        if (L[i] == '0' and R[i] == '0'):
            ans += '0'
        elif (L[i] == '0' and R[i] == '1'
              or L[i] == '1' and R[i] == '0'):
            ans += '1'
        else:
            ans += '0'
    return ans

def oaep_pad(message, nonce_r_k0, g, h):
    k1 = ''.join(str(x) for x in [0] * (g - len(message)))
    mm = toBinary(message + k1)
    G = final_xor(mm, mgf1(nonce_r_k0, len(mm)))
    H = final_xor(nonce_r_k0, mgf1(G, len(nonce_r_k0)))
    return G + H

def encrypt(message, n, public_key, private_key, nonce, g, h):
    oaep = oaep_pad(message, nonce, g, h)
    # m_int = bits_to_int(oaep)
    oaep_decimal = int(toDecimal(oaep))


    lista_letras = []
    for x in range(len(oaep), 8, -8):
        letra = pow(int(oaep[x-8:x],2), int(public_key),int(n))
        lista_letras.append(letra)
    print(lista_letras)

    lista_binario = []
    for x in lista_letras[::-1]:
        bina = pow(x, int(private_key), int(n))
        lista_binario.append(bina)
    print(lista_binario)
    a = pow(oaep_decimal, int(public_key), int(n))
    b = pow(a, int(private_key), int(n))
    # print(len(oaep)) # cifrar oaep com RSA
    # print()
    # print(len(str(oaep_decimal)))
    # print()
    # print(str(b))]
    # print(oaep)
    return 

# def decrypt(ciphertext, n, private_key, g, h):
#     cipher = string_to_bits(ciphertext)
#     c_int = bits_to_int(cipher)
#     m_int = pow(c_int, private_key, n)
#     m_int = convert_to_bits(m_int)
#     oaep = pad_bits(m_int, g+h)
#     G = oaep[:g]
#     H = oaep[g:]
#     nonce = xor(H, hash(G, h))
#     mm = xor(G, hash(nonce,g))
#     return bits_to_string(mm[:g])

if __name__ == '__main__':
    msg = "1075462638942343170431007712712127768414212437191421284944632765736253882681546365485768531246449887912356478022273320923931899161274047736815281870140443582272543795350602127347816487471774352874411819310657595256838955520063051402124010906155485945532369919498537478984507880257644094624149592666037664402496401554924765022240179072013951231063735237353428480802994142353720567174365800721569876025430606757585912851909076673398538099749966699486706843702355682395924056194086697368433490876213555264521280020156496440291830674913490768383627410341453117166000692169350546248614587196656123888756299370384315012187281851441410435"
    n = "19048935368631953475760093602328077659617239509964402277027146826813815867785094071788913295243765772226257923381276299956686978055002918396101208607693283549738187629466017726861440625151093995801073378618061355980131719993329136307370162199849836683279935326562293798833231761577928442106463093553191393110827571534059198334234622448491939613327813311491579041676049549039253847386160927813568533562130019290993795406202286541646962464738253856795645339669908149080181539772910019660987383190729182171860598997352960979194212621994444606286749401600810722329309173976149393508894323304786562055516154299651015380133"
    public_key = "129411339615955422569181589335382354089280095724688166649585225565315143458081904297707681552407476610664933514926744214490100236649296338384877218465137104850884033210749273144118695239795593079798273590490521956833323918503839793000647230689437092404348322835714679809242656412349418964016671185241149879823"
    private_key = "12054520812782802344848890640420323879558638977696717710486585033990463037853458829554593497094304020365204573684701092654171508438157311329927343800285753889534847323326447849767039646536196465570706052100227416227520758094460454361460261963887379957881050389164705940047253451819388807373791565603639596044573500841493786977033754444004924559588212795067463144703245485504529990664520776941809257511577369812582367768878752670153196270680934520196299067760557372940286486109536384178091552250915675835050412590979481093630917199740761005895389903667917228936606835721619330544109024062367789226353930776315572368387"
    
    # print(len(n.encode('utf-8')))
    # print(int(len(public_key)))

    g = int(len(msg))
    g+=5
    h = int(len(msg))
    h+=5

    nonce = toBinary(''.join(str(x) for x in [0] * g)) # g bits
    encrypt(msg, n, public_key, private_key, nonce, g, h)

    # tt = '00011000 01110000 10000010'
    # print(toDecimal(tt))