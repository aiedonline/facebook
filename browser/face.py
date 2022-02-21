import time, os, inspect, sys, random; 

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.insert(0, ROOT);

from browser.browser import *;

TEMPO_TELA = 5;
TEMPO_DIGITACAO = 0.1;

class Face(Browser):
    def __init__(self, username, password, path_directory_browser, terminal=True):
        path_directory_browser = path_directory_browser + "/" + username;
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
        
    # canal aiedonline
    def publicar_grupo(self, url_grupo, texto):
        self.navegar('https://www.facebook.com/');
        time.sleep( random.randint(3, 5) );
        self.navegar('https://www.facebook.com/groups/');
        time.sleep( random.randint(1, 2) );
        self.navegar('https://www.facebook.com/groups/feed/');
        self.scroll(interacoes = random.randint(3, 5), wait=1);
        self.navegar(url_grupo);
        time.sleep(random.randint(3, 5));
        # Este elemento eu não estou no grupo, mas eu peço para entrar
        if self.existe_elemento('//*[contains(@class, "r516eku6 k83vx86k") and div[1]/div[1]/div[1]/div[1]/div[1]/span[contains(@class, "bwm1u5wc")] ]/div[1]/div[1]/div[1]/div[1]/div[1]/span'):
            self.clicar('//*[contains(@class, "r516eku6 k83vx86k") and div[1]/div[1]/div[1]/div[1]/div[1]/span[contains(@class, "bwm1u5wc")]     ]/div[1]/div[1]/div[1]/div[1]/div[1]/span');
            time.sleep(random.randint(60, 90));
            return False;
        
        # publicar
        if self.existe_elemento('//*[@data-pagelet="GroupInlineComposer"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span'):
            self.clicar('//*[@data-pagelet="GroupInlineComposer"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span');
            time.sleep(random.randint(10, 15));
            text_xpath = '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div' #/div/div/div
            self.escrever(text_xpath, texto + " ");
            time.sleep(random.randint(15,25));
            self.clicar('/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div');
            return True;
        return False;


# --------------------------------- PARA TESTAR --------------------------------
#import sys, json;
#browface = Face("sua conta no face", "sua senha da sua conta", terminal=False);
#if browface.validar():
#    browface.logar();
#    browface.scroll(5, 2);
#time.sleep(50);



