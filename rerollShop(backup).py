from pyautogui import *
import pyautogui
import time
import datetime
import random
import win32api
import win32con
import sys
import tkinter as tk
from tkinter import IntVar, ttk
import threading
import keyboard
import mouse


# Crea una instancia de Tkinter
root = tk.Tk()

# Crea variables para almacenar los resultados de la vista
covenant_count_val = IntVar()
mystic_count_val  = IntVar()
refresh_count_val  = IntVar()
skystones_consumed_val  = IntVar()
gold_consumed_val  = IntVar()

# Estado de pausa
pause_flag = False
stop_flag = False

# Contadores
mystic_count = 0
covenant_count = 0
refresh_count = 0

timeout = 5 # Si el programa se bloquea durante 5 segundos, terminar
debug_timer = 0 #Para hacer pruebas poner en 2, hara que despues del scroll espere 2 segundos para dar tiempo a comprobar
exit_flag = 0
cove_buyed = False
mystic_buyed = False
run_timeout = 0

rand_x = random.randrange(-60, 60)
rand_y = random.randrange(-15, 15)

# Define una función para pausar o reanudar la ejecución de la macro
def pause_resume_macro():
    global pause_flag
    pause_flag = not pause_flag

# Define una función para actualizar los resultados en la interfaz
def update_results():
    label_covenant_count.config(text="Covenants comprados: " + str(covenant_count_val.get()))
    label_mystic_count.config(text="Mystics comprados: " + str(mystic_count_val.get()))
    label_refresh_count.config(text="Refrescos realizados: " + str(refresh_count_val.get()))
    label_skystones_consumed.config(text="Skystones consumidas: " + str(refresh_count_val.get() * 3))
    label_gold_consumed.config(text="Oro consumido: " + str(covenant_count_val.get() * 184000 + mystic_count_val.get() * 280000))


# Define una función para pausar la ejecución de la macro
def pause_macro():
    global pause_flag
    pause_flag = not pause_flag

def stop_macro(event=None):
    global stop_flag
    stop_flag = not stop_flag

# Define una función para ejecutar la macro en segundo plano
def run_macro():
    global run_timeout, stop_flag
    stop_flag = False
    # Obtener el valor del campo de entrada
    minutes = int(entry.get())
    # Convertir minutos a segundos
    run_timeout = minutes * 60
    macro_thread = threading.Thread(target=macro)
    macro_thread.start()

# Define una función para actualizar los resultados en la interfaz
def update_results():
    label_covenant_count.config(text="Covenants comprados: " + str(covenant_count * 5))
    label_mystic_count.config(text="Mystics comprados: " + str(mystic_count * 50))
    label_refresh_count.config(text="Refrescos realizados: " + str(refresh_count))
    label_skystones_consumed.config(text="Skystones consumidas: " + str(refresh_count * 3))
    label_gold_consumed.config(text="Oro consumido: " + str(covenant_count * 184000 + mystic_count * 280000))

def on_closing():
    global exit_flag
    exit_flag = 1
    time.sleep(1)
    sys.exit()

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.4)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def buy(bookmark):
    chk_dispatch()
    global mystic_count, covenant_count, timeout, cove_buyed, mystic_buyed
    medalla_count = 0

    if bookmark == 'covenant':
        medalla_img = 'my_images/covenant.png'
        buy_button = 'my_images/Buy_button_Covenant.png'
    else:
        medalla_img = 'my_images/mystic.png'
        buy_button = 'my_images/Buy_button_Mystic.png'

    pos = None
    buy_start = time.time()

    while pos is None and time.time() < (buy_start + timeout):
        pos = pyautogui.locateOnScreen(medalla_img, confidence=0.8)

    if pos is not None and not stop_flag:
        pos_center = pyautogui.center(pos)
        # Hacer clic en comprar 
        click(pos_center.x + 800 + rand_x, pos_center.y + 40 + rand_y)
        click(pos_center.x + 800 + rand_x, pos_center.y + 30 + rand_y)
        time.sleep(random.uniform(0.2, 0.4)) # Esperar por el botón de confirmación

        # Confirmar compra
        timeout_start = time.time()
        buy_button_pos = None

        while time.time() < (timeout_start + timeout):
            if pause_flag:
                time.sleep(0.1)
                continue
            buy_button_pos = pyautogui.locateOnScreen(buy_button, confidence=0.6)

            if buy_button_pos is not None:
                buy_button_center = pyautogui.center(buy_button_pos)
                click(buy_button_center[0] + 70 + rand_x, buy_button_center[1] + rand_y)
                click(buy_button_center[0] + 70 + rand_x, buy_button_center[1] + rand_y)
                medalla_count += 1
                break

    if medalla_count > 0:
        if bookmark == 'covenant':
            covenant_count += medalla_count
            cove_buyed = True
        else:
            mystic_count += medalla_count
            mystic_buyed = True
    update_results()


def chk_cove(pos):
    global cove_buyed
    if pos is not None and not cove_buyed:
        time.sleep(random.uniform(0.2, 0.4))
        buy('covenant')

def chk_mystic(pos):
    global mystic_buyed
    if pos is not None and not mystic_buyed:
        time.sleep(random.uniform(0.2, 0.4))
        buy('mystic')

def chk_dispatch():
    pos = pyautogui.locateOnScreen('my_images/dispatch_confirm.png', confidence=0.8)
    if pos is not None:
        time.sleep(1)
        pos_center = pyautogui.center(pos)
        click(pos_center.x + rand_x, pos_center.y + rand_y)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.4)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def scroll_down():
    time.sleep(random.uniform(0.2, 0.4))
    #==============================================================================
    # SI EL CLICK DEL SCROLL LO HACE MUY CERCA DE LAS IMAGENES DE LOS ITEMS/HEROES REDUCIR EL VALOR DE LA X 
    # ej: random.randint(1200, 1400)
    #==============================================================================
    scroll_pt_x = random.randint(1100, 1400)
    scroll_pt_y = random.randint(500, 780)
    click(scroll_pt_x, scroll_pt_y)
    time.sleep(random.uniform(0.2, 0.4)) #añadido

    #==============================================================================
    # SI NO FUNCIONA EL SCROLL, COMENTAR LAS TRES LINEAS SIGUIENTES Y DESCOMENTAR LA 4ª
    #==============================================================================
    # pyautogui.mouseDown(button='left')
    # time.sleep(random.uniform(0.2, 0.4))
    # pyautogui.mouseUp(button='left', x=scroll_pt_x, y=scroll_pt_y - 300)
    # pyautogui.scroll(-2, x=scroll_pt_x, y=scroll_pt_y)
    pyautogui.scroll(-4, x=scroll_pt_x, y=scroll_pt_y) #añadido
    time.sleep(random.uniform(0.2, 0.4)) #añadido

def refresh():
    chk_dispatch()
    RB_pos = pyautogui.locateOnScreen('my_images/refresh_button.png', confidence=0.8)
    global rand_x, rand_y, refresh_count, cove_buyed, mystic_buyed, pause_flag

    if RB_pos is not None and not stop_flag:
        RB_center = pyautogui.center(RB_pos)
        click(RB_center[0] + rand_x, RB_center[1] + rand_y)
        click(RB_center[0] + rand_x, RB_center[1] + rand_y)
        time.sleep(0.1) # Esperar a que aparezca la confirmación

        timeout_start = time.time()

        while time.time() < (timeout_start + timeout):
            if pause_flag:
                time.sleep(0.1)
                continue
            confirm_pos = pyautogui.locateOnScreen('my_images/confirm_button.png', confidence=0.8)

            if confirm_pos is not None:
                confirm_center = pyautogui.center(confirm_pos)
                click(confirm_center[0] + rand_x, confirm_center[1] + rand_y)
                click(confirm_center[0] + rand_x, confirm_center[1] + rand_y)
                refresh_count += 1
                break
    mystic_buyed = False
    cove_buyed = False
    update_results()


def macro():
    global exit_flag, debug_timer, covenant_count, mystic_count, refresh_count, macro_thread

    macro_thread = threading.current_thread()
    
    while exit_flag == 0 and not stop_flag:
        if not pause_flag:
            start_time = time.time()
            #time.sleep(2) # Esperar 2 segundos por si el usuario necesita hacer clic en Bluestacks
            
            chk_dispatch()

            # Localizar botón de refresco
            RB_pos = pyautogui.locateOnScreen('my_images/refresh_button.png', confidence=0.8)

            if RB_pos is None:
                print("Error: Botón de refresco no encontrado.")
                sys.exit()

            while exit_flag == 0 and time.time() < start_time + run_timeout and not stop_flag:
                chk_dispatch()
                Coven_pos = pyautogui.locateOnScreen('my_images/covenant.png', confidence=0.8)
                Mystic_pos = pyautogui.locateOnScreen('my_images/mystic.png', confidence=0.8)

                # Comprobar covenants/mystics
                chk_cove(Coven_pos)
                chk_mystic(Mystic_pos)

                # Desplazarse hacia abajo
                scroll_down()

                time.sleep(0.5)
                Coven_pos2 = pyautogui.locateOnScreen('my_images/covenant.png', confidence=0.8)
                Mystic_pos2 = pyautogui.locateOnScreen('my_images/mystic.png', confidence=0.8)

                # Comprobar covenants/mystics nuevamente
                chk_cove(Coven_pos2)
                chk_mystic(Mystic_pos2)

                # Actualizar la lista
                refresh()

                if not stop_flag:
                    break

                time.sleep(0.5)


    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_datetime = datetime.timedelta(seconds=elapsed_time)

    # Actualiza los resultados en las variables
    covenant_count_val.set(covenant_count)
    mystic_count_val.set(mystic_count)
    refresh_count_val.set(refresh_count)

    # Actualiza los resultados en la interfaz
    update_results()


# Configurar el tamaño y título de la ventana
root.geometry("300x200")
root.title("Epic Seven Macro")

# Configurar la ventana para que esté siempre en primer plano
root.wm_attributes("-topmost", 1)

# Crear un estilo base
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

# Crear un contenedor para el campo de entrada y el botón
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Crear el campo de entrada
entry = ttk.Entry(frame)
entry.grid(row=0, column=0)

# Crear un botón para ejecutar la macro
button_run_macro = ttk.Button(frame, text="Iniciar", command=run_macro)
button_run_macro.grid(row=0, column=1, padx=10)

# Crear etiquetas para mostrar los resultados
label_covenant_count = ttk.Label(root, text="Covenants comprados: " + str(covenant_count))
label_covenant_count.pack()

label_mystic_count = ttk.Label(root, text="Mystics comprados: " + str(mystic_count))
label_mystic_count.pack()

label_refresh_count = ttk.Label(root, text="Refrescos realizados: " + str(refresh_count))
label_refresh_count.pack()

label_skystones_consumed = ttk.Label(root, text="Skystones consumidas: " + str(refresh_count * 3))
label_skystones_consumed.pack()

label_gold_consumed = ttk.Label(root, text="Oro consumido: " + str(covenant_count * 184000 + mystic_count * 280000))
label_gold_consumed.pack()

# Enlazar la pulsación de tecla de Escape para detener la macro
mouse.on_right_click(stop_macro)
keyboard.on_press_key("esc", stop_macro, suppress=True)

root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar el bucle principal de la interfaz de usuario
root.mainloop()