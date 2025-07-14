import tkinter as tk
from tkinter import messagebox, scrolledtext
from services.ollama_service import OllamaService

class LLMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local LLaMA Runner")
        self.root.geometry("600x400")
        self.ollama_service = OllamaService()
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)
        
        tk.Label(self.main_frame, text="Local LLaMA Runner", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Open Chat", command=self.open_chat).pack(pady=10)
        tk.Button(self.main_frame, text="Exit", command=self.root.quit).pack(pady=10)
    
    def open_chat(self):
        if not self.ollama_service.is_model_ready():
            messagebox.showerror("Error", "Model is not ready. Ensure Docker is running.")
            return
        
        chat_window = tk.Toplevel(self.root)
        chat_window.title("Chat with LLaMA")
        chat_window.geometry("600x400")
        
        self.chat_area = scrolledtext.ScrolledText(chat_window, height=20, width=60)
        self.chat_area.pack(padx=10, pady=10)
        
        self.input_field = tk.Entry(chat_window, width=50)
        self.input_field.pack(padx=10, pady=5)
        self.input_field.focus_set()
        
        tk.Button(chat_window, text="Send", command=self.send_message).pack(pady=5)
    
    def send_message(self):
        user_input = self.input_field.get()
        if not user_input:
            return
        
        self.chat_area.insert(tk.END, f"You: {user_input}\n")
        self.input_field.delete(0, tk.END)
        
        response = self.ollama_service.generate_response(user_input)
        self.chat_area.insert(tk.END, f"LLaMA: {response}\n\n")
        self.chat_area.see(tk.END)