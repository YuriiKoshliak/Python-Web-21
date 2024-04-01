from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote_plus
import mimetypes
from pathlib import Path
import json
import socket
import threading


class HttpGetHandler(BaseHTTPRequestHandler):
    # Обробка POST запитів
    def do_POST(self):
        # Читання даних з запиту
        data = self.rfile.read(int(self.headers.get('Content-Length')))
        # Збереження даних у JSON файл
        save_to_json(data)
        print(f"{unquote_plus(data.decode()) = }")
        # Відправка перенаправлення на головну сторінку
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        
    # Обробка GET запитів
    def do_GET(self):
        # Розбір URL запиту
        url = urlparse(self.path)
        # Відправка HTML сторінок або статичних файлів в залежності від шляху URL
        match url.path:
            case '/':
                self.send_html("index.html")
            case '/message':
                self.send_html("message.html")
            case _:
                file_path = Path(url.path[1:])
                if file_path.exists():
                    self.send_static(str(file_path))
                else:
                    self.send_html("error.html", 404)

    # Відправка статичних файлів            
    def send_static(self, static_filename):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        # print(f"{mt = }")
        if mt:
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(static_filename, 'rb') as f:
            self.wfile.write(f.read())

    # Відправка HTML сторінок
    def send_html(self, html_filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(html_filename, 'rb') as f:
            self.wfile.write(f.read())

# Функція для збереження даних у JSON файлі        
def save_to_json(raw_data, filename="storage/data.json"):
    # Декодування даних і перетворення у словник
    data = unquote_plus(raw_data.decode())
    dict_data = {key: value for key, value in [el.split("=") for el in data.split("&")]}
    # Отримання поточного часу
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    # Читання існуючого вмісту файлу або ініціалізація нового словника, якщо файл не існує або порожній
    try:
        with open(filename, "r", encoding="utf-8") as f:
            file_content = f.read().strip()
            data_json = json.loads(file_content) if file_content else {}
    except FileNotFoundError:
        data_json = {}
    # Додавання нового запису
    data_json[current_time] = dict_data
    # Запис оновленого словника назад у файл
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data_json, f, ensure_ascii=False, indent=2)

# Функція для запуску HTTP сервера
def run_http_server(server_class=HTTPServer, handler_class=HttpGetHandler, port=3000):
    server_address = ('', port)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

# Функція для запуску UDP сервера
def run_udp_server(host='', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"UDP Server listening on port {port}")
    try:
        while True:
            data, address = server_socket.recvfrom(1024)
            print(f'Connection from {address}')
            print(f'Received message: {data.decode()}')
            # Перетворення байт-рядка у словник
            message_dict = json.loads(data.decode())
            print(f'Message as dictionary: {message_dict}')
            # Збереження словника у файл JSON
            save_to_json(message_dict)
    except KeyboardInterrupt:
        server_socket.close()


if __name__ == '__main__':
    # Запуск HTTP сервера у окремому потоці
    http_thread = threading.Thread(target=run_http_server)
    http_thread.start()
    # Запуск UDP сервера у основному потоці
    run_udp_server()