from tkinter import *
from tkinter import ttk
from src.client import Client


class ChatDemo(Frame, Client):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root

        self.chat_message = StringVar()

        self.build_gui()

    def build_gui(self):
        self.root.geometry("640x480")
        self.root.title("Chat Demo")

        frame = Frame(self.root)
        frame.grid()
        self.grid()

        menubar = Menu(self.root)

        chatbar = Menu(menubar, tearoff=0)
        chatbar.add_command(label='Start Server')
        chatbar.add_command(label='Connect')
        chatbar.add_separator()
        chatbar.add_command(label='Quit')
        menubar.add_cascade(label='Chat', menu=chatbar)
        self.root.config(menu=menubar)

        chat_window = Text(frame, width=64, height=20, bg='white')
        chat_window.configure(state=DISABLED)
        chat_window.grid(column=0, row=0, padx=(5,5), pady=(0,10), columnspan=1)

        chat_entry = Entry(frame, width=85, textvariable=self.chat_message)
        chat_entry.grid(column=0, row=1, sticky=W, padx=(5,5), pady=(0,10), columnspan=1)
        chat_entry.bind('<Return>', self.send_chat_message)
        chat_entry.focus_set()

        send_button = Button(frame, text="Send", command=self.send_chat_message)
        send_button.grid(row=1, column=1, columnspan=1, padx=(5,5), pady=(0,0), sticky=E+W)

    def send_chat_message(self):
        print('MESSAGE SENT!')

def main():
    root = Tk()
    app = ChatDemo(root)
    root.mainloop()


if __name__ == '__main__':
    main()