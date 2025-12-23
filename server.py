from wsgiref.simple_server import make_server
from wsgi import application

if __name__ == '__main__':
    port = 8000
    print(f"Servidor corriendo en http://localhost:{port}...")
    server = make_server('', port, application)
    server.serve_forever()
