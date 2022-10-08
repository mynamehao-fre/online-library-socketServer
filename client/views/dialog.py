from tkinter import messagebox


def mmessagebox(title="Online Library", msg="Something is wrong :(", type="warn"):
    # type are: warn, error, info
    if type == "error":
        messagebox.showerror(title, msg)
    elif type == "warn":
        messagebox.showwarning(title, msg)
    else:
        messagebox.showinfo(title, msg)


def yesno(title="Question", question="Yes or No?"):
    return messagebox.askyesno(title, question)
