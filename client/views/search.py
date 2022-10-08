import tkinter as tk
from tkinter import ttk
import views.textstyles as style


class Search(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.create_widgets()

    def create_widgets(self):
        self.spacer = tk.Label(self, height=2, width=5, anchor=tk.E)
        self.spacer.grid(row=0, column=0)

        self.lbl_query = tk.Label(
            self, height=1, text="Query:", width=6, justify="left", anchor=tk.E, font=style.label_font)
        self.lbl_query.grid(row=1, column=1, sticky=tk.E,
                            padx=10, pady=0, columnspan=1)
        self.txt_query = tk.Entry(
            self, width=36, bg="#FFFFFF", font=style.entry_font)
        self.txt_query.grid(row=1, column=2, sticky=tk.W,
                            padx=10, pady=10, columnspan=3)

        self.btn_search = tk.Button(
            self, text="Search", width=6, height=1, font=style.btn_font,
            activebackground=style.btn_style['actbg'], bg=style.btn_style['bg'], fg=style.btn_style['fg'])
        self.btn_search.grid(row=1, column=5, sticky=tk.W,
                             padx=10, pady=10, columnspan=1)

        self.spacer1 = tk.Label(self, height=1, width=5)
        self.spacer1.grid(row=2, column=0)

        self.lbl_result = tk.Label(
            self, height=1, text="~ " * 6 + " Result " + " ~" * 6, width=30, font="Helvetica 16 bold italic", bg="#c7ecee", fg="#2a363d")
        self.lbl_result.grid(row=3, column=1, sticky=tk.W+tk.E,
                             padx=10, pady=0, columnspan=5)
        self.scb_result = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scb_result.grid(
            row=4, column=6, sticky=tk.N+tk.S+tk.W, columnspan=1)
        cols = ("ID", "Title", "Author", "Published date", "Type")
        self.tbl_result = ttk.Treeview(
            self, columns=cols, show="headings", yscrollcommand=self.scb_result.set, selectmode="browse", height=12)
        self.scb_result.config(command=self.tbl_result.yview)
        self.tbl_result.grid(row=4, column=1, sticky=tk.E,
                             padx=0, pady=10, columnspan=5)

        for col in cols:
            self.tbl_result.heading(col, text=col)
            self.tbl_result.column(col, width=160, stretch=True)
        self.tbl_result.column("ID", width=80, stretch=True)

        self.btn_clear = tk.Button(
            self, text="Clear", width=6, height=1, command=self.clear_result, fg="yellow", activebackground="orange", bg="#cc0000", font="Helvatica 12 bold italic")
        self.btn_clear.grid(row=5, column=5, sticky=tk.E,
                            padx=0, pady=10, columnspan=1)

    def show_result(self, table):
        self.clear_result()
        if len(table) == 0:
            table = [["No result"] * 5]
        for row in table:
            self.tbl_result.insert("", "end", values=row)

    def clear_result(self):
        for rowid in self.tbl_result.get_children():
            self.tbl_result.delete(rowid)

    def clear_query(self):
        self.txt_query.delete(0, tk.END)

    def get_query(self):
        return self.txt_query.get()

    def get_bookid(self):
        curItem = self.tbl_result.focus()
        if not curItem:
            return None
        return self.tbl_result.item(curItem)['values'][0:2]
