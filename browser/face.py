import time, os, inspect, sys; 

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.insert(0, ROOT);

from browser import *;

TEMPO_TELA = 5;
TEMPO_DIGITACAO = 0.1;

class Face(Browser):
    def __init__(self, username, password, terminal=True):
        path_directory_browser = CURRENTDIR + "/tmp/face_" + username;
        super().__init__(socks5=None, terminal=terminal, path_directory_browser=path_directory_browser);
        self.username = username;
        self.password = password;
        
    def logar(self):
        self.navegar("https://www.facebook.com/");
        if self.existe_elemento('//*[@data-pagelet="Stories"]') == False:
            self.escrever('//*[@id="email"]', self.username, latencia=TEMPO_DIGITACAO);
            self.escrever('//*[@id="pass"]',  self.password, latencia=0.2);
            self.clicar('//*[@name="login"]');
            time.sleep(60);
        return True;


# --------------------------------- PARA TESTAR --------------------------------
#import sys, json;
#browface = Face("sua conta no face", "sua senha da sua conta", terminal=False);
#if browface.validar():
#    browface.logar();
#    browface.scroll(5, 2);
#time.sleep(50);



