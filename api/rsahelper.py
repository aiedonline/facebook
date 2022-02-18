import base64, os
from Crypto import Cipher;
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5

class RsaHelper():
    def __init__(self):
        user_path = os.path.expanduser("~");
        self.key_pub = None; self.key_priv = None;
        
        if not os.path.exists(user_path + "/.ssh"):
            os.makedirs(user_path + "/.ssh");
        
        if not os.path.exists(user_path + "/.ssh/public_bot.pem") or not os.path.exists(user_path + "/.ssh/private_bot.pem"):
            self.key_priv = RSA.generate(1024);
            self.key_pub = self.key_priv.publickey();
            with open (user_path + "/.ssh/private_bot.pem", "bw") as prv_file:
                prv_file.write(self.key_priv.exportKey());
            with open (user_path + "/.ssh/public_bot.pem", "bw") as pub_file:
                pub_file.write(self.key_pub.exportKey());
        else:
            with open(user_path + "/.ssh/public_bot.pem", "rb") as k:
                self.key_pub = RSA.importKey(k.read());
            with open(user_path + "/.ssh/private_bot.pem", "rb") as k:
                self.key_priv = RSA.importKey(k.read());
    def encrypt(self, data):
        cipher = Cipher_PKCS1_v1_5.new(self.key_pub);
        return base64.b64encode( cipher.encrypt(data.encode()) ).decode();
    def decrypt(self, data):
        decipher = Cipher_PKCS1_v1_5.new(self.key_priv);
        return decipher.decrypt(base64.b64decode( data.encode()) , None).decode();




