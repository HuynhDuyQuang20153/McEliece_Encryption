# python app.py     (để chạy chương trình)
# npm run obfuscate (để làm rối mã js)

from flask import Flask, request, redirect, render_template, send_file
from flask_sse import sse
from controller import *
import json
import os 
import numpy as np


from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt', 'xlsx'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), "Save_data_cipher")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")


path_save_cipher = None
location_save_plaintext = None
cipherText = None
matrix_encoder = None
already_assigned = None
encoder = None


G = np.array([[1, 1, 0, 1],
            [1, 0, 1, 1],
            [1, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

H = np.array([[1, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]])

R = np.array([[0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1]])

S = random__matrix_S(4)
S_inv = np.linalg.inv(S).astype(int)
P = random_matrix_P(7)
P_inv = np.linalg.inv(P).astype(int)



# ----------------RENDER HTML ------------------ #
@app.route('/')
def render_mceliece():
    return render_template('mceliece.html')



# ---------------- ENCRYPT ------------------ #
@app.route('/cipher', methods=['POST'])
def get_cipher():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    path_save_data_cipher = os.path.join(os.getcwd(), "Save_data_cipher")
    if not os.path.exists(path_save_data_cipher):
        os.mkdir(path_save_data_cipher)

    max_index = 0
    for f in os.listdir(path_save_data_cipher):
        if f.startswith("Save_turn_") and os.path.isdir(os.path.join(path_save_data_cipher, f)):
            index = int(f.split("_")[2])
            if index > max_index:
                max_index = index

    path_save_turn = os.path.join(path_save_data_cipher, "Save_turn_" + str(max_index + 1))
    if not os.path.exists(path_save_turn):
        os.mkdir(path_save_turn)

    filename_upload = secure_filename(file.filename)
    path_filename_upload = os.path.join(path_save_turn, filename_upload)
    file.save(path_filename_upload)

    type_file_upload = check_type_file_upload(filename_upload)

    global cipherText
    global matrix_encoder
    global already_assigned
    global encoder
    global path_save_cipher

    matrix_encoder, binary_matrix, already_assigned, encoder =  read_input_file(path_filename_upload, type_file_upload)
    os.remove(path_filename_upload)
    list_4_bits = split_binary_string(binary_matrix, 4)
    Gp = create_key(G, S, P)
    cipherText = create_encrypt(list_4_bits, Gp)

    name, ext = os.path.splitext(filename_upload)
    if ext == '.txt':
        ext_2 = '.txt'
    elif ext == '.xlsx':
        ext_2 = '.xlsx.txt'

    if len(name) > 10:
        new_name = name[:5] + '....' + name[-3:]
        filename_Enc_save = name + '_Enc' + ext_2
        path_save_cipher = save_cipher_file(filename_Enc_save, cipherText, path_save_turn)

        input_div = f'{new_name+ext}'
        output_div = new_name + '_Enc' + ext_2
        response = {'filename_input_1': input_div, 'filename_output_1': output_div}
        return json.dumps(response), 200, {'Content-Type': 'application/json'}
    
    filename_Enc_save = name + '_Enc' + ext  
    path_save_cipher = save_cipher_file(filename_Enc_save, cipherText, path_save_turn)

    input_div = f'{filename_upload}'
    output_div = name + '_Enc' + ext_2
    response = {'filename_input_1': input_div, 'filename_output_1': output_div}
    return json.dumps(response), 200, {'Content-Type': 'application/json'}



# ---------------- DECRYPT ------------------ #
@app.route('/plain', methods=['POST'])
def get_plain():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    path_save_data_plain = os.path.join(os.getcwd(), "Save_data_plain")
    if not os.path.exists(path_save_data_plain):
        os.mkdir(path_save_data_plain)

    max_index_2 = 0
    for f in os.listdir(path_save_data_plain):
        if f.startswith("Save_turn_") and os.path.isdir(os.path.join(path_save_data_plain, f)):
            index = int(f.split("_")[2])
            if index > max_index_2:
                max_index_2 = index

    filename_upload = secure_filename(file.filename)
    path_filename_upload = os.path.join(path_save_data_plain, filename_upload)
    file.save(path_filename_upload)

    path_save_turn = os.path.join(path_save_data_plain, "Save_turn_" + str(max_index_2 + 1))
    if not os.path.exists(path_save_turn):
        os.mkdir(path_save_turn)

    name, ext = os.path.splitext(filename_upload)
    if name[-5:] == '.xlsx':
        ext_2 = '.xlsx'
        type_file_upload = False
    else:
        ext_2 = '.txt'
        type_file_upload = True

    global matrix_encoder
    global already_assigned
    global encoder
    global location_save_plaintext

    data_read = read_output_file(path_filename_upload) 
    os.remove(path_filename_upload)
    dec_matrix_4bit = create_decrypt(data_read, P_inv, S_inv, R, H)
    dec_matrix = matrix_back(dec_matrix_4bit)
    encoder_back = encode_back(dec_matrix, matrix_encoder)
    text_recovery = get_backtext(already_assigned, encoder, encoder_back, type_file_upload)

    show_input_2 = filename_upload
    if len(show_input_2) > 18:
        save_name_plain = name[:-9] + '_Dec' + ext_2    
        location_save_plaintext = save_plain_file(save_name_plain, text_recovery, path_save_turn, type_file_upload)

        show_input_new = show_input_2[:10] + '....' + show_input_2[-8:]
        output_div = show_input_2[:10] + '....' + '_Dec' + ext_2
        response = {'filename_input_2': show_input_new, 'filename_output_2': output_div}
        return json.dumps(response), 200, {'Content-Type': 'application/json'}
    
    save_name_plain = name[:-4] + '_Dec' + ext_2   
    location_save_plaintext = save_plain_file(save_name_plain, text_recovery, path_save_turn, type_file_upload)

    output_div = name[:-4] + '_Dec' + ext_2
    response = {'filename_input_2': show_input_2, 'filename_output_2': output_div}
    return json.dumps(response), 200, {'Content-Type': 'application/json'}


@app.route('/download-cipher', methods=['GET'])
def download():
    global path_save_cipher
    file_path = path_save_cipher  
    return send_file(file_path, as_attachment=True)


@app.route('/download-plain', methods=['GET'])
def download_2():
    global location_save_plaintext
    file_path = location_save_plaintext  
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
