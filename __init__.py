from cryptography.fernet import Fernet
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# 🔐 Clé de session (utilisée pour encrypt/decrypt classiques)
key = Fernet.generate_key()
f = Fernet(key)

# ➕ Nouvelle route pour afficher la clé
@app.route('/get_key')
def get_key():
    return f"Voici la clé générée pour cette session : {key.decode()}"

# 🔐 Encrypt par défaut
@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}"

# 🔓 Décryptage par défaut
@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        token_bytes = token.encode()
        valeur_decryptee = f.decrypt(token_bytes)
        return f"Valeur décryptée : {valeur_decryptee.decode()}"
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}"

# 🔐 Encrypt avec clé personnalisée (GET)
@app.route('/encrypt_custom/<key>/<message>')
def encrypt_custom_get(key, message):
    try:
        f_custom = Fernet(key.encode())
        token = f_custom.encrypt(message.encode())
        return f"Message encrypté : {token.decode()}"
    except Exception as e:
        return f"Erreur d'encryptage : {str(e)}"

# 🔓 Décrypt avec clé personnalisée (GET)
@app.route('/decrypt_custom/<key>/<token>')
def decrypt_custom_get(key, token):
    try:
        f_custom = Fernet(key.encode())
        message = f_custom.decrypt(token.encode())
        return f"Message décrypté : {message.decode()}"
    except Exception as e:
        return f"Erreur de décryptage : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
