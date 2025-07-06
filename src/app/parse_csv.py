from tkinter import filedialog

def select_file():
    filedialog.askopenfilename(title="Select a File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])