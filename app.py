from flask import Flask, request, send_file, render_template_string
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import os
import io

app = Flask(__name__)

# Tạo khóa AES từ khóa người dùng nhập (độ dài tự do)
def get_aes_key(user_key: str) -> bytes:
    return SHA256.new(user_key.encode()).digest()  # 32 bytes

# Mã hóa file bằng AES
def encrypt_file(file_data: bytes, key: bytes) -> bytes:
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_data = cipher.encrypt(file_data)
    return iv + encrypted_data  # Ghép IV vào đầu để giải mã sau

# Giải mã file bằng AES
def decrypt_file(file_data: bytes, key: bytes) -> bytes:
    iv = file_data[:16]
    encrypted_data = file_data[16:]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(encrypted_data)

# Giao diện web đơn giản
HTML = '''
<!doctype html>
<title>AES Encrypt/Decrypt</title>
<h2>AES File Encryptor/Decryptor</h2>
<form method=post enctype=multipart/form-data action="/process">
    <input type=file name=file required><br><br>
    <input type=text name=key placeholder="Nhập khóa (độ dài bất kỳ)" required><br><br>
    <select name=action>
        <option value="encrypt">Mã hóa</option>
        <option value="decrypt">Giải mã</option>
    </select><br><br>
    <input type=submit value="Thực hiện">
</form>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['file']
    user_key = request.form['key']
    action = request.form['action']

    key = get_aes_key(user_key)
    file_data = file.read()

    if action == 'encrypt':
        result = encrypt_file(file_data, key)
        output_filename = file.filename + '.enc'
    else:
        try:
            result = decrypt_file(file_data, key)
            output_filename = file.filename.replace('.enc', '.dec')
        except Exception:
            return "❌ Giải mã thất bại. Có thể khóa sai hoặc file hỏng."

    return send_file(
        io.BytesIO(result),
        as_attachment=True,
        download_name=output_filename,
        mimetype='application/octet-stream'
    )

if __name__ == '__main__':
    app.run(debug=True)
