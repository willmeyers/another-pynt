from tkinter import *
from tkinter import ttk
from src.client import Client
from server import chat_server
from src.net import Message


class ChatDemo(Client, Frame):
    ''' The ChatDemo class is a basic chat program built using Tk. It inherits from the Frame class and the Client class.
    This is the controller for the program, everything is controlled thorugh this class. Ignore messy GUI code... just a demo.

    '''

    def __init__(self, root):
        Client.__init__(self)
        Frame.__init__(self, root)
        self.start()

        self.root = root
        self.frame = Frame(self.root)
        self.frame.grid()
        self.grid()

        self.host_entry_text = StringVar()
        self.port_entry_text = StringVar()
        self.chat_entry_text = StringVar()

        self.chat_window = Text(self.frame, width=64, height=20, bg='white')
        self.chat_window.insert(END, '[!] NOT CONNECTED\n')
        self.chat_window.configure(state=DISABLED)

        self.build_gui()

        self.connect_request = Message('CONN', ('string',))
        self.chat_message = Message('CHAT', ('string', 'string'))

        self.name = None

        @self.message('CHAT')
        def chat_recv(message, addr):
            try:
                _, name, m = self.chat_message.unpack(message)
                self.print_chat_message(name, m)
            except Exception as err:
                print(err)

    def build_gui(self):
        ''' Builds the GUI for the program '''
        self.root.title("Chat Demo")

        menubar = Menu(self.root)

        chatbar = Menu(menubar, tearoff=0)
        chatbar.add_command(label='Host', command=self.open_server_host_dialog)
        chatbar.add_command(label='Connect', command=self.open_server_connect_dialog)
        chatbar.add_separator()
        chatbar.add_command(label='Quit')
        menubar.add_cascade(label='Chat', menu=chatbar)
        self.root.config(menu=menubar)

        self.chat_window.grid(column=0, row=0, padx=(5,5), pady=(0,10), columnspan=1)

        chat_entry = Entry(self.frame, width=85, textvariable=self.chat_entry_text)
        chat_entry.grid(column=0, row=1, sticky=W, padx=(5,5), pady=(0,10), columnspan=1)
        chat_entry.bind('<Return>', self.send_chat_message)
        chat_entry.focus_set()

        send_button = Button(self.frame, text="Send", command=self.send_chat_message)
        send_button.grid(row=1, column=1, columnspan=1, padx=(5,5), pady=(0,0), sticky=E+W)

    def open_server_host_dialog(self):
        top = Toplevel(self.root)
        top.grid()

        host_label = Label(top, text='Host')
        host_label.grid(column=0, row=0, sticky=W, padx=(5,5), pady=(0,10), columnspan=1)
        host_entry = Entry(top, width=32, textvariable=self.host_entry_text)
        host_entry.grid(column=1, row=0, sticky=W, padx=(5,5), pady=(0,10), columnspan=1)

        port_label = Label(top, text='Port')
        port_label.grid(column=0, row=1, sticky=W, padx=(5,5), pady=(0,10), columnspan=1)
        port_entry = Entry(top, width=32, textvariable=self.port_entry_text)
        port_entry.grid(column=1, row=1, sticky=W, padx=(5,5), pady=(0,10), columnspan=1)

        start_button = Button(top, text='Start', command=self.start_server)
        start_button.grid(column=1, row=2, sticky=E, padx=(5,5), pady=(0,10), columnspan=1)

    def open_server_connect_dialog(self):
        top = Toplevel(self.root)
        top.grid()

        host_label = Label(top, text='Host')
        host_label.grid(column=0, row=0, sticky=W, padx=(5,5), pady=(0,10), columnspan=1)
        host_entry = Entry(top, width=32, textvariable=self.host_entry_text)
        host_entry.grid(column=1, row=0, sticky=W, padx=(5,5), pady=(0,10), columnspan=1)
        host_entry.bind('<Return>', self.connect_to_server)

        port_label = Label(top, text='Port')
        port_label.grid(column=0, row=1, sticky=W, padx=(5,5), pady=(0,10), columnspan=1)
        port_entry = Entry(top, width=32, textvariable=self.port_entry_text)
        port_entry.grid(column=1, row=1, sticky=W, padx=(5,5), pady=(0,10), columnspan=1)
        port_entry.bind('<Return>', self.connect_to_server)

        conn_button = Button(top, text='Connect', command=self.connect_to_server)
        conn_button.grid(column=1, row=2, sticky=E, padx=(5,5), pady=(0,10), columnspan=1)

    def start_server(self):
        self.chat_window.configure(state=NORMAL)
        self.chat_window.insert(END, 'Started server.\n')
        self.chat_window.configure(state=DISABLED)

        chat_server.start()

    def connect_to_server(self):
        self.set_server_addr((self.host_entry_text.get(), int(self.port_entry_text.get())))
        self.name = input('ENTER NAME > ')
        m = self.connect_request.pack(self.name.encode())
        self.simple_send(m)
        self.chat_window.configure(state=NORMAL)
        self.chat_window.insert(END, 'Successfully connected to server.\n')
        self.chat_window.configure(state=DISABLED)

    def send_chat_message(self):
        self.chat_window.configure(state=NORMAL)
        m = self.chat_message.pack(self.name.encode(), self.chat_entry_text.get().encode())
        self.simple_send(m)
        self.chat_entry_text.set('')
        self.chat_window.configure(state=DISABLED)

    def print_chat_message(self, name, message):
        self.chat_window.configure(state=NORMAL)
        self.chat_window.insert(END, name.decode().rstrip('\0')+'> '+message.decode().rstrip('\0')+'\n')
        self.chat_window.configure(state=DISABLED)


def main():
    root = Tk()
    app = ChatDemo(root)
    root.mainloop()

    app.shutdown()


if __name__ == '__main__':
    main()