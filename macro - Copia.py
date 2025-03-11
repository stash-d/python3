import os
import time
import threading
import ctypes
import keyboard

# Configuração do SendInput (clique ultra-rápido)
SendInput = ctypes.windll.user32.SendInput

# Estrutura INPUT para eventos do mouse
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("mi", MouseInput)]

# Definições de evento do mouse
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

# Variáveis de controle
click_rate = 34
macro_running = False
thread_macro = None

# Simula um clique ultra-rápido
click_down = Input(type=INPUT_MOUSE, mi=MouseInput(dwFlags=MOUSEEVENTF_LEFTDOWN))
click_up = Input(type=INPUT_MOUSE, mi=MouseInput(dwFlags=MOUSEEVENTF_LEFTUP))

def click_mouse():
    SendInput(1, ctypes.byref(click_down), ctypes.sizeof(click_down))
    SendInput(1, ctypes.byref(click_up), ctypes.sizeof(click_up))

# Loop da macro super otimizado
def click_loop():
    global macro_running
    interval_ns = int(1e9 / click_rate)  # Tempo entre cliques em nanosegundos
    next_click = time.monotonic_ns()

    while macro_running:
        click_mouse()
        next_click += interval_ns
        
        while time.monotonic_ns() < next_click:
            ctypes.windll.kernel32.Sleep(0)  # Evita uso excessivo de CPU

# Inicia a macro
def start_macro():
    global macro_running, thread_macro
    if macro_running:
        print("Macro já está rodando.")
        return

    print("✅ Macro Iniciada!")
    macro_running = True
    thread_macro = threading.Thread(target=click_loop, daemon=True)
    thread_macro.start()

# Para a macro
def stop_macro():
    global macro_running
    if not macro_running:
        print("Macro não está rodando.")
        return

    print("🛑 Macro Parada!")
    macro_running = False

# Aumenta a taxa de cliques
def increase_click_rate():
    global click_rate
    click_rate += 1
    print(f"🔥 Taxa aumentada para {click_rate} CPS")

# Diminui a taxa de cliques
def decrease_click_rate():
    global click_rate
    if click_rate > 1:
        click_rate -= 1
        print(f"🐢 Taxa reduzida para {click_rate} CPS")

# Exibe o menu
def show_menu():
    print("\n--- Menu de Comandos ---")
    print("F9: Iniciar Macro")
    print("F8: Parar Macro")
    print("F7: Aumentar Taxa de Cliques")
    print("F6: Diminuir Taxa de Cliques")
    print("Esc: Sair do Programa")
    print("------------------------")

# Encerra o programa instantaneamente
def exit_program():
    print("❌ Encerrando programa...")
    stop_macro()
    os._exit(0)

# Atalhos de teclado
keyboard.add_hotkey('F9', start_macro)
keyboard.add_hotkey('F8', stop_macro)
keyboard.add_hotkey('F7', increase_click_rate)
keyboard.add_hotkey('F6', decrease_click_rate)
keyboard.add_hotkey('Esc', exit_program)

# Exibe o menu
show_menu()

# Mantém o programa rodando até pressionar ESC
keyboard.wait('Esc')
