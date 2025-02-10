import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        self.length_var = tk.IntVar(value=12)
        
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.colors = {
            'bg': '#FFFFFF',
            'fg': '#2D3436',
            'accent': '#0984E3',
            'secondary': '#636E72',
            'entry_bg': '#F0F0F0',
            'progress': '#00B894'
        }

        self.style.configure('.', font=('Segoe UI', 10))
        self.style.configure('TButton', 
                           padding=8, 
                           background=self.colors['accent'],
                           foreground='white')
        
        self.style.configure('TCheckbutton', 
                           background=self.colors['bg'],
                           foreground=self.colors['fg'],
                           indicatorcolor=self.colors['accent'])
        
        self.style.configure('TEntry',
                           fieldbackground=self.colors['entry_bg'],
                           foreground=self.colors['fg'],
                           insertcolor=self.colors['fg'])
        
        self.style.configure('Horizontal.TProgressbar',
                           background=self.colors['progress'],
                           troughcolor=self.colors['bg'])

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.settings_frame = ttk.LabelFrame(self.main_frame, text="Настройки")
        self.output_frame = ttk.Frame(self.main_frame)
        
        self.length_label = ttk.Label(self.settings_frame, text="Длина пароля:")
        self.length_spin = ttk.Spinbox(self.settings_frame, 
                                     from_=4, 
                                     to=64, 
                                     textvariable=self.length_var,
                                     width=5)
        
        self.options_frame = ttk.Frame(self.settings_frame)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        self.upper_check = ttk.Checkbutton(self.options_frame, text="A-Z", variable=self.upper_var)
        self.lower_check = ttk.Checkbutton(self.options_frame, text="a-z", variable=self.lower_var)
        self.digits_check = ttk.Checkbutton(self.options_frame, text="0-9", variable=self.digits_var)
        self.symbols_check = ttk.Checkbutton(self.options_frame, text="!@#", variable=self.symbols_var)
        
        self.generate_btn = ttk.Button(self.main_frame, 
                                     text="Сгенерировать", 
                                     command=self.generate_password)
        
        self.copy_btn = ttk.Button(self.output_frame, 
                                 text="Копировать", 
                                 command=self.copy_password)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.output_frame, 
                                      textvariable=self.password_var, 
                                      font=('Consolas', 12), 
                                      state='readonly',
                                      width=24)
        
        self.security_bar = ttk.Progressbar(self.main_frame, 
                                          length=200, 
                                          mode='determinate')
        self.security_label = ttk.Label(self.main_frame, text="Надёжность: -")

    def setup_layout(self):
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.settings_frame.grid(row=0, column=0, sticky=tk.EW, pady=10)
        self.length_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.length_spin.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.options_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.upper_check.pack(side=tk.LEFT, padx=10)
        self.lower_check.pack(side=tk.LEFT, padx=10)
        self.digits_check.pack(side=tk.LEFT, padx=10)
        self.symbols_check.pack(side=tk.LEFT, padx=10)
        
        self.generate_btn.grid(row=1, column=0, pady=15, sticky=tk.EW)
        
        self.output_frame.grid(row=2, column=0, sticky=tk.EW, pady=10)
        self.password_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.copy_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.security_bar.grid(row=3, column=0, pady=(15, 5), sticky=tk.EW)
        self.security_label.grid(row=4, column=0, pady=(0, 10))
        
        self.main_frame.columnconfigure(0, weight=1)
        self.settings_frame.columnconfigure(0, weight=1)

    def generate_password(self):
        characters = []
        if self.upper_var.get():
            characters.extend(string.ascii_uppercase)
        if self.lower_var.get():
            characters.extend(string.ascii_lowercase)
        if self.digits_var.get():
            characters.extend(string.digits)
        if self.symbols_var.get():
            characters.extend('!@#$%^&*()_+-=')
            
        if not characters:
            messagebox.showerror("Ошибка", "Выберите хотя бы один набор символов")
            return
            
        try:
            length = self.length_var.get()
            password = ''.join(random.choice(characters) for _ in range(length))
            self.password_var.set(password)
            self.evaluate_password_strength(password)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def copy_password(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")

    def evaluate_password_strength(self, password):
        strength = 0
        if len(password) >= 12: strength += 1
        if any(c.isupper() for c in password): strength += 1
        if any(c.islower() for c in password): strength += 1
        if any(c.isdigit() for c in password): strength += 1
        if any(c in '!@#$%^&*()_+-=' for c in password): strength += 1
        
        self.security_bar['value'] = (strength / 5) * 100
        self.security_label.config(text=f"Надёжность: {['Долбоеб?', 'Средняя', 'Хорошая', 'Очень хорошая', 'Отличная'][strength-1]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
