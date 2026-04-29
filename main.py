import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = 'movies.json'

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []

        # Создаем поля
        self.create_widgets()
        # Загружаем данные
        self.load_data()

    def create_widgets(self):
        # Поля
        tk.Label(self.root, text="Название:").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Жанр:").grid(row=1, column=0)
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Год выпуска:").grid(row=2, column=0)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Рейтинг:").grid(row=3, column=0)
        self.rating_entry = tk.Entry(self.root)
        self.rating_entry.grid(row=3, column=1)

        # Кнопка добавления
        self.add_button = tk.Button(self.root, text="Добавить фильм", command=self.add_movie)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=('title', 'genre', 'year', 'rating'), show='headings')
        self.tree.heading('title', text='Название')
        self.tree.heading('genre', text='Жанр')
        self.tree.heading('year', text='Год выпуска')
        self.tree.heading('rating', text='Рейтинг')
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=6, column=0)
        self.genre_filter = ttk.Combobox(self.root, values=[])
        self.genre_filter.grid(row=6, column=1)
        self.genre_filter.bind("<<ComboboxSelected>>", self.filter_movies)

        tk.Label(self.root, text="Фильтр по году:").grid(row=7, column=0)
        self.year_filter = ttk.Combobox(self.root, values=[])
        self.year_filter.grid(row=7, column=1)
        self.year_filter.bind("<<ComboboxSelected>>", self.filter_movies)

        # Очистка фильтров
        self.clear_button = tk.Button(self.root, text="Сбросить фильтры", command=self.load_data)
        self.clear_button.grid(row=8, column=0, columnspan=2, pady=5)

    def load_data(self):
        self.movies = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.movies = json.load(f)
        self.display_movies(self.movies)
        self.update_filters()

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year_str = self.year_entry.get()
        rating_str = self.rating_entry.get()

        # Валидация
        if not (title and genre and year_str and rating_str):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        try:
            year = int(year_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return
        try:
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }

        self.movies.append(movie)
        self.save_data()
        self.load_data()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def display_movies(self, movies):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for m in movies:
            self.tree.insert('', tk.END, values=(m['title'], m['genre'], m['year'], m['rating']))

    def update_filters(self):
        genres = set(m['genre'] for m in self.movies)
        years = set(str(m['year']) for m in self.movies)
        self.genre_filter['values'] = ['Все'] + sorted(genres)
        self.year_filter['values'] = ['Все'] + sorted(years)
        self.genre_filter.set('Все')
        self.year_filter.set('Все')

    def filter_movies(self, event=None):
        genre = self.genre_filter.get()
        year = self.year_filter.get()

        filtered = self.movies
        if genre != 'Все':
            filtered = [m for m in filtered if m['genre'] == genre]
        if year != 'Все':
            filtered = [m for m in filtered if str(m['year']) == year]
        self.display_movies(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()