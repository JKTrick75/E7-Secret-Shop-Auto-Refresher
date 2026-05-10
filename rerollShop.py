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

# --- FUNCIONES DE CONTROL ---
def pause_resume_macro():
    global pause_flag
    pause_flag = not pause_flag

def pause_macro():
    global pause_flag
    pause_flag = not pause_flag

def stop_macro(event=None):
    global stop_flag
    stop_flag = not stop_flag

def run_macro():
    global run_timeout, stop_flag, skystones_max, use_time_flag, use_skystones_flag
    stop_flag = False
    
    minutes = entry_minutes.get()
    skystones = entry_skystones.get()
    
    if not minutes or not skystones:
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

    macro_thread = threading.Thread(target=macro, daemon=True)
    macro_thread.start()

def update_results():
    # Actualiza la vista con los contadores reales
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

# --- FUNCIONES DE ACCIÓN (RATÓN Y COMPRAS) ---

def click(x, y):
    # MEJORA: Aleatoriedad generada en cada clic para mayor seguridad y evitar clics robóticos repetitivos
    rand_x = random.randrange(-12, 12)
    rand_y = random.randrange(-5, 5)
    
    win32api.SetCursorPos((int(x + rand_x), int(y + rand_y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(random.uniform(0.1, 0.25))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.3)

def buy(bookmark):
    global mystic_count, covenant_count, timeout, cove_buyed, mystic_buyed, width
    medalla_count = 0

    if bookmark == 'covenant':
        medalla_img = 'my_images/covenant.png'
        buy_button = 'my_images/Buy_button_Covenant.png'
    else:
        medalla_img = 'my_images/mystic.png'
        buy_button = 'my_images/Buy_button_Mystic.png'

    # MEJORA: La imagen del botón pequeño de comprar en la lista
    buy_list_button = 'my_images/buy_list_button.png'

    pos = None
    buy_start = time.time()

    while pos is None and time.time() < (buy_start + timeout):
        pos = pyautogui.locateOnScreen(medalla_img, confidence=0.8)

    if pos is not None and not stop_flag:
        # MEJORA: En lugar de usar un porcentaje del ancho (width*0.87), buscamos el botón visualmente.
        # Es 100% preciso sin importar cómo escale la pantalla.
        region_busqueda = (int(pos.left), int(pos.top - 20), int(width - pos.left), int(pos.height + 40))
        btn_pos = pyautogui.locateOnScreen(buy_list_button, confidence=0.7, region=region_busqueda)
        
        if btn_pos is not None:
            btn_center = pyautogui.center(btn_pos)
            click(btn_center.x, btn_center.y)
            time.sleep(random.uniform(0.4, 0.6)) # Esperar ventana de confirmación

            # Confirmar compra en la ventana emergente
            timeout_start = time.time()
            buy_button_pos = None

            while time.time() < (timeout_start + timeout):
                if pause_flag:
                    time.sleep(0.1)
                    continue
                buy_button_pos = pyautogui.locateOnScreen(buy_button, confidence=0.6)

                if buy_button_pos is not None:
                    buy_button_center = pyautogui.center(buy_button_pos)
                    # Aquí hacemos clic en el botón grande azul de confirmación
                    click(buy_button_center.x, buy_button_center.y)
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

def scroll_down():
    global width, height
    time.sleep(random.uniform(0.2, 0.4))
    
    # Coordenadas donde se hace el scroll (mitad derecha de la pantalla para evitar hacer clic en ítems)
    scroll_pt_x = random.randint(round(width*0.55), round(width*0.7))
    scroll_pt_y = random.randint(round(height*0.2), round(height*0.65))

    # Mantenemos tu configuración original para LDPlayer (Rueda del ratón)
    win32api.SetCursorPos((scroll_pt_x, scroll_pt_y))
    time.sleep(random.uniform(0.2, 0.4))
    mouse.wheel(-8)
    time.sleep(random.uniform(0.6, 0.7))

def refresh():
    RB_pos = pyautogui.locateOnScreen('my_images/refresh_button.png', confidence=0.8)
    global refresh_count, cove_buyed, mystic_buyed, pause_flag

    if RB_pos is not None and not stop_flag:
        RB_center = pyautogui.center(RB_pos)
        click(RB_center.x, RB_center.y)
        time.sleep(0.1) # Esperar a que aparezca la confirmación

        timeout_start = time.time()

        while time.time() < (timeout_start + timeout):
            if pause_flag:
                time.sleep(0.1)
                continue
            confirm_pos = pyautogui.locateOnScreen('my_images/confirm_button.png', confidence=0.8)

            if confirm_pos is not None:
                confirm_center = pyautogui.center(confirm_pos)
                click(confirm_center.x, confirm_center.y)
                refresh_count += 1
                
                # --- PAUSA DE CARGA ---
                time.sleep(1.5) 
                break
                
    mystic_buyed = False
    cove_buyed = False
    update_results()

# --- FUNCIONES DE EXPORTACIÓN (CSV) ---
def obtener_fecha():
    return datetime.now().strftime('%d/%m/%y')

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
            'ss/cov': 0 if covenant_count == 0 else (refresh_count * 3)/(covenant_count*5),
            'ss/mystics': 0 if mystic_count == 0 else (refresh_count * 3)/(mystic_count*50),
            'Cuenta': entry_nombre.get()
        }
    ]

    archivo_csv = 'datos.csv'
    guardar_en_csv(valores_nuevos, archivo_csv)

# --- BUCLE PRINCIPAL (MACRO) ---
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
                
                # Control de límite de Skystones
                if use_skystones_flag:
                    if not (refresh_count * 3) < skystones_max:
                        stop_flag = True

                if stop_flag:
                    break

                # 1. Comprobar covenants/mystics antes del scroll
                chk_cove()
                chk_mystic()
                
                # 2. Desplazarse hacia abajo
                scroll_down()
                time.sleep(0.5)
                
                # 3. Comprobar covenants/mystics después del scroll
                chk_cove()
                chk_mystic()

                # 4. Actualizar la tienda
                refresh()
                time.sleep(0.5)

    # Al terminar o detener, actualizar interfaz
    covenant_count_val.set(covenant_count)
    mystic_count_val.set(mystic_count)
    refresh_count_val.set(refresh_count)
    update_results()

# --- INTERFAZ GRÁFICA (UI) ---
root.geometry("370x240")
root.title("Epic Seven Macro - Optimized")
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

entry_minutes = ttk.Entry(frame, width=12)
entry_minutes.grid(row=0, column=1)
entry_skystones = ttk.Entry(frame, width=12)
entry_skystones.grid(row=1, column=1)
entry_nombre = ttk.Entry(frame, width=12)
entry_nombre.grid(row=2, column=1)

# Crear un botón para ejecutar la macro
button_run_macro = ttk.Button(frame, text="Iniciar", command=run_macro)
button_run_macro.grid(row=0, column=2, rowspan=1, padx=10, pady=(0, 5), sticky="NS")

# Crear un botón para exportar
button_export_csv = ttk.Button(frame, text="Exportar", command=save_csv)
button_export_csv.grid(row=1, column=2, rowspan=1, padx=10, pady=(0, 5), sticky="NS")

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