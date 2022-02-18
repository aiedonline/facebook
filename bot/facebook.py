import os, sys, inspect, time, random, datetime, uuid;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);
sys.path.insert(0, ROOT);

from browser.face import *;
from browser.youtube import *;
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
rc = RsaHelper();

def lista_urls(user_id):
    publicar = [];
    sql = "select distinct grp.*  , (select date_insert from `history` as his where his.group_id = grp.id order by date_insert desc limit 1) as ultima_data  from theme_group as tgr inner join `group` as grp on tgr.group_id = grp.id  inner join group_account as gacc on ( grp.id = gacc.group_id and gacc.account_id = %s )  where tgr.theme_id in (   select distinct theme_id from group_account as gcc inner join theme_group as thg on gcc.group_id = thg.group_id where gcc.account_id = %s)   order by ultima_data asc";
    # Listar os grupos do usuário com publicação mais antiga na frente
    grupos = mysql.datatable(sql, (user_id, user_id, ));
    for grupo in grupos:
        if grupo['ultima_data'] == None or (((datetime.now() - grupo['ultima_data']).seconds // 3600) + ((datetime.now() - grupo['ultima_data']).days * 24))  > NUMERO_HORAS_SEM_PUBLICAR_GRUPO:
            grupo['urls'] = [];
            sql = "select distinct url.*,  (select date_insert from `history` as his where his.group_id = thg.group_id and url_id = url.id order by date_insert desc limit 1) as date_history from theme_group as thg inner join url_theme urt on thg.theme_id = urt.theme_id   inner join url on urt.url_id = url.id  where thg.group_id = %s order by date_history asc";
            # Agora vamos ligar do grupo um vídeo que foi publicado há muito tempo atrás
            links = mysql.datatable(sql, (grupo['id'], ));
            for link in links:
                if link['start'] < datetime.now():
                    if link['date_history'] == None or (datetime.now() - link['date_history']).days > link['interval']:
                        grupo['urls'].append(link);
            if len(grupo['urls']) > 0:
                publicar.append(grupo);
        else:
            hour_to_start = (((datetime.now() - grupo['ultima_data']).seconds // 3600) + ((datetime.now() - grupo['ultima_data']).days * 24));
            print("\033[0;32m", hour_to_start, "\t" , grupo['url'], "\033[0;0m", "- Tem publicação feita há: ", NUMERO_HORAS_SEM_PUBLICAR_GRUPO);
    return publicar;

def publicar(browface, grupo, account_id):
    browface.navegar('https://www.facebook.com/');
    time.sleep(5);
    browface.navegar('https://www.facebook.com/groups/feed/');
    browface.scroll(interacoes =3, wait=1);
    browface.navegar(grupo['url']);
    time.sleep(TEMPO_ESPERA);
    # Se eu não estou no grupo, então!!!! já sabe né aguarda um tempo e exit
    if browface.existe_elemento('//*[contains(@class, "r516eku6 k83vx86k") and div[1]/div[1]/div[1]/div[1]/div[1]/span[contains(@class, "bwm1u5wc")] ]/div[1]/div[1]/div[1]/div[1]/div[1]/span'):
        browface.clicar('//*[contains(@class, "r516eku6 k83vx86k") and div[1]/div[1]/div[1]/div[1]/div[1]/span[contains(@class, "bwm1u5wc")]     ]/div[1]/div[1]/div[1]/div[1]/div[1]/span');
        time.sleep(90);
        return False;
    if browface.existe_elemento('//*[@data-pagelet="GroupInlineComposer"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span'):
        browface.clicar('//*[@data-pagelet="GroupInlineComposer"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span');
        time.sleep(TEMPO_TELA);
        text_xpath = '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div' #/div/div/div
        for video in grupo['urls']:
            browface.escrever(text_xpath, video['url'] + "&" + str(uuid.uuid4()) + " ");
            time.sleep(random.randint(5,10));
            browface.clicar('/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div');
            print('Salvo', mysql.noquery("INSERT INTO history (group_id, url_id, date_insert) values( %s, %s, %s )", (grupo['id'], video['id'], datetime.now().strftime('%Y-%m-%dT%H:%M'),  )));
            print("Link publicado:", "\033[0;32m", video['title'], "\033[0;0m",  "no grupo:", "\033[1;36m", grupo['url'], "\033[0;0m", "em", datetime.now().strftime('%Y-%m-%dT%H:%M'));
            return True;
    else:
        sql = "delete from group_account where group_id = %s and account_id = %s";
        print(sql, (grupo['id'], account_id,  ));
        print("\033[0;33m", "[-] Excluindo grupo:", "\033[0;0m", mysql.noquery(sql, (grupo['id'], account_id,  )));
    return False;




def run_browser():
    browface = None;
    try:
        users = mysql.datatable("select * from account");
        for user in users:
            sucesso = 0;
            # procurar tudo que tenho para publicar
            grupos = lista_urls(user['id']);
            print("Total de grupos para este usuário: ", len(grupos));
            if len(grupos) > 0:
                browface = Face(user['username'], rc.decrypt(user['password']), terminal=False);
                if not browface.validar():
                    print("BOT não ofuscao....");
                    sys.exit(0);
                browface.logar();
                for grupo in grupos:
                    time.sleep(TEMPO_ESPERA);
                    if publicar(browface, grupo, user['id']) == True:
                        time.sleep(random.randint(21, 30));
                        sucesso += 1;
                    if sucesso > 5:
                        return;
                if sucesso > 5:
                    return;
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
