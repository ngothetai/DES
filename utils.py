import constants

# Chuyển đổi từ bản rõ sang các khối nhị phân
def char_to_bin(char):
    # Lấy mã ASCII của kí tự
    ascii_code = ord(char)
    # Chuyển mã ASCII thành chuỗi binary (loại bỏ "0b" ở đầu chuỗi binary)
    bin_code = bin(ascii_code)[2:]
    # Đảm bảo chuỗi binary luôn có độ dài 8 (8-bit)
    return bin_code.zfill(8)


def binary_to_char(binary_str):
    # Chuyển chuỗi binary thành số nguyên
    decimal_num = int(binary_str, 2)
    # Chuyển số nguyên thành kí tự
    char = chr(decimal_num)
    return char


def plaintext_to_binary(plaintext):
    binary_code = ''
    for char in plaintext:
        binary_code += char_to_bin(char)

    # Chia mã nhị phân thành các khối 64 bit, nếu khối nào không đủ sẽ chèn thêm 0 ở đầu
    binary_code = '0' * (64 - len(binary_code)%64) + binary_code
    binary_code = [binary_code[i:i+64] for i in range(0, len(binary_code), 64)]
    return binary_code


def binary_to_plaintext(binary_code):
    plaintext = ''
    for i in range(0, len(binary_code), 64):
        plaintext += binary_to_char(binary_code[i:i+64])
    return plaintext


def binary_to_hex(binary_str):
    # Chuyển chuỗi số nhị phân thành số nguyên thập phân
    decimal_num = int(binary_str, 2)

    # Chuyển số nguyên thập phân thành dạng hexa
    hex_value = hex(decimal_num)[2:]

    return hex_value

# Các hàm mã hóa DES


def read_plaintext_from_file(path_file:str):
    plaintext = ''
    with open(path_file) as f:
        plaintext = f.read()
    return plaintext


def permute(code, index_table, n):
    permutation = ""
    for i in range(0, n):
        permutation = permutation + code[index_table[i]-1]
    return permutation


def xor_strings(str1:str, str2:str):
    # Đảm bảo hai chuỗi có cùng độ dài
    length = min(len(str1), len(str2))
    str1 = str1[:length]
    str2 = str2[:length]

    # XOR bit-wise giữa từng cặp bit trong hai chuỗi
    result = ''.join(str(int(bit1) ^ int(bit2)) for bit1, bit2 in zip(str1, str2))

    return result



def f_func(R:str, K:str):
    res1 = permute(R, constants.E, 48) # 48-bits
    res2 = K # 48-bits
    res = xor_strings(res1, res2) # 48-bits
    index_s = 1
    bit_code = ''

    for i in range(0, 48, 6):
        data = res[i:i+6]
        row = int(data[0] + data[-1], 2)
        col = int(data[1:-1], 2)
        num = constants.S[index_s-1][row][col]
        bit = bin(num)[2:].zfill(4)
        bit_code += bit
        index_s += 1
    return permute(bit_code, constants.P, 32)


def generate_keys(key):
    def shift_left(k, nth_shifts):
        s = ""
        for i in range(nth_shifts):
            for j in range(1, len(k)):
                s = s + k[j]
            s = s + k[0]
            k = s
            s = ""
        return k
    hihi = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    k1 = permute(key, constants.PC_1, 56)
    C = k1[:28]
    D = k1[28:]
    keys = []
    for i in range(16):
        C = shift_left(C, hihi[i])
        D = shift_left(D, hihi[i])
        keys.append(permute(C+D, constants.PC_2, 48))
    return keys


def encrypt_DES(data:str, keys):
    data = permute(data, constants.IP, 64)
    L = data[:32]
    R = data[32:]

    for i in range(16):
        L_after = R
        R_after = xor_strings(L, f_func(R, keys[i]))
        if i != 15:
            L, R = L_after, R_after
    out = permute(R+L, constants.IP_1, 64)
    return out