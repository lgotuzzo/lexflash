#!/usr/bin/env python3
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import csv
import random
import sqlite3
from datetime import datetime

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LexFlash")
        self.root.configure(bg="black")

        self.user_name = simpledialog.askstring("Nombre", "Ingresa tu nombre:")
        self.user_score = 0
        self.max_errors = 5

        self.connection = sqlite3.connect("flashcards_scores.db")
        self.create_scores_table()

        file_path = self.choose_file()
        if not file_path:
            messagebox.showwarning("Cancelado", "No se seleccionó ningún archivo.")
            self.root.destroy()
            return

        self.show_csv_format_info()
        self.flashcards = self.load_flashcards(file_path)

        if not self.flashcards:
            messagebox.showerror("Error", "No se encontraron tarjetas válidas en el archivo.")
            self.root.destroy()
            return

        self.label_word = tk.Label(root, text="", font=("Helvetica", 20), fg="white", bg="black")
        self.options_buttons = []
        self.btn_next = tk.Button(root, text="Siguiente", command=self.next_flashcard, font=("Helvetica", 20))
        self.btn_exit = tk.Button(root, text="Salir", command=self.on_closing, font=("Helvetica", 20), bg="red", fg="white")
        self.btn_scores = tk.Button(root, text="Puntajes", command=self.show_scores, font=("Helvetica", 20), bg="green", fg="white")
        self.timer_label = tk.Label(root, text="Tiempo restante:", font=("Helvetica", 20), fg="white", bg="black")
        self.timer_value = tk.Label(root, text="", font=("Helvetica", 20), fg="white", bg="black")
        self.score_label = tk.Label(root, text="Puntaje: {}".format(self.user_score), font=("Helvetica", 20), fg="white", bg="black")

        self.question_time = 30
        self.remaining_time = 0
        self.timer = None

        self.label_word.pack(pady=20)
        for i in range(4):
            btn = tk.Button(root, text="", command=lambda i=i: self.check_translation(i), font=("Helvetica", 16))
            self.options_buttons.append(btn)
            btn.pack(pady=10)
        self.btn_next.pack(pady=10)
        self.btn_exit.pack(pady=10)
        self.btn_scores.pack(pady=10)
        self.timer_label.pack(pady=5)
        self.timer_value.pack(pady=5)
        self.score_label.pack(pady=5)

        self.current_flashcard = None
        self.errors_count = 0
        self.next_flashcard()

    def choose_file(self):
        return filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )

    def show_csv_format_info(self):
        messagebox.showinfo(
            "Formato del archivo CSV",
            "El archivo CSV debe tener dos columnas separadas por punto y coma (;):\n\n"
            "Ejemplo:\n"
            "Hola;Hello\n"
            "Casa;House\n"
            "Gato;Cat\n\n"
            "⚠️ No uses encabezados ni espacios innecesarios."
        )

    def create_scores_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                score INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def insert_score(self, score):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO scores (user_name, score) VALUES (?, ?)", (self.user_name, score))
        self.connection.commit()

    def load_flashcards(self, file_path):
        flashcards = []
        try:
            with open(file_path, newline='', encoding='latin-1') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                for row in reader:
                    if row and len(row) >= 2:
                        flashcards.append({'word': row[0].strip(), 'translation': row[1].strip()})
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        return flashcards

    def next_flashcard(self):
        self.stop_timer()
        self.current_flashcard = random.choice(self.flashcards)
        self.label_word.config(text=self.current_flashcard['word'])

        distractors = [card['translation'] for card in self.flashcards if card['translation'] != self.current_flashcard['translation']]
        options = [self.current_flashcard['translation']]
        options.extend(random.sample(distractors, min(3, len(distractors))))
        random.shuffle(options)

        for i, option in enumerate(options):
            self.options_buttons[i].config(text=option)

        self.remaining_time = self.question_time
        self.update_timer()

    def check_translation(self, option_index):
        translation = self.options_buttons[option_index].cget("text")
        correct_translation = self.current_flashcard['translation']

        if translation == correct_translation:
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            self.user_score += 1
        else:
            messagebox.showerror("Incorrecto", f"Respuesta incorrecta. La respuesta correcta es: {correct_translation}")
            self.errors_count += 1

        self.score_label.config(text="Puntaje: {}".format(self.user_score))

        if self.errors_count >= self.max_errors:
            messagebox.showinfo("Fin del juego", f"¡Has alcanzado el máximo de errores!\nPuntaje final: {self.user_score}")
            self.on_closing()
        else:
            self.next_flashcard()

    def update_timer(self):
        if self.remaining_time >= 0:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.timer_value.config(text="{:02}:{:02}".format(minutes, seconds))
            self.remaining_time -= 1
            self.timer = self.root.after(1000, self.update_timer)
        else:
            self.timer_value.config(text="Tiempo agotado")
            self.stop_timer()
            self.errors_count += 1
            self.score_label.config(text="Puntaje: {}".format(self.user_score))
            messagebox.showerror("Tiempo agotado", f"Se acabó el tiempo. La respuesta correcta era: {self.current_flashcard['translation']}")
            if self.errors_count >= self.max_errors:
                messagebox.showinfo("Fin del juego", f"¡Has alcanzado el máximo de errores!\nPuntaje final: {self.user_score}")
                self.on_closing()
            else:
                self.next_flashcard()

    def stop_timer(self):
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None

    def show_scores(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_name, score, timestamp FROM scores ORDER BY score DESC")
        scores = cursor.fetchall()

        scores_window = tk.Toplevel(self.root)
        scores_window.title("Puntajes")
        scores_window.configure(bg="black")

        scores_label = tk.Label(scores_window, text="Puntajes", font=("Helvetica", 20), fg="white", bg="black")
        scores_label.pack(pady=10)

        for score in scores:
            score_text = f"{score[0]} - Puntaje: {score[1]} - Fecha: {score[2]}"
            score_label = tk.Label(scores_window, text=score_text, font=("Helvetica", 12), fg="white", bg="black")
            score_label.pack()

    def on_closing(self):
        if self.user_score > 0:
            self.insert_score(self.user_score)
        self.connection.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
