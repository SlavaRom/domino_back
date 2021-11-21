from http.server import HTTPServer, BaseHTTPRequestHandler
import psycopg2
import json
import os


class S(BaseHTTPRequestHandler):
    def __init__(self):
        self.sql = Sql()

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
        ans = self.sql.get_class_list()
        print("Answer: " + ans)
        self.wfile.write(self._html(ans))

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

    def get_class_list(self):
        res = self.cur.execute("select distinct class_number from Domino;")
        res2 = res.fetchall()
        self.conn.commit()
        somedict = {"classes": [x for x in res2]}
        ans = json.dumps(somedict, ensure_ascii=False)
        return ans

    def get_theme_list(self, class_number):
        sql = Sql()
        cursor = sql.conn.cursor()
        query = f"select distinct theme from Domino where class_number = {class_number};"
        res = cursor.execute(query).fetchall()
        somedict = {"class_number": class_number, "themes": [x for x in res]}
        ans = json.dumps(somedict, ensure_ascii=False)
        return ans


if __name__ == "__main__":
    run()
