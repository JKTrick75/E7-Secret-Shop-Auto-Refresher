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
import csv
import os
from datetime import datetime

# Crea una instancia de Tkinter
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
# Crea variables para almacenar los resultados de la vista
covenant_count_val = IntVar()
mystic_count_val  = IntVar()
refresh_count_val  = IntVar()
skystones_consumed_val  = IntVar()
gold_consumed_val  = IntVar()

# Estado de pausa
pause_flag = False
stop_flag = False
use_time_flag = False
use_skystones_flag = False

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
skystones_max = 0

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
    global run_timeout, stop_flag, skystones_max, use_time_flag, use_skystones_flag
    stop_flag = False
    # Obtener el valor del campo de entrada
    minutes = entry_minutes.get()
    skystones = entry_skystones.get()
    if not minutes or not skystones:
        # Al menos uno de los campos de entrada está vacío
        # Activar la bandera correspondiente según si se usa tiempo o skystones
        if not minutes:
            use_time_flag = False
        if not skystones:
            use_skystones_flag = False
    if minutes:
        use_time_flag = True
        run_timeout = int(minutes) * 60
    if skystones:
        use_skystones_flag = True
        skystones_max = int(skystones)

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
    global mystic_count, covenant_count, timeout, cove_buyed, mystic_buyed, width
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
    #==============================================================================
    # SI HACE CLICK FUERA AL INTENTAR COMPRAR, AJUSTAR EL VALOR POR DEFECTO DE 'X' 800 AL CORRECTO SEGUN VUESTRA PANTALLA Y EL DE LA 'Y' TAMBIEN SI ES NECESARIO
    #==============================================================================
        click(round(width*0.87) + rand_x, pos_center.y + 40 + rand_y)
        click(round(width*0.87) + rand_x, pos_center.y + 30 + rand_y)
        time.sleep(random.uniform(0.4, 0.6)) # Esperar por el botón de confirmación

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


def chk_cove():
    global cove_buyed
    pos = pyautogui.locateOnScreen('my_images/covenant.png', confidence=0.8)
    if pos is not None and not cove_buyed:
        time.sleep(random.uniform(0.2, 0.4))
        buy('covenant')

def chk_mystic():
    global mystic_buyed
    pos = pyautogui.locateOnScreen('my_images/mystic.png', confidence=0.8)
    if pos is not None and not mystic_buyed:
        time.sleep(random.uniform(0.2, 0.4))
        buy('mystic')

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.6)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def scroll_down():
    global width, height
    time.sleep(random.uniform(0.2, 0.4))
    #==============================================================================
    # SI EL CLICK DEL SCROLL LO HACE MUY CERCA DE LAS IMAGENES DE LOS ITEMS/HEROES REDUCIR EL VALOR DE LA X 
    # ej: random.randint(1200, 1400)
    #==============================================================================
    scroll_pt_x = random.randint(round(width*0.55), round(width*0.7))
    scroll_pt_y = random.randint(round(height*0.2), round(height*0.65))
    click(scroll_pt_x, scroll_pt_y)

    #==============================================================================
    # SI NO FUNCIONA EL SCROLL, COMENTAR LAS TRES LINEAS SIGUIENTES Y DESCOMENTAR LA 4ª
    #==============================================================================
    #Mumu
    #pyautogui.mouseDown(button='left')
    #time.sleep(random.uniform(0.4, 0.6))
    #pyautogui.mouseUp(button='left', x=scroll_pt_x, y=scroll_pt_y - 300)
    #Bluestack
    #pyautogui.scroll(-2, x=scroll_pt_x, y=scroll_pt_y)
    #LDPlayer
    time.sleep(random.uniform(0.6, 0.7))
    mouse.wheel(-8)
    
    time.sleep(random.uniform(0.6, 0.7))

def refresh():
    RB_pos = pyautogui.locateOnScreen('my_images/refresh_button.png', confidence=0.8)
    global rand_x, rand_y, refresh_count, cove_buyed, mystic_buyed, pause_flag

    rand_x = random.randrange(-60, 60)
    rand_y = random.randrange(-15, 15)
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

def obtener_fecha():
    fecha_actual = datetime.now().strftime('%d/%m/%y')
    return fecha_actual

def guardar_en_csv(valores, archivo):
    existe = os.path.exists(archivo)
    
    with open(archivo, mode='a', newline='') as csv_file:
        fieldnames = ['Fecha', 'Skystones','Covenants', 'Mystics', 'Oro', 'ss/cov', 'ss/mystics', 'Cuenta']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        if not existe:
            writer.writeheader()
        
        for valor in valores:
            valor['Fecha'] = obtener_fecha()
            writer.writerow(valor)

def save_csv():
    valores_nuevos = [
    {   'Fecha': '',
        'Skystones': refresh_count * 3,
        'Covenants': covenant_count * 5,
        'Mystics': mystic_count * 50,
        'Oro': covenant_count * 184000 + mystic_count * 280000,
        'ss/cov': 0 if covenant_count == 0 else (refresh_count * 3)/covenant_count*5,
        'ss/mystics': 0 if mystic_count == 0 else (refresh_count * 3)/mystic_count*50,
        'Cuenta': entry_nombre.get()
    }
    ]

    archivo_csv = 'datos.csv'
    guardar_en_csv(valores_nuevos, archivo_csv)


def macro():
    global exit_flag, debug_timer, covenant_count, mystic_count, refresh_count, macro_thread, use_skystones_flag, use_time_flag, skystones_max, stop_flag

    macro_thread = threading.current_thread()
    start_time = time.time()

    while exit_flag == 0 and not stop_flag:
        if not pause_flag:

            # Localizar botón de refresco
            RB_pos = pyautogui.locateOnScreen('my_images/refresh_button.png', confidence=0.8)

            if RB_pos is None:
                print("Error: Botón de refresco no encontrado.")
                sys.exit()

            while exit_flag == 0 and ((use_time_flag == False) or (time.time() - start_time) < run_timeout) and not stop_flag:
                print(refresh_count * 3, skystones_max)
                if use_skystones_flag:
                    if not (refresh_count * 3) < skystones_max:
                        stop_flag = True

                if stop_flag:
                    break


                # Comprobar covenants/mystics
                chk_cove()
                chk_mystic()
                # Desplazarse hacia abajo
                scroll_down()

                sleep(0.5)
                # Comprobar covenants/mystics nuevamente
                chk_cove()
                chk_mystic()

                # Actualizar la lista
                refresh()
                time.sleep(0.5)

    # Actualiza los resultados en las variables
    covenant_count_val.set(covenant_count)
    mystic_count_val.set(mystic_count)
    refresh_count_val.set(refresh_count)

    # Actualiza los resultados en la interfaz
    update_results()


# Configurar el tamaño y título de la ventana
root.geometry("370x240")
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

label_minutes = ttk.Label(frame, text="Minutos:")
label_minutes.grid(row=0, column=0, sticky="W", padx=5, pady=2)
label_skystones = ttk.Label(frame, text="Skystones:")
label_skystones.grid(row=1, column=0, sticky="W", padx=5, pady=2)
label_nombre = ttk.Label(frame, text="Nombre:")
label_nombre.grid(row=2, column=0, sticky="W", padx=5, pady=2)

# Crear el campo de entrada
entry_minutes = ttk.Entry(frame)
entry_minutes.grid(row=0, column=1)
entry_skystones = ttk.Entry(frame)
entry_skystones.grid(row=1, column=1)
entry_nombre = ttk.Entry(frame)
entry_nombre.grid(row=2, column=1)

# Crear un botón para ejecutar la macro
button_run_macro = ttk.Button(frame, text="Iniciar", command=run_macro)
button_run_macro.grid(row=0, column=2, rowspan=1, padx=10, pady=(0, 5), sticky="NS")
# Crear un botón para exportar
button_run_macro = ttk.Button(frame, text="Exportar", command=save_csv)
button_run_macro.grid(row=1, column=2, rowspan=1, padx=10, pady=(0, 5), sticky="NS")

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
keyboard.on_press_key("esc", stop_macro, suppress=True)
mouse.on_right_click(stop_macro)

root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar el bucle principal de la interfaz de usuario
root.mainloop()