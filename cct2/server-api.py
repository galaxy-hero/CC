import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

from db import MySQLConnection


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def send_my_headers(self):
        self.send_header('Content-Type', 'application/json')

    def end_headers(self):
        self.send_my_headers()
        super().end_headers()

    def do_GET(self):
        if re.search(r'/api/v1/items/*', self.path) is not None:
            MySQLConnection.init()
            c = MySQLConnection.connector.cursor()
            c.execute("""SELECT * FROM products""")
            rows = c.fetchall()
            response_data = [{'id': row[0], 'name': row[1], 'description': row[2], 'price': int(row[3])} for row in
                             rows]

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        elif re.search(r'/api/v1/item/\d+', self.path) is not None:
            print(self.path)
            item_id = self.path.split('/')[-1]
            print(item_id)
            MySQLConnection.init()
            c = MySQLConnection.connector.cursor()
            c.execute("""SELECT * FROM products WHERE id = %s""" % item_id)
            row = c.fetchone()
            if row is None:
                self.send_response(404)
                self.end_headers()
                return
            response_data = {'id': row[0], 'name': row[1], 'description': row[2], 'price': int(row[3])}

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'{"msg":"forbidden"}')
        return

    def do_POST(self):
        if re.search(r'/api/v1/items/*', self.path) is not None:
            ctype = self.headers.get_content_type()
            if ctype == 'application/json':
                clength = int(self.headers.get('Content-Length'))
                req_data = json.loads(self.rfile.read(clength), encoding='utf-8')
                if type(req_data) != list:
                    # Bad input
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"msg":"body should be a list"}')
                    return
                values_string = ''
                for item in req_data:
                    values_string = values_string + "('%s', '%s', '%s')," % (
                        item['name'], item['description'], item['price'])
                values_string = values_string[:-1] + ';'

                MySQLConnection.init()
                mysql_conn = MySQLConnection.connector
                c = mysql_conn.cursor()
                c.execute("""INSERT INTO products (name, description, price) VALUES """ + values_string)
                mysql_conn.commit()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"msg":"items inserted"}')

            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"msg":"content-type should be application/json"}')

        elif re.search(r'/api/v1/item/*', self.path) is not None:
            ctype = self.headers.get_content_type()
            if ctype == 'application/json':
                clength = int(self.headers.get('Content-Length'))
                req_data = json.loads(self.rfile.read(clength), encoding='utf-8')
                MySQLConnection.init()
                mysql_conn = MySQLConnection.connector
                c = mysql_conn.cursor()
                c.execute("""INSERT INTO products (name, description, price) VALUES ('%s', '%s', '%s')""" % (
                    req_data['name'], req_data['description'], req_data['price']))
                mysql_conn.commit()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"msg":"item inserted"}')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"msg":"content-type should be application/json"}')
        else:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'{"msg":"forbidden"}')
        return

    def do_PUT(self):
        pass

    def do_DELETE(self):
        if re.search(r'/api/v1/items/*', self.path) is not None:
            MySQLConnection.init()
            c = MySQLConnection.connector.cursor()
            c.execute("""DELETE FROM products""")
            # MySQLConnection.connector.commit()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"msg":"deleted"}')

        elif re.search(r'/api/v1/item/\d+', self.path) is not None:
            print(self.path)
            item_id = self.path.split('/')[-1]
            print(item_id)
            MySQLConnection.init()
            c = MySQLConnection.connector.cursor()
            c.execute("""SELECT * FROM products WHERE id = %s""" % item_id)
            row = c.fetchone()
            if row is None:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"msg":"not found"}')
                return
            c.execute("""DELETE FROM products WHERE id = %s""" % item_id)
            MySQLConnection.connector.commit()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"msg":"deleted"}')
        else:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'{"msg":"forbidden"}')
        return


if __name__ == '__main__':
    server_address = ('', 8000)
    httpdd = HTTPServer(server_address, HTTPRequestHandler)
    httpdd.serve_forever()
