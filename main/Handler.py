from http.server import HTTPServer, BaseHTTPRequestHandler
# import pyodbc
import psycopg2
from datetime import datetime
import json


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()

        # query = """select Base.class, Base.theme, Base.variant, Domino.left_side, Domino.right_side, Domino.correct_answer
        #                                 from Base, Domino
        #                                 where Base.id_domino = Domino.id"""
        ans = get_class_list()
        # print("Answer: " + ans)
        self.wfile.write(ans.encode())


def do_HEAD(self):
    self._set_headers()


def do_POST(self):
    # Doesn't do anything with posted data
    self._set_headers()
    self.wfile.write(self._html("POST!"))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=80):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


class Sql:
    def __init__(self):
        self.conn = psycopg2.connect(
            'postgres://xdxcqcwnkfqqie:3b3bc8ebe684cd8f4f4b96c2569a0d0b796b885faf0c6800cd3712739d7fe982@ec2-99-81-177-233.eu-west-1.compute.amazonaws.com:5432/d9coav5liftcvu',
            sslmode='require')
        self.cur = self.conn.cursor()

    def get_class_list(self):
        # query = "select * from Domino;"
        res = self.cur.execute("select * from Domino;")
        res2 = res.fetchone()
        self.conn.commit()
        for i in res2:
            print(i)
        somedict = {"classes": [list(x) for x in res2]}
        ans = json.dumps(somedict, ensure_ascii=False)
        return ans

    def get_theme_list(self, class_number):
        sql = Sql()
        cursor = sql.conn.cursor()
        query = f"select distinct theme from [dbo].[Domino] where class_number = {class_number}"
        res = cursor.execute(query).fetchall()
        # for i in res:
        #     print(i)
        somedict = {"classes": [str(x[0]) for x in res]}
        ans = json.dumps(somedict, ensure_ascii=False)
        return ans

def get_class_list():
    sql = Sql()
    # query = "select * from Domino;"
    res = sql.cur.execute("select * from Domino;")
    res2 = sql.cur.fetchall()
    sql.conn.commit()
    sql.cur.close()
    sql.conn.close()
    for i in res2:
        print(i)
    somedict = {"classes": [x for x in res2]}
    ans = json.dumps(somedict, ensure_ascii=False)
    print("Answer: " + ans)
    return ans
if __name__ == "__main__":
    run()
