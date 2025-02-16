# Sinh vien 1: Huynh Duy Quang - 19520141
# Sinh vien 2: Tran Xuan Thang - 19524341

from mathutils import *
import numpy as np


class McEliece_create_key:
    def __init__(self, G, S, P):
        self.G = G
        self.S = S
        self.P = P
        self.Gp = None

    def keys(self):
        try:
            self.Gp = create_matrix_Gp(self.G, self.S, self.P)
        except ValueError as e:
            print(f"Error from 'class_mceliece_key': {e}")
        return None


class McEliece_create_encrypt:
    def __init__(self, split_bits_list, Gp):
        self.split_bits_list = split_bits_list
        self.Gp = Gp
        self.y = None

    def encrypt(self):
        try:
            enc_msg = []
            for split_bits in self.split_bits_list:
                enc_bits = hamming_encrypt(split_bits, self.Gp)
                enc_msg.append(enc_bits)
            self.y = enc_msg
        except ValueError as e:
            print(f"Error from 'class_mceliece_encrypt': {e}")
        return None



class McEliece_create_decrypt:
    def __init__(self, dec_bit, P_inv, S_inv, R, H):
        self.dec_bit = dec_bit
        self.P_inv = P_inv
        self.S_inv = S_inv
        self.x = None
        self.R = R
        self.H = H

    def decrypt(self):
        try:
            dec_msg_0 = []
            for enc_bits in self.dec_bit:
                dec_msg = []
                for abc in enc_bits:
                    enc_bits = np.array([int(x) for x in abc])
                    c_hat = np.mod(enc_bits.dot(self.P_inv), 2)
                    err_idx = detect_error(c_hat, self.H)
                    flip_bit(c_hat, err_idx)
                    m_hat = hamming7_4_decode(c_hat, self.R)
                    m_out = np.mod(m_hat.dot(self.S_inv), 2)
                    str_dec = ''.join(str(x) for x in m_out)
                    dec_msg.append(str_dec)
                dec_msg_0.append(dec_msg)
            self.x = dec_msg_0

        except ValueError as e:
            print(f"Error from 'class_mceliece_decrypt': {e}")
            
        return None

