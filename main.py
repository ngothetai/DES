import constants
from utils import *


plainText = read_plaintext_from_file('text.txt')
binary_blocks = plaintext_to_binary(plainText)
encrypt_code = []
keygen = plaintext_to_binary('12345')
keys = generate_keys(keygen[0]) # Chuyển keygen ban đầu thành 16 subkeys

for block in binary_blocks:
    res = binary_to_hex(encrypt_DES(block, keys)).upper()
    encrypt_code.append(res)

print(encrypt_code)