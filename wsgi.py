import os
import mimetypes
import re
import uuid
from urllib.parse import parse_qs
from http.cookies import SimpleCookie
import DB

# Almacenamiento de sesiones en memoria
SESSIONS = {}

def get_session(environ):
    cookie_header = environ.get('HTTP_COOKIE')
    if not cookie_header:
        return None
    cookie = SimpleCookie(cookie_header)
    if 'session_id' in cookie:
        session_id = cookie['session_id'].value
        return SESSIONS.get(session_id)
    return None

def create_session(user_data):
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = user_data
    return session_id

def destroy_session(environ):
    cookie_header = environ.get('HTTP_COOKIE')
    if cookie_header:
        cookie = SimpleCookie(cookie_header)
        if 'session_id' in cookie:
            session_id = cookie['session_id'].value
            if session_id in SESSIONS:
                del SESSIONS[session_id]

def replace_header_buttons(html_content, logged_in):
    if not logged_in:
        return html_content

    logout_btn = '<button><a href="/logout">Cerrar Sesión</a></button>'

    # Patrón 1: Enlaces relativos (como en index.html)
    p1 = re.compile(r'<button><a href="static/Paginas/inicio_sesion\.html">Iniciar Sesión</a></button>\s*<button><a href="static/Paginas/registrar\.html">Registrarse</a></button>', re.DOTALL)

    # Patrón 2: Enlaces directos (como en archivos dentro de static/Paginas/)
    p2 = re.compile(r'<button><a href="inicio_sesion\.html">Iniciar Sesión</a></button>\s*<button><a href="registrar\.html">Registrarse</a></button>', re.DOTALL)

    if p1.search(html_content):
        return p1.sub(logout_btn, html_content)
    elif p2.search(html_content):
        return p2.sub(logout_btn, html_content)

    return html_content

def serve_file(environ, start_response, filepath, content_type=None):
    try:
        # Asegurar que no se salga del directorio actual
        if '..' in filepath:
             start_response('403 Forbidden', [('Content-Type', 'text/plain')])
             return [b'Forbidden']

        with open(filepath, 'rb') as f:
            content = f.read()

        # Si es HTML, intentar modificar los botones dinámicamente
        if filepath.endswith('.html'):
            user = get_session(environ)
            logged_in = user is not None
            try:
                content_str = content.decode('utf-8')
                content_str = replace_header_buttons(content_str, logged_in)
                content = content_str.encode('utf-8')
                if not content_type:
                    content_type = 'text/html; charset=utf-8'
            except UnicodeDecodeError:
                # Si falla la decodificación, servir tal cual (ej. imágenes)
                pass

        if not content_type:
            content_type, _ = mimetypes.guess_type(filepath)

        if not content_type:
            content_type = 'application/octet-stream'

        start_response('200 OK', [('Content-Type', content_type), ('Content-Length', str(len(content)))])
        return [content]
    except FileNotFoundError:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')

    # Ruta raiz
    if path == '/' or path == '/index.html':
        return serve_file(environ, start_response, 'index.html', 'text/html; charset=utf-8')

    # Ruta Logout
    if path == '/logout':
        destroy_session(environ)
        # Redirigir al inicio y borrar cookie (opcionalmente expirar, pero destruir sesión en servidor basta)
        start_response('302 Found', [('Location', '/')])
        return [b'']

    # Archivos estáticos
    if path.startswith('/static/'):
        filepath = path.lstrip('/') # Remover slash inicial

        # Manejo de POST para Login y Registro
        # Como los formularios tienen action="#", el navegador envía POST a la misma URL del archivo
        if method == 'POST':
            try:
                content_length = int(environ.get('CONTENT_LENGTH', 0))
            except ValueError:
                content_length = 0

            body = environ['wsgi.input'].read(content_length).decode('utf-8')
            post_data = parse_qs(body)

            def get_val(key):
                return post_data.get(key, [''])[0]

            # Registro
            if path.endswith('registrar.html'):
                nombre = get_val('nombre')
                gmail = get_val('correo')
                contrasenia = get_val('contraseña')

                # Checkbox
                recibir = 'correos_recibidos' in post_data

                if DB.crear_usuario(gmail, nombre, contrasenia, recibir):
                    # Login automático
                    session_id = create_session({'gmail': gmail, 'nombre': nombre})
                    cookie = SimpleCookie()
                    cookie['session_id'] = session_id
                    cookie['session_id']['path'] = '/'

                    headers = [('Location', '/'), ('Set-Cookie', cookie.output(header='').strip())]
                    start_response('302 Found', headers)
                    return [b'']
                else:
                    # Error al crear (podría ser duplicado).
                    # Por simplicidad recargamos la página (idealmente mostrar error)
                    pass

            # Login
            elif path.endswith('inicio_sesion.html'):
                gmail = get_val('correo')
                contrasenia = get_val('contraseña')

                user = DB.validar_usuario(gmail, contrasenia)
                if user:
                    session_id = create_session(user)
                    cookie = SimpleCookie()
                    cookie['session_id'] = session_id
                    cookie['session_id']['path'] = '/'

                    headers = [('Location', '/'), ('Set-Cookie', cookie.output(header='').strip())]
                    start_response('302 Found', headers)
                    return [b'']
                else:
                    # Credenciales inválidas
                    pass

        # Si es GET o POST fallido, servir el archivo
        return serve_file(environ, start_response, filepath)

    # 404
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'Not Found']
