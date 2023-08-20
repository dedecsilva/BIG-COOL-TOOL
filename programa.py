import pyautogui
import pygetwindow
import psutil
import time
import threading
import colorama
import datetime
import json
import subprocess
import os
import requests
import wget
import sys
import screeninfo
from pkg_resources import resource_filename

current_version = 1.5

colorama.init(convert=True)

# AUTO UPDATE

repo_url = f"https://api.github.com/repos/dedecsilva/BIG-COOL-TOOL/releases/latest"
nome_base_do_executável = "BIG COOL TOOL".replace(" ", ".")
raiz_dos_executáveis = os.path.dirname(os.path.abspath(__file__))

if requests.get(repo_url).status_code == 200:
    latest_release = requests.get(repo_url).json()
    latest_version = latest_release["tag_name"]
    
latest_version = float(latest_version)
    
if latest_version > current_version:
    print("NOVA VERSÃO DISPONÍVEL", (latest_version))
    atualizar_ou_não = int(input("GOSTARIA DE ATUALIZAR PARA A VERSÃO MAIS RECENTE? (1> SIM | 2> NÃO): "))
    if atualizar_ou_não == 1:
        url_do_executável = latest_release["assets"][0]["browser_download_url"]
        nome_do_executável = f"{nome_base_do_executável} {latest_version}.exe"
        
        print("BAIXANDO A NOVA VERSÃO...")
        print()
        wget.download(url_do_executável, nome_do_executável)
        print("DOWNLOAD CONCLUÍDO. ABRA A VERSÃO MAIS RECENTE PARA EXCLUIR A VERSÃO ANTIGA")
        print()
        input("PRESSIONE QUALQUER TECLA PARA FECHAR O PROGRAMA...")
        sys.exit()
        
for arquivo in os.listdir(raiz_dos_executáveis):  
    if arquivo.endswith(".exe") and "BIG COOL TOOL" in arquivo and arquivo != f"{nome_base_do_executável} {current_version}.exe":
            os.remove(os.path.join(raiz_dos_executáveis, arquivo))
            print( colorama.Back.RED + " VERSÕES ANTIGAS REMOVIDAS " + colorama.Back.RESET)

# CRIAR E ATUALIZAR ARQUIVO DE CONFIGURAÇÃO

config_padrao = {
    "processo_roblox": "Windows10Universal.exe",
    "processo_cmd": "cmd.exe",
    "nome_janela_erro_electron": "Roblox Not Found",
    "ok_erro": "imagens/Error button image.png",
    "inject_button_img_fluxus": "imagens/Inject button image fluxus.png",
    "inject_button_img_electron": "imagens/Inject button image electron.png",
    "tempo_para_fechar_todas_as_instancias_em_horas": 3,
    "caminho_electron": "",
    "caminho_fluxus": "",
    "tempo_para_dar_auto_attach_em_segundos": 60,
    "tempo_para_arrumar_as_janelas_em_segundos": 120,
    "tempo_para_fechar_erros_do_account_manager_em_segundos": 300
}

def criar_arquivo_config_padrao(nome_do_arquivo):
    with open(nome_do_arquivo, "w") as f:
        json.dump(config_padrao, f, indent=4)

def atualizar_arquivo_config(nome_do_arquivo):
    if os.path.exists(nome_do_arquivo):
        with open(nome_do_arquivo, "r") as f:
            config_atual = json.load(f)

        for chave in config_padrao:
            if chave not in config_atual:
                config_atual[chave] = config_padrao[chave]

        with open(nome_do_arquivo, "w") as f:
            json.dump(config_atual, f, indent=4)

nome_do_arquivo_config = "config.json"

if not os.path.exists(nome_do_arquivo_config):
    criar_arquivo_config_padrao(nome_do_arquivo_config)
    print("ARQUIVO DE CONFIGURAÇÃO CRIADO")
    print()
    input("Pressione qualquer tecla para continuar...")
    os.system("cls")
else:
    with open(nome_do_arquivo_config, "r") as f:
        config_atual = json.load(f)

    chaves_atuais = set(config_atual.keys())
    chaves_padrao = set(config_padrao.keys())

    novas_chaves = chaves_padrao - chaves_atuais

    if novas_chaves:
        atualizar_arquivo_config(nome_do_arquivo_config)
        print("ARQUIVO DE CONFIGURAÇÃO ATUALIZADO")
        print()
        input("Pressione qualquer tecla para continuar...")
        os.system("cls")

# PROGRAMA PRINCIPAL

título = """
    __________  ____  __   
   /_  __/ __ \/ __ \/ /   
    / / / / / / / / / /    
   / / / /_/ / /_/ / /___  
  /_/  \____/\____/_____/  
                           
"""

print(colorama.Back.CYAN + colorama.Fore.BLACK + título + colorama.Back.RESET + colorama.Fore.RESET)
print()

print (f"{colorama.Back.BLUE} VERSÃO ATUAL: {current_version} {colorama.Back.RESET}")
print()
print (colorama.Back.WHITE + colorama.Fore.BLACK + " LENDO CONFIGURAÇÃO DO ARQUIVO CONFIG.JSON " + colorama.Back.RESET + colorama.Fore.RESET)
print()

def print_with_timestamp(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M")
    print(f"{timestamp} | {msg}")

def carregar_configuração_do_programa(nome_do_arquivo):
    with open(nome_do_arquivo, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

config = carregar_configuração_do_programa("config.json")

processo_roblox = config["processo_roblox"]
processo_cmd = config["processo_cmd"]
nome_da_janela_de_erro_electron = config["nome_janela_erro_electron"]
ok_erro = resource_filename(__name__, config["ok_erro"])
inject_button_img_fluxus = resource_filename(__name__, config["inject_button_img_fluxus"])
inject_button_img_electron = resource_filename(__name__, config["inject_button_img_electron"])

caminho_electron = config["caminho_electron"]
caminho_fluxus = config["caminho_fluxus"]

tempo_para_fechar_todas_as_instancias = int(config["tempo_para_fechar_todas_as_instancias_em_horas"]) * 3600
tempo_para_dar_auto_attach = int(config["tempo_para_dar_auto_attach_em_segundos"])
tempo_para_arrumar_as_janelas = int(config["tempo_para_arrumar_as_janelas_em_segundos"])
tempo_para_fechar_erros_do_account_manager = int(config["tempo_para_fechar_erros_do_account_manager_em_segundos"])

definir_auto_attach = int(input("DEFINA QUAL AUTO ATTACH VOCÊ VAI USAR (1 > FLUXUS | 2 > ELECTRON | 3 > NENHUM): "))
print()
limite_de_processos_abertos = int(input("DEFINA QUANTAS INSTÂNCIAS DEVEM ESTAR ABERTAS PARA USAR O AUTO ATTACH: "))
print()

def Arrumar_janelas():
    while True:
        windows = pygetwindow.getWindowsWithTitle("Roblox")
        windows = [window for window in windows if window.title != "Roblox Account Manager"]

        monitor_info = screeninfo.get_monitors()[0]
        monitor_width = monitor_info.width
        monitor_height = monitor_info.height

        max_windows_per_row = 10
        x_offset = 100 
        y_offset = 100 
        width = 100
        height = 100

        current_x = 0
        current_y = 0
        windows_in_current_row = 0

        for i, window in enumerate(windows):
            if windows_in_current_row >= max_windows_per_row:
                current_x = 0
                current_y += y_offset
                windows_in_current_row = 0

            if current_x + width > monitor_width:
                current_x = 0
                current_y += y_offset
                windows_in_current_row = 0

            if current_y + height > monitor_height:
                break

            window.resizeTo(width, height)

            window_x = min(current_x, monitor_width - width)
            window_y = min(current_y, monitor_height - height)

            window.moveTo(window_x, window_y)

            current_x += x_offset
            windows_in_current_row += 1
            
        time.sleep(tempo_para_arrumar_as_janelas)

def Injetar_fluxus(limite_de_processos):
     while True:
         
        def count_processes_by_name(processo_roblox):
            count = 0
            for process in psutil.process_iter(['name']):
                if process.info['name'] == processo_roblox:
                    count += 1
            return count

        current_count = count_processes_by_name(processo_roblox)
        
        if current_count >= limite_de_processos:
            time.sleep(5)
            fluxusWindow = pygetwindow.getWindowsWithTitle("MainWindow")
            if fluxusWindow:
                fluxusWindow = fluxusWindow[0]
                fluxusWindow.restore()
                time.sleep(5)
                    
                ok_erro_button = pyautogui.locateOnScreen(ok_erro, confidence=0.7)

                if ok_erro_button:
                    pyautogui.click(ok_erro_button)
                    time.sleep(2)
                    ok_erro_button = pyautogui.locateOnScreen(ok_erro, confidence=0.7)
                    pyautogui.click(ok_erro_button)
                    time.sleep(2)
                    inject_button = pyautogui.locateOnScreen(inject_button_img_fluxus, confidence=0.7)
                    pyautogui.click(inject_button)
                    time.sleep(5)
                    fluxusWindow.minimize()
                    print_with_timestamp ("FLUXUS INJETADO E ERROS FECHADOS")
                    print()
                else:
                    inject_button = pyautogui.locateOnScreen(inject_button_img_fluxus, confidence=0.7)
                    pyautogui.click(inject_button)
                    time.sleep(5)
                    fluxusWindow.minimize()
                    print_with_timestamp ("FLUXUS INJETADO")
                    print()
            else:
                print_with_timestamp ("FLUXUS NÃO ENCONTRADO")
                print()
                subprocess.run(caminho_fluxus)

            time.sleep(tempo_para_dar_auto_attach)
        
def Injetar_electron(limite_de_processos, nome_da_janela_de_erro_do_electron):
     while True:
         
        def count_processes_by_name(processo_roblox):
            count = 0
            for process in psutil.process_iter(['name']):
                if process.info['name'] == processo_roblox:
                    count += 1
            return count

        current_count = count_processes_by_name(processo_roblox)
        
        if current_count >= limite_de_processos:
            time.sleep(5)
            electronWindow = pygetwindow.getWindowsWithTitle("Electron")
            if electronWindow:
                electronWindow = electronWindow[0]
                electronWindow.restore()
                time.sleep(5)
                
                def detectar_janela_de_erro_do_electron(nome_da_janela_de_erro_do_electron):
                    return pygetwindow.getWindowsWithTitle(nome_da_janela_de_erro_do_electron)
                    
                janela_de_erro = detectar_janela_de_erro_do_electron(nome_da_janela_de_erro_do_electron)

                if janela_de_erro:
                    for janela_de_erro in janela_de_erro:
                        janela_de_erro.close()
                    inject_button = pyautogui.locateOnScreen(inject_button_img_electron, confidence=0.7)
                    pyautogui.click(inject_button)
                    time.sleep(5)
                    electronWindow.minimize()
                    print_with_timestamp ("ELECTRON INJETADO E ERROS FECHADOS")
                    print()
                else:
                    inject_button = pyautogui.locateOnScreen(inject_button_img_electron, confidence=0.7)
                    pyautogui.click(inject_button)
                    time.sleep(5)
                    electronWindow.minimize()
                    print_with_timestamp ("ELECTRON INJETADO")
                    print()
            else:
                print_with_timestamp ("ELECTRON NÃO ENCONTRADO, ABRINDO...")
                print()
                subprocess.run(caminho_electron)

            time.sleep(tempo_para_dar_auto_attach)

def Printar_quantas_janelas_estão_abertas():
    while True:
        
        def count_processes_by_name(processo_roblox):
            count = 0
            for process in psutil.process_iter(['name']):
                if process.info['name'] == processo_roblox:
                    count += 1
            return count

        current_count = count_processes_by_name(processo_roblox)
        
        if current_count == 0:
            print_with_timestamp ("NENHUMA INSTÂNCIA ESTÁ ABERTA")
            print ()
            time.sleep(10)
        else:
            if current_count == 1:
                print_with_timestamp (f"{current_count} INSTÂNCIA ESTÁ ABERTA")
                print ()
                time.sleep(10)
            else:
                print_with_timestamp (f"{current_count} INSTÂNCIAS ESTÃO ABERTAS")
                print ()
                time.sleep(10)
                
def Fechar_erros_do_account_manager(processo_cmd):
    while True:
        time.sleep(tempo_para_fechar_erros_do_account_manager)
        for process in psutil.process_iter(['name']):
            if process.info['name'] == processo_cmd:
                process.kill()
                print_with_timestamp ("ERROS DO ACCOUNT MANAGER FECHADOS")
                print()
            else:
                print_with_timestamp ("SEM ERROS DO ACCOUNT MANAGER")
                print()

def Fechar_todas_instancias_a_cada_determinado_tempo(processo_roblox):
    while True:
        time.sleep(tempo_para_fechar_todas_as_instancias)
        for process in psutil.process_iter(['name']):
            if process.info['name'] == processo_roblox:
                process.kill()
                print_with_timestamp ("TODAS instancias FORAM FECHADAS")
                print()
        
# Lógica de execução das threads

# 1° - Definir auto attach para printar em primeiro lugar se o auto attach está ativado ou desativado
# 2° - Printar as janelas abertas, pois é uma informação fundamental pro programa
# 3° - Arrumar janelas, porque depois de injetar o fluxus é a função principal do programa
# 4° - Fechar erros do account manager pois, depois de arrumar as janelas é a outra principal função do programa
# 5° - Por final fechar todas as instancias, pois é a coisa que mais demora pro programa fazer, como se ela fosse a última camada que ele executa

Thread_arrumar_janelas = threading.Thread(target=Arrumar_janelas)
Thread_injetar_fluxus = threading.Thread(target=Injetar_fluxus, args=(limite_de_processos_abertos,))
Thread_injetar_eletron = threading.Thread(target=Injetar_electron, args=(limite_de_processos_abertos, nome_da_janela_de_erro_electron))
Thread_fechar_todas_instancias_a_cada_determinado_tempo = threading.Thread(target=Fechar_todas_instancias_a_cada_determinado_tempo, args=(processo_roblox,))
Thread_printar_quantas_janelas_estão_abertas = threading.Thread(target=Printar_quantas_janelas_estão_abertas)
Thread_fechar_erros_do_account_manager = threading.Thread(target=Fechar_erros_do_account_manager,args=(processo_cmd,))

if definir_auto_attach == 1:
    Thread_injetar_fluxus.start()
    print(colorama.Back.MAGENTA + " AUTO ATTACH FLUXUS ATIVADO " + colorama.Back.RESET)
    print()
if definir_auto_attach == 2:
    Thread_injetar_eletron.start()
    print(colorama.Back.BLUE + " AUTO ATTACH ELECTRON ATIVADO " + colorama.Back.RESET)
    print()
if definir_auto_attach == 3:
    print(colorama.Back.RED + " AUTO ATTACH DESATIVADO " + colorama.Back.RESET)
    print()

Thread_printar_quantas_janelas_estão_abertas.start()
Thread_arrumar_janelas.start()
Thread_fechar_erros_do_account_manager.start()
Thread_fechar_todas_instancias_a_cada_determinado_tempo.start()