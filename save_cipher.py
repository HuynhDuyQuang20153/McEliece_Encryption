import os

class Excel_input:
    def __init__(self, file_enc, cipherText, path_save):
        self.path_save = path_save
        self.file_enc = file_enc
        self.cipherText = cipherText
        self.location_save_cipher = None

    def Excel_Write_input(self):
        txt_path = os.path.join(self.path_save, self.file_enc)

        with open(txt_path, 'w') as file:
            for row in self.cipherText:
                file.write(' '.join(row) + '\n')

        # print(f"\t- Save cipher '.txt' in: {txt_path}")
        self.location_save_cipher = txt_path
        return self.location_save_cipher
