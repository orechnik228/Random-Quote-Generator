import tkinter as tk
from tkinter import ttk, messagebox
import json
import random


class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("600x500")

        # Предопределенные цитаты
        self.base_quotes = [
            {"text": "Жизнь — это то, что случается, когда ты занят другими планами.", "author": "Джон Леннон",
             "theme": "Жизнь"},
            {"text": "Логика может привести вас от пункта А к пункту Б, а воображение — куда угодно.",
             "author": "Альберт Эйнштейн", "theme": "Наука"},
            {"text": "Успех — это способность идти от одной неудачи к другой, не теряя энтузиазма.",
             "author": "Уинстон Черчилль", "theme": "Успех"},
            {"text": "Ваше время ограничено, не тратьте его, живя чужой жизнью.", "author": "Стив Джобс",
             "theme": "Жизнь"},
        ]

        self.history = self.load_history()

        # --- Верхняя панель (Генерация) ---
        frame_top = tk.Frame(root, pady=10)
        frame_top.pack(fill="x")

        self.label_quote = tk.Label(frame_top, text="Нажмите кнопку, чтобы получить цитату",
                                    wraplength=500, font=("Arial", 12, "italic"))
        self.label_quote.pack(pady=10)

        btn_generate = tk.Button(frame_top, text="Сгенерировать цитату", command=self.generate_quote, bg="#4CAF50",
                                 fg="white")
        btn_generate.pack()

        # --- Средняя панель (Фильтры) ---
        frame_filter = tk.LabelFrame(root, text="Фильтр истории", padx=10, pady=5)
        frame_filter.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_filter, text="Автор:").grid(row=0, column=0)
        self.filter_author = tk.Entry(frame_filter)
        self.filter_author.grid(row=0, column=1, padx=5)

        tk.Label(frame_filter, text="Тема:").grid(row=0, column=2)
        self.filter_theme = tk.Entry(frame_filter)
        self.filter_theme.grid(row=0, column=3, padx=5)

        btn_apply = tk.Button(frame_filter, text="Применить", command=self.update_history_list)
        btn_apply.grid(row=0, column=4, padx=5)

        # --- Нижняя панель (История) ---
        tk.Label(root, text="История генераций:").pack()
        self.tree = ttk.Treeview(root, columns=("Текст", "Автор", "Тема"), show='headings')
        self.tree.heading("Текст", text="Цитата")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Тема", text="Тема")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.update_history_list()

    def generate_quote(self):
        quote = random.choice(self.base_quotes)
        self.label_quote.config(text=f"«{quote['text']}»\n— {quote['author']}")

        # Добавляем в историю и сохраняем
        self.history.append(quote)
        self.save_history()
        self.update_history_list()

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    def load_history(self):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def update_history_list(self):
        # Очистка таблицы
        for i in self.tree.get_children():
            self.tree.delete(i)

        author_q = self.filter_author.get().lower()
        theme_q = self.filter_theme.get().lower()

        # Фильтрация и отображение
        for q in reversed(self.history):  # Последние сверху
            if author_q in q["author"].lower() and theme_q in q["theme"].lower():
                self.tree.insert("", tk.END, values=(q["text"], q["author"], q["theme"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()