import pyautogui
import pygetwindow
import psutil
import time
import threading
import colorama
import datetime
import cv2
import ctypes
import sys
from ctypes import wintypes as wts

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

def Arrumar_janelas(processo_roblox, limite_de_processos_abertos):
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

            HWND = wts.HWND
            UINT = wts.UINT

            hwnd_desktop = user32.GetDesktopWindow()
            user32.TileWindows(hwnd_desktop, 0x0001, None, 0, None)
            user32.TileWindows(hwnd_desktop, 0x0002, None, 0, None)
                    
            time.sleep(300)

def Injetar_fluxus(processo_roblox, limite_de_processos):
     while True:
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

def Fechar_erros_do_account_manager(processo_cmd):
    while True:
        for process in psutil.process_iter(['name']):
            if process.info['name'] == processo_cmd:
                process.kill()
                print_with_timestamp ("ERROS DO ACCOUNT MANAGER FECHADOS")
                print()
            else:
                print_with_timestamp ("SEM ERROS DO ACCOUNT MANAGER")
                print()
            time.sleep(300)

def Printar_quantas_janelas_estão_abertas(processo_roblox):
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

def Fechar_todas_instâncias_a_cada_determinado_tempo(delay):
    while True:
        time.sleep(delay)
        for process in psutil.process_iter(['name']):
            if process.info['name'] == processo_roblox:
                process.kill()
                print_with_timestamp ("TODAS INSTÂNCIAS FORAM FECHADAS")
                print()
        

thread1 = threading.Thread(target=Arrumar_janelas, args=(processo_roblox, limite_de_processos_abertos))
thread2 = threading.Thread(target=Injetar_fluxus, args=(processo_roblox, limite_de_processos_abertos))
thread3 = threading.Thread(target=Fechar_todas_instâncias_a_cada_determinado_tempo, args=(delay,))
thread4 = threading.Thread(target=Printar_quantas_janelas_estão_abertas, args=(processo_roblox,))
thread5 = threading.Thread(target=Fechar_erros_do_account_manager,args=(processo_cmd,))

if injetar_fluxus_ou_não == 1:
    thread2.start()
    print(colorama.Back.GREEN + " AUTO ATTACH FLUXUS ATIVADO " + colorama.Back.RESET)
    print()
else:
    print(colorama.Back.RED + " AUTO ATTACH FLUXUS DESATIVADO " + colorama.Back.RESET)
    print()
thread1.start()
thread3.start()
thread4.start()
thread5.start()