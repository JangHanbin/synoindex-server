import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


config = {
    'bindAddr': 'localhost',
    'bindPort': 50000
}


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        query = urlparse(self.path).query
        query_components = parse_qs(query)

        if "args" in query_components:

            args = query_components.get('args')
            path = query_components.get('path')

            if args and path:
                msg = indexing(args[0], path[0])
            else:
                msg = 'Usage : {0}?args=[options: -a -A -R -D ...]&path=[file-path]'.format(self.address_string()+self.path)
        else:
            msg = 'Synoindex response OK to clients!'

        self.send_response(200)
        self.end_headers()
        self.wfile.write(msg.encode())

        return


def indexing(args, path):
    msg = 'Synoindex %s %s' % (str(args), str(path))
    pname = '/usr/syno/bin/synoindex'
    if os.path.isfile(pname):
        try:
            cmd = [pname, args, path.encode('utf-8')]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
        except Exception as e:
            msg = 'Exception:%s' % e
    else:
        msg = 'Synoindex is not exist'
    return msg


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = (config['bindAddr'], config['bindPort'])
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print('Stopping httpd...')