from cryptography.fernet import Fernet
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Clé de chiffrement par défaut pour la session
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}"

# ✅ Séquence 5 - Exercice 1 : Route de décryptage
@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        token_bytes = token.encode()
        valeur_decryptee = f.decrypt(token_bytes)
        return f"Valeur décryptée : {valeur_decryptee.decode()}"
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}"

# ✅ Séquence 5 - Exercice 2 : Clé personnalisée - Encrypt
@app.route('/encrypt_custom', methods=['POST'])
def encrypt_custom():
    message = request.form.get('message')
    custom_key = request.form.get('key')
    try:
        f_custom = Fernet(custom_key.encode())
        token = f_custom.encrypt(message.encode())
        return f"Message encrypté : {token.decode()}"
    except Exception as e:
        return f"Erreur : {str(e)}"

# ✅ Séquence 5 - Exercice 2 : Clé personnalisée - Decrypt
@app.route('/decrypt_custom', methods=['POST'])
def decrypt_custom():
    token = request.form.get('token')
    custom_key = request.form.get('key')
    try:
        f_custom = Fernet(custom_key.encode())
        message = f_custom.decrypt(token.encode())
        return f"Message décrypté : {message.decode()}"
    except Exception as e:
        return f"Erreur : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
