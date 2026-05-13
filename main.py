"""
Portfolio Manager — Pure Python Desktop App
Requires: pip install pandas openpyxl
Run: python main.py
"""
import tkinter as tk
from ui.main_window import MainWindow

def main():
    root = tk.Tk()
    root.configure(bg='#f0f2f7')
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
