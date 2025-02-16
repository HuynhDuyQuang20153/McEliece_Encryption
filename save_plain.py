import os
import pandas as pd

class Excel_output:
    def __init__(self, file_dec, text_recovery, path_save, type_file_upload):
        self.file_dec = file_dec
        self.text_recovery = text_recovery
        self.path_save = path_save
        self.type_file_upload = type_file_upload
        self.path_save_plain = None

    def Excel_Write_output(self):
        if self.type_file_upload:
            txt_path = os.path.join(self.path_save, self.file_dec)
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(self.text_recovery)

            # print(f"\t- Save PlainText '.txt' in: {txt_path}")
            self.path_save_plain = txt_path
            return self.path_save_plain

        else:
            df = pd.DataFrame(self.text_recovery)
            df.columns = range(df.shape[1])

            df2 = df.applymap(lambda x: pd.to_numeric(x, errors='ignore') if isinstance(x, str) else x)
            xlsx_path = os.path.join(self.path_save, self.file_dec)
            df2.to_excel(xlsx_path, startrow=0, index=False, columns=None, header=False)

            # print(f"\t- Save PlainText .'xlsx' in: {xlsx_path}")
            self.path_save_plain = xlsx_path
            return self.path_save_plain