import ast
import base64
import csv
import functools
import http.client
import inspect
import json
import logging
import os
import re
import smtplib
import sqlite3
import ssl
import subprocess
import sys
import time
import zipfile
from calendar import monthrange
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from functools import wraps
from http.client import HTTPSConnection
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib import request
from urllib.parse import urlparse, urlencode

ver = "2.2.5"


def cprint(data, indent=0):
    """
    Prints data with color-coding based on nested data types.

    Args:
        data (any): The data to print.
        indent (int): The indentation level.

    Returns:
        None

    İç içe veri türlerine göre renklendirme yaparak çıktı verir.

    Args:
        data (any): Yazdırılacak veri.
        indent (int): Girinti seviyesi.

    Returns:
        None
    """

    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "reset": "\033[0m"
    }

    def print_with_indent(string, indent_level):
        print(" " * 4 * indent_level + string)

    def colorize_numbers(string):
        def replace_with_color(match):
            value = match.group(0)
            if '.' in value:
                return f'{colors["yellow"]}{value}{colors["reset"]}'
            else:
                return f'{colors["blue"]}{value}{colors["reset"]}'

        return re.sub(r'\d+\.\d+|\d+', replace_with_color, string)

    if isinstance(data, str):
        print_with_indent(f'{colors["green"]}String: {colorize_numbers(data)}{colors["reset"]}', indent)
    elif isinstance(data, int):
        print_with_indent(f'{colors["blue"]}Integer: {data}{colors["reset"]}', indent)
    elif isinstance(data, float):
        print_with_indent(f'{colors["yellow"]}Float: {data}{colors["reset"]}', indent)
    elif isinstance(data, bool):
        print_with_indent(f'{colors["cyan"]}Boolean: {data}{colors["reset"]}', indent)
    elif isinstance(data, list):
        print_with_indent(f'{colors["magenta"]}List:{colors["reset"]}', indent)
        for item in data:
            cprint(item, indent + 1)
    elif isinstance(data, dict):
        print_with_indent(f'{colors["red"]}Dictionary:{colors["reset"]}', indent)
        for key, value in data.items():
            print_with_indent(f'{colors["green"]}{key}:{colors["reset"]}', indent + 1)
            cprint(value, indent + 2)
    else:
        print_with_indent(str(data), indent)


def crange(*args):
    """
    Türkçe:
    Belirtilen tekil sayıları, harfleri ve aralıkları içeren bir liste döndürür.

    Parametreler:
    *args: int, str
        - int: Tekil sayılar.
        - str: 'başlangıç-bitiş' formatında aralıklar veya virgülle ayrılmış harfler.

    Dönüş:
    List[Union[int, str]]: Belirtilen tekil sayıları, harfleri ve aralıkları içeren genişletilmiş liste.

    İngilizce:
    Returns a list containing specified individual numbers, letters, and ranges.

    Parameters:
    *args: int or str
        - int: Individual numbers.
        - str: Ranges in 'start-end' format or comma-separated letters.

    Returns:
    List[Union[int, str]]: Expanded list containing specified individual numbers, letters, and ranges.
    """
    ranges = []
    for arg in args:
        if isinstance(arg, int):
            ranges.append(arg)
        elif isinstance(arg, str):
            if '-' in arg:
                start, end = arg.split('-')
                if start.isdigit() and end.isdigit():
                    ranges.extend(range(int(start), int(end) + 1))
                else:
                    ranges.extend(chr(c) for c in range(ord(start), ord(end) + 1))
            else:
                ranges.extend(arg.split(','))
    return ranges


class CemirUtilsAMP:
    """
    A utility class for fetching HTML content, converting it to AMP format, and saving it to a file.

    HTML içeriğini getirme, AMP formatına dönüştürme ve dosyaya kaydetme için bir yardımcı sınıf.
    """

    def fetch_html(self, url):
        """
        Fetch HTML content from a given URL.

        Verilen URL'den HTML içeriğini al.

        Parameters:
        url (str): The URL to fetch the HTML content from.
                   HTML içeriğini almak için URL.

        Returns:
        str: The fetched HTML content as a string.
             Alınan HTML içeriği string olarak.

        Raises:
        Exception: If the URL cannot be fetched, raises an exception with the status code and reason.
                   URL alınamazsa, durum kodu ve nedeni ile bir istisna yükseltir.
        """
        parsed_url = urlparse(url)
        headers = {'User-Agent': 'CemirUtils'}
        conn = http.client.HTTPSConnection(parsed_url.netloc)
        conn.request("GET", parsed_url.path, headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            html_content = response.read().decode('utf-8')
            conn.close()
            return html_content
        else:
            conn.close()
            raise Exception(f"Failed to fetch URL {url}: {response.status} {response.reason}")

    def convert_to_amp(self, html_content):
        """
        Convert the given HTML content to AMP format.

        Verilen HTML içeriğini AMP formatına dönüştür.

        Parameters:
        html_content (str): The HTML content to convert.
                            Dönüştürülecek HTML içeriği.

        Returns:
        str: The converted HTML content in AMP format.
             AMP formatında dönüştürülmüş HTML içeriği.
        """
        # Add AMP HTML boilerplate
        html_content = html_content.replace('<html', '<html ⚡').replace('xmlns="http://www.w3.org/1999/xhtml"', '')

        # Add AMP specific meta tags and script
        head_close_idx = html_content.find('</head>')
        if head_close_idx != -1:
            amp_meta = '''
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
<script async src="https://cdn.ampproject.org/v0.js"></script>
<style amp-boilerplate>body{visibility:hidden} .amp {visibility:visible}</style>
<noscript><style amp-boilerplate>body{visibility:visible}</style></noscript>
'''
            html_content = html_content[:head_close_idx] + amp_meta + html_content[head_close_idx:]

        # Convert img tags to amp-img
        html_content = self.convert_img_tags(html_content)

        # Convert video tags to amp-video
        html_content = self.convert_video_tags(html_content)

        return html_content

    def convert_img_tags(self, html_content):
        """
        Convert all <img> tags in the HTML content to <amp-img> tags.

        HTML içeriğindeki tüm <img> etiketlerini <amp-img> etiketlerine dönüştür.

        Parameters:
        html_content (str): The HTML content containing <img> tags.
                            <img> etiketleri içeren HTML içeriği.

        Returns:
        str: The HTML content with <img> tags converted to <amp-img> tags.
             <img> etiketleri <amp-img> etiketlerine dönüştürülmüş HTML içeriği.
        """
        # Simple img to amp-img conversion
        img_start = html_content.find('<img')
        while img_start != -1:
            img_end = html_content.find('>', img_start)
            if img_end == -1:
                break
            img_tag = html_content[img_start:img_end + 1]
            amp_img_tag = img_tag.replace('<img', '<amp-img').replace('/>', ' layout="responsive" width="600" height="400"></amp-img>')
            html_content = html_content[:img_start] + amp_img_tag + html_content[img_end + 1:]
            img_start = html_content.find('<img', img_start + len(amp_img_tag))
        return html_content

    def convert_video_tags(self, html_content):
        """
        Convert all <video> tags in the HTML content to <amp-video> tags.

        HTML içeriğindeki tüm <video> etiketlerini <amp-video> etiketlerine dönüştür.

        Parameters:
        html_content (str): The HTML content containing <video> tags.
                            <video> etiketleri içeren HTML içeriği.

        Returns:
        str: The HTML content with <video> tags converted to <amp-video> tags.
             <video> etiketleri <amp-video> etiketlerine dönüştürülmüş HTML içeriği.
        """
        # Simple video to amp-video conversion
        video_start = html_content.find('<video')
        while video_start != -1:
            video_end = html_content.find('</video>', video_start)
            if video_end == -1:
                break
            video_tag = html_content[video_start:video_end + 8]
            amp_video_tag = video_tag.replace('<video', '<amp-video').replace('</video>', '</amp-video>').replace('>', ' layout="responsive" width="600" height="400">')
            html_content = html_content[:video_start] + amp_video_tag + html_content[video_end + 8:]
            video_start = html_content.find('<video', video_start + len(amp_video_tag))
        return html_content

    def save_to_file(self, content, filename):
        """
        Save the given content to a file with the specified filename.

        Verilen içeriği belirtilen dosya adıyla bir dosyaya kaydet.

        Parameters:
        content (str): The content to save.
                       Kaydedilecek içerik.
        filename (str): The name of the file to save the content in.
                        İçeriğin kaydedileceği dosyanın adı.
        """
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        cprint(f"Content saved to {filename}")


class CemirUtilsHTTP:

    def __init__(self):
        """
        CemirUtilsHTTP
        Initializes the CemirUtilsHTTP class with default headers.
        """

        self.default_headers = {"User-Agent": "CemirUtils"}

    def get_methods(self):
        """
        Prints the names of all available methods in the CemirUtilsHTTP class.

        CemirUtilsHTTP sınıfının mevcut tüm metodlarının isimlerini yazdırır.
        """
        return [method for method in dir(CemirUtilsHTTP) if callable(getattr(CemirUtilsHTTP, method)) and not method.startswith("__")]

    def server(self, port=8000, ip='127.0.0.1', ssl_cert=None, ssl_key=None, username=None, password=None, directory=None):
        """
        Starts an HTTP server on the specified IP and port with optional SSL and basic authentication.

        Belirtilen IP ve port üzerinde isteğe bağlı SSL ve temel kimlik doğrulama ile bir HTTP sunucusu başlatır.

        Parameters:
        port (int): The port number for the server. Default is 8000.
        ip (str): The IP address for the server. Default is '127.0.0.1'.
        ssl_cert (str): Path to the SSL certificate file.
        ssl_key (str): Path to the SSL key file.
        username (str): Username for basic authentication.
        password (str): Password for basic authentication.
        directory (str): Directory to serve files from.
        """

        class CemirUtilsHTTPRequestHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)

            def do_GET(self):
                if username and password:
                    if not self.check_basic_auth(username, password):
                        self.send_response(401)
                        self.send_header('WWW-Authenticate', 'Basic realm="CemirUtils"')
                        self.end_headers()
                        self.wfile.write(b'Unauthorized')
                        return

                super().do_GET()

            def check_basic_auth(self, username, password):
                auth_header = self.headers.get('Authorization')
                if auth_header is None:
                    return False

                auth_type, auth_value = auth_header.split(None, 1)
                if auth_type.lower() != 'basic':
                    return False

                encoded_credentials = auth_value.encode('utf-8')
                credentials = base64.b64decode(encoded_credentials).decode('utf-8')
                auth_username, auth_password = credentials.split(':', 1)

                return auth_username == username and auth_password == password

        httpd = HTTPServer((ip, port), CemirUtilsHTTPRequestHandler)

        if ssl_cert and ssl_key:
            httpd.socket = ssl.wrap_socket(httpd.socket, certfile=ssl_cert, keyfile=ssl_key, server_side=True)
            print(f"Starting HTTP server with SSL on https://{ip}:{port}")

        print(f"Starting HTTP server on http://{ip}:{port}")
        httpd.serve_forever()

    def send_request(self, url, method='GET', headers=None, data=None, destination=None):
        """
        Send an HTTP request to the given URL with the specified method, headers, and data, using the default User-Agent if not provided in headers. If destination is provided, download the file to the destination path.

        Belirtilen URL'ye belirtilen yöntem, başlıklar ve verilerle bir HTTP isteği gönderir. Başlıklarda belirtilmemişse varsayılan Kullanıcı Aracısı'nı kullanır. Hedef belirtilmişse, dosyayı hedef yola indirir.

        Parameters:
        url (str): The request URL.
        method (str): The HTTP method (GET, POST, etc.). Default is 'GET'.
        headers (dict): The request headers.
        data (bytes): The request data.
        destination (str): Path to save the response content.

        Returns:
        str: The response details in JSON format or an error message.
        """

        if headers is None or "User-Agent" not in headers:
            headers = self.default_headers.copy()
        try:
            req = request.Request(url, headers=headers or self.default_headers, method=method, data=data)
            with request.urlopen(req) as response:
                content = response.read()
                result = {
                    "url": url,
                    "method": method,
                    "headers": dict(response.headers),
                    "content": "Binary data (PDF, image, etc.)"
                }
                if destination:
                    with open(destination, 'wb') as f:
                        f.write(content)
                    result["saved_to"] = destination
                return json.dumps(result, indent=4)
        except Exception as e:
            return f"Failed to send request to {url}, error: {str(e)}"

    def get(self, url, params=None, headers=None, verify_ssl=True):
        """
        Sends a GET request.

        Bir GET isteği gönderir.

        Parameters:
        url (str): The request URL.
        params (dict): URL parameters.
        headers (dict): Request headers.
        verify_ssl (bool): SSL verification control.

        Returns:
        dict, str: JSON response or plain text.
        """
        if headers is None or "User-Agent" not in headers:
            headers = self.default_headers.copy()

        if params:
            url += '?' + urlencode(params)

        req = request.Request(url, headers=headers)
        response = request.urlopen(req, timeout=10, context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def post(self, url, data=None, headers=None, verify_ssl=True):
        """
        Sends a POST request.

        Bir POST isteği gönderir.

        Parameters:
        url (str): The request URL.
        data (dict): Data to be sent.
        headers (dict): Request headers.
        verify_ssl (bool): SSL verification control.

        Returns:
        dict, str: JSON response or plain text.
        """
        if headers is None or "User-Agent" not in headers:
            headers = self.default_headers.copy()

        if data:
            data = urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='POST')
        response = request.urlopen(req, timeout=10, context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def put(self, url, data=None, headers=None, verify_ssl=True):
        """
        Sends a PUT request.

        Bir PUT isteği gönderir.

        Parameters:
        url (str): The request URL.
        data (dict): Data to be sent.
        headers (dict): Request headers.
        verify_ssl (bool): SSL verification control.

        Returns:
        dict, str: JSON response or plain text.
        """
        if headers is None or "User-Agent" not in headers:
            headers = self.default_headers.copy()

        if data:
            data = urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='PUT')
        response = request.urlopen(req, timeout=10, context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def delete(self, url, headers=None, verify_ssl=True):
        """
        Sends a DELETE request.

        Bir DELETE isteği gönderir.

        Parameters:
        url (str): The request URL.
        headers (dict): Request headers.
        verify_ssl (bool): SSL verification control.

        Returns:
        dict, str: JSON response or plain text.
        """
        if headers is None or "User-Agent" not in headers:
            headers = self.default_headers.copy()

        req = request.Request(url, headers=headers, method='DELETE')
        response = request.urlopen(req, timeout=10, context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def patch(self, url, data=None, headers=None, verify_ssl=True):
        """
        Sends a PATCH request.

        Bir PATCH isteği gönderir.

        Parameters:
        url (str): The request URL.
        data (dict): Data to be sent.
        headers (dict): Request headers.
        verify_ssl (bool): SSL verification control.

        Returns:
        dict, str: JSON response or plain text.
        """
        if headers is None or "User-Agent" not in headers:
            headers = self.default_headers.copy()

        if data:
            data = urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='PATCH')
        response = request.urlopen(req, timeout=10, context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content


class CemirUtilsLoopTimer:
    """
    CemirUtilsLoopTimer is a utility class for measuring and reporting the execution time
    of loops within a function.

    CemirUtilsLoopTimer, bir işlev içindeki döngülerin yürütme süresini ölçmek ve raporlamak
    için kullanılan bir yardımcı sınıftır.
    """

    def __init__(self):
        """
        Initializes a new instance of CemirUtilsLoopTimer, setting up an empty list to store
        loop execution times.

        CemirUtilsLoopTimer'ın yeni bir örneğini başlatır ve döngü yürütme sürelerini depolamak
        için boş bir liste oluşturur.
        """
        self.loop_times = []

    class LoopTimerContext:
        """
        Context manager class for timing individual loops.

        Bireysel döngüleri zamanlamak için bağlam yöneticisi sınıfı.
        """

        def __init__(self, timer):
            """
            Initializes the LoopTimerContext with a reference to the parent timer.

            LoopTimerContext'i üst zamanlayıcıya bir referans ile başlatır.

            Args:
                timer (CemirUtilsLoopTimer): The parent timer instance.
            """
            self.timer = timer

        def __enter__(self):
            """
            Starts timing when entering the context.

            Bağlama girildiğinde zamanlamayı başlatır.

            Returns:
                self
            """
            self.start = time.time()
            return self

        def __exit__(self, *args):
            """
            Stops timing and records the elapsed time when exiting the context.

            Bağlamdan çıkarken zamanlamayı durdurur ve geçen süreyi kaydeder.
            """
            self.timer.loop_times.append(time.time() - self.start)

    def check_loop(self):
        """
        Returns a LoopTimerContext instance for timing a loop.

        Bir döngüyü zamanlamak için bir LoopTimerContext örneği döndürür.

        Returns:
            LoopTimerContext
        """
        return self.LoopTimerContext(self)

    def extract_loops(self, code):
        """
        Extracts loop nodes from the given code.

        Verilen koddaki döngü düğümlerini çıkarır.

        Args:
            code (str): The source code to analyze.

        Returns:
            list: A list of tuples containing loop nodes and their types.
        """
        return [(node, type(node).__name__) for node in ast.walk(ast.parse(code)) if isinstance(node, (ast.For, ast.While))]

    def loop_timer_decorator(self, func):
        """
        Decorator to measure and print the execution time of loops within a function.

        Bir işlev içindeki döngülerin yürütme süresini ölçmek ve yazdırmak için dekoratör.

        Args:
            func (function): The function to decorate.

        Returns:
            function: The wrapped function with timing logic.
        """

        def wrapper(*args, **kwargs):
            start_func_time = time.time()
            func_code = inspect.getsource(func)
            loop_nodes = self.extract_loops(func_code)
            result = func(*args, **kwargs)
            end_func_time = time.time()

            cprint("------------------")
            for i, (node, node_type) in enumerate(loop_nodes):
                cprint(f"Loop {i + 1} ({node_type} at line {node.lineno}): {self.loop_times[i]:.2f} seconds")
            cprint(f"Total execution time of '{func.__name__}': {end_func_time - start_func_time:.2f} seconds")
            cprint("------------------")

            self.loop_times.clear()
            return result

        return wrapper

    def loop(self, func):
        """
        Decorates a function to time its loops and print their execution times.

        Bir işlevi zamanlamak ve döngü yürütme sürelerini yazdırmak için süsler.

        Args:
            func (function): The function to decorate.

        Returns:
            function: The decorated function.
        """
        return self.loop_timer_decorator(func)


class CemirUtilsDecorators:
    def __init__(self):
        pass

    @staticmethod
    def webhook_request(url, headers=None):
        """
        Creates a decorator to send the result of a function to a specified webhook URL via a POST request.

        :param url: The URL of the webhook.
        :param headers: Optional headers to include in the request.
        :return: A decorator that sends the function result as a JSON payload to the specified URL.

        Belirtilen webhook URL'sine POST isteğiyle bir işlevin sonucunu göndermek için bir dekoratör oluşturur.

        :param url: Webhook'un URL'si.
        :param headers: İsteğe dahil edilecek isteğe bağlı başlıklar.
        :return: İşlev sonucunu JSON yükü olarak belirtilen URL'ye gönderen bir dekoratör.
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                parsed_url = urlparse(url)
                conn = HTTPSConnection(parsed_url.netloc)
                default_headers = {'Content-type': 'application/json'}
                if headers:
                    default_headers.update(headers)
                payload = json.dumps(func(*args, **kwargs))
                conn.request('POST', parsed_url.path, body=payload, headers=default_headers)
                response = conn.getresponse()
                response_data = response.read().decode()
                return json.loads(response_data)

            return wrapper

        return decorator

    @staticmethod
    def timeit(func):
        """
        Creates a decorator to measure the execution time of a function.

        :param func: The function to be decorated.
        :return: The decorated function with execution time measurement.

        Bir işlevin yürütme süresini ölçmek için bir dekoratör oluşturur.

        :param func: Dekore edilecek işlev.
        :return: Yürütme süresi ölçümü ile dekore edilmiş işlev.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Function '{func.__name__}' took {elapsed_time:.4f} seconds")
            return result

        return wrapper

    @staticmethod
    def log(func):
        """
        Creates a decorator to log the function call and its return value.

        :param func: The function to be decorated.
        :return: The decorated function with logging.

        İşlev çağrısını ve dönüş değerini kaydetmek için bir dekoratör oluşturur.

        :param func: Dekore edilecek işlev.
        :return: Kayıt ile dekore edilmiş işlev.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling function '{func.__name__}' with arguments {args} and keyword arguments {kwargs}")
            result = func(*args, **kwargs)
            print(f"Function '{func.__name__}' returned {result}")
            return result

        return wrapper

    @staticmethod
    def retry(retries=3, delay=1):
        """
        Creates a decorator to retry a function if it raises an exception.

        :param retries: The number of retries.
        :param delay: The delay between retries in seconds.
        :return: The decorated function with retry logic.

        Bir işlevin bir istisna yükseltmesi durumunda yeniden denemek için bir dekoratör oluşturur.

        :param retries: Yeniden deneme sayısı.
        :param delay: Yeniden denemeler arasındaki gecikme süresi (saniye cinsinden).
        :return: Yeniden deneme mantığı ile dekore edilmiş işlev.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(1, retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        print(f"Attempt {attempt} failed: {e}")
                        if attempt < retries:
                            time.sleep(delay)
                print(f"Function '{func.__name__}' failed after {retries} attempts")

            return wrapper

        return decorator

    @staticmethod
    def cache(func):
        """
        Creates a decorator to cache the result of a function call.

        :param func: The function to be decorated.
        :return: The decorated function with caching.

        Bir işlev çağrısının sonucunu önbelleğe almak için bir dekoratör oluşturur.

        :param func: Dekore edilecek işlev.
        :return: Önbellekleme ile dekore edilmiş işlev.
        """
        cache_data = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in cache_data:
                print(f"Returning cached result for {func.__name__} with args {args} and kwargs {kwargs}")
                return cache_data[key]
            result = func(*args, **kwargs)
            cache_data[key] = result
            return result

        return wrapper

    @staticmethod
    def deprecate(message):
        """
        Creates a decorator to mark a function as deprecated.

        :param message: The deprecation message.
        :return: The decorated function with a deprecation warning.

        Bir işlevi kullanımdan kaldırılmış olarak işaretlemek için bir dekoratör oluşturur.

        :param message: Kullanımdan kaldırma mesajı.
        :return: Kullanımdan kaldırma uyarısı ile dekore edilmiş işlev.
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"WARNING: {func.__name__} is deprecated. {message}")
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def debug(func):
        """
        Creates a decorator to debug a function by printing its arguments and return value.

        :param func: The function to be decorated.
        :return: The decorated function with debugging.

        Bir işlevi hata ayıklamak için, işlevin argümanlarını ve dönüş değerini yazdıran bir dekoratör oluşturur.

        :param func: Dekore edilecek işlev.
        :return: Hata ayıklama ile dekore edilmiş işlev.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"DEBUG: Calling function '{func.__name__}' with arguments {args} and keyword arguments {kwargs}")
            result = func(*args, **kwargs)
            print(f"DEBUG: Function '{func.__name__}' returned {result}")
            return result

        return wrapper

    @staticmethod
    def cache_with_expiry(expiry_time):
        """
        Creates a decorator to cache the result of a function call with an expiry time.

        :param expiry_time: The time in seconds after which the cache expires.
        :return: The decorated function with caching and expiry.

        Bir işlev çağrısının sonucunu belirli bir süre sonra sona erecek şekilde önbelleğe almak için bir dekoratör oluşturur.

        :param expiry_time: Önbelleğin sona erme süresi (saniye cinsinden).
        :return: Önbellekleme ve sona erme ile dekore edilmiş işlev.
        """
        cache_data = {}

        def decorator(func):
            def wrapper(*args, **kwargs):
                key = (args, frozenset(kwargs.items()))
                if key in cache_data:
                    if time.time() - cache_data[key]["timestamp"] < expiry_time:
                        print(f"Returning cached result for {func.__name__} with args {args} and kwargs {kwargs}")
                        return cache_data[key]["result"]
                result = func(*args, **kwargs)
                cache_data[key] = {"result": result, "timestamp": time.time()}
                return result

            return wrapper

        return decorator

    @staticmethod
    def before_after(func):
        """
        Creates a decorator to execute actions before and after a function call.

        :param func: The function to be decorated.
        :return: The decorated function with before and after actions.

        Bir işlev çağrısından önce ve sonra eylemler gerçekleştirmek için bir dekoratör oluşturur.

        :param func: Dekore edilecek işlev.
        :return: Önce ve sonra eylemler ile dekore edilmiş işlev.
        """

        def wrapper(*args, **kwargs):
            print("Starting transaction")
            result = func(*args, **kwargs)
            print("Committing transaction")
            return result

        return wrapper

    @staticmethod
    def rate_limit(max_calls, period):
        """
        Creates a decorator to limit the rate of function calls.

        :param max_calls: The maximum number of calls allowed within the period.
        :param period: The time period in seconds for the rate limit.
        :return: The decorated function with rate limiting.

        Bir işlev çağrılarının oranını sınırlamak için bir dekoratör oluşturur.

        :param max_calls: Belirli bir zaman dilimi içinde izin verilen maksimum çağrı sayısı.
        :param period: Oran sınırı için zaman dilimi (saniye cinsinden).
        :return: Oran sınırlaması ile dekore edilmiş işlev.
        """
        call_times = []

        def decorator(func):
            def wrapper(*args, **kwargs):
                nonlocal call_times
                now = time.time()
                call_times.append(now)
                call_times = [t for t in call_times if now - t < period]
                if len(call_times) > max_calls:
                    raise RuntimeError("Rate limit exceeded")
                return func(*args, **kwargs)

            return wrapper

        return decorator


class CemirUtilsFunctionNotification:
    """
    CemirUtilsFunctionNotification

    This class provides functionality to send email notifications when a function is called.

    Attributes:
        smtp_server (str): The SMTP server address.
        smtp_port (int): The SMTP server port.
        smtp_user (str): The SMTP server username.
        smtp_password (str): The SMTP server password.
        from_email (str): The email address from which notifications are sent.

    Methods:
        notify(to_email, subject): Decorator to notify when the decorated function is called.
        send_notification(to_email, subject, func_name, result): Sends an email notification with the function call details.
    """

    """
    CemirUtilsFunctionNotification

    Bu sınıf, bir işlev çağrıldığında e-posta bildirimleri göndermek için işlevsellik sağlar.

    Nitelikler:
        smtp_server (str): SMTP sunucusunun adresi.
        smtp_port (int): SMTP sunucusunun portu.
        smtp_user (str): SMTP sunucusunun kullanıcı adı.
        smtp_password (str): SMTP sunucusunun şifresi.
        from_email (str): Bildirimlerin gönderileceği e-posta adresi.

    Metotlar:
        notify(to_email, subject): Dekoratör, süslenen işlev çağrıldığında bildirimde bulunur.
        send_notification(to_email, subject, func_name, result): İşlev çağrısı detaylarıyla bir e-posta bildirimi gönderir.
    """

    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_email = smtp_user

    def notify(self, to_email, subject):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.send_notification(to_email, subject, func.__name__, result)
                return result

            return wrapper

        return decorator

    def send_notification(self, to_email, subject, func_name, result):
        try:
            body = f"The function {func_name} was called."
            body += f"\n\nReturn: {result}"
            body += f"\n\nThe subject: {subject}"
            body += f"\n\nTime: {datetime.now()}"

            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            print("Email was sent!")

        except smtplib.SMTPAuthenticationError:
            error_message = "Error: The server didn't accept the username/password combination."
            logging.error(error_message)
        except smtplib.SMTPConnectError:
            error_message = "Error: Unable to establish a connection to the email server."
            logging.error(error_message)
        except smtplib.SMTPServerDisconnected:
            error_message = "Error: Server unexpectedly disconnected."
            logging.error(error_message)
        except Exception as e:
            error_message = f"An error occurred: {e}"
            logging.error(error_message)


class CemirUtilsEmail:
    """
    CemirUtilsEmail

    This class provides methods to send emails with optional HTML content and attachments.

    Attributes:
        smtp_host (str): The SMTP host address.
        smtp_port (int): The SMTP port number.
        smtp_user (str): The SMTP username.
        smtp_pass (str): The SMTP password.
        smtp_ssl (bool): Use SSL for SMTP connection.

    Methods:
        html_to_plain(html): Converts HTML content to plain text.
        zip_attachments(attachments): Zips multiple attachment files into a single ZIP file.
        send_email(to_email, subject, body_html, attachments=None, zip_files=False): Sends an email with HTML content and optional attachments.
    """

    """
    CemirUtilsEmail

    Bu sınıf, isteğe bağlı HTML içeriği ve eklerle e-posta göndermek için yöntemler sağlar.

    Nitelikler:
        smtp_host (str): SMTP sunucusunun adresi.
        smtp_port (int): SMTP port numarası.
        smtp_user (str): SMTP kullanıcı adı.
        smtp_pass (str): SMTP şifresi.
        smtp_ssl (bool): SMTP bağlantısı için SSL kullanın.

    Metotlar:
        html_to_plain(html): HTML içeriğini düz metne dönüştürür.
        zip_attachments(attachments): Birden fazla eki tek bir ZIP dosyasında arşivler.
        send_email(to_email, subject, body_html, attachments=None, zip_files=False): HTML içeriği ve isteğe bağlı eklerle bir e-posta gönderir.
    """

    def __init__(self, smtp_host, smtp_port, smtp_user, smtp_pass, smtp_ssl=True):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.smtp_ssl = smtp_ssl

        # Set up logging
        logging.basicConfig(filename='email_errors.log', level=logging.ERROR)

    def html_to_plain(self, html):
        # Basit string işleme ile HTML'yi plain text'e çevir
        plain_text = html.replace('<br>', '\n').replace('<br/>', '\n').replace('</p>', '\n\n').replace('<p>', '').replace('<h1>', '\n\n').replace('</h1>', '\n\n')
        plain_text = plain_text.replace('<h2>', '\n\n').replace('</h2>', '\n\n').replace('<h3>', '\n\n').replace('</h3>', '\n\n')
        plain_text = plain_text.replace('<strong>', '').replace('</strong>', '').replace('<em>', '').replace('</em>', '')
        plain_text = plain_text.replace('<ul>', '\n').replace('</ul>', '').replace('<li>', '\n- ').replace('</li>', '').replace('<div>', '\n').replace('</div>', '\n')
        plain_text = plain_text.replace('<html>', '').replace('</html>', '').replace('<body>', '').replace('</body>', '')
        plain_text = plain_text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        return ''.join(plain_text.splitlines())  # Satır sonlarını temizle

    def zip_attachments(self, attachments):
        zip_filename = 'attachments.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file_path in attachments:
                if os.path.isfile(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
        return zip_filename

    def send_email(self, to_email, subject, body_html, attachments=None, zip_files=False, sender_name=None):
        try:
            # Check if all attachment files exist
            if attachments:
                missing_files = [file_path for file_path in attachments if not os.path.isfile(file_path)]
                if missing_files:
                    error_message = f"{datetime.now()}: Missing attachment files: {', '.join(missing_files)}"
                    logging.error(error_message)
                    print(error_message)
                    return  # Exit without sending the email

            # Set up the server
            if self.smtp_ssl:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context)
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()

            # Login to the server
            server.login(self.smtp_user, self.smtp_pass)

            # Create the email
            msg = MIMEMultipart('alternative')

            msg['From'] = formataddr((str(sender_name or ""), self.smtp_user))


            msg['To'] = to_email
            msg['Subject'] = subject

            # Convert HTML to plain text
            body_plain = self.html_to_plain(body_html)

            # Attach plain text and HTML parts
            part1 = MIMEText(body_plain, 'plain')
            part2 = MIMEText(body_html, 'html')
            msg.attach(part1)
            msg.attach(part2)

            # Handle attachments
            if attachments:
                if zip_files:
                    zip_filename = self.zip_attachments(attachments)
                    with open(zip_filename, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={zip_filename}',
                    )
                    msg.attach(part)
                    os.remove(zip_filename)  # Temp zip dosyasını sil
                else:
                    for file_path in attachments:
                        if os.path.isfile(file_path):
                            with open(file_path, 'rb') as f:
                                part = MIMEBase('application', 'octet-stream')
                                part.set_payload(f.read())
                                encoders.encode_base64(part)

                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={os.path.basename(file_path)}',
                            )
                            msg.attach(part)

            # Send the email
            server.sendmail(self.smtp_user, to_email, msg.as_string())

            # Close the server
            server.quit()

            print("Email sent successfully")
            return True
        except smtplib.SMTPAuthenticationError:
            error_message = "Error: The server didn't accept the username/password combination."
            logging.error(error_message)
            print(error_message)
            return False
        except smtplib.SMTPConnectError:
            error_message = "Error: Unable to establish a connection to the email server."
            logging.error(error_message)
            print(error_message)
            return False
        except smtplib.SMTPServerDisconnected:
            error_message = "Error: Server unexpectedly disconnected."
            logging.error(error_message)
            print(error_message)
            return False
        except Exception as e:
            error_message = f"An error occurred: {e}"
            logging.error(error_message)
            print(error_message)
            return False


class CemirUtilsConditions:
    """
    CemirUtilsConditions

    This class provides functionality to collect and evaluate conditions within a function.

    Attributes:
        conditions (list): A list to store conditions.

    Methods:
        condition_collector(func): A decorator to collect and evaluate conditions within the decorated function.
    """

    """
    CemirUtilsConditions

    Bu sınıf, bir işlev içindeki koşulları toplamak ve değerlendirmek için işlevsellik sağlar.

    Nitelikler:
        conditions (list): Koşulları depolamak için bir liste.

    Metotlar:
        condition_collector(func): Süslenen işlev içindeki koşulları toplamak ve değerlendirmek için bir dekoratör.
    """

    def __init__(self):
        self.conditions = []

    def condition_collector(self, func):
        def wrapper(*args, **kwargs):
            self.conditions.clear()
            source_lines, starting_line_number = inspect.getsourcelines(func)
            local_vars = {}

            def trace_function(frame, event, arg):
                if event == 'return':
                    local_vars.update(frame.f_locals)
                return trace_function

            sys.settrace(trace_function)
            result = func(*args, **kwargs)
            sys.settrace(None)

            skip_next_conditions = False

            for idx, line in enumerate(source_lines):
                stripped_line = line.strip()
                if stripped_line.startswith("if"):
                    skip_next_conditions = False  # Reset at the start of each new if block
                    condition = stripped_line.split(":")[0].strip()
                    try:
                        if eval(condition.split(" ", 1)[1], globals(), local_vars):
                            self.conditions.append((stripped_line, starting_line_number + idx))
                            skip_next_conditions = True
                    except Exception:
                        pass
                elif stripped_line.startswith("elif"):
                    if not skip_next_conditions:
                        condition = stripped_line.split(":")[0].strip()
                        try:
                            if eval(condition.split(" ", 1)[1], globals(), local_vars):
                                self.conditions.append((stripped_line, starting_line_number + idx))
                                skip_next_conditions = True
                        except Exception:
                            pass
                elif stripped_line.startswith("else"):
                    if not skip_next_conditions:
                        self.conditions.append((stripped_line, starting_line_number + idx))
                    skip_next_conditions = True

            # Print the collected conditions with line numbers
            for condition, line_num in self.conditions:
                print(f"Line {line_num}: {condition}")

            return result

        return wrapper


class Dict2Dot(dict):
    """
    A dictionary subclass that allows for dot notation access to dictionary attributes.

    Bir sözlük alt sınıfı olup, sözlük öğelerine nokta notasyonu ile erişim sağlar.

    Methods:
    ----------
    __getattr__(self, key):
        Returns the value of the given key. If the value is a dictionary, it converts it to a Dict2Dot object.
        Verilen anahtarın değerini döndürür. Eğer değer bir sözlük ise, bunu Dict2Dot nesnesine dönüştürür.
    """

    def __getattr__(self, key):
        """
        Returns the value of the given key. If the value is a dictionary, it converts it to a Dict2Dot object.

        Verilen anahtarın değerini döndürür. Eğer değer bir sözlük ise, bunu Dict2Dot nesnesine dönüştürür.

        Parameters:
        ----------
        key : str
            The key to retrieve the value for.
            Değerini almak için anahtar.

        Raises:
        ----------
        AttributeError
            If the key does not exist in the dictionary.
            Anahtar sözlükte bulunamazsa.
        """
        if key in self:
            value = self[key]
            if isinstance(value, dict):
                return Dict2Dot(value)
            return value
        else:
            raise AttributeError(f"'{self.__class__.__name__}' objesinde '{key}' anahtarı bulunamadı.")


class IPGeolocation:
    def __init__(self):
        self.database_url = "https://download.ip2location.com/lite/IP2LOCATION-LITE-DB1.CSV.ZIP"
        self.database_file = "IP2LOCATION-LITE-DB1.CSV"
        self.download_path = os.path.join(os.getcwd(), "ip_database.zip")
        self.db_file = os.path.join(os.getcwd(), "ip_geolocation.db")
        self.connection = None
        self.cursor = None

    def ip_to_int(self, ip):
        """
        Converts an IP address to an integer.

        Bir IP adresini tam sayıya dönüştürür.

        Args:
            ip (str): The IP address to convert. / Dönüştürülecek IP adresi.

        Returns:
            int: The integer representation of the IP address. / IP adresinin tam sayı temsili.
        """
        parts = ip.split('.')
        return int(parts[0]) * 256 ** 3 + int(parts[1]) * 256 ** 2 + int(parts[2]) * 256 + int(parts[3])

    def int_to_ip(self, ip_int):
        """
        Converts an integer to an IP address.

        Bir tam sayıyı IP adresine dönüştürür.

        Args:
            ip_int (int): The integer to convert. / Dönüştürülecek tam sayı.

        Returns:
            str: The IP address representation of the integer. / Tam sayının IP adresi temsili.
        """
        octet_1 = ip_int // (256 ** 3) % 256
        octet_2 = ip_int // (256 ** 2) % 256
        octet_3 = ip_int // 256 % 256
        octet_4 = ip_int % 256
        return f"{octet_1}.{octet_2}.{octet_3}.{octet_4}"

    def download_database(self, force_download=False):
        """
        Downloads the IP2Location database.

        IP2Location veritabanını indirir.

        Args:
            force_download (bool): Whether to force the download of the zip file. / Zip dosyasını yeniden indirme zorunluluğu.
        """
        try:
            if force_download or not os.path.isfile(self.database_file):
                # Download the database file
                print("Downloading the database file... / Veritabanı dosyasını indiriyor...")
                request.urlretrieve(self.database_url, self.download_path)
                print("Database file downloaded! / Veritabanı dosyası indirildi!")

                # Extract the zip file
                with zipfile.ZipFile(self.download_path, "r") as zip_ref:
                    zip_ref.extractall(os.getcwd())
        except Exception as e:
            print(f"An error occurred: {e} / Hata oluştu: {e}")

    def create_sqlite_db(self):
        """
        Creates the SQLite database and imports the CSV file into it.

        SQLite veritabanını oluşturur ve CSV dosyasını içine aktarır.
        """
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()

            print("Creating SQLite database table... / SQLite veritabanı tablosu oluşturuluyor...")
            # Create the table
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS ip_geolocation
                        (ip_start INTEGER PRIMARY KEY,
                        ip_end INTEGER,
                        country_code TEXT,
                        country_name TEXT)''')

            # Read the CSV file and import it into the database
            with open(self.database_file, "r", encoding="utf-8") as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    self.cursor.execute("INSERT INTO ip_geolocation VALUES (?, ?, ?, ?)", row)

            print("SQLite database table created! / SQLite veritabanı tablosu oluşturuldu!")

            # Commit the changes
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e} / Hata oluştu: {e}")

    def get_ip_location(self, ip_address, force_download=False):
        """
        Returns the location information for the given IP address.

        Verilen IP adresinin lokasyon bilgisini döndürür.

        Args:
            ip_address (str): The IP address to lookup. / Sorgulanacak IP adresi.
            force_download (bool): Whether to force the download of the zip file. / Zip dosyasını yeniden indirme zorunluluğu.

        Returns:
            dict: The location information for the IP address. / IP adresinin lokasyon bilgisi.
        """
        try:
            # Create the SQLite database if it does not exist or if force download is requested
            if not os.path.isfile(self.db_file) or force_download:
                self.download_database(force_download)
                self.create_sqlite_db()

            # Query the location information for the IP address
            print("Querying the location information for the IP address... / IP adresinin lokasyon bilgisini sorguluyor...")
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()

            # SQLite query
            query = "SELECT * FROM ip_geolocation WHERE ip_start <= ? AND ip_end >= ?"
            ip_int = self.ip_to_int(ip_address)
            self.cursor.execute(query, (ip_int, ip_int))
            row = self.cursor.fetchone()
            if row:
                return {"status": True, "ip_address": ip_address, "ipint": ip_int, "country_code": row[2], "country_name": row[3]}
            else:
                return {"status": False, "ip_address": ip_address}
        except Exception as e:
            print(f"An error occurred: {e} / Hata oluştu: {e}")
            return None


class CemirPostgreSQL:
    def __init__(self, dbhost, dbport, dbuser, dbpassword, dbname, timeout=10, dbcreate_db_if_not_exists=False):
        """
        Initialize the CemirPostgreSQL instance.

        Args:
            dbhost (str): Veritabanı hostu / Database host.
            dbport (int): Veritabanı portu / Database port.
            dbuser (str): Veritabanı kullanıcısı / Database user.
            dbpassword (str): Veritabanı şifresi / Database password.
            dbname (str): Veritabanı adı / Database name.
            timeout (int, optional): Sorgu zaman aşımı süresi / Query timeout. Default is 10.
            dbcreate_db_if_not_exists (bool, optional): Eğer veritabanı yoksa oluştur / Create database if not exists.
        """
        self.dbhost = dbhost
        self.dbport = dbport
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbname = dbname
        self.timeout = timeout
        self.dbcreate_db_if_not_exists = dbcreate_db_if_not_exists

        if dbcreate_db_if_not_exists:
            self.create_database(dbname)

    def get_methods(self):
        """
        CemirPostgreSQL sınıfının mevcut tüm metodlarının isimlerini yazdırır.
        Prints all available method names of the CemirPostgreSQL class.
        """
        return [method for method in dir(CemirPostgreSQL) if callable(getattr(CemirPostgreSQL, method)) and not method.startswith("__")]

    def parse_output(self, output):
        """
        psql komutunun çıktısını parse ederek dict yapısına çevirir.
        Parses the output of a psql command and converts it into a dictionary.

        Args:
            output (str): psql komutunun çıktısı / Output of the psql command.

        Returns:
            dict: Dict formatında çıktı / Output in dict format.
        """
        lines = output.strip().split('\n')
        headers = lines[0].split('|')
        data = []

        for line in lines[2:-1]:  # İlk iki satır ve son satır başlık ve ayırıcılar olduğu için atlanır / Skip first two and last line as they are headers and separators
            values = line.split('|')
            data.append({header.strip(): value.strip() for header, value in zip(headers, values)})

        return data

    def execute_query(self, query, dbname=None):
        """
        Veritabanına SQL sorgusu gönderir ve sonucu döndürür.
        Sends an SQL query to the database and returns the result.

        Args:
            query (str): SQL sorgusu / SQL query.
            dbname (str, optional): Veritabanı adı / Database name. Eğer verilmezse, self.dbname kullanılır / If not provided, self.dbname is used.

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi / Query result or error information in JSON format.
        """
        if dbname is None:
            dbname = self.dbname

        query = query.replace("\n", "").strip()
        command = f'''PGPASSWORD={self.dbpassword} psql -h {self.dbhost} -p {self.dbport} -U {self.dbuser} -d {dbname} -c {json.dumps(query, ensure_ascii=False)}'''

        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=self.timeout)
            if result.returncode != 0:
                error_info = {
                    "error": "Query failed",
                    "message": result.stderr.strip()
                }
                return json.dumps(error_info, ensure_ascii=False)
            return result.stdout.strip()
        except subprocess.TimeoutExpired as e:
            error_info = {
                "error": "TimeOut",
                "message": f"timed out"
            }
            return json.dumps(error_info, ensure_ascii=False)

    def raw(self, query, print_query=False):
        """
        Ham SQL sorgusu çalıştırır ve sonucu döndürür.
        Executes a raw SQL query and returns the result.

        Args:
            query (str): SQL sorgusu / SQL query.
            print_query (bool, optional): Sorguyu yazdır / Print the query. Default is False.

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi / Query result or error information in JSON format.
        """
        if print_query: print(query)
        return self.execute_query(query)

    def insert(self, table_name, columns, values, get_id=False):
        """
        Veritabanına yeni kayıt ekler.
        Inserts a new record into the database.

        Args:
            table_name (str): Tablo adı / Table name.
            columns (tuple): Kolon adları / Column names (örnek/example: ("id", "name", "data")).
            values (tuple): Kolon değerleri / Column values (örnek/example: (1, "John Doe", {"age": 30, "city": "Istanbul"})).
            get_id (bool): İşlem yapılan ID / Get the ID of the inserted record.

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi / Query result or error information in JSON format.
        """
        columns_str = ', '.join(columns)

        formatted_values = []
        for value in values:
            if isinstance(value, dict):
                formatted_values.append(f"'{json.dumps(value)}'::jsonb")
            else:
                formatted_values.append(f"'{value}'")

        values_str = ', '.join(formatted_values)
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"
        if get_id:
            query += f" RETURNING id;"
            try:
                result = self.execute_query(query).split()[2]
                return {"error": False, "id": int(result)}
            except ValueError:
                return self.execute_query(query)

        return self.execute_query(query)

    def create_database(self, dbname):
        """
        Belirtilen ad ile yeni bir veritabanı oluşturur.
        Creates a new database with the specified name.

        Args:
            dbname (str): Oluşturulacak veritabanının adı / Name of the database to be created.

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi / Query result or error information in JSON format.
        """
        query = f"CREATE DATABASE {dbname};"
        return self.execute_query(query, dbname='postgres')

    def create_table(self, table_name, schema):
        """
        Veritabanında tablo oluşturur.
        Creates a table in the database.

        Args:
            table_name (str): Tablo adı / Table name.
            schema (str): Tablo şeması / Table schema (örnek/example: "id SERIAL PRIMARY KEY, name VARCHAR(100), data JSONB").

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi / Query result or error information in JSON format.
        """
        query = f"CREATE TABLE {table_name} ({schema});"
        return self.execute_query(query)

    def read(self, table_name, columns='*', condition=None):
        """
        Veritabanından kayıt okur.
        Reads records from the database.

        Args:
            table_name (str): Tablo adı / Table name.
            columns (str or tuple, optional): Kolon adları / Column names. Default is '*'.
            condition (str, optional): Koşul / Condition.

        Returns:
            list or dict: Sorgu sonucu veya JSON formatında hata bilgisi / Query result or error information in JSON format.
        """
        if isinstance(columns, tuple):
            columns = ', '.join(columns)

        query = f"SELECT {columns} FROM {table_name}"

        if condition:
            query += f" WHERE {condition}"

        query += ";"

        result = self.parse_output(self.execute_query(query))

        if len(result) == 1:
            print(result[0], type(result[0]))
            return result[0]
        return result

    def update(self, table_name, updates, condition, get_id=False):
        """
        Veritabanındaki kaydı günceller.
        Updates a record in the database.

        Args:
            table_name (str): Tablo adı / Table name.
            updates (dict): Güncellemeler / Updates (örnek/example: {"name": "Jane Doe"}).
            condition (str): Koşul / Condition (örnek/example: "id = 1").
            get_id (bool): İşlem yapılan ID / Get the ID of the updated record.

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi / Query result or error information in JSON format.
        """
        update_str = ', '.join(f"{k} = '{json.dumps(v)}'" if isinstance(v, dict) else f"{k} = '{v}'" for k, v in updates.items())
        query = f"UPDATE {table_name} SET {update_str} WHERE {condition}"
        if get_id:
            query += f" RETURNING id;"
            try:
                result = self.execute_query(query).split()[2]
                return {"error": False, "id": int(result)}
            except ValueError:
                return self.execute_query(query)

        return self.execute_query(query)

    def delete(self, table_name, condition):
        """
        Veritabanındaki kaydı siler.
        Deletes a record from the database.

        Args:
            table_name (str): Tablo adı / Table name.
            condition (str): Koşul / Condition (örnek/example: "id = 1").

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi / Query result or error information in JSON format.
        """
        query = f"DELETE FROM {table_name} WHERE {condition};"
        try:
            result = int(self.execute_query(query).split()[1])
            if result == 0:
                return {"error": True, "status": "record_not_found"}
            if result > 0:
                return {"error": False, "status": "record_deleted"}
        except:
            return self.execute_query(query)


class CemirUtils:

    def __init__(self, data=None):
        """
        CemirUtils sınıfının yapıcı fonksiyonu. Verilen veriyi sınıfın 'data' değişkenine atar.

        Constructor function for the CemirUtils class. Assigns the given data to the class 'data' variable.

        Parametre/Parameter:
        data (list, dict): İşlenecek sayısal veri listesi veya sözlük. / List or dictionary of numerical data to be processed.
        """
        self.data = data
        self.default_headers = {"User-Agent": "CemirUtils"}

    def get_methods(self):
        """
        CemirUtils sınıfının mevcut tüm metodlarının isimlerini döner.

        Returns the names of all current methods of the CemirUtils class.
        """
        return [method for method in dir(CemirUtils) if callable(getattr(CemirUtils, method)) and not method.startswith("__")]

    def linux_ls(self, path="."):
        """
        Verilen yoldaki dosya ve dizinleri listeler.

        Lists files and directories in the given path.

        Parametre/Parameter:
        path (str): Dosya yolu. / Path to list files and directories from.
        """
        return subprocess.run(["ls", "-l", path], capture_output=True, text=True).stdout

    def linux_cat(self, filename):
        """
        Bir dosyanın içeriğini gösterir.

        Displays the contents of a file.

        Parametre/Parameter:
        filename (str): Dosya adı. / Name of the file.
        """
        return subprocess.run(["cat", filename], capture_output=True, text=True).stdout

    def linux_touch(self, filename):
        """
        Boş bir dosya oluşturur veya dosyanın erişim ve değiştirme zamanlarını günceller.

        Creates an empty file or updates the access and modification times of a file.

        Parametre/Parameter:
        filename (str): Dosya adı. / Name of the file.
        """
        return subprocess.run(["touch", filename], capture_output=True, text=True).stdout

    def linux_cp(self, source, destination):
        """
        Dosya veya dizinleri kaynaktan hedefe kopyalar.

        Copies files or directories from source to destination.

        Parametreler/Parameters:
        source (str): Kaynak dosya veya dizin. / Source file or directory.
        destination (str): Hedef dosya veya dizin. / Destination file or directory.
        """
        return subprocess.run(["cp", "-r", source, destination], capture_output=True, text=True).stdout

    def linux_mv(self, source, destination):
        """
        Dosya veya dizinleri kaynaktan hedefe taşır veya yeniden adlandırır.

        Moves or renames files or directories from source to destination.

        Parametreler/Parameters:
        source (str): Kaynak dosya veya dizin. / Source file or directory.
        destination (str): Hedef dosya veya dizin. / Destination file or directory.
        """
        return subprocess.run(["mv", source, destination], capture_output=True, text=True).stdout

    def linux_rm(self, path):
        """
        Dosya veya dizinleri siler.

        Removes files or directories.

        Parametre/Parameter:
        path (str): Silinecek dosya veya dizin. / File or directory to remove.
        """
        return subprocess.run(["rm", "-r", path], capture_output=True, text=True).stdout

    def linux_mkdir(self, directory):
        """
        Yeni bir dizin oluşturur.

        Creates a new directory.

        Parametre/Parameter:
        directory (str): Oluşturulacak dizin. / Directory to create.
        """
        return subprocess.run(["mkdir", directory], capture_output=True, text=True).stdout

    def linux_rmdir(self, directory):
        """
        Boş bir dizini kaldırır.

        Removes an empty directory.

        Parametre/Parameter:
        directory (str): Kaldırılacak dizin. / Directory to remove.
        """
        return subprocess.run(["rmdir", directory], capture_output=True, text=True).stdout

    def linux_cut(self, delimiter, fields, filename):
        """
        Bir dosyadan belirli bir ayraç ve alanlara göre veri çıkarır.

        Extracts fields from a file based on a delimiter.

        Parametreler/Parameters:
        delimiter (str): Ayraç karakteri. / Delimiter character.
        fields (str): Çıkarılacak alanlar. / Fields to extract.
        filename (str): Dosya adı. / Name of the file.
        """
        return subprocess.run(["cut", f"-d{delimiter}", f"-f{fields}", filename], capture_output=True, text=True).stdout

    def linux_gzip(self, filename):
        """
        gzip kullanarak dosyaları sıkıştırır veya açar.

        Compresses or decompresses files using gzip.

        Parametre/Parameter:
        filename (str): Dosya adı. / Name of the file.
        """
        return subprocess.run(["gzip", filename], capture_output=True, text=True).stdout

    def linux_find(self, path, filename):
        """
        Bir dizin hiyerarşisinde dosya arar.

        Searches for files in a directory hierarchy.

        Parametreler/Parameters:
        path (str): Arama yapılacak yol. / Path to search.
        filename (str): Aranacak dosya adı. / Name of the file to search for.
        """
        return subprocess.run(["find", path, "-name", filename], capture_output=True, text=True).stdout

    def linux_grep(self, pattern, filename):
        """
        Bir dosyada belirli bir deseni arar.

        Searches for a pattern in a file.

        Parametreler/Parameters:
        pattern (str): Aranacak desen. / Pattern to search for.
        filename (str): Dosya adı. / Name of the file.
        """
        return subprocess.run(["grep", pattern, filename], capture_output=True, text=True).stdout

    def time_days_between_dates(self, date1, date2):
        """
        İki tarih arasındaki gün sayısını hesaplar.

        Calculates the number of days between two dates.

        Parametreler/Parameters:
        date1 (str): İlk tarih (YYYY-MM-DD formatında). / First date (in YYYY-MM-DD format).
        date2 (str): İkinci tarih (YYYY-MM-DD formatında). / Second date (in YYYY-MM-DD format).

        Dönüş/Returns:
        int: İki tarih arasındaki gün sayısı. / Number of days between two dates.
        """
        date_format = "%Y-%m-%d"
        d1 = datetime.strptime(date1, date_format)
        d2 = datetime.strptime(date2, date_format)
        delta = d2 - d1
        return delta.days

    def time_hours_minutes_seconds_between_times(self, time1, time2):
        """
        İki zaman arasındaki saat, dakika ve saniye farkını hesaplar.

        Calculates the difference in hours, minutes, and seconds between two times.

        Parametreler/Parameters:
        time1 (str): İlk zaman (HH:MM:SS formatında). / First time (in HH:MM:SS format).
        time2 (str): İkinci zaman (HH:MM:SS formatında). / Second time (in HH:MM:SS format).

        Dönüş/Returns:
        tuple: Saat, dakika ve saniye farkı. / Difference in hours, minutes, and seconds.
        """
        time_format = "%H:%M:%S"
        t1 = datetime.strptime(time1, time_format)
        t2 = datetime.strptime(time2, time_format)
        delta = t2 - t1
        total_seconds = delta.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return int(hours), int(minutes), int(seconds)

    def time_until_date(self, future_date):
        """
        Belirli bir tarihe kadar kalan yıl, ay, gün, saat, dakika ve saniye hesaplar.

        Calculates the remaining years, months, days, hours, minutes, and seconds until a specific date.

        Parametre/Parameter:
        future_date (str): Gelecek tarih (YYYY-MM-DD HH:MM:SS formatında). / Future date (in YYYY-MM-DD HH:MM:SS format).

        Dönüş/Returns:
        tuple: Kalan gün, saat, dakika ve saniye. / Remaining days, hours, minutes, and seconds.
        """
        date_format = "%Y-%m-%d %H:%M:%S"
        now = datetime.now()
        future = datetime.strptime(future_date, date_format)
        delta = future - now
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return days, hours, minutes, seconds

    def time_add_days_to_date(self, date, days):
        """
        Belirtilen tarihe gün sayısı ekleyerek yeni bir tarih hesaplar.

        Calculates a new date by adding a specified number of days to the given date.

        Parametreler/Parameters:
        date (str): Başlangıç tarihi (YYYY-MM-DD formatında). / Starting date (in YYYY-MM-DD format).
        days (int): Eklenecek gün sayısı. / Number of days to add.

        Dönüş/Returns:
        datetime: Yeni tarih. / New date.
        """
        date_format = "%Y-%m-%d"
        d = datetime.strptime(date, date_format)
        new_date = d + timedelta(days=days)
        return new_date

    def time_add_days_and_format(self, date, days):
        """
        Belirtilen tarihe gün sayısı ekleyip yeni tarihi istenilen dilde gün adı ile birlikte formatlar.

        Adds a specified number of days to the given date and formats the new date with the day name in the desired language.

        Parametreler/Parameters:
        date (str): Başlangıç tarihi (YYYY-MM-DD formatında). / Starting date (in YYYY-MM-DD format).
        days (int): Eklenecek gün sayısı. / Number of days to add.

        Dönüş/Returns:
        str: Formatlanmış yeni tarih ve gün adı. / Formatted new date with day name.
        """
        new_date = self.time_add_days_to_date(date, days)
        formatted_date = new_date.strftime("%Y-%m-%d")
        return f"{formatted_date} ({new_date})"

    def time_is_weekend(self, date):
        """
        Bir tarihin hafta sonu olup olmadığını kontrol eder.

        Checks if a date is a weekend.

        Parametre/Parameter:
        date (str): Tarih (YYYY-MM-DD formatında). / Date (in YYYY-MM-DD format).

        Dönüş/Returns:
        bool: Hafta sonu ise True, değilse False. / True if it is a weekend, False otherwise.
        """
        date_format = "%Y-%m-%d"
        d = datetime.strptime(date, date_format)
        return d.weekday() >= 5  # 5 = Cumartesi, 6 = Pazar

    def time_is_leap_year(self, year):
        """
        Bir yılın artık yıl olup olmadığını kontrol eder.

        Checks if a year is a leap year.

        Parametre/Parameter:
        year (int): Yıl. / Year.

        Dönüş/Returns:
        bool: Artık yıl ise True, değilse False. / True if it is a leap year, False otherwise.
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def time_days_in_month(self, year, month):
        """
        Bir ay içindeki gün sayısını döndürür.

        Returns the number of days in a month.

        Parametreler/Parameters:
        year (int): Yıl. / Year.
        month (int): Ay. / Month.

        Dönüş/Returns:
        int: Ay içindeki gün sayısı. / Number of days in the month.
        """
        return monthrange(year, month)[1]

    def time_next_weekday(self, date, weekday):
        """
        Bir tarihten sonraki belirli bir günün tarihini döndürür (örneğin, bir sonraki Pazartesi).

        Returns the date of the next specified weekday (e.g., the next Monday) after a given date.

        Parametreler/Parameters:
        date (str): Başlangıç tarihi (YYYY-MM-DD formatında). / Starting date (in YYYY-MM-DD format).
        weekday (int): Hedef gün (0 = Pazartesi, 1 = Salı, vb.). / Target weekday (0 = Monday, 1 = Tuesday, etc.).

        Dönüş/Returns:
        datetime: Bir sonraki hedef günün tarihi. / Date of the next target weekday.
        """
        date_format = "%Y-%m-%d"
        d = datetime.strptime(date, date_format)
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Hedef gün zaten bu hafta geçmiş / Target day already passed this week
            days_ahead += 7
        return d + timedelta(days=days_ahead)

    @staticmethod
    def time_to_datetime(date):
        """
        Bir tarihi datetime türüne çevirir.

        Converts a date to datetime type.

        Parametre/Parameter:
        date (str): Tarih (YYYY-MM-DD formatında). / Date (in YYYY-MM-DD format).

        Dönüş/Returns:
        datetime: Tarih. / Date as datetime.
        """
        return datetime.strptime(date, "%Y-%m-%d")

    def time_since(self, past_date):
        """
        Belirli bir tarihten geçen yıl, ay, gün, saat, dakika ve saniyeyi hesaplar.

        Calculates the years, months, days, hours, minutes, and seconds since a specific date.

        Parametre/Parameter:
        past_date (str): Geçmiş tarih (YYYY-MM-DD HH:MM:SS formatında). / Past date (in YYYY-MM-DD HH:MM:SS format).

        Dönüş/Returns:
        dict: Geçen yıl, ay, gün, saat, dakika ve saniyeleri içeren sözlük. / Dictionary containing elapsed years, months, days, hours, minutes, and seconds.
        """
        past_date = datetime.strptime(past_date, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        delta = now - past_date

        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        seconds = delta.seconds % 60

        return {
            'years': years,
            'months': months,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }

    def time_business_days_between_dates(self, date1, date2):
        """
        İki tarih arasındaki iş günü sayısını hesaplar.

        Calculates the number of business days between two dates.

        Parametreler/Parameters:
        date1 (str): İlk tarih (YYYY-MM-DD formatında). / First date (in YYYY-MM-DD format).
        date2 (str): İkinci tarih (YYYY-MM-DD formatında). / Second date (in YYYY-MM-DD format).

        Dönüş/Returns:
        int: İki tarih arasındaki iş günü sayısı. / Number of business days between the two dates.
        """
        date_format = "%Y-%m-%d"
        d1 = datetime.strptime(date1, date_format)
        d2 = datetime.strptime(date2, date_format)
        day_generator = (d1 + timedelta(x) for x in range((d2 - d1).days + 1))
        business_days = sum(1 for day in day_generator if day.weekday() < 5)
        return business_days

    def str_replace_multiple(self, text, replacements):
        """
        Verilen metinde çoklu değiştirme işlemi yapar.

        Performs multiple replacements in the given text.

        Parametreler/Parameters:
        text (str): Değiştirilecek metin. / Text to be replaced.
        replacements (dict): Değiştirilecek değer çiftleri (anahtar: eski değer, değer: yeni değer). / Pairs of values to replace (key: old value, value: new value).

        Dönüş/Returns:
        str: Değiştirilmiş metin. / Replaced text.
        """
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def str_replace_with_last(self, text, values):
        """
        Verilen metinde belirtilen tüm değerleri son değer ile değiştirir.

        Replaces all specified values in the given text with the last value.

        Parametreler/Parameters:
        text (str): Değiştirilecek metin. / Text to be replaced.
        values (tuple): Değiştirilecek değerler. / Values to replace.

        Dönüş/Returns:
        str: Değiştirilmiş metin. / Replaced text.
        """
        if not values:
            return text
        last_value = values[-1]
        for value in values[:-1]:
            text = text.replace(value, last_value)
        return text

    def list_multiply_by_scalar(self, scalar):
        """
        Veri listesindeki her bir elemanı verilen skaler değer ile çarpar.

        Multiplies each element in the data list by the given scalar value.

        Parametre/Parameter:
        scalar (int, float): Çarpılacak skaler değer. / Scalar value to multiply.

        Dönüş/Returns:
        list: Skaler değer ile çarpılmış veri listesi. / Data list multiplied by scalar value.
        """
        if isinstance(self.data, list):
            return [x * scalar for x in self.data]
        else:
            raise TypeError("Veri tipi liste olmalıdır. / Data type must be a list.")

    def list_get_frequency(self, value):
        """
        Verilen değerin veri listesinde kaç kez geçtiğini sayar.

        Counts how many times the given value appears in the data list.

        Parametre/Parameter:
        value: Sayılacak değer. / Value to count.

        Dönüş/Returns:
        int: Değerin listede kaç kez geçtiği. / Number of times the value appears in the list.
        """
        if isinstance(self.data, list):
            return self.data.count(value)
        else:
            raise TypeError("Veri tipi liste olmalıdır. / Data type must be a list.")

    def list_reverse(self):
        """
        Veri listesini tersine çevirir.

        Reverses the data list.

        Dönüş/Returns:
        list: Tersine çevrilmiş veri listesi. / Reversed data list.
        """
        if isinstance(self.data, list):
            return self.data[::-1]
        else:
            raise TypeError("Veri tipi liste olmalıdır. / Data type must be a list.")

    def list_get_max_value(self):
        """
        Veri listesindeki en büyük değeri döner.

        Returns the maximum value in the data list.

        Dönüş/Returns:
        int, float: Veri listesindeki en büyük değer. / Maximum value in the data list.
        """
        if isinstance(self.data, list):
            return max(self.data)
        else:
            raise TypeError("Veri tipi liste olmalıdır. / Data type must be a list.")

    def list_get_min_value(self):
        """
        Veri listesindeki en küçük değeri döner.

        Returns the minimum value in the data list.

        Dönüş/Returns:
        int, float: Veri listesindeki en küçük değer. / Minimum value in the data list.
        """
        if isinstance(self.data, list):
            return min(self.data)
        else:
            raise TypeError("Veri tipi liste olmalıdır. / Data type must be a list.")

    def dict_filter_by_key(self, key):
        """
        Sözlükte veya sözlüklerin bulunduğu listede belirtilen anahtara sahip elemanları filtreler.

        Filters elements in the dictionary or list of dictionaries by the specified key.

        Parametre/Parameter:
        key: Filtreleme yapılacak anahtar. / Key to filter by.

        Dönüş/Returns:
        dict, list: Filtrelenmiş veri. / Filtered data.
        """
        if isinstance(self.data, dict):
            return {k: v for k, v in self.data.items() if k == key}
        elif isinstance(self.data, list):
            return [item for item in self.data if isinstance(item, dict) and key in item]
        else:
            raise TypeError("Veri tipi sözlük veya sözlük listesi olmalıdır. / Data type must be a dictionary or list of dictionaries.")

    def dict_get_keys(self):
        """
        Sözlükteki veya sözlüklerin bulunduğu listedeki anahtarları döner.

        Returns the keys in the dictionary or list of dictionaries.

        Dönüş/Returns:
        list: Anahtarlar listesi. / List of keys.
        """
        if isinstance(self.data, dict):
            return list(self.data.keys())
        elif isinstance(self.data, list):
            return [key for item in self.data if isinstance(item, dict) for key in item.keys()]
        else:
            raise TypeError("Veri tipi sözlük veya sözlük listesi olmalıdır. / Data type must be a dictionary or list of dictionaries.")

    def dict_merge(self, *dicts):
        """
        Verilen sözlükleri birleştirir.

        Merges the given dictionaries.

        Parametreler/Parameters:
        *dicts (dict): Birleştirilecek sözlükler. / Dictionaries to merge.

        Dönüş/Returns:
        dict: Birleştirilmiş sözlük. / Merged dictionary.
        """
        if all(isinstance(d, dict) for d in dicts):
            merged = {}
            for d in dicts:
                merged.update(d)
            return merged
        else:
            raise TypeError("Tüm parametreler sözlük olmalıdır. / All parameters must be dictionaries.")

    def list_filter_greater_than(self, threshold):
        """
        Belirtilen eşik değerinden büyük olan öğeleri filtreler.

        Filters elements greater than the specified threshold.

        Parametre/Parameter:
        threshold (int/float): Eşik değer. / Threshold value.

        Dönüş/Returns:
        list: Eşik değerinden büyük olan öğeleri içeren liste. / List of elements greater than the threshold.
        """
        return [x for x in self.data if x > threshold]

    def list_filter_less_than(self, threshold):
        """
        Belirtilen eşik değerinden küçük olan öğeleri filtreler.

        Filters elements less than the specified threshold.

        Parametre/Parameter:
        threshold (int/float): Eşik değer. / Threshold value.

        Dönüş/Returns:
        list: Eşik değerinden küçük olan öğeleri içeren liste. / List of elements less than the threshold.
        """
        return [x for x in self.data if x < threshold]

    def list_flatten(self):
        """
        Çok katmanlı listeyi tek katmana indirger.

        Flattens a multi-layered list into a single layer.

        Dönüş/Returns:
        list: Tek katmanlı liste. / Single-layered list.
        """
        if isinstance(self.data, list) and all(isinstance(i, list) for i in self.data):
            return [item for sublist in self.data for item in sublist]
        else:
            raise TypeError("Veri tipi çok katmanlı liste olmalıdır. / Data type must be a multi-layered list.")

    def list_sum_values(self):
        """
        Listedeki tüm sayısal değerlerin toplamını hesaplar.

        Calculates the sum of all numerical values in the list.

        Dönüş/Returns:
        int/float: Listedeki sayısal değerlerin toplamı. / Sum of numerical values in the list.
        """
        return sum(self.data)

    def list_average(self):
        """
        Listedeki sayısal değerlerin ortalamasını hesaplar.

        Calculates the average of numerical values in the list.

        Dönüş/Returns:
        float: Listedeki sayısal değerlerin ortalaması. Liste boşsa 0 döner. / Average of numerical values in the list. Returns 0 if the list is empty.
        """
        return sum(self.data) / len(self.data) if self.data else 0

    def list_head(self, n=5):
        """
        Listenin ilk n elemanını döndürür.

        Returns the first n elements of the list.

        Parametre/Parameter:
        n (int): Döndürülecek eleman sayısı (varsayılan 5). / Number of elements to return (default is 5).

        Dönüş/Returns:
        list: İlk n eleman. / First n elements.
        """
        return self.data[:n]

    def list_tail(self, n=5):
        """
        Listenin son n elemanını döndürür.

        Returns the last n elements of the list.

        Parametre/Parameter:
        n (int): Döndürülecek eleman sayısı (varsayılan 5). / Number of elements to return (default is 5).

        Dönüş/Returns:
        list: Son n eleman. / Last n elements.
        """
        return self.data[-n:]

    def list_main(self, n=5):
        """
        Listenin ortadaki elemanlarını döndürür. Eğer listenin uzunluğu 2n veya daha küçükse tüm listeyi döndürür.

        Returns the middle elements of the list. If the list length is 2n or less, returns the entire list.

        Parametre/Parameter:
        n (int): Kenarlardan kesilecek eleman sayısı (varsayılan 5). / Number of elements to trim from the edges (default is 5).

        Dönüş/Returns:
        list: Ortadaki elemanlar. / Middle elements.
        """
        if len(self.data) <= 2 * n:
            return self.data
        return self.data[n:-n]

    def list_unique_values(self):
        """
        Listenin benzersiz elemanlarını döndürür.

        Returns the unique elements of the list.

        Dönüş/Returns:
        list: Benzersiz elemanlar. / Unique elements.
        """
        return list(set(self.data))

    def list_sort_asc(self):
        """
        Listeyi artan sırada sıralar.

        Sorts the list in ascending order.

        Dönüş/Returns:
        list: Artan sırada sıralanmış liste. / List sorted in ascending order.
        """
        return sorted(self.data)

    def list_sort_desc(self):
        """
        Listeyi azalan sırada sıralar.

        Sorts the list in descending order.

        Dönüş/Returns:
        list: Azalan sırada sıralanmış liste. / List sorted in descending order.
        """
        return sorted(self.data, reverse=True)
