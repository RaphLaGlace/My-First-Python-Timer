import tkinter as tk
import sys
import time

# Vérification OS pour le son
if sys.platform.startswith("win"):
    import winsound


# VARIABLES GLOBALES
running = False
remaining_time = 0
total_time = 0


# ⏳ Mise à jour du minuteur
def update_timer():
    global remaining_time, running

    if running and remaining_time > 0:
        remaining_time -= 1
        label_time.config(text=format_time(remaining_time))
        update_progress()
        window.after(1000, update_timer)

    elif remaining_time == 0 and running:
        label_time.config(text="Ding Dong", fg="#ff4444")
        running = False
        play_sound()


# 🎨 Mise à jour de la barre de progression
def update_progress():
    if total_time > 0:
        fill = (remaining_time / total_time) * bar_width
        canvas.coords(progress_bar, 0, 0, bar_width - fill, bar_height)


# 🔊 Son de fin
def play_sound():
    for i in range(13):
        window.bell()
        time.sleep(2000000000000000000000)  # Linux/Mac : beep Tkinter


# ⏱️ Format d'affichage
def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


# 🔢 Lecture du temps dans l’entrée
def read_input_time():
    try:
        return int(entry_time.get())
    except ValueError:
        return 0


# ▶️ Démarrer
def start():
    global running, remaining_time, total_time

    if not running:
        total_time = read_input_time()
        remaining_time = total_time
        label_time.config(text=format_time(remaining_time), fg="white")
        update_progress()
        running = True
        update_timer()


# ⏸️ Arrêter
def stop():
    global running
    running = False


# 🔁 Reset
def reset():
    global running, remaining_time, total_time

    running = False
    total_time = read_input_time()
    remaining_time = total_time
    label_time.config(text=format_time(remaining_time), fg="white")
    update_progress()


# ❌ Fermer
def close():
    window.destroy()


# ----- INTERFACE -----
window = tk.Tk()
window.title("Minuteur")
window.config(bg="#1e1e2f")
window.geometry("380x300")
window.resizable(False, False)


# 🎛️ Champ d’entrée
entry_time = tk.Entry(window, font=("Arial", 18), width=8, justify="center",
                      fg="#ffffff", bg="#333344", insertbackground="white",
                      relief="flat")
entry_time.insert(0, "60")
entry_time.pack(pady=10)


# 🕒 Label du temps
label_time = tk.Label(window, text="01:00", font=("Arial", 42, "bold"),
                      fg="white", bg="#1e1e2f")
label_time.pack(pady=10)


# 📊 Barre de progression
bar_width = 300
bar_height = 25

canvas = tk.Canvas(window, width=bar_width, height=bar_height,
                   bg="#444455", highlightthickness=0)
canvas.pack(pady=10)

progress_bar = canvas.create_rectangle(0, 0, bar_width, bar_height, fill="#66cc66")


# 🖱️ Bouton stylé
def styled_button(text, command, bg, fg="white"):
    return tk.Button(window, text=text, command=command,
                     font=("Arial", 12, "bold"),
                     fg=fg, bg=bg,
                     relief="flat", padx=10, pady=5,
                     activebackground="#555577")


# 🔘 Boutons
btn_start = styled_button("Démarrer", start, "#3c8d0d")
btn_start.pack(side="left", padx=10, pady=15)

btn_stop = styled_button("Arrêter", stop, "#cc8400")
btn_stop.pack(side="left", padx=10)

btn_reset = styled_button("Reset", reset, "#0066cc")
btn_reset.pack(side="left", padx=10)

btn_close = styled_button("Fermer", close, "#aa0000")
btn_close.pack(side="left", padx=10)


window.mainloop()
