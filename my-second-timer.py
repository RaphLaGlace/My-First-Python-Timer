import tkinter as tk
import sys
import time

# Vérification OS pour le son
if sys.platform.startswith("win"):
    import winsound


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minuteur")
        self.root.config(bg="#1e1e2f")
        self.root.geometry("380x300")
        self.root.resizable(False, False)

        # Variables du minuteur
        self.running = False
        self.remaining_time = 0
        self.total_time = 0

        self.create_widgets()

    # ----------------------------------------
    # 🔧 Interface graphique
    # ----------------------------------------
    def create_widgets(self):

        # Zone d’entrée
        self.entry_time = tk.Entry(
            self.root, font=("Arial", 18), width=8, justify="center",
            fg="#ffffff", bg="#333344", insertbackground="white",
            relief="flat"
        )
        self.entry_time.insert(0, "60")
        self.entry_time.pack(pady=10)

        # Écran du temps
        self.label_time = tk.Label(
            self.root, text="01:00", font=("Arial", 42, "bold"),
            fg="white", bg="#1e1e2f"
        )
        self.label_time.pack(pady=10)

        # Barre de progression
        self.bar_width = 300
        self.bar_height = 25

        self.canvas = tk.Canvas(
            self.root, width=self.bar_width, height=self.bar_height,
            bg="#444455", highlightthickness=0
        )
        self.canvas.pack(pady=10)

        self.progress_bar = self.canvas.create_rectangle(
            0, 0, self.bar_width, self.bar_height, fill="#66cc66"
        )

        # Boutons
        self.add_buttons()

    def styled_button(self, text, command, bg, fg="white"):
        return tk.Button(
            self.root, text=text, command=command,
            font=("Arial", 12, "bold"),
            fg=fg, bg=bg,
            relief="flat", padx=10, pady=5,
            activebackground="#555577"
        )

    def add_buttons(self):
        self.btn_start = self.styled_button("Démarrer", self.start, "#3c8d0d")
        self.btn_start.pack(side="left", padx=10, pady=15)

        self.btn_stop = self.styled_button("Arrêter", self.stop, "#cc8400")
        self.btn_stop.pack(side="left", padx=10)

        self.btn_reset = self.styled_button("Reset", self.reset, "#0066cc")
        self.btn_reset.pack(side="left", padx=10)

        self.btn_close = self.styled_button("Fermer", self.close, "#aa0000")
        self.btn_close.pack(side="left", padx=10)

    # ----------------------------------------
    # ⏱️ Logique du minuteur
    # ----------------------------------------
    def start(self):
        if not self.running:
            self.total_time = self.read_input_time()
            self.remaining_time = self.total_time
            self.label_time.config(text=self.format_time(self.remaining_time), fg="white")
            self.update_progress()
            self.running = True
            self.update_timer()

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.total_time = self.read_input_time()
        self.remaining_time = self.total_time
        self.label_time.config(text=self.format_time(self.remaining_time), fg="white")
        self.update_progress()

    def close(self):
        self.root.destroy()

    def read_input_time(self):
        try:
            return int(self.entry_time.get())
        except ValueError:
            return 0

    def format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    # ----------------------------------------
    # 🔄 Mise à jour du minuteur
    # ----------------------------------------
    def update_timer(self):
        if self.running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.label_time.config(text=self.format_time(self.remaining_time))
            self.update_progress()
            self.root.after(1000, self.update_timer)

        elif self.remaining_time == 0 and self.running:
            self.label_time.config(text="Ding Dong", fg="#ff4444")
            self.running = False
            self.play_sound()

    def update_progress(self):
        if self.total_time > 0:
            fill = (self.remaining_time / self.total_time) * self.bar_width
            self.canvas.coords(self.progress_bar, 0, 0, self.bar_width - fill, self.bar_height)

    # ----------------------------------------
    # 🔊 Son de fin
    # ----------------------------------------
    def play_sound(self):
        for _ in range(3):
            self.root.bell()
            time.sleep(0.3)


# ----------------------------------------
# 🚀 Lancement de l’application
# ----------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
