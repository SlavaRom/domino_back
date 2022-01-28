from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2
import json
import re
import os
from urllib.parse import unquote_plus


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        # self._set_headers()
        ans = ''
        a = self.path.split('/')[1:]
        if len(a) == 1 and a[0].isdigit():
            ans = get_theme_list(int(a[0]))
        elif len(a) == 1 and a[0] == '':
            ans = get_class_list()
        elif len(a) == 2:
            ans = get_id_variant_countDominoshek_list(int(a[0]), unquote_plus(a[1]))
        elif len(a) == 3:
            id_domino, count_dominoshek = get_id_Domino(int(a[0]), unquote_plus(a[1]), int(a[2]))
            ans = get_all_Dominoshek_list(id_domino, count_dominoshek)
        print("Answer: " + ans)
        self.send_response(200)
        self.send_header("Accept-Encoding", "gzip, deflate, br")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(ans.encode())
        self.wfile.flush()
        self.connection.close()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.wfile.write(self._html("POST!"))


def run(server_class=HTTPServer, handler_class=S, addr='', port=int(os.environ.get('PORT', '8000'))):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


class Sql:
    def __init__(self):
        self.conn = psycopg2.connect(
            'postgres://ebibkbpkmajcmc:3debdeb3e863c248bd647e707ce36209c7d1b548073dadfc963ba0c13a6687c7@ec2-63-32-30-191.eu-west-1.compute.amazonaws.com:5432/dba0k1bgq8tlgs',
            sslmode='require')
        self.cur = self.conn.cursor()


def get_class_list():
    sql = Sql()
    res = sql.cur.execute("select distinct class_number from Domino order by class_number;")
    res2 = sql.cur.fetchall()
    sql.conn.commit()
    sql.cur.close()
    sql.conn.close()
    somedict = {"classes": [x[0] for x in res2]}
    ans = json.dumps(somedict, ensure_ascii=False)
    return ans


def get_theme_list(class_number):
    sql = Sql()
    res = sql.cur.execute(f"select distinct theme from Domino where class_number = {class_number};")
    res2 = sql.cur.fetchall()
    sql.conn.commit()
    sql.cur.close()
    sql.conn.close()
    somedict = {"class_number": class_number, "themes": [x[0] for x in res2]}
    ans = json.dumps(somedict, ensure_ascii=False)
    return ans


def get_id_variant_countDominoshek_list(class_number, theme):
    sql = Sql()
    res = sql.cur.execute(
        f"select variant from Domino where class_number = {class_number} and theme like\'{theme}\';")
    res2 = sql.cur.fetchall()
    sql.conn.commit()
    sql.cur.close()
    sql.conn.close()
    somedict = {"class_number": class_number, "theme": theme, "var": [x[0] for x in res2]}
    ans = json.dumps(somedict, ensure_ascii=False)
    return ans

def get_id_Domino(class_number, theme, var):
    sql = Sql()
    res = sql.cur.execute(
        f"select id, count_dominoshek from Domino where class_number = {class_number} and theme like'{theme}' and variant = {var};")
    res2 = sql.cur.fetchone()
    sql.conn.commit()
    sql.cur.close()
    sql.conn.close()
    return res2

def get_all_Dominoshek_list(id, count_dominoshek):
    sql = Sql()
    res = sql.cur.execute(
        f"select left_side, right_side, position from Dominoshka join (select id_dominoshki, position from "
        f"Input where id_domino = {id}) S on Dominoshka.id = S.id_dominoshki;")
    res2 = sql.cur.fetchall()
    sql.conn.commit()
    sql.cur.close()
    sql.conn.close()
    somedict = {"dominoshki": [x for x in res2], "count_dominoshek": count_dominoshek}
    ans = json.dumps(somedict, ensure_ascii=False)
    return ans


if __name__ == "__main__":
    run()
