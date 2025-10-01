import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import itertools
import string
import random
import re

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей / Password Generator")
        self.root.geometry("600x900")

        # Словарь для локализации
        self.texts = {
            "ru": {
                "title": "Генератор паролей",
                "keywords_label": "Введите ключевые слова (через пробел):",
                "min_length_label": "Минимальная длина пароля:",
                "max_length_label": "Максимальная длина пароля:",
                "max_passwords_label": "Максимальное количество паролей:",
                "leet_label": "Использовать l33t-подстановки (a → @, o → 0)",
                "separators_label": "Использовать разделители (_ - .)",
                "suffixes_label": "Добавить суффиксы (! @ 123 2025)",
                "prefixes_label": "Добавить префиксы (pass admin)",
                "custom_chars_label": "Пользовательские символы для суффиксов:",
                "case_label": "Вариации регистра (нижний, верхний)",
                "double_label": "Удваивать слова (wowa → wowawowa)",
                "mix_chars_label": "Смешивать символы (wowa → w1o2w3a)",
                "reverse_label": "Обратный порядок (wowa → awow)",
                "partial_label": "Частичные слова (wowa → wow, wa)",
                "dates_label": "Словарь дат (30 09 → 3009, 0930)",
                "complexity_label": "Фильтр сложности (буквы+числа+символы)",
                "generate_button": "Сгенерировать пароли",
                "save_button": "Сохранить в файл",
                "clear_button": "Очистить вывод",
                "log_button": "Показать лог",
                "language_label": "Язык интерфейса:",
                "options_frame": "Шаблоны",
                "error_no_keywords": "Введите хотя бы одно ключевое слово!",
                "error_no_passwords": "Сначала сгенерируйте пароли!",
                "error_invalid_length": "Проверьте значения длины пароля!",
                "error_invalid_max_passwords": "Максимальное количество паролей должно быть числом > 0!",
                "success_save": "Пароли сохранены в {}",
                "result_prefix": "Сгенерировано {} паролей:\n\n"
            },
            "en": {
                "title": "Password Generator",
                "keywords_label": "Enter keywords (space-separated):",
                "min_length_label": "Minimum password length:",
                "max_length_label": "Maximum password length:",
                "max_passwords_label": "Maximum number of passwords:",
                "leet_label": "Use l33t substitutions (a → @, o → 0)",
                "separators_label": "Use separators (_ - .)",
                "suffixes_label": "Add suffixes (! @ 123 2025)",
                "prefixes_label": "Add prefixes (pass admin)",
                "custom_chars_label": "Custom characters for suffixes:",
                "case_label": "Case variations (lower, upper)",
                "double_label": "Double words (wowa → wowawowa)",
                "mix_chars_label": "Mix characters (wowa → w1o2w3a)",
                "reverse_label": "Reverse order (wowa → awow)",
                "partial_label": "Partial words (wowa → wow, wa)",
                "dates_label": "Date dictionary (30 09 → 3009, 0930)",
                "complexity_label": "Complexity filter (letters+numbers+symbols)",
                "generate_button": "Generate Passwords",
                "save_button": "Save to File",
                "clear_button": "Clear Output",
                "log_button": "Show Log",
                "language_label": "Interface language:",
                "options_frame": "Templates",
                "error_no_keywords": "Enter at least one keyword!",
                "error_no_passwords": "Generate passwords first!",
                "error_invalid_length": "Check password length values!",
                "error_invalid_max_passwords": "Maximum number of passwords must be a number > 0!",
                "success_save": "Passwords saved to {}",
                "result_prefix": "Generated {} passwords:\n\n"
            }
        }
        self.current_lang = "ru"

        # Прокручиваемая область
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.main_frame = tk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._resize_canvas)

        # Выбор языка
        self.language_label = tk.Label(self.main_frame, text=self.texts[self.current_lang]["language_label"])
        self.language_label.pack(anchor="w", padx=10, pady=5)
        self.lang_var = tk.StringVar(value="ru")
        tk.OptionMenu(self.main_frame, self.lang_var, "ru", "en", command=self.update_language).pack(anchor="w", padx=10, pady=5)

        # Поле для ключевых слов
        self.keywords_label = tk.Label(self.main_frame, text=self.texts[self.current_lang]["keywords_label"])
        self.keywords_label.pack(anchor="w", padx=10)
        self.input_entry = tk.Entry(self.main_frame, width=50)
        self.input_entry.pack(padx=10, pady=5)

        # Поля для длины пароля и количества
        self.min_length_label = tk.Label(self.main_frame, text=self.texts[self.current_lang]["min_length_label"])
        self.min_length_label.pack(anchor="w", padx=10)
        self.min_length_entry = tk.Entry(self.main_frame, width=10)
        self.min_length_entry.insert(0, "4")
        self.min_length_entry.pack(anchor="w", padx=10, pady=5)

        self.max_length_label = tk.Label(self.main_frame, text=self.texts[self.current_lang]["max_length_label"])
        self.max_length_label.pack(anchor="w", padx=10)
        self.max_length_entry = tk.Entry(self.main_frame, width=10)
        self.max_length_entry.insert(0, "20")
        self.max_length_entry.pack(anchor="w", padx=10, pady=5)

        self.max_passwords_label = tk.Label(self.main_frame, text=self.texts[self.current_lang]["max_passwords_label"])
        self.max_passwords_label.pack(anchor="w", padx=10)
        self.max_passwords_entry = tk.Entry(self.main_frame, width=10)
        self.max_passwords_entry.insert(0, "1000")
        self.max_passwords_entry.pack(anchor="w", padx=10, pady=5)

        # Рамка для чекбоксов
        self.options_frame = tk.LabelFrame(self.main_frame, text=self.texts[self.current_lang]["options_frame"], padx=10, pady=10)
        self.options_frame.pack(fill="x", padx=10, pady=5)

        # Чекбоксы для шаблонов
        self.use_leet = tk.BooleanVar(value=True)
        self.use_separators = tk.BooleanVar(value=True)
        self.use_suffixes = tk.BooleanVar(value=True)
        self.use_prefixes = tk.BooleanVar(value=True)
        self.use_case = tk.BooleanVar(value=True)
        self.use_double = tk.BooleanVar(value=False)
        self.use_mix_chars = tk.BooleanVar(value=False)
        self.use_reverse = tk.BooleanVar(value=False)
        self.use_partial = tk.BooleanVar(value=False)
        self.use_dates = tk.BooleanVar(value=False)
        self.use_complexity = tk.BooleanVar(value=False)

        self.leet_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["leet_label"], variable=self.use_leet)
        self.leet_check.pack(anchor="w")
        self.separators_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["separators_label"], variable=self.use_separators)
        self.separators_check.pack(anchor="w")
        self.suffixes_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["suffixes_label"], variable=self.use_suffixes)
        self.suffixes_check.pack(anchor="w")
        self.prefixes_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["prefixes_label"], variable=self.use_prefixes)
        self.prefixes_check.pack(anchor="w")
        self.case_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["case_label"], variable=self.use_case)
        self.case_check.pack(anchor="w")
        self.double_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["double_label"], variable=self.use_double)
        self.double_check.pack(anchor="w")
        self.mix_chars_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["mix_chars_label"], variable=self.use_mix_chars)
        self.mix_chars_check.pack(anchor="w")
        self.reverse_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["reverse_label"], variable=self.use_reverse)
        self.reverse_check.pack(anchor="w")
        self.partial_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["partial_label"], variable=self.use_partial)
        self.partial_check.pack(anchor="w")
        self.dates_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["dates_label"], variable=self.use_dates)
        self.dates_check.pack(anchor="w")
        self.complexity_check = tk.Checkbutton(self.options_frame, text=self.texts[self.current_lang]["complexity_label"], variable=self.use_complexity)
        self.complexity_check.pack(anchor="w")

        # Пользовательские символы
        self.custom_chars_label = tk.Label(self.main_frame, text=self.texts[self.current_lang]["custom_chars_label"])
        self.custom_chars_label.pack(anchor="w", padx=10)
        self.custom_chars_entry = tk.Entry(self.main_frame, width=20)
        self.custom_chars_entry.insert(0, "!@#")
        self.custom_chars_entry.pack(anchor="w", padx=10, pady=5)

        # Прогресс-бар
        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress, maximum=100)
        self.progress_bar.pack(fill="x", padx=10, pady=5)

        # Кнопки
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill="x", padx=10, pady=5)
        self.generate_button = tk.Button(self.button_frame, text=self.texts[self.current_lang]["generate_button"], command=self.generate_passwords)
        self.generate_button.pack(side="left", padx=5)
        self.save_button = tk.Button(self.button_frame, text=self.texts[self.current_lang]["save_button"], command=self.save_to_file)
        self.save_button.pack(side="left", padx=5)
        self.clear_button = tk.Button(self.button_frame, text=self.texts[self.current_lang]["clear_button"], command=self.clear_output)
        self.clear_button.pack(side="left", padx=5)
        self.log_button = tk.Button(self.button_frame, text=self.texts[self.current_lang]["log_button"], command=self.show_log)
        self.log_button.pack(side="left", padx=5)

        # Текстовое поле для результата
        self.result_text = tk.Text(self.main_frame, height=8, width=60)
        self.result_text.pack(padx=10, pady=10)

        # Логи
        self.log_messages = []

        # Список для хранения паролей
        self.passwords = []

    def _resize_canvas(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def update_language(self, lang):
        self.current_lang = lang
        self.root.title(self.texts[lang]["title"])
        self.language_label.config(text=self.texts[lang]["language_label"])
        self.keywords_label.config(text=self.texts[lang]["keywords_label"])
        self.min_length_label.config(text=self.texts[lang]["min_length_label"])
        self.max_length_label.config(text=self.texts[lang]["max_length_label"])
        self.max_passwords_label.config(text=self.texts[lang]["max_passwords_label"])
        self.leet_check.config(text=self.texts[lang]["leet_label"])
        self.separators_check.config(text=self.texts[lang]["separators_label"])
        self.suffixes_check.config(text=self.texts[lang]["suffixes_label"])
        self.prefixes_check.config(text=self.texts[lang]["prefixes_label"])
        self.case_check.config(text=self.texts[lang]["case_label"])
        self.double_check.config(text=self.texts[lang]["double_label"])
        self.mix_chars_check.config(text=self.texts[lang]["mix_chars_label"])
        self.reverse_check.config(text=self.texts[lang]["reverse_label"])
        self.partial_check.config(text=self.texts[lang]["partial_label"])
        self.dates_check.config(text=self.texts[lang]["dates_label"])
        self.complexity_check.config(text=self.texts[lang]["complexity_label"])
        self.custom_chars_label.config(text=self.texts[lang]["custom_chars_label"])
        self.generate_button.config(text=self.texts[lang]["generate_button"])
        self.save_button.config(text=self.texts[lang]["save_button"])
        self.clear_button.config(text=self.texts[lang]["clear_button"])
        self.log_button.config(text=self.texts[lang]["log_button"])
        self.options_frame.config(text=self.texts[lang]["options_frame"])

    def clear_output(self):
        self.result_text.delete(1.0, tk.END)
        self.progress.set(0)
        self.passwords = []
        self.log_messages.append("Output cleared")

    def show_log(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Лог / Log")
        log_window.geometry("400x300")
        log_text = tk.Text(log_window, height=15, width=50)
        log_text.pack(padx=10, pady=10)
        for msg in self.log_messages:
            log_text.insert(tk.END, msg + "\n")
        log_text.config(state="disabled")

    def generate_passwords(self):
        keywords = self.input_entry.get().strip().split()
        if not keywords:
            messagebox.showerror("Ошибка / Error", self.texts[self.current_lang]["error_no_keywords"])
            self.log_messages.append("Error: No keywords entered")
            return

        try:
            min_length = int(self.min_length_entry.get())
            max_length = int(self.max_length_entry.get())
            if min_length < 1 or max_length < min_length:
                messagebox.showerror("Ошибка / Error", self.texts[self.current_lang]["error_invalid_length"])
                self.log_messages.append("Error: Invalid length values")
                return
            max_passwords = int(self.max_passwords_entry.get())
            if max_passwords < 1:
                messagebox.showerror("Ошибка / Error", self.texts[self.current_lang]["error_invalid_max_passwords"])
                self.log_messages.append("Error: Invalid max passwords")
                return
        except ValueError:
            messagebox.showerror("Ошибка / Error", self.texts[self.current_lang]["error_invalid_length"])
            self.log_messages.append("Error: Invalid input for length or max passwords")
            return

        self.progress.set(0)
        self.log_messages.append(f"Starting generation with keywords: {keywords}")
        self.passwords = self._generate_passwords(keywords, min_length, max_length, max_passwords)
        self.progress.set(100)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, self.texts[self.current_lang]["result_prefix"].format(len(self.passwords)))
        for pwd in self.passwords[:50]:
            self.result_text.insert(tk.END, pwd + "\n")
        self.log_messages.append(f"Generated {len(self.passwords)} passwords")

    def _generate_passwords(self, keywords, min_length, max_length, max_passwords):
        passwords = set()
        leet_dict = {'a': ['@', '4'], 'o': ['0'], 'i': ['1', '!'], 's': ['5', '$']}
        prefixes = ['pass', 'admin', 'user', '2025'] if self.use_prefixes.get() else []
        suffixes = ['123', '2023', '2025'] + list(self.custom_chars_entry.get()) if self.use_suffixes.get() else []
        mix_chars = list("0123456789!@#$") if self.use_mix_chars.get() else []

        def get_leet_variations(word):
            variations = [word]
            if not self.use_leet.get():
                return variations
            for i, char in enumerate(word.lower()):
                if char in leet_dict:
                    new_variations = []
                    for var in variations:
                        for replacement in leet_dict[char]:
                            new_variations.append(var[:i] + replacement + var[i+1:])
                    variations.extend(new_variations)
            return variations

        def get_case_variations(word):
            if not self.use_case.get():
                return [word]
            return [word, word.capitalize(), word.upper(), word.lower()]

        def get_partial_variations(word):
            variations = [word]
            if not self.use_partial.get():
                return variations
            for i in range(1, len(word)):
                variations.append(word[:i])
            return variations

        def get_mixed_variations(word):
            if not self.use_mix_chars.get():
                return [word]
            variations = []
            for i in range(1, len(word)):
                for char in mix_chars:
                    variations.append(word[:i] + char + word[i:])
            return variations

        def get_date_variations(numbers):
            variations = []
            if not self.use_dates.get():
                return variations
            for num in numbers:
                if num.isdigit():
                    variations.extend([num, num.zfill(2), num.zfill(4)])
            for i, num1 in enumerate(numbers):
                for num2 in numbers[i+1:]:
                    if num1.isdigit() and num2.isdigit():
                        variations.extend([num1 + num2, num2 + num1, num1 + num2.zfill(2), num2.zfill(2) + num1])
            return variations

        def is_complex(password):
            if not self.use_complexity.get():
                return True
            has_letter = bool(re.search(r'[a-zA-Z]', password))
            has_number = bool(re.search(r'\d', password))
            has_symbol = bool(re.search(r'[!@#$%^&*_\-.]', password))
            return has_letter and has_number and has_symbol

        all_words = []
        numbers = [kw for kw in keywords if kw.isdigit()]
        for keyword in keywords:
            if keyword.isalpha():
                leet_vars = get_leet_variations(keyword)
                for var in leet_vars:
                    all_words.extend(get_case_variations(var))
                    if self.use_double.get():
                        all_words.extend(get_case_variations(var + var))
                    if self.use_reverse.get():
                        all_words.extend(get_case_variations(var[::-1]))
                    all_words.extend(get_partial_variations(var))
                    all_words.extend(get_mixed_variations(var))
            else:
                all_words.append(keyword)

        all_words.extend(get_date_variations(numbers))

        total_combinations = sum(len(list(itertools.permutations(all_words, length))) for length in range(1, len(all_words) + 1))
        current = 0
        for length in range(1, len(all_words) + 1):
            for combo in itertools.permutations(all_words, length):
                current += 1
                self.progress.set((current / total_combinations) * 100)
                self.root.update()
                if len(passwords) >= max_passwords:
                    return list(passwords)
                password = ''.join(combo)
                if min_length <= len(password) <= max_length and is_complex(password):
                    passwords.add(password)
                if self.use_separators.get():
                    for sep in ['_', '-', '.']:
                        sep_password = sep.join(combo)
                        if min_length <= len(sep_password) <= max_length and is_complex(sep_password):
                            passwords.add(sep_password)
                for suffix in suffixes:
                    suffixed = ''.join(combo) + suffix
                    if min_length <= len(suffixed) <= max_length and is_complex(suffixed):
                        passwords.add(suffixed)
                    if self.use_separators.get():
                        for sep in ['_', '-', '.']:
                            sep_suffixed = sep.join(combo) + suffix
                            if min_length <= len(sep_suffixed) <= max_length and is_complex(sep_suffixed):
                                passwords.add(sep_suffixed)
                for prefix in prefixes:
                    prefixed = prefix + ''.join(combo)
                    if min_length <= len(prefixed) <= max_length and is_complex(prefixed):
                        passwords.add(prefixed)
                    if self.use_separators.get():
                        for sep in ['_', '-', '.']:
                            sep_prefixed = prefix + sep.join(combo)
                            if min_length <= len(sep_prefixed) <= max_length and is_complex(prefixed):
                                passwords.add(sep_prefixed)
                    for suffix in suffixes:
                        full = prefix + ''.join(combo) + suffix
                        if min_length <= len(full) <= max_length and is_complex(full):
                            passwords.add(full)
                        if self.use_separators.get():
                            for sep in ['_', '-', '.']:
                                sep_full = prefix + sep.join(combo) + suffix
                                if min_length <= len(sep_full) <= max_length and is_complex(sep_full):
                                    passwords.add(sep_full)
        return list(passwords)

    def save_to_file(self):
        if not self.passwords:
            messagebox.showerror("Ошибка / Error", self.texts[self.current_lang]["error_no_passwords"])
            self.log_messages.append("Error: No passwords to save")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                for pwd in self.passwords:
                    f.write(pwd + '\n')
            messagebox.showinfo("Успех / Success", self.texts[self.current_lang]["success_save"].format(file_path))
            self.log_messages.append(f"Passwords saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()