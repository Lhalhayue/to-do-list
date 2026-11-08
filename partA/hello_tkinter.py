import tkinter as tk

root = tk.Tk()
root.title("Tkinter Hello World")
root.geometry("350x180")

message = tk.Label(root, text="Hello, welcome to Tkinter!")
message.pack(pady=20)

def change_message():
    message.config(text="Button clicked!")

button = tk.Button(root, text="Click Me", command=change_message)
button.pack()

root.mainloop()
