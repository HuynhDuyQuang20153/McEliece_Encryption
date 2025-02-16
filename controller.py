from mceliece import *
from save_plain import *
from save_cipher import *
from mathutils import *
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def read_input_file(path_save_read, choose):
    try:
        if choose: 
            with open(path_save_read, encoding='utf-8') as f:
                text = f.read() 
            # print("Data: \n", text)

            with open(path_save_read, encoding='utf-8') as f:
                data_line = f.readlines()
            data_line = [line.strip() for line in data_line]  
            tokens = [doc.split() for doc in data_line]
                    
            label_encoder = LabelEncoder()
            encoder = label_encoder
            label_encoder.fit([token for doc in tokens for token in doc])
            X = [[label_encoder.transform([token])[0] for token in doc] for doc in tokens]
            already_assigned = None 

            check = can_create_matrix(X)
            if check:
                matrix_text = np.array(X)
            else:
                matrix_text, already_assigned = paddingMatrix(X)
            
            rows = matrix_text.shape[0]
            cols = matrix_text.shape[1]
            binary_matrix = []

            for i in range(rows):  
                for j in range(cols):  
                    abc = str(matrix_text[i, j])
                    bi_str = ""
                    for char in abc:
                        ascii_value = ord(char)         
                        binary = bin(ascii_value)[2:].zfill(8)
                        bi_str += binary 
                    binary_matrix.append(bi_str)

            return matrix_text, binary_matrix, already_assigned, encoder
        
        else:
            header = list(range(pd.read_excel(path_save_read).shape[1]))
            df = pd.read_excel(path_save_read, header=None)
            df.columns = header + df.columns[len(header):].tolist()
            df.fillna('', inplace=True)

            data_line = np.array(df)
            for i in range(len(data_line)):
                for j in range(len(data_line[i])):
                    if isinstance(data_line[i][j], int) or isinstance(data_line[i][j], float):
                        data_line[i][j] = str(data_line[i][j])

            label_encoder = LabelEncoder()
            encoder = label_encoder
            label_encoder.fit([token for doc in data_line for token in doc])

            already_assigned = None 
            text = None

            X = [[label_encoder.transform([token])[0] for token in doc] for doc in data_line]
            max_length = max([len(row) for row in X])
            input = np.zeros((len(X), max_length))
            already_assigned = np.zeros_like(input, dtype=bool)

            for i, row in enumerate(X):
                input[i, :len(row)] = row
                already_assigned[i, :len(row)] = True

            matrix_text = input.astype(int)
            rows = matrix_text.shape[0]
            cols = matrix_text.shape[1]
            binary_matrix = []

            for i in range(rows):  
                for j in range(cols):  
                    abc = str(matrix_text[i, j])
                    bi_str = ""
                    for char in abc:
                        ascii_value = ord(char)         
                        binary = bin(ascii_value)[2:].zfill(8)
                        bi_str += binary 
                    binary_matrix.append(bi_str)

            return matrix_text, binary_matrix, already_assigned, encoder
        
    except Exception as e:
        print("ERROR READ INPUT FILE: ", e)
    return None



def read_output_file(path):
    try:
        array_dec = []
        with open(path, encoding='utf-8') as file:
            for line in file:
                row = line.strip().split(' ')
                array_dec.append(row)   
        return array_dec
    except Exception as e:
        print("ERROR READ OUTPUT FILE: ", e)
    return None



def create_key(G, S, P):
    try:
        mc = McEliece_create_key(G, S, P)
        mc.keys()
        return mc.Gp  
    except Exception as e:
        print("ERROR CREATE KEY:", e)



def create_encrypt(bits_list, Gp):
    try:
        mc = McEliece_create_encrypt(bits_list, Gp)
        mc.encrypt()
        return mc.y
    except Exception as e:
        print("ERROR CREATE ENCRYPT:", e)



def save_cipher_file(name, cipherText, path_save):
    try:
        # print("\n\n\t************************* SAVE DATA CIPHER *************************")
        excel = Excel_input(name, cipherText, path_save)
        excel.Excel_Write_input()
        return excel.location_save_cipher
    except Exception as e:
        print("ERROR SAVE DATA CIPHER:", e)



def save_plain_file(name, text_recovery, path_save, choose):
    try:
        # print("\n\n\t***************************** SAVE DATA PLAIN ******************************")
        excel = Excel_output(name, text_recovery, path_save, choose)
        excel.Excel_Write_output()
        return excel.path_save_plain
    except Exception as e:
        print("ERROR SAVE DATA PLAIN:", e)



def create_decrypt(dec_bit, P_inv, S_inv, R, H):
    try:
        mc = McEliece_create_decrypt(dec_bit, P_inv, S_inv, R, H)
        mc.decrypt()
        return mc.x  
    except Exception as e:
        print("ERROR CREATE DECRYPT:", e)



def get_backtext(already_assigned, encoder, plainText, type_file_upload):
    try:
        if already_assigned is not None:
            X = []
            for i, row in enumerate(plainText):
                if np.all(already_assigned[i, :len(row)]):
                    X.append(list(row))

                elif not np.all(already_assigned[i, :len(row)]):
                    positive_indices = np.where(row >= 0)[0][:len(row)]
                    X.append(list(row[positive_indices]))

            for i in range(len(X)):
                for j in range(len(X[i])):
                    X[i][j] = int(X[i][j])

            if type_file_upload == False:
                # print(f"X: {X}")
                fake = []
                for doc in X:
                    words = encoder.inverse_transform(doc)
                    fake.append(words)

                # print(f"fake: \n{fake}")
                return fake
            
            else:
                texts = []
                for doc in X:
                    words = encoder.inverse_transform(doc)
                    text = " ".join(words)
                    texts.append(text)     
        
        else:
            texts = []
            for doc in plainText:
                words = encoder.inverse_transform(doc)
                text = " ".join(words)
                texts.append(text)
    
        text_final = '\n'.join(texts)
        return text_final
    except Exception as e:
        print("ERROR RECOVERY TEXT:", e)



def check_type_file_upload(file):
    try:
        return '.' in file and \
            file.rsplit('.', 1)[1].lower() in {'txt'}
    except Exception as e:
        print("ERROR CHECK TYPE FILE:", e)
