from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2
import json
import re

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
        self._set_headers()
        ans = ''
        a = self.path[1:].isdigit()
        print(a)
        if self.path == "/":
            ans = get_class_list()
        elif self.path[1:].isdigit():
            ans = get_theme_list(int(self.path[1:]))
        print("Answer: " + ans)
        self.wfile.write(ans.encode())

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
            'postgres://xdxcqcwnkfqqie:3b3bc8ebe684cd8f4f4b96c2569a0d0b796b885faf0c6800cd3712739d7fe982@ec2-99-81-177-233.eu-west-1.compute.amazonaws.com:5432/d9coav5liftcvu',
            sslmode='require')
        self.cur = self.conn.cursor()


def get_class_list():
    sql = Sql()
    res = sql.cur.execute("select distinct class_number from Domino;")
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

def get_input_list(class_number, theme):
    sql = Sql()
    res = sql.cur.execute(f"select id, variant, count_dominoshek from Domino where class_number = {class_number} and theme like\'{theme}\';")
    res2 = sql.cur.fetchall()
    sql.conn.commit()
    sql.cur.close()
    sql.conn.close()
    somedict = {"class_number": class_number, "theme": theme, "input": [x for x in res2]}
    ans = json.dumps(somedict, ensure_ascii=False)
    return ans


if __name__ == "__main__":
    run()
