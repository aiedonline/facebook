import base64, os
from Crypto import Cipher;
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5

class RsaHelper():
    def __init__(self, path_to_pem=None, name_file_pem="bot.pem"):
        if path_to_pem == None:
            path_to_pem = os.path.expanduser("~");
        
        if not os.path.exists(path_to_pem):
            os.makedirs(path_to_pem);
        
        if not os.path.exists(path_to_pem + "/.ssh"):
            os.makedirs(path_to_pem + "/.ssh");

        self.key_pub = None; self.key_priv = None;
        
        if not os.path.exists(path_to_pem + "/.ssh/public_" + name_file_pem) or not os.path.exists(path_to_pem + "/.ssh/private_"  + name_file_pem):
            self.key_priv = RSA.generate(1024);
            self.key_pub = self.key_priv.publickey();
            with open (path_to_pem + "/.ssh/private_" + name_file_pem, "bw") as prv_file:
                prv_file.write(self.key_priv.exportKey());
            with open (path_to_pem + "/.ssh/public_"  + name_file_pem, "bw") as pub_file:
                pub_file.write(self.key_pub.exportKey());
        else:
            with open(path_to_pem + "/.ssh/public_" + name_file_pem, "rb") as k:
                self.key_pub = RSA.importKey(k.read());
            with open(path_to_pem + "/.ssh/private_" + name_file_pem, "rb") as k:
                self.key_priv = RSA.importKey(k.read());
    def encrypt(self, data):
        cipher = Cipher_PKCS1_v1_5.new(self.key_pub);
        return base64.b64encode( cipher.encrypt(data.encode()) ).decode();
    def decrypt(self, data):
        decipher = Cipher_PKCS1_v1_5.new(self.key_priv);
        return decipher.decrypt(base64.b64decode( data.encode()) , None).decode();


#r = RsaHelper(name_file_pem="meu.pem");
#texto = "Botafogo campeão, será!!!! Deus salve Textor";
#criptografado = r.encrypt(texto);
#descriptografado = r.decrypt(criptografado);
#print(texto);
#print(criptografado);
#print(descriptografado);
