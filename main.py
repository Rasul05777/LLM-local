import tkinter as tk
from gui.app import LLMApp

if __name__ == "__main__":
    root = tk.Tk()
    app = LLMApp(root)
    root.mainloop()