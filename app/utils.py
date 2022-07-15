import re
import os
import string
import random
from datetime import datetime

def verify_email_valid(user):
    return bool(re.match(r"[a-zA-Z0-9]+@[a-z]+.[a-z]+.?b?r?", user))

def verify_cpf_valid(user):
    return bool(re.match(r"[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}", user))

def validates_cpf(cpf):
    if len(cpf) != 11:
        return False

    cpf = cpf.replace('.', '').replace('-', '')

    novo_cpf = cpf[:9]

    conta = sum(int(novo_cpf[p]) * c for p, c in enumerate(range(10, 1, -1)))
    conta_2 = 11 - (conta % 11)

    primeiro_digito = '0' if conta_2 > 9 else str(conta_2)
    novo_cpf += primeiro_digito

    conta = sum(int(novo_cpf[p]) * c for p, c in enumerate(range(11, 1, -1)))
    conta_2 = 11 - (conta % 11)

    segundo_digito = '0' if conta_2 > 9 else str(conta_2)
    novo_cpf += segundo_digito
    
    return novo_cpf == cpf


def validates_cnpj(cnpj):
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    if len(cnpj) != 14:
        return False
    new_cnpj = cnpj[:12]
    p_num = list(cnpj[:4])
    rest = list(cnpj[4:12])

    calc = sum(
        int(p_num[pos]) * num for pos, num in enumerate(range(5, 1, -1))
    )

    for pos, num in enumerate(range(9, 1, -1)):
        calc += int(rest[pos]) * num

    account = 11 - (calc % 11)

    new_cnpj += '0' if account > 9 else str(account)
    p_num = list(new_cnpj[:5])
    rest = list(new_cnpj[5:13])

    for pos, num in enumerate(range(6, 1, -1)):
        calc += int(p_num[pos]) * num

    for pos, num in enumerate(range(9, 1, -1)):
        calc += int(rest[pos]) * num

    account = 11 - (calc % 11)

    new_cnpj += '0' if account > 9 else str(account)

    return new_cnpj == cnpj

def generate_hash_code(size_block = 5, qtd_blocks = 4, split_by = '-'):
    str_all_char_available = string.ascii_uppercase + string.digits
    blocks = []
    for item in range(qtd_blocks):
        block = [random.choice(str_all_char_available) for num in range(size_block)]
        block_join = ''.join(block)
        blocks.append(block_join)
    str_blocks = split_by.join(blocks)
    return str_blocks

if __name__ == '__main__':
    print(generate_hash_code())