import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import threading
from services.ollama_service import OllamaService

class LLMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local LLaMA Runner")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.ollama_service = OllamaService()

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12))

        self.main_frame = ttk.Frame(self.root, padding=40)
        self.main_frame.pack(expand=True)

        ttk.Label(self.main_frame, text="Local LLaMA Runner", font=("Helvetica", 20, "bold")).pack(pady=20)

        self.status_label = ttk.Label(self.main_frame, text="Checking model readiness...", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.open_chat_btn = ttk.Button(self.main_frame, text="Open Chat", command=self.open_chat, state="disabled")
        self.open_chat_btn.pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(self.main_frame, text="Exit", command=self.root.quit).pack(pady=10, ipadx=10, ipady=5)

        self.poll_model_ready()

    def open_chat(self):
        if not self.ollama_service.is_model_ready():
            messagebox.showinfo("Info", "Model is still downloading, please wait.")
            return

        chat_window = tk.Toplevel(self.root)
        chat_window.title("Chat with LLaMA")
        chat_window.geometry("700x550")

        chat_frame = ttk.Frame(chat_window, padding=10)
        chat_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, font=("Helvetica", 12))
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0,10))

        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X)

        self.input_field = ttk.Entry(input_frame)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_field.focus_set()

        ttk.Button(input_frame, text="Send", command=self.send_message).pack(side=tk.LEFT, padx=(10,0))

    def send_message(self):
        user_input = self.input_field.get()
        if not user_input:
            return

        self.chat_area.insert(tk.END, f"You: {user_input}\n")
        self.input_field.delete(0, tk.END)

        response = self.ollama_service.generate_response(user_input)
        self.chat_area.insert(tk.END, f"LLaMA: {response}\n\n")
        self.chat_area.see(tk.END)

    def poll_model_ready(self):
        def _worker():
            ready = self.ollama_service.is_model_ready()
            self.root.after(0, lambda: self._on_model_check(ready))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_model_check(self, ready: bool):
        if ready:
            self.status_label.config(text="Model ready.")
            self.open_chat_btn.config(state="normal")
        else:
            self.status_label.config(text="Downloading model, please wait…")
            self.root.after(2000, self.poll_model_ready)