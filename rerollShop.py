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

# ==========================================
# CONFIGURACIÓN INICIAL Y VARIABLES GLOBALES
# ==========================================

# Crea una instancia de la ventana de la interfaz (Tkinter)
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# Variables vinculadas a la interfaz para actualizar los textos en tiempo real
covenant_count_val = IntVar()
mystic_count_val  = IntVar()
refresh_count_val  = IntVar()
skystones_consumed_val  = IntVar()
gold_consumed_val  = IntVar()

# Banderas (Flags) de estado para controlar el flujo del programa
pause_flag = False         # Controla si el bot está en pausa
stop_flag = False          # Controla si el bot debe detenerse por completo
use_time_flag = False      # Indica si el usuario puso un límite de tiempo
use_skystones_flag = False # Indica si el usuario puso un límite de Skystones

# Contadores internos de estadísticas
mystic_count = 0
covenant_count = 0
refresh_count = 0

timeout = 5 # Tiempo máximo de espera (segundos) para encontrar un botón antes de rendirse
debug_timer = 0 # Para hacer pruebas. Si se cambia, añade pausas extra
exit_flag = 0 # Bandera para cerrar la aplicación entera
cove_buyed = False # Evita comprar la misma medalla dos veces en el mismo vistazo
mystic_buyed = False
run_timeout = 0 # Tiempo total que debe ejecutarse (en segundos)
skystones_max = 0 # Límite máximo de skystones a gastar

# ==========================================
# FUNCIONES DE CONTROL (BOTONES Y TECLAS)
# ==========================================

def pause_resume_macro():
    # Alterna entre pausar y reanudar
    global pause_flag
    pause_flag = not pause_flag

def pause_macro():
    global pause_flag
    pause_flag = not pause_flag

def stop_macro(event=None):
    # Detiene la ejecución del bucle principal de la macro
    global stop_flag
    stop_flag = True

def run_macro():
    # Inicia la macro tras leer los datos de la interfaz
    global run_timeout, stop_flag, skystones_max, use_time_flag, use_skystones_flag
    stop_flag = False
    
    # Leer valores de las cajas de texto
    minutes = entry_minutes.get()
    skystones = entry_skystones.get()
    
    # Evaluar qué límites ha establecido el usuario
    if not minutes or not skystones:
        if not minutes:
            use_time_flag = False
        if not skystones:
            use_skystones_flag = False
            
    if minutes:
        use_time_flag = True
        run_timeout = int(minutes) * 60 # Convertir minutos a segundos
    if skystones:
        use_skystones_flag = True
        skystones_max = int(skystones)

    # Iniciar la macro en un Hilo (Thread) separado. 
    # Esto es VITAL para que la ventanita de Windows no se quede congelada mientras el bot trabaja.
    macro_thread = threading.Thread(target=macro, daemon=True)
    macro_thread.start()

def update_results():
    # Actualiza los textos de la interfaz con los contadores multiplicados por su coste real
    label_covenant_count.config(text="Covenants comprados: " + str(covenant_count * 5))
    label_mystic_count.config(text="Mystics comprados: " + str(mystic_count * 50))
    label_refresh_count.config(text="Refrescos realizados: " + str(refresh_count))
    label_skystones_consumed.config(text="Skystones consumidas: " + str(refresh_count * 3))
    label_gold_consumed.config(text="Oro consumido: " + str(covenant_count * 184000 + mystic_count * 280000))

def on_closing():
    # Cierra la aplicación de forma segura al darle a la 'X' de la ventana
    global exit_flag
    exit_flag = 1
    time.sleep(1)
    sys.exit()

# ==========================================
# FUNCIONES DE ACCIÓN (RATÓN Y BÚSQUEDA VISUAL)
# ==========================================

def click(x, y):
    # SISTEMA ANTI-BANEOS BÁSICO: Aleatoriedad en coordenadas y tiempos de pulsación.
    # Evita que los clics sean robóticos y repetitivos en el mismo píxel y milisegundo exacto.
    rand_x = random.randrange(-12, 12)
    rand_y = random.randrange(-5, 5)
    
    # Mover el ratón con la pequeña desviación generada
    win32api.SetCursorPos((int(x + rand_x), int(y + rand_y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0) # Presiona clic izquierdo
    time.sleep(random.uniform(0.1, 0.25)) # Mantiene pulsado entre 0.1 y 0.25 seg (Simula pulso humano)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0) # Suelta clic izquierdo
    time.sleep(0.3) # Breve pausa tras hacer el clic

def buy(bookmark):
    # Lógica principal de compra. Recibe el tipo de medalla ('covenant' o 'mystic')
    global mystic_count, covenant_count, timeout, cove_buyed, mystic_buyed, width
    medalla_count = 0

    # Seleccionar las imágenes correctas según lo que queramos comprar
    if bookmark == 'covenant':
        medalla_img = 'my_images/covenant.png'
        buy_button = 'my_images/Buy_button_Covenant.png'
    else:
        medalla_img = 'my_images/mystic.png'
        buy_button = 'my_images/Buy_button_Mystic.png'

    pos = None
    buy_start = time.time()

    # PASO 1: Buscar la imagen de la medalla en la pantalla
    while pos is None and time.time() < (buy_start + timeout):
        pos = pyautogui.locateOnScreen(medalla_img, confidence=0.8)

    if pos is not None and not stop_flag:
        pos_center = pyautogui.center(pos)
        
        # ==============================================================================
        # MECÁNICA RECUPERADA: DESPLAZARSE A LA DERECHA Y PULSAR
        # ==============================================================================
        # Calculamos la coordenada X usando el 87% del ancho de tu pantalla (como estaba 
        # en tu última versión). La coordenada Y será la altura de la medalla + 35 píxeles 
        # hacia abajo para centrar el clic en el botón.
        # SI HACE CLIC EN EL AIRE, AJUSTA ESTOS DOS VALORES:
        
        clic_x = int(width * 0.87)             # Ajusta el 0.87 si se queda corto o se pasa
        clic_y = int(pos_center.y + 35)        # Ajusta el +35 si hace clic muy arriba o abajo
        
        click(clic_x, clic_y)
        time.sleep(random.uniform(0.4, 0.6)) # Esperar a que emerja el popup central
        
        # PASO 2: Buscar el botón grande azul de confirmación final en el popup emergente
        timeout_start = time.time()
        buy_button_pos = None

        while time.time() < (timeout_start + timeout):
            if pause_flag:
                time.sleep(0.1)
                continue
            buy_button_pos = pyautogui.locateOnScreen(buy_button, confidence=0.6)

            if buy_button_pos is not None:
                buy_button_center = pyautogui.center(buy_button_pos)
                click(buy_button_center.x, buy_button_center.y) # Compra confirmada
                medalla_count += 1
                break

    # Registrar qué se ha comprado
    if medalla_count > 0:
        if bookmark == 'covenant':
            covenant_count += medalla_count
            cove_buyed = True
        else:
            mystic_count += medalla_count
            mystic_buyed = True
    update_results()

def chk_cove():
    # Comprueba si hay Covenants y, si no se han comprado ya, llama a la función buy()
    global cove_buyed
    pos = pyautogui.locateOnScreen('my_images/covenant.png', confidence=0.8)
    if pos is not None and not cove_buyed:
        time.sleep(random.uniform(0.2, 0.4)) # Retardo natural de reacción
        buy('covenant')

def chk_mystic():
    # Comprueba si hay Mystics y, si no se han comprado ya, llama a la función buy()
    global mystic_buyed
    pos = pyautogui.locateOnScreen('my_images/mystic.png', confidence=0.8)
    if pos is not None and not mystic_buyed:
        time.sleep(random.uniform(0.2, 0.4)) # Retardo natural de reacción
        buy('mystic')

def scroll_down():
    global width, height
    time.sleep(random.uniform(0.2, 0.4))
    
    # Coordenadas aleatorias para situar el ratón y hacer el scroll.
    # Se usa la mitad derecha de la pantalla (width*0.55 a 0.7) para no hacer clic accidentalmente en ítems.
    scroll_pt_x = random.randint(round(width*0.55), round(width*0.7))
    scroll_pt_y = random.randint(round(height*0.2), round(height*0.65))

    # Ejecución del scroll (Configurado actualmente para LDPlayer con la rueda del ratón)
    win32api.SetCursorPos((scroll_pt_x, scroll_pt_y))
    time.sleep(random.uniform(0.2, 0.4))

    # Acción scroll (comentar/descomentar según emulador usado)
    # --- LDPLAYER ---
    mouse.wheel(-4)
    # --- BLUE STACKS ---
    # pyautogui.scroll(-1, x=scroll_pt_x, y=scroll_pt_y)

    time.sleep(random.uniform(0.6, 0.7))

def refresh():
    # Lógica para darle al botón de Refrescar tienda con Skystones
    RB_pos = pyautogui.locateOnScreen('my_images/refresh_button.png', confidence=0.8)
    global refresh_count, cove_buyed, mystic_buyed, pause_flag

    if RB_pos is not None and not stop_flag:
        RB_center = pyautogui.center(RB_pos)
        click(RB_center.x, RB_center.y)
        time.sleep(0.1) # Esperar a que aparezca la confirmación de Skystones

        timeout_start = time.time()

        while time.time() < (timeout_start + timeout):
            if pause_flag:
                time.sleep(0.1)
                continue
            confirm_pos = pyautogui.locateOnScreen('my_images/confirm_button.png', confidence=0.8)

            if confirm_pos is not None:
                confirm_center = pyautogui.center(confirm_pos)
                click(confirm_center.x, confirm_center.y) # Confirmar gasto de 3 Skystones
                refresh_count += 1
                
                # --- PAUSA CRÍTICA DE CARGA ---
                # Espera 1.5s para dar tiempo al juego a terminar la animación de la nueva tienda.
                time.sleep(1.5) 
                break
                
    # Reiniciar banderas para la nueva tanda de ítems
    mystic_buyed = False
    cove_buyed = False
    update_results()

# ==========================================
# FUNCIONES DE EXPORTACIÓN (ARCHIVOS CSV)
# ==========================================

def obtener_fecha():
    # Devuelve la fecha actual formateada para el Excel
    return datetime.now().strftime('%d/%m/%y')

def guardar_en_csv(valores, archivo):
    # Escribe o crea un archivo CSV (Excel) con los datos del reroll actual
    existe = os.path.exists(archivo)
    
    with open(archivo, mode='a', newline='') as csv_file:
        fieldnames = ['Fecha', 'Skystones','Covenants', 'Mystics', 'Oro', 'ss/cov', 'ss/mystics', 'Cuenta']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Si el archivo no existía, escribe la cabecera primero
        if not existe:
            writer.writeheader()
        
        for valor in valores:
            valor['Fecha'] = obtener_fecha()
            writer.writerow(valor)

def save_csv():
    # Genera el diccionario con las estadísticas finales para exportarlas
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

# ==========================================
# BUCLE PRINCIPAL (EL CEREBRO DE LA MACRO)
# ==========================================

def macro():
    global exit_flag, debug_timer, covenant_count, mystic_count, refresh_count, macro_thread, use_skystones_flag, use_time_flag, skystones_max, stop_flag

    macro_thread = threading.current_thread()
    start_time = time.time()

    # Este bucle se ejecuta indefinidamente hasta que pasen los minutos, se gasten las SS o se pulse ESC.
    while exit_flag == 0 and not stop_flag:
        if not pause_flag:

            # Asegurarse de que estamos en la tienda comprobando el botón de refresco
            RB_pos = pyautogui.locateOnScreen('my_images/refresh_button.png', confidence=0.8)

            if RB_pos is None:
                print("Error: Botón de refresco no encontrado. Asegúrate de tener la tienda abierta.")
                sys.exit()

            # Bucle activo de farmeo
            while exit_flag == 0 and ((use_time_flag == False) or (time.time() - start_time) < run_timeout) and not stop_flag:
                
                # Comprobar límite de seguridad de Skystones
                if use_skystones_flag:
                    if not (refresh_count * 3) < skystones_max:
                        stop_flag = True

                if stop_flag:
                    break

                # Secuencia de acciones del Bot:
                # 1. Comprobar fila superior
                chk_cove()
                chk_mystic()
                
                # 2. Desplazarse hacia abajo (Scroll)
                scroll_down()
                time.sleep(0.8)
                
                # 3. Comprobar fila inferior post-scroll
                chk_cove()
                chk_mystic()

                # 4. Actualizar la tienda para empezar de nuevo
                refresh()
                time.sleep(0.5)

    # Cuando el bucle termina, actualizar las variables de la UI por última vez
    covenant_count_val.set(covenant_count)
    mystic_count_val.set(mystic_count)
    refresh_count_val.set(refresh_count)
    update_results()

# ==========================================
# INTERFAZ GRÁFICA (DISEÑO VISUAL UI)
# ==========================================

root.geometry("370x240")
root.title("Epic Seven Macro - Optimized")
root.wm_attributes("-topmost", 1) # Mantiene la ventanita siempre encima del juego

# Crear un estilo base para las fuentes
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

# Crear un contenedor (Frame) para organizar los campos de texto
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Textos descriptivos (Labels)
label_minutes = ttk.Label(frame, text="Minutos:")
label_minutes.grid(row=0, column=0, sticky="W", padx=5, pady=2)
label_skystones = ttk.Label(frame, text="Skystones:")
label_skystones.grid(row=1, column=0, sticky="W", padx=5, pady=2)
label_nombre = ttk.Label(frame, text="Nombre:")
label_nombre.grid(row=2, column=0, sticky="W", padx=5, pady=2)

# Cajas donde el usuario escribe (Entries)
entry_minutes = ttk.Entry(frame, width=12)
entry_minutes.grid(row=0, column=1)
entry_skystones = ttk.Entry(frame, width=12)
entry_skystones.grid(row=1, column=1)
entry_nombre = ttk.Entry(frame, width=12)
entry_nombre.grid(row=2, column=1)

# Botones de Acción
button_run_macro = ttk.Button(frame, text="Iniciar", command=run_macro)
button_run_macro.grid(row=0, column=2, rowspan=1, padx=10, pady=(0, 5), sticky="NS")

# Crear un botón para exportar
button_export_csv = ttk.Button(frame, text="Exportar", command=save_csv)
button_export_csv.grid(row=1, column=2, rowspan=1, padx=10, pady=(0, 5), sticky="NS")

# Etiquetas dinámicas que muestran los resultados en tiempo real
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

# ==========================================
# EVENTOS DE TECLADO/RATÓN Y ARRANQUE
# ==========================================

# Atajos de seguridad para detener el bot inmediatamente
keyboard.on_press_key("esc", stop_macro, suppress=True) # Pulsar la tecla ESCAPE
mouse.on_right_click(stop_macro)                        # Hacer Clic Derecho

# Comportamiento al cerrar la ventana
root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar el bucle principal de la interfaz de usuario (Mantiene la ventana abierta)
root.mainloop()