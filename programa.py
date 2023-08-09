import pyautogui
import pygetwindow
import psutil
import time
import threading
import colorama
import datetime
import cv2
import ctypes

colorama.init(convert=True)

título = """
    __________  ____  __   
   /_  __/ __ \/ __ \/ /   
    / / / / / / / / / /    
   / / / /_/ / /_/ / /___  
  /_/  \____/\____/_____/  
                           
"""

print(colorama.Back.CYAN + colorama.Fore.WHITE + título + colorama.Back.RESET + colorama.Fore.RESET)
print()

def print_with_timestamp(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M")
    print(f"{timestamp} | {msg}")

processo_roblox = "Windows10Universal.exe"
processo_cmd = "cmd.exe"
ok_erro = "Error button image.png"
inject_button_img = "Inject button image.png"
injetar_fluxus_ou_não = int(input("ATIVAR AUTO ATTACH FLUXUS? (1 > SIM | 2 > NÃO): "))
print()
limite_de_processos_abertos = int(input("DEFINA QUANTAS INSTÂNCIAS ABERTAS PARA COMEÇAR ARRUMAR AS JANELAS E INJETAR O FLUXUS: "))
print()
delay = int(10800)

def Arrumar_janelas(limite_de_processos_abertos):
    while True:
        
        def count_processes_by_name(processo_roblox):
            count = 0
            for process in psutil.process_iter(['name']):
                if process.info['name'] == processo_roblox:
                    count += 1
            return count

        current_count = count_processes_by_name(processo_roblox)
        
        if current_count >= limite_de_processos_abertos:    
            time.sleep(5)
            user32 = ctypes.WinDLL("user32.dll")

            hwnd_desktop = user32.GetDesktopWindow()
            user32.TileWindows(hwnd_desktop, 0x0001, None, 0, None)
            user32.TileWindows(hwnd_desktop, 0x0002, None, 0, None)
                        
            time.sleep(300)

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
                    inject_button = pyautogui.locateOnScreen(inject_button_img, confidence=0.7)
                    pyautogui.click(inject_button)
                    time.sleep(5)
                    fluxusWindow.minimize()
                    print_with_timestamp ("FLUXUS INJETADO E ERROS FECHADOS")
                    print()
                else:
                    inject_button = pyautogui.locateOnScreen(inject_button_img, confidence=0.7)
                    pyautogui.click(inject_button)
                    time.sleep(5)
                    fluxusWindow.minimize()
                    print_with_timestamp ("FLUXUS INJETADO")
                    print()
            else:
                print_with_timestamp ("FLUXUS NÃO ENCONTRADO")
                print()

        time.sleep(30)

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
        time.sleep(300)
        for process in psutil.process_iter(['name']):
            if process.info['name'] == processo_cmd:
                process.kill()
                print_with_timestamp ("ERROS DO ACCOUNT MANAGER FECHADOS")
                print()
            else:
                print_with_timestamp ("SEM ERROS DO ACCOUNT MANAGER")
                print()

def Fechar_todas_instâncias_a_cada_determinado_tempo(processo_roblox, delay):
    while True:
        time.sleep(delay)
        for process in psutil.process_iter(['name']):
            if process.info['name'] == processo_roblox:
                process.kill()
                print_with_timestamp ("TODAS INSTÂNCIAS FORAM FECHADAS")
                print()
        
# Lógica de execução das threads

# 1° - Injetar fluxus para printar em primeiro lugar se o auto attach está ativado ou desativado
# 2° - Printar as janelas abertas, pois é uma informação fundamental pro programa
# 3° - Arrumar janelas, porque depois de injetar o fluxus é a função principal do programa
# 4° - Fechar erros do account manager pois, depois de arrumar as janelas é a outra principal função do programa
# 5° - Por final fechar todas as instâncias, pois é a coisa que mais demora pro programa fazer, como se ela fosse a última camada que ele executa

Thread_arrumar_janelas = threading.Thread(target=Arrumar_janelas, args=(limite_de_processos_abertos,))
Thread_injetar_fluxus = threading.Thread(target=Injetar_fluxus, args=(limite_de_processos_abertos,))
Thread_fechar_todas_instâncias_a_cada_determinado_tempo = threading.Thread(target=Fechar_todas_instâncias_a_cada_determinado_tempo, args=(processo_roblox, delay))
Thread_printar_quantas_janelas_estão_abertas = threading.Thread(target=Printar_quantas_janelas_estão_abertas)
Thread_fechar_erros_do_account_manager = threading.Thread(target=Fechar_erros_do_account_manager,args=(processo_cmd,))

if injetar_fluxus_ou_não == 1:
    Thread_injetar_fluxus.start()
    print(colorama.Back.GREEN + " AUTO ATTACH FLUXUS ATIVADO " + colorama.Back.RESET)
    print()
else:
    print(colorama.Back.RED + " AUTO ATTACH FLUXUS DESATIVADO " + colorama.Back.RESET)
    print()
Thread_printar_quantas_janelas_estão_abertas.start()
Thread_arrumar_janelas.start()
Thread_fechar_erros_do_account_manager.start()
Thread_fechar_todas_instâncias_a_cada_determinado_tempo.start()