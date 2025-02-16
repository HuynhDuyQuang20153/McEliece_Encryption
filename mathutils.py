import numpy as np
import random
from joblib import Parallel, delayed


def brute_force(A, B):
    n, m, p = A.shape[0], A.shape[1], B.shape[1]
    C = np.zeros((n, p))
    for i in range(n):
        for j in range(p):
            for k in range(m):
                C[i][j] += A[i][k]*B[k][j]
    return C


def split(matrix):
    n = len(matrix)
    return matrix[:n//2, :n//2], matrix[:n//2, n//2:], matrix[n//2:, :n//2], matrix[n//2:, n//2:]


def strassen_nxn(A, B, m):
    if len(A) <= 2:
        return brute_force(A, B)

    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    arg_list = [(np.add(A11,A22), np.add(B11,B22), m), 
                 (np.add(A21,A22), B11, m), (A11, np.subtract(B12,B22), m), 
                 (A22, np.subtract(B21,B11), m), (np.add(A11,A12), B22, m), 
                 (np.subtract(A11,A21), np.add(B11,B12), m), 
                 (np.subtract(A12,A22), np.add(B21,B22), m)]
    
    results = Parallel(n_jobs=7)(delayed(strassen_nxn)(A, B, m) for A, B, m in arg_list)
    p1, p2, p3, p4, p5, p6, p7 = get_strassen(results)

    C11 = np.add(np.subtract(np.add(p1,p4), p5),p7) 
    C12 = np.add(p3,p5)
    C21 = np.add(p2,p4) 
    C22 = np.subtract(np.subtract(np.add(p3, p1), p2), p6)

    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    C = C[:m, :m]
    return C


def strassen_nxm(A, B, n, m):
    if len(A) <= 2:
        return brute_force(A, B)

    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    arg_list = [(np.add(A11,A22), np.add(B11,B22), n, m), 
                 (np.add(A21,A22), B11, n, m), (A11, np.subtract(B12,B22), n, m), 
                 (A22, np.subtract(B21,B11), n, m), (np.add(A11,A12), B22, n, m), 
                 (np.subtract(A11,A21), np.add(B11,B12), n, m), 
                 (np.subtract(A12,A22), np.add(B21,B22), n, m)]
    
    results = Parallel(n_jobs=7)(delayed(strassen_nxm)(A, B, n, m) for A, B, n, m in arg_list)
    p1, p2, p3, p4, p5, p6, p7 = get_strassen(results)

    C11 = np.add(np.subtract(np.add(p1,p4), p5),p7) 
    C12 = np.add(p3,p5)
    C21 = np.add(p2,p4) 
    C22 = np.subtract(np.subtract(np.add(p3, p1), p2), p6)

    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    C = C[:n, :m]
    return C


def get_strassen(res):
    try:
        p1 = res[0]
        p2 = res[1]
        p3 = res[2]
        p4 = res[3]
        p5 = res[4]
        p6 = res[5]
        p7 = res[6]
        return p1, p2, p3, p4, p5, p6, p7
    
    except ValueError as e:
        print(f"Error from 'get_strassen': {e}")

    return None


def string_to_binary(text):
    try:
        binary_string = ""
        for char in text:
            ascii_value = ord(char)                 
            binary = bin(ascii_value)[2:].zfill(8)  
            binary_string += binary                 
        return binary_string
    except ValueError as e:
        print(f"Error from 'string_to_binary': {e}")
    return None


def random__matrix_S(n):
    try:
        a = np.random.randint(0, 2, size=(n, n))
        while np.linalg.det(a) == 0:
            a = np.random.randint(0, 2, size=(n, n))
        return a
    except ValueError as e:
        print(f"Error from 'random__matrix_S': {e}")
    return None


def random_matrix_P(n):
    try:
        i = np.eye(n)
        p = np.random.permutation(i)
        return p.astype(int)
    except ValueError as e:
        print(f"Error from 'random_matrix_P': {e}")
    return None


# def create_matrix_Gp(G, S, P):
#     try:
#         return np.transpose(np.mod((S.dot(np.transpose(G))).dot(P), 2))
#     except ValueError as e:
#         print(f"Error from 'create_matrix_Gp': {e}")
#     return None

def create_matrix_Gp(G, S, P):
    try:
        G1 = np.transpose(G)
        SG = np.mod(S.dot(G1), 2)
        SGP = np.mod(SG.dot(P), 2)
        s_row = S.shape[0]   # 4 dong S
        g_col = G1.shape[1]  # 7 cot G
        p_col = P.shape[1]   # 7 cot P
        q = 2 ** int(np.ceil(np.log2(max(len(G1), len(P), len(S), len(G1[0]), len(P[0]), len(S[0]))))) # 8 dong 8 cot
        A_new = np.zeros((q, q))
        A_new[:len(G1), :len(G1[0])] = G1
        B_new = np.zeros((q, q))
        B_new[:len(P), :len(P[0])] = P
        C_new = np.zeros((q, q))
        C_new[:len(S), :len(S[0])] = S
        Gp_1 = np.mod(strassen_nxm(C_new, A_new, s_row, g_col), 2).astype(int)
        Gp_1_row = Gp_1.shape[0]   # 4 dong G_1
        Gp_1_new = np.zeros((q, q))
        Gp_1_new[:len(Gp_1), :len(Gp_1[0])] = Gp_1
        G_hat = np.transpose(np.mod(strassen_nxm(Gp_1_new, B_new, Gp_1_row, p_col), 2)).astype(int)
        return G_hat
    except ValueError as e:
        print(f"Error from 'create_matrix_Gp': {e}")
    return None





def can_create_matrix(X):
    try:
        num_cols = len(X[0])
        same_num_cols = True
        for row in X:
            if len(row) != num_cols:
                same_num_cols = False
                break
        return same_num_cols
    except ValueError as e:
        print(f"Error from 'can_create_matrix': {e}")
    return None 


def paddingMatrix(X):
    try:
        max_length = max([len(row) for row in X])
        input = np.full((len(X), max_length), -1)
        already_assigned = np.zeros_like(input, dtype=bool)
        for i, row in enumerate(X):
            input[i, :len(row)] = row
            already_assigned[i, :len(row)] = True
        return input.astype(int), already_assigned
    except ValueError as e:
        print(f"Error from 'padding to matrix': {e}")
    return None 


def split_binary_string(str, n):
    try:
        new = []
        for abc in str:
            bits_list = [abc[i:i + n] for i in range(0, len(abc), n)]
            if len(bits_list[-1]) < 4 and len(bits_list[-1]) > 0:
                number = (4 - len(bits_list[-1])) + bits_list[-1]
                bits_list[-1] = '0'*number
            new.append(bits_list)
        return new
    except ValueError as e:
        print(f"Error from 'split_binary_string': {e}")
    return None


def add_single_bit_error(enc_bits):
    error = [0] * 7
    idx = random.randint(0, 6)
    error[idx] = 1
    return np.mod(enc_bits + error, 2)


def hamming_encrypt(p_str, G_hat):
    try:
        arr = []
        index = 0
        for abc in p_str:
            p = np.array([int(x) for x in abc])
            prod = np.mod(G_hat.dot(p), 2)
            err_enc_bits = add_single_bit_error(prod)
            if index < len(p_str):
                str_enc = ''.join(str(x) for x in err_enc_bits)
                arr.append(str_enc)
                index += 1
        return arr
    except ValueError as e:
        print(f"Error from 'hamming_encrypt': {e}")
    return None


def matrix_back(dec_matrix_4bit):
    try:
        ggg = []
        for elec in dec_matrix_4bit:
            elec_index = ""
            for abc in elec:
                elec_index+=abc
            ggg.append(elec_index)
        # print("\nBinary_matrix_data_after_decode: \n", ggg)
        return ggg
    except ValueError as e:
        print(f"Error from 'matrix_back': {e}")
    return None


def bits_to_str(arr, matrix_B):
    rows = matrix_B.shape[0]
    cols = matrix_B.shape[1]
    decimal_value = []

    for pt in arr:
        my_chunks_mini = [pt[i:i + 8] for i in range(0, len(pt), 8)]
        de_f = ""
        for abc in my_chunks_mini:
            my_chars = chr(int(abc, 2))
            de_f += my_chars 
        decimal_value.append(de_f)

    index = 0
    for i in range(rows):
        for j in range(cols):
            if index < len(decimal_value):
                matrix_B[i][j] = decimal_value[index]
                index += 1
    return matrix_B


def encode_back(dec_matrix, matrix_encoder):
    try:
        matrix_B = np.full_like(matrix_encoder, -1)
        txt = bits_to_str(dec_matrix, matrix_B)
        # print('\nMatrix_data_after_decode: \n', txt)
        return txt
    except ValueError as e:
        print(f"Error from 'matrix_back': {e}")
    return None


def hamming7_4_decode(c, R):
    prod = np.mod(R.dot(c), 2)
    return prod


def flip_bit(bits, n):
    bits[n] = (bits[n] + 1) % 2


def detect_error(err_enc_bits, H):
    err_idx_vec = np.mod(H.dot(err_enc_bits), 2)
    err_idx_vec = err_idx_vec[::-1]
    err_idx = int(''.join(str(bit) for bit in err_idx_vec), 2)
    return err_idx - 1


def add_error(enc_bits):
    try:
        error = [0] * 7
        idx = random.randint(0, 6)
        error[idx] = 1
        return np.mod(enc_bits + error, 2)
    except ValueError as e:
        print(f"Error from 'add_error': {e}")
    return None


def find_error(err_enc_bits, H):
    try:
        err_idx_vec = np.mod(H.dot(err_enc_bits), 2)
        err_idx_vec = err_idx_vec[::-1]
        err_idx = int(''.join(str(bit) for bit in err_idx_vec), 2)
        return err_idx - 1
    except ValueError as e:
        print(f"Error from 'find_error': {e}")
    return None


def fix_bit(bits, n):
    try:
        bits[n] = (bits[n] + 1) % 2
    except ValueError as e:
        print(f"Error from 'fix_bit': {e}")
    return None


def hamming_decrypt(c, R):
    try:
        prod = np.mod(R.dot(c), 2)
        return prod
    except ValueError as e:
        print(f"Error from 'hamming_decrypt': {e}")
    return None

