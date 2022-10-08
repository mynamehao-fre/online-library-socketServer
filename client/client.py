import socket as sk
import tkinter as tk
import pickle
import views.textstyles as style
#client.connect(('flex12fre', 54321))
from views.connect import Connect
from views.login import Login
from views.signup import Signup
from views.search import Search
from views.book import Book

from views.dialog import mmessagebox, yesno


class Client(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.username = tk.StringVar()
        self.username.set('Not logged in')

        self.geometry('800x740')
        self.title('Online Library')
        self.resizable(False, False)
        self.grid()

        # Header
        self.head = tk.Frame(self, bg='#7ed6df')
        self.head.pack(side='top', fill='both', expand=1)
        self.head.grid_rowconfigure(0, weight=1)
        self.head.grid_columnconfigure(0, weight=1)

        # Body
        self.body = tk.Frame(self)
        self.body.pack(side="top", fill="both", expand=True)
        self.body.grid_rowconfigure(0, weight=1)
        self.body.grid_columnconfigure(0, weight=1)

        # Create widgets
        self.frame = None
        self.frames = {}
        self.create_header()
        self.create_frames()
        self.bind_action()

    def run(self):
        self.show_frame('Connect')
        self.mainloop()

    def create_header(self):
        '''Init header element'''
        self.lbl_app = tk.Label(
            self.head, text='HCMUS Online Library', height=1, font=style.logo_font, bg="#f9cdad", fg="#ec2049")
        self.lbl_app.grid(row=0, column=0, sticky=tk.W, padx=30, pady=10,
                          ipadx=10, ipady=10, columnspan=2, rowspan=2)
        self.lbl_user = tk.Label(
            self.head, textvariable=self.username, height=1, bg="#7ed6df", fg="#aa2e00", font=style.user_font)
        self.lbl_user.grid(row=0, column=2, sticky=tk.E, ipadx=10,
                           padx=10, pady=0, columnspan=1)

        self.btn_logout = tk.Button(
            self.head, text="Log out", width=6, height=1, bg='#97c1a9', fg='#000000')
        self.btn_logout.grid(row=0, column=3, sticky=tk.E, ipadx=5,
                             padx=5, pady=0)
        self.btn_logout.grid_remove()

    def create_frames(self):
        for frame in (Connect, Login, Search, Signup):
            page_name = frame.__name__
            instance = frame(parent=self.body)
            instance.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = instance

    def bind_action(self):
        self.bind("<Destroy>", self.quit_prog)

        self.btn_logout["command"] = self.logout

        self.frames['Connect'].btn_connect['command'] = self.connect

        self.frames["Login"].btn_login["command"] = self.login
        self.frames["Login"].btn_newacc["command"] = lambda: self.show_frame(
            "Signup")

        self.frames["Signup"].btn_signup["command"] = self.signup
        self.frames["Signup"].btn_back["command"] = lambda: self.show_frame(
            "Login")

        self.frames["Search"].btn_search["command"] = self.search
        self.frames["Search"].tbl_result.bind(
            "<Double-1>", lambda e: self.book())

    def show_frame(self, page_name):
        self.frame = self.frames[page_name]
        self.frame.tkraise()

    def connect(self):
        ip = self.frame.get_info()
        if ip.strip(' ') == '':
            mmessagebox('Invalid Input', 'Please enter an IP address', 'warn')
            return

        try:
            self._socket.connect((ip, 54321))
            helo_message = self._socket.recv(1024).decode('utf8')
            if helo_message == 'OVERFLOW':
                self._socket.close()
                raise
            mmessagebox('Accepted', 'Connected to library', 'info')
            self.show_frame('Login')
        except:
            mmessagebox(
                'Failed', 'Unable to connect, please try again', 'error')

    def login(self):
        usr, pas = self.frame.get_info()

        try:
            if usr.strip(' ') == "":
                raise ValueError("username")
            if pas.strip(' ') == "":
                raise ValueError("password")
            if not usr.isalnum():
                raise ValueError("username contains only [A-z][0-9] character")
        except ValueError as ve:
            mmessagebox('Invalid input',
                        'Please enter your ' + str(ve), 'warn')
            return

        try:
            self._socket.sendall(bytes('\t'.join(["LOGIN", usr, pas]), "utf8"))
            response = self._socket.recv(1024).decode('utf8')

            if response == 'SUCCESS':
                mmessagebox('Log in successful', 'Welcome, ' + usr, 'info')
                self.username.set(usr)
                self.btn_logout.grid()
                self.show_frame('Search')
            else:
                errmsg = response.split(' ', 1)[1]
                mmessagebox("Log in failed", errmsg, "warn")
        except:
            if yesno("CONNECTION FAILURE", "The connection to the server HAS FAILED :(\nDo you want to logout and reconnect?"):
                self.logout()
                self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                self.show_frame("Connect")

    def signup(self):
        usr, pas, chk = self.frame.get_info()

        try:
            if usr.strip(' ') == "":
                raise ValueError("username")
            if not usr.isalnum():
                raise ValueError("username contains only [A-z][0-9] character")
            if pas.strip(' ') == "":
                raise ValueError("password")
            if chk.strip(' ') == "":
                raise ValueError("password again")
            if not pas == chk:
                raise ValueError("mismatch")
        except ValueError as ve:
            if str(ve) == "mismatch":
                mmessagebox("Wrong password",
                            "Your password inputs don't match", "warn")
            else:
                mmessagebox("Invalid input",
                            "Please enter your " + str(ve), "warn")
            return

        try:
            self._socket.sendall(
                bytes('\t'.join(['SIGNUP', usr, pas]), 'utf8'))
            response = self._socket.recv(1024).decode('utf8')

            if response == 'SUCCESS':
                mmessagebox(
                    'Sign up successful', 'Account created, please go\nback to log in page', 'info')
            else:
                errmsg = response.split(' ', 1)[1]
                mmessagebox("Sign up failed", errmsg, "warn")
        except:
            if yesno("CONNECTION FAILURE", "The connection to the server HAS FAILED :(\nDo you want to logout and reconnect?"):
                self.logout()
                self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                self.show_frame("Connect")

    def logout(self):
        try:
            self._socket.sendall(bytes("LOGOUT", "utf8"))
        except:
            pass
        finally:
            self.username.set("Not logged in")
            self.btn_logout.grid_remove()
            self.frames["Connect"].clear_all()
            self.frames["Login"].clear_all()
            self.frames["Signup"].clear_all()
            self.frames["Search"].clear_result()
            self.frames["Search"].clear_query()
            self.show_frame("Login")

    def search(self):
        query = self.frame.get_query()
        analyze = query.split(maxsplit=1)
        try:
            if len(analyze) != 2:
                raise
            if analyze[0].upper() != 'F_ID':
                if analyze[1][0] != '"' or analyze[1][-1] != '"':
                    raise
        except:
            mmessagebox('Invalid input',
                        'Please enter a correct query', 'warn')
            return

        query = ' '.join(query.split())

        try:
            self._socket.sendall(bytes('\t'.join(["SEARCH", query]), "utf8"))
            response = pickle.loads(self._socket.recv(1024))
            self.frame.show_result(response)
        except:
            if yesno("CONNECTION FAILURE", "The connection to the server HAS FAILED :(\nDo you want to logout and reconnect?"):
                self.logout()
                self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                self.show_frame("Connect")

    def book(self):
        book = self.frame.get_bookid()
        if not book:
            return
        try:
            self._socket.sendall(bytes('\t'.join(["BOOK", book[0]]), "utf8"))
            response = self._socket.recv(1024).decode("utf8")
            Book(tk.Toplevel(self), book[0], book[1], response, self.download)
        except:
            if yesno("CONNECTION FAILURE", "The connection to the server HAS FAILED :(\nDo you want to logout and reconnect?"):
                self.logout()
                self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                self.show_frame("Connect")

    def download(self, bookid):
        self._socket.sendall(bytes('\t'.join(["DOWNLOAD", bookid]), "utf8"))

    def quit_prog(self, event):
        try:
            if str(event.widget) == '.':
                self._socket.sendall(bytes("QUIT", "utf8"))
                self._socket.close()
        except:
            pass


if __name__ == '__main__':
    app = Client()
    app.run()
