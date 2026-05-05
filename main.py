import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os
from datetime import datetime

# ========== ПРЕДОПРЕДЕЛЁННЫЕ ЦИТАТЫ ==========
DEFAULT_QUOTES = [
    ("Будь изменением, которое ты хочешь видеть в мире.", "Махатма Ганди", "Мотивация"),
    ("Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "Джон Леннон", "Жизнь"),
    ("Воображение важнее знания.", "Альберт Эйнштейн", "Наука"),
    ("Ваше время ограничено, не тратьте его на чужую жизнь.", "Стив Джобс", "Успех"),
    ("Не судите по ошибкам других.", "Конфуций", "Мудрость"),
    ("Вставай и иди к своей мечте.", "Джим Керри", "Мотивация"),
    ("Кто хочет — ищет способ, кто не хочет — ищет причину.", "Сократ", "Мудрость"),
    ("Действие — это ключ к успеху.", "Пабло Пикассо", "Успех"),
]

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator — Генератор случайных цитат")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        
        # Данные
        self.available_quotes = []   # Все доступные цитаты
        self.history = []            # История сгенерированных цитат
        
        # Загрузка из JSON
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        self.refresh_filters()
        self.update_history_display()
    
    # ========== РАБОТА С JSON ==========
    def load_data(self):
        """Загружает историю и пользовательские цитаты из JSON"""
        if os.path.exists("quotes.json"):
            try:
                with open("quotes.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.history = data.get("history", [])
                    user_quotes = data.get("user_quotes", [])
                    default_list = [{"text": q[0], "author": q[1], "theme": q[2]} for q in DEFAULT_QUOTES]
                    self.available_quotes = default_list + user_quotes
            except:
                self.init_default_data()
        else:
            self.init_default_data()
            self.save_data()
    
    def init_default_data(self):
        """Инициализация начальными данными"""
        self.available_quotes = [{"text": q[0], "author": q[1], "theme": q[2]} for q in DEFAULT_QUOTES]
        self.history = []
    
    def save_data(self):
        """Сохраняет историю и пользовательские цитаты в JSON"""
        default_texts = [q[0] for q in DEFAULT_QUOTES]
        user_quotes = [q for q in self.available_quotes if q["text"] not in default_texts]
        
        data = {
            "history": self.history,
            "user_quotes": user_quotes
        }
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    # ========== ИНТЕРФЕЙС ==========
    def create_widgets(self):
        # --- Панель текущей цитаты ---
        frame_display = tk.LabelFrame(self.root, text="📖 Текущая цитата", padx=10, pady=10, font=("Arial", 10, "bold"))
        frame_display.pack(fill="x", padx=10, pady=5)
        
        self.label_quote = tk.Label(frame_display, text="Нажмите кнопку «Сгенерировать цитату»", 
                                     font=("Arial", 12), wraplength=800, justify="left", fg="#2c3e50")
        self.label_quote.pack(anchor="w", pady=5)
        
        self.label_author = tk.Label(frame_display, text="", font=("Arial", 10, "italic"), fg="#7f8c8d")
        self.label_author.pack(anchor="e", pady=5)
        
        btn_frame = tk.Frame(frame_display)
        btn_frame.pack(fill="x", pady=5)
        self.btn_generate = tk.Button(btn_frame, text="🎲 Сгенерировать цитату", command=self.generate_quote,
                                       bg="#3498db", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5)
        self.btn_generate.pack(side="left", padx=5)
        
        # --- Панель добавления новой цитаты ---
        frame_add = tk.LabelFrame(self.root, text="➕ Добавить свою цитату", padx=10, pady=10, font=("Arial", 10, "bold"))
        frame_add.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_add, text="Текст цитаты:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.entry_text = tk.Entry(frame_add, width=65, font=("Arial", 10))
        self.entry_text.grid(row=0, column=1, padx=5, pady=3)
        
        tk.Label(frame_add, text="Автор:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=3)
        self.entry_author = tk.Entry(frame_add, width=30, font=("Arial", 10))
        self.entry_author.grid(row=1, column=1, sticky="w", padx=5, pady=3)
        
        tk.Label(frame_add, text="Тема:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=3)
        self.entry_theme = tk.Entry(frame_add, width=20, font=("Arial", 10))
        self.entry_theme.grid(row=2, column=1, sticky="w", padx=5, pady=3)
        
        self.btn_add = tk.Button(frame_add, text="📝 Добавить цитату", command=self.add_quote,
                                  bg="#2ecc71", fg="white", font=("Arial", 10))
        self.btn_add.grid(row=3, column=1, sticky="w", pady=5, padx=5)
        
        # --- Панель фильтрации ---
        frame_filter = tk.LabelFrame(self.root, text="🔍 Фильтрация", padx=10, pady=10, font=("Arial", 10, "bold"))
        frame_filter.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_filter, text="По автору:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.filter_author = ttk.Combobox(frame_filter, values=[], state="readonly", width=25, font=("Arial", 10))
        self.filter_author.grid(row=0, column=1, padx=5, pady=5)
        self.filter_author.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())
        
        tk.Label(frame_filter, text="По теме:", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5)
        self.filter_theme = ttk.Combobox(frame_filter, values=[], state="readonly", width=20, font=("Arial", 10))
        self.filter_theme.grid(row=0, column=3, padx=5, pady=5)
        self.filter_theme.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())
        
        self.btn_reset = tk.Button(frame_filter, text="🔄 Сбросить фильтры", command=self.reset_filters,
                                    bg="#e74c3c", fg="white", font=("Arial", 10))
        self.btn_reset.grid(row=0, column=4, padx=10, pady=5)
        
        # --- История цитат ---
        frame_history = tk.LabelFrame(self.root, text="📜 История сгенерированных цитат", padx=10, pady=10, font=("Arial", 10, "bold"))
        frame_history.pack(fill="both", expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(frame_history)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox = tk.Listbox(frame_history, yscrollcommand=scrollbar.set, height=12,
                                           font=("Consolas", 9), bg="#ecf0f1", selectbackground="#3498db")
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)
    
    def refresh_filters(self):
        """Обновляет выпадающие списки фильтров"""
        authors = sorted(set(q["author"] for q in self.available_quotes))
        themes = sorted(set(q["theme"] for q in self.available_quotes))
        self.filter_author["values"] = ["Все"] + authors
        self.filter_theme["values"] = ["Все"] + themes
        self.filter_author.set("Все")
        self.filter_theme.set("Все")
    
    # ========== ФИЛЬТРАЦИЯ ==========
    def get_filtered_quotes(self):
        """Возвращает отфильтрованный список цитат"""
        selected_author = self.filter_author.get()
        selected_theme = self.filter_theme.get()
        
        filtered = self.available_quotes[:]
        if selected_author and selected_author != "Все":
            filtered = [q for q in filtered if q["author"] == selected_author]
        if selected_theme and selected_theme != "Все":
            filtered = [q for q in filtered if q["theme"] == selected_theme]
        return filtered
    
    def apply_filter(self):
        """Применяет фильтр и показывает результат"""
        filtered = self.get_filtered_quotes()
        messagebox.showinfo("Фильтр применён", f"Доступно цитат по фильтру: {len(filtered)}")
    
    def reset_filters(self):
        """Сбрасывает фильтры"""
        self.filter_author.set("Все")
        self.filter_theme.set("Все")
        messagebox.showinfo("Фильтры сброшены", "Теперь доступны все цитаты")
    
    # ========== ГЕНЕРАЦИЯ ЦИТАТЫ ==========
    def generate_quote(self):
        """Генерирует случайную цитату из отфильтрованного списка"""
        filtered = self.get_filtered_quotes()
        if not filtered:
            messagebox.showwarning("Нет цитат", "Нет цитат, соответствующих выбранным фильтрам.")
            return
        
        quote = random.choice(filtered)
        self.label_quote.config(text=f"«{quote['text']}»")
        self.label_author.config(text=f"— {quote['author']} (тема: {quote['theme']})")
        
        # Добавление в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            "text": quote["text"],
            "author": quote["author"],
            "theme": quote["theme"],
            "timestamp": timestamp
        })
        self.save_data()
        self.update_history_display()
    
    def update_history_display(self):
        """Обновляет отображение истории"""
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.history[-100:]):
            disp = f"[{entry['timestamp']}] {entry['author']}: {entry['text'][:70]}"
            self.history_listbox.insert(tk.END, disp)
    
    # ========== ДОБАВЛЕНИЕ ЦИТАТЫ (С ВАЛИДАЦИЕЙ) ==========
    def add_quote(self):
        """Добавляет новую цитату с проверкой на пустые строки"""
        text = self.entry_text.get().strip()
        author = self.entry_author.get().strip()
        theme = self.entry_theme.get().strip()
        
        # Проверка на пустые строки
        if not text:
            messagebox.showerror("Ошибка", "❌ Текст цитаты не может быть пустым!")
            return
        if not author:
            messagebox.showerror("Ошибка", "❌ Укажите автора!")
            return
        if not theme:
            messagebox.showerror("Ошибка", "❌ Укажите тему цитаты!")
            return
        
        # Проверка на дубликат
        for q in self.available_quotes:
            if q["text"] == text and q["author"] == author:
                messagebox.showwarning("Предупреждение", "⚠️ Такая цитата уже существует!")
                return
        
        # Добавление
        new_quote = {"text": text, "author": author, "theme": theme}
        self.available_quotes.append(new_quote)
        self.save_data()
        self.refresh_filters()
        
        # Очистка полей
        self.entry_text.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_theme.delete(0, tk.END)
        
        messagebox.showinfo("Успех", f"✅ Цитата добавлена!\n\nАвтор: {author}\nТема: {theme}")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()