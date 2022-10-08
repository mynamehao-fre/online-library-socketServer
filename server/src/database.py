import sqlite3


class Database:
    def __init__(self, link='assets/library.db'):
        self.link = link
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        # create table
        # create table BooK
        self.cur.execute("""
      CREATE TABLE IF NOT EXISTS BOOK(
        ID NCHAR(5) PRIMARY KEY,
        Name NVARCHAR(50),
        Author NVARCHAR(30),
        PublishYear YEAR,
        Type NVARCHAR(30),
        Link NVARCHAR(40)
      )
    """)
        # Create table account
        self.cur.execute("""
      CREATE TABLE IF NOT EXISTS ACCOUNT (
        Username VARCHAR(30) PRIMARY KEY,
        Password VARCHAR(30)
      )
    """)
        # self.cur.execute(
        #     "INSERT INTO BOOK VALUES ('CS001', 'Beyound the Wall', 'Ambrose Bierce', 1899, 'Computer Science', 'assets/books/book1.txt')")
        # self.cur.execute(
        #     "INSERT INTO BOOK VALUES ('NV001', 'Hello World', 'Alex', 1939, 'Novel', 'assets/books/book2.txt')")
        # self.cur.execute(
        #     "INSERT INTO BOOK VALUES ('SK001', 'Time management', 'Lorem', 2020, 'Soft kill', 'assets/books/book3.txt')")
        # self.conn.commit()
        # self.cur.execute("INSERT INTO ACCOUNT VALUES ('haonhat', 'admin')")
        # self.cur.execute("INSERT INTO ACCOUNT VALUES ('admin', 'admin')")
        # self.conn.commit()
        self.cur.close()
        self.conn.close()

    def account_sign_in(self, username, password):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "SELECT username, password FROM ACCOUNT WHERE username = '%s'" % username)
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        if(result):
            if (result[0][1] == password):
                return "SUCCESS"
            return "FAIL Incorrect password"
        else:
            return "FAIL Invalid account"

    def account_sign_up(self, username, password):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()

        self.cur.execute(
            """SELECT username FROM ACCOUNT WHERE username = '%s'""" % username)
        if (not self.cur.fetchall()):
            self.cur.execute("""INSERT INTO ACCOUNT VALUES ('%s', '%s')""" % (
                username, password.replace("'", "''")))
            self.conn.commit()
            msg = "SUCCESS"
        else:
            msg = "FAIL Username already exists"

        self.cur.close()
        self.conn.close()
        return msg

    def book_query(self, query):
        if len(query.split(maxsplit=1)) != 2:  # invalid query
            return []
        qtype, param = query.split(maxsplit=1)
        qtype = qtype[2:].upper()
        if(qtype == 'ID'):
            param = "'"+param+"'"
        param = param.upper()
        param = param[0] + param[1:-1].replace('"', '""') + param[-1]

        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()

        try:
            self.cur.execute(
                "SELECT ID, Name, Author, PublishYear, Type FROM BOOK WHERE UPPER(" + qtype + ") = %s" % param)
        except:
            return []
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return result

    def get_book(self, ID):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT Link FROM BOOK WHERE ID = '%s'" % ID)
        link = self.cur.fetchall()[0][0]
        fi = open(link, 'r', encoding='utf8')
        content = fi.read()
        fi.close()
        self.cur.close()
        self.conn.close()
        return content

    def get_all_book(self):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * from BOOK")
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return result

    def get_one_book(self, ID):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * from BOOK where ID = '%s'" % ID.upper())
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return result

    def delete_one_book(self, ID):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("""DELETE FROM BOOK WHERE ID = '%s'""" % ID.upper())
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def update_one_book(self, book):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute("""DELETE FROM BOOK WHERE ID = '%s'""" % book[0])
        self.cur.execute("""INSERT INTO BOOK VALUES """ +
                         str(book).replace("\\'", "''"))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def insert_new_book(self, book):
        self.conn = sqlite3.connect(self.link)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """SELECT ID FROM BOOK WHERE ID = '%s'""" % book[0].upper())
        flag = False
        if not self.cur.fetchall():  # if ID not already exists
            self.cur.execute("""INSERT INTO BOOK VALUES """ +
                             str(book).replace("\\'", "''"))
            self.conn.commit()
            flag = True
        self.cur.close()
        self.conn.close()
        return flag
