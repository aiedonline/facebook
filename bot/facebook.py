import os, sys, inspect, time, random, datetime, uuid, traceback;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.insert(0, ROOT);

from browser.face import *;
#from browser.youtube import *;
from api.mysqlhelper import *;
from api.rsahelper import *;
from datetime import datetime
from datetime import timedelta
from datetime import date  

CONFIG = json.loads(open(ROOT + "/data/config.json").read());
mysql = My(CONFIG['database']['host'], CONFIG['database']['database'], CONFIG['database']['user'], CONFIG['database']['password']);

TEMPO_ESPERA = 5;
TEMPO_DIGITACAO = 0.1;
NUMERO_HORAS_SEM_PUBLICAR_GRUPO = 8;
rc = RsaHelper(name_file_pem="bot_face_conta2");

def run_browser():
    browface = None;
    try:
        users = mysql.datatable("select * from account");
        for user in users:
            browface = Face(user['username'], rc.decrypt(user['password']), CONFIG["bot"]["path_tmp_dir"], terminal=False);
            if not browface.validar():
                print("BOT não ofuscao....");
                sys.exit(0);
            browface.logar();
            #browface.publicar_grupo("https://www.facebook.com/groups/2134026936882220", "https://youtu.be/ny6oJBPrirU");
            time.sleep(180);
    except KeyboardInterrupt:
        print("Ok, saindo da execução");
        sys.exit(0);
    except:
        traceback.print_exc();
    finally:
        browface = None;
        time.sleep(60);

def main():
    while True:
        run_browser();
        time.sleep(random.randint(60*20,60*30));
main();
