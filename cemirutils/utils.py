import base64
import csv
import functools
import inspect
import json
import logging
import os
import smtplib
import sqlite3
import ssl
import subprocess
import sys
import time
import urllib.request
import zipfile
from calendar import monthrange
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib import request, parse

ver = "1.1.2"


class CemirUtilsDecorators:
    @staticmethod
    def timeit(func):
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
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling function '{func.__name__}' with arguments {args} and keyword arguments {kwargs}")
            result = func(*args, **kwargs)
            print(f"Function '{func.__name__}' returned {result}")
            return result

        return wrapper

    @staticmethod
    def retry(retries=3, delay=1):
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
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"WARNING: {func.__name__} is deprecated. {message}")
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def debug(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"DEBUG: Calling function '{func.__name__}' with arguments {args} and keyword arguments {kwargs}")
            result = func(*args, **kwargs)
            print(f"DEBUG: Function '{func.__name__}' returned {result}")
            return result
        return wrapper

    @staticmethod
    def cache_with_expiry(expiry_time):
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
        def wrapper(*args, **kwargs):
            print("Starting transaction")
            result = func(*args, **kwargs)
            print("Committing transaction")
            return result
        return wrapper

class CemirUtilsEmail:
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

    def send_email(self, to_email, subject, body_html, attachments=None, zip_files=False):
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
            msg['From'] = self.smtp_user
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
        except smtplib.SMTPAuthenticationError:
            error_message = "Error: The server didn't accept the username/password combination."
            logging.error(error_message)
            print(error_message)
        except smtplib.SMTPConnectError:
            error_message = "Error: Unable to establish a connection to the email server."
            logging.error(error_message)
            print(error_message)
        except smtplib.SMTPServerDisconnected:
            error_message = "Error: Server unexpectedly disconnected."
            logging.error(error_message)
            print(error_message)
        except Exception as e:
            error_message = f"An error occurred: {e}"
            logging.error(error_message)
            print(error_message)


class CemirUtilsConditions:
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
    def __getattr__(self, key):
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
        parts = ip.split('.')
        return int(parts[0]) * 256 ** 3 + int(parts[1]) * 256 ** 2 + int(parts[2]) * 256 + int(parts[3])

    def int_to_ip(self, ip_int):
        octet_1 = ip_int // (256 ** 3) % 256
        octet_2 = ip_int // (256 ** 2) % 256
        octet_3 = ip_int // 256 % 256
        octet_4 = ip_int % 256
        return f"{octet_1}.{octet_2}.{octet_3}.{octet_4}"

    def download_database(self, force_download=False):
        """
        IP2Location veritabanını indirir.

        Args:
            force_download (bool): Zip dosyasını yeniden indirme zorunluluğu.
        """
        try:
            if force_download or not os.path.isfile(self.database_file):
                # Veritabanı dosyasını indir
                print("Veritabanı dosyasını indiriyor...")
                urllib.request.urlretrieve(self.database_url, self.download_path)
                print("Veritabanı dosyasını indirildi!")

                # Zip dosyasını çıkart
                with zipfile.ZipFile(self.download_path, "r") as zip_ref:
                    zip_ref.extractall(os.getcwd())
        except Exception as e:
            print(f"Hata oluştu: {e}")

    def create_sqlite_db(self):
        """
        SQLite veritabanını oluşturur ve Csv dosyasını içine aktarır.
        """
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()

            print("SQlite Veritabanı Tabloyu oluşturuluyor...")
            # Tabloyu oluştur
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS ip_geolocation
                        (ip_start INTEGER PRIMARY KEY,
                        ip_end INTEGER,
                        country_code TEXT,
                        country_name TEXT)''')

            # Csv dosyasını oku ve veritabanına aktar
            with open(self.database_file, "r", encoding="utf-8") as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Başlık satırını atla
                for row in csv_reader:
                    self.cursor.execute("INSERT INTO ip_geolocation VALUES (?, ?, ?, ?)", row)

            print("SQlite Veritabanı Tabloyu oluşturdu!")

            # Değişiklikleri kaydet
            self.connection.commit()
        except Exception as e:
            print(f"Hata oluştu: {e}")

    def get_ip_location(self, ip_address, force_download=False):
        """
        Verilen IP adresinin lokasyon bilgisini döndürür.

        Args:
            ip_address (str): IP adresi.
            force_download (bool): Zip dosyasını yeniden indirme zorunluluğu.

        Returns:
            str: IP adresinin lokasyon bilgisi.
        """
        try:
            # SQLite veritabanını oluştur (eğer daha önce oluşturulmadıysa)
            if not os.path.isfile(self.db_file) or force_download:
                self.download_database(force_download)
                self.create_sqlite_db()

            # IP adresinin lokasyon bilgisini sorgula
            print("IP adresinin lokasyon bilgisini sorgula...")
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()

            # SQLite sorgusu
            query = "SELECT * FROM ip_geolocation WHERE ip_start <= ? AND ip_end >= ?"
            ip_int = self.ip_to_int(ip_address)
            self.cursor.execute(query, (ip_int, ip_int))
            row = self.cursor.fetchone()
            if row:
                return {"status": True, "ip_address": ip_address, "ipint": ip_int, "country_code": row[2], "country_name": row[3]}
            else:
                return {"status": False, "ip_address": ip_address}
        except Exception as e:
            print(f"Hata oluştu: {e}")
            return None


class CemirPostgreSQL:
    def __init__(self, dbhost, dbport, dbuser, dbpassword, dbname, timeout=10, dbcreate_db_if_not_exists=False):
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
        """
        return [method for method in dir(CemirPostgreSQL) if callable(getattr(CemirPostgreSQL, method)) and not method.startswith("__")]

    def parse_output(self, output):

        """
        psql komutunun çıktısını parse ederek dict yapısına çevirir.

        Args:
            output (str): psql komutunun çıktısı.

        Returns:
            dict: Dict formatında çıktı.
        """
        lines = output.strip().split('\n')
        headers = lines[0].split('|')
        data = []

        for line in lines[2:-1]:  # İlk iki satır ve son satır başlık ve ayırıcılar olduğu için atlanır
            values = line.split('|')
            data.append({header.strip(): value.strip() for header, value in zip(headers, values)})

        return data

    def execute_query(self, query, dbname=None):
        """
        Veritabanına SQL sorgusu gönderir ve sonucu döndürür.

        Args:
            query (str): SQL sorgusu.
            dbname (str, optional): Veritabanı adı. Eğer verilmezse, self.dbname kullanılır.

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
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
        if print_query: print(query)
        return self.execute_query(query)

    def insert(self, table_name, columns, values, get_id=False):
        """
        Veritabanına yeni kayıt ekler.

        Args:
            table_name (str): Tablo adı.
            columns (tuple): Kolon adları (örnek: ("id", "name", "data")).
            values (tuple): Kolon değerleri (örnek: (1, "John Doe", {"age": 30, "city": "Istanbul"})).
            get_id (bool): İşlem yapılan ID

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
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

        Args:
            dbname (str): Oluşturulacak veritabanının adı.

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
        """
        query = f"CREATE DATABASE {dbname};"
        return self.execute_query(query, dbname='postgres')

    def create_table(self, table_name, schema):
        """
        Veritabanında tablo oluşturur.

        Args:
            table_name (str): Tablo adı.
            schema (str): Tablo şeması (örnek: "id SERIAL PRIMARY KEY, name VARCHAR(100), data JSONB").

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
        """
        query = f"CREATE TABLE {table_name} ({schema});"
        return self.execute_query(query)

    def read(self, table_name, columns='*', condition=None):
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

        Args:
            table_name (str): Tablo adı.
            updates (dict): Güncellemeler (örnek: {"name": "Jane Doe"}).
            condition (str): Koşul (örnek: "id = 1").
            get_id (bool): İşlem yapılan ID
        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
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

        Args:
            table_name (str): Tablo adı.
            condition (str): Koşul (örnek: "id = 1").

        Returns:
            str: Sorgu sonucu veya JSON formatında hata bilgisi.
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
        CemirUtils sınıfının yapıcı fonksiyonu.
        Verilen veriyi sınıfın 'data' değişkenine atar.

        Parametre:
        data (list, dict): İşlenecek sayısal veri listesi veya sözlük.
        """
        self.data = data
        self.default_headers = {"User-Agent": "CemirUtils"}

    def get_methods(self):
        """
        CemirUtils sınıfının mevcut tüm metodlarının isimlerini yazdırır.
        """
        return [method for method in dir(CemirUtils) if callable(getattr(CemirUtils, method)) and not method.startswith("__")]

    # Linux komutlarını Python üzerinden çağırarak işlem yapmak için kullanılır.

    def linux_ls(self, path="."):
        """
        List files and directories in the given path.
        """
        return subprocess.run(["ls", "-l", path], capture_output=True, text=True).stdout

    def linux_cat(self, filename):
        """
        Display the contents of a file.
        """
        return subprocess.run(["cat", filename], capture_output=True, text=True).stdout

    def linux_touch(self, filename):
        """
        Create an empty file or update the access and modification times of a file.
        """
        return subprocess.run(["touch", filename], capture_output=True, text=True).stdout

    def linux_cp(self, source, destination):
        """
        Copy files or directories from source to destination.
        """
        return subprocess.run(["cp", "-r", source, destination], capture_output=True, text=True).stdout

    def linux_mv(self, source, destination):
        """
        Move or rename files or directories from source to destination.
        """
        return subprocess.run(["mv", source, destination], capture_output=True, text=True).stdout

    def linux_rm(self, path):
        """
        Remove files or directories.
        """
        return subprocess.run(["rm", "-r", path], capture_output=True, text=True).stdout

    def linux_mkdir(self, directory):
        """
        Create a new directory.
        """
        return subprocess.run(["mkdir", directory], capture_output=True, text=True).stdout

    def linux_rmdir(self, directory):
        """
        Remove an empty directory.
        """
        return subprocess.run(["rmdir", directory], capture_output=True, text=True).stdout

    def linux_cut(self, delimiter, fields, filename):
        """
        Extract fields from a file based on a delimiter.
        """
        return subprocess.run(["cut", f"-d{delimiter}", f"-f{fields}", filename], capture_output=True, text=True).stdout

    def linux_gzip(self, filename):
        """
        Compress or decompress files using gzip.
        """
        return subprocess.run(["gzip", filename], capture_output=True, text=True).stdout

    def linux_find(self, path, filename):
        """
        Search for files in a directory hierarchy.
        """
        return subprocess.run(["find", path, "-name", filename], capture_output=True, text=True).stdout

    def linux_grep(self, pattern, filename):
        """
        Search for a pattern in a file.
        """
        return subprocess.run(["grep", pattern, filename], capture_output=True, text=True).stdout

    # def tcp_listen_for_icmp(self, print_query=False, insert_db=True):
    #     """
    #     NOT: scriptin çalışması için sudo gerektirir.
    #
    #     Örnek Servis:
    #
    #     sudo nano /etc/systemd/system/ping_logger.service
    #
    #         [Unit]
    #         Description=Ping Logger Service
    #         After=network.target
    #
    #         [Service]
    #         ExecStart=/usr/bin/python3 /path/to/ping_logger.py
    #         Restart=always
    #         User=root
    #         Group=root
    #
    #         [Install]
    #         WantedBy=multi-user.target
    #
    #     * sudo systemctl daemon-reload
    #     * sudo systemctl enable ping_logger
    #     * sudo systemctl start ping_logger
    #
    #     :param insert_db: bool
    #     :param print_query: bool
    #     :return:
    #     """
    #     if insert_db:
    #         self.insert_raw("""CREATE TABLE ping_log (id SERIAL PRIMARY KEY, contents JSONB NOT NULL);""")
    #
    #     # Raw soket oluşturma
    #     try:
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    #     except:
    #         print("raw soket dinleme işlemleri için sudo yetkisi gerekir!!")
    #         exit(1)
    #
    #     while True:
    #         # Paket alımı
    #         packet, addr = sock.recvfrom(65565)
    #         packet_length = len(packet)
    #
    #         # IP başlığı ayrıştırma
    #         ip_header = packet[0:20]
    #         iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
    #         version_ihl = iph[0]
    #         version = version_ihl >> 4
    #         ihl = version_ihl & 0xF
    #         iph_length = ihl * 4
    #         ttl = iph[5]
    #         protocol = iph[6]
    #         source_ip = socket.inet_ntoa(iph[8])
    #         dest_ip = socket.inet_ntoa(iph[9])
    #
    #         # ICMP başlığı ayrıştırma
    #         icmp_header = packet[iph_length:iph_length + 8]
    #         icmph = struct.unpack('!BBHHH', icmp_header)
    #         icmp_type = icmph[0]
    #         code = icmph[1]
    #         checksum = icmph[2]
    #         packet_id = icmph[3]
    #         sequence = icmph[4]
    #
    #         if icmp_type == 8:  # Ping Request
    #             timestamp = datetime.now()
    #             contents = {
    #                 "sequence": sequence,
    #                 "dest_ip": dest_ip,
    #                 "source_ip": source_ip,
    #                 "ttl": ttl,
    #                 "timestamp": timestamp.isoformat(),
    #                 "packet_length": packet_length,
    #
    #                 # "icmp_type": icmp_type,
    #                 # "checksum": checksum,
    #                 # "packet_id": packet_id,
    #                 # "protocol": protocol
    #             }
    #
    #             if insert_db:
    #                 self.insert_raw(f"""INSERT INTO ping_log (contents) VALUES ('{json.dumps(contents)}');""")
    #
    #             if print_query:
    #                 print(contents)

    def time_days_between_dates(self, date1, date2):
        """
        İki tarih arasındaki gün sayısını hesaplar.


        Args:
            date1 (str): İlk tarih (YYYY-MM-DD formatında).
            date2 (str): İkinci tarih (YYYY-MM-DD formatında).


        Returns:
            int: İki tarih arasındaki gün sayısı.
        """
        date_format = "%Y-%m-%d"
        d1 = datetime.strptime(date1, date_format)
        d2 = datetime.strptime(date2, date_format)
        delta = d2 - d1
        return delta.days

    def time_hours_minutes_seconds_between_times(self, time1, time2):
        """
        İki zaman arasındaki saat, dakika ve saniye farkını hesaplar.


        Args:
            time1 (str): İlk zaman (HH:MM:SS formatında).
            time2 (str): İkinci zaman (HH:MM:SS formatında).


        Returns:
            tuple: Saat, dakika ve saniye farkı.
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


        Args:
            future_date (str): Gelecek tarih (YYYY-MM-DD HH:MM:SS formatında).


        Returns:
            tuple: Kalan gün, saat, dakika ve saniye.
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


        Args:
            date (str): Başlangıç tarihi (YYYY-MM-DD formatında).
            days (int): Eklenecek gün sayısı.

        * Örnek:
        >>> utils =CemirUtils()
        >>> utils.time_add_days_to_date("2024-05-10", 100)

        Returns:
            datetime: Yeni tarih.
        """
        date_format = "%Y-%m-%d"
        d = datetime.strptime(date, date_format)
        new_date = d + timedelta(days=days)
        return new_date

    def time_add_days_and_format(self, date, days):
        """
        Belirtilen tarihe gün sayısı ekleyip yeni tarihi istenilen dilde gün adı ile birlikte formatlar.


        Args:
            date (str): Başlangıç tarihi (YYYY-MM-DD formatında).
            days (int): Eklenecek gün sayısı.

        Returns:
            str: Formatlanmış yeni tarih ve gün adı.
        """
        new_date = self.time_add_days_to_date(date, days)
        formatted_date = new_date.strftime("%Y-%m-%d")
        return f"{formatted_date} ({new_date})"

    def time_is_weekend(self, date):
        """
        Bir tarihin hafta sonu olup olmadığını kontrol eder.


        Args:
            date (str): Tarih (YYYY-MM-DD formatında).


        Returns:
            bool: Hafta sonu ise True, değilse False.
        """
        date_format = "%Y-%m-%d"
        d = datetime.strptime(date, date_format)
        return d.weekday() >= 5  # 5 = Cumartesi, 6 = Pazar

    def time_is_leap_year(self, year):
        """
        Bir yılın artık yıl olup olmadığını kontrol eder.


        Args:
            year (int): Yıl.


        Returns:
            bool: Artık yıl ise True, değilse False.
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def time_days_in_month(self, year, month):
        """
        Bir ay içindeki gün sayısını döndürür.


        Args:
            year (int): Yıl.
            month (int): Ay.


        Returns:
            int: Ay içindeki gün sayısı.
        """
        return monthrange(year, month)[1]

    def time_next_weekday(self, date, weekday):
        """
        Bir tarihten sonraki belirli bir günün tarihini döndürür (örneğin, bir sonraki Pazartesi).


        Args:
            date (str): Başlangıç tarihi (YYYY-MM-DD formatında).
            weekday (int): Hedef gün (0 = Pazartesi, 1 = Salı, vb.).


        Returns:
            datetime: Bir sonraki hedef günün tarihi.
        """
        date_format = "%Y-%m-%d"
        d = datetime.strptime(date, date_format)
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Hedef gün zaten bu hafta geçmiş
            days_ahead += 7
        return d + timedelta(days=days_ahead)

    @staticmethod
    def time_todatetime(date):
        """
        Bir tarihi datetime türüne çevirir

        Args:
            date (str): Tarih (YYYY-MM-DD formatında).

        * Örnek:
        >>> utils =CemirUtils()
        >>> print(utils.time_todatetime("2024-05-10"))

        Returns:
            str: Formatlanmış tarih.
        """

        return datetime.strptime(date, "%Y-%m-%d")

    def time_since(self, past_date):
        """
        Belirli bir tarihten geçen yıl, ay, gün, saat, dakika ve saniyeyi hesaplar.

        Parametre:
        past_date (str): Geçmiş tarih (yyyy-mm-dd HH:MM:SS formatında)

        Dönüş:
        dict: Geçen yıl, ay, gün, saat, dakika ve saniyeleri içeren sözlük.

        Örnek:
        >>> cem = CemirUtils(None)
        >>> cem.time_since('2020-01-01 00:00:00')
        {'years': 4, 'months': 4, 'days': 25, 'hours': 14, 'minutes': 35, 'seconds': 10}
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


        Args:
        date1 (str): İlk tarih (YYYY-MM-DD formatında).
        date2 (str): İkinci tarih (YYYY-MM-DD formatında).


        Returns:
            int: İki tarih arasındaki iş günü sayısı.
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


        Args:
            text (str): Değiştirilecek metin.
            replacements (dict): Değiştirilecek değer çiftleri (anahtar: eski değer, değer: yeni değer).

        Örnek:

        >>> utils = CemirUtils()
        >>> print(utils.str_replace_multiple("asd muslu asd", {"asd": "muslu", "muslu": "emir"}))

        Returns:
            str: Değiştirilmiş metin.
        """
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def str_replace_with_last(self, text, values):
        """
        Verilen metinde belirtilen tüm değerleri son değer ile değiştirir.


        Args:
            text (str): Değiştirilecek metin.
            values (tuple): Değiştirilecek değerler.

        Örnek:

        >>> utils = CemirUtils()
        >>> print(utils.str_replace_with_last("asd muslu asd", ("muslu", "emir"}))


        Returns:
            str: Değiştirilmiş metin.
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

        Parametre:
        scalar (int, float): Çarpılacak skaler değer.

        Dönüş:
        list: Skaler değer ile çarpılmış veri listesi.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.list_multiply_by_scalar(2)
        [2, 4, 6]
        """
        if isinstance(self.data, list):
            return [x * scalar for x in self.data]
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def list_get_frequency(self, value):
        """
        Verilen değerin veri listesinde kaç kez geçtiğini sayar.

        Parametre:
        value: Sayılacak değer.

        Dönüş:
        int: Değerin listede kaç kez geçtiği.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 2, 3])
        >>> ceml.list_get_frequency(2)
        2
        """
        if isinstance(self.data, list):
            return self.data.count(value)
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def list_reverse(self):
        """
        Veri listesini tersine çevirir.

        Dönüş:
        list: Tersine çevrilmiş veri listesi.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.list_reverse()
        [3, 2, 1]
        """
        if isinstance(self.data, list):
            return self.data[::-1]
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def list_get_max_value(self):
        """
        Veri listesindeki en büyük değeri döner.

        Dönüş:
        int, float: Veri listesindeki en büyük değer.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.list_get_max_value()
        3
        """
        if isinstance(self.data, list):
            return max(self.data)
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def list_get_min_value(self):
        """
        Veri listesindeki en küçük değeri döner.

        Dönüş:
        int, float: Veri listesindeki en küçük değer.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.list_get_min_value()
        1
        """
        if isinstance(self.data, list):
            return min(self.data)
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def dict_filter_by_key(self, key):
        """
        Sözlükte veya sözlüklerin bulunduğu listede belirtilen anahtara sahip elemanları filtreler.

        Parametreler:
        key: Filtreleme yapılacak anahtar.

        Dönüş:
        dict, list: Filtrelenmiş veri.

        Örnek:
        >>> cemd = CemirUtils({'a': 1, 'b': 2, 'c': 3})
        >>> cemd.dict_filter_by_key('b')
        {'b': 2}

        >>> ceml = CemirUtils([{'a': 1}, {'b': 2}, {'a': 3}])
        >>> ceml.dict_filter_by_key('a')
        [{'a': 1}, {'a': 3}]
        """
        if isinstance(self.data, dict):
            return {k: v for k, v in self.data.items() if k == key}
        elif isinstance(self.data, list):
            return [item for item in self.data if isinstance(item, dict) and key in item]
        else:
            raise TypeError("Veri tipi sözlük veya sözlük listesi olmalıdır.")

    def dict_get_keys(self):
        """
        Sözlükteki veya sözlüklerin bulunduğu listedeki anahtarları döner.

        Dönüş:
        list: Anahtarlar listesi.

        Örnek:
        >>> cemd = CemirUtils({'a': 1, 'b': 2, 'c': 3})
        >>> cemd.dict_get_keys()
        ['a', 'b', 'c']

        >>> ceml = CemirUtils([{'a': 1}, {'b': 2}, {'a': 3}])
        >>> ceml.dict_get_keys()
        ['a', 'b', 'a']
        """
        if isinstance(self.data, dict):
            return list(self.data.keys())
        elif isinstance(self.data, list):
            return [key for item in self.data if isinstance(item, dict) for key in item.keys()]
        else:
            raise TypeError("Veri tipi sözlük veya sözlük listesi olmalıdır.")

    def dict_merge(self, *dicts):
        """
        Verilen sözlükleri birleştirir.

        Parametreler:
        *dicts (dict): Birleştirilecek sözlükler.

        Dönüş:
        dict: Birleştirilmiş sözlük.

        Örnek:
        >>> cemd = CemirUtils({})
        >>> cemd.dict_merge({'a': 1}, {'b': 2})
        {'a': 1, 'b': 2}
        """
        if all(isinstance(d, dict) for d in dicts):
            merged = {}
            for d in dicts:
                merged.update(d)
            return merged
        else:
            raise TypeError("Tüm parametreler sözlük olmalıdır.")

    def list_filter_greater_than(self, threshold):
        """
        Belirtilen eşik değerinden büyük olan öğeleri filtreler.

        Parametre:
        threshold (int/float): Eşik değer.

        Dönüş:
        list: Eşik değerinden büyük olan öğeleri içeren liste.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.list_filter_greater_than(5)
        [9, 6]
        """
        return [x for x in self.data if x > threshold]

    def list_filter_less_than(self, threshold):
        """
        Belirtilen eşik değerinden küçük olan öğeleri filtreler.

        Parametre:
        threshold (int/float): Eşik değer.

        Dönüş:
        list: Eşik değerinden küçük olan öğeleri içeren liste.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.list_filter_less_than(4)
        [3, 1, 1, 2, 3]
        """
        return [x for x in self.data if x < threshold]

    def list_flatten(self):
        """
        Çok katmanlı listeyi tek katmana indirger.

        Dönüş:
        list: Tek katmanlı liste.

        Örnek:
        >>> ceml = CemirUtils([[1, 2], [3, 4], [5]])
        >>> ceml.list_flatten()
        [1, 2, 3, 4, 5]
        """
        if isinstance(self.data, list) and all(isinstance(i, list) for i in self.data):
            return [item for sublist in self.data for item in sublist]
        else:
            raise TypeError("Veri tipi çok katmanlı liste olmalıdır.")

    def list_sum_values(self):
        """
        Listedeki tüm sayısal değerlerin toplamını hesaplar.

        Dönüş:
        int/float: Listedeki sayısal değerlerin toplamı.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.list_sum_values()
        44
        """
        return sum(self.data)

    def list_average(self):
        """
        Listedeki sayısal değerlerin ortalamasını hesaplar.

        Dönüş:
        float: Listedeki sayısal değerlerin ortalaması. Liste boşsa 0 döner.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.list_average()
        4.0
        """
        return sum(self.data) / len(self.data) if self.data else 0

    def list_head(self, n=5):
        """
        Listenin ilk n elemanını döndürür.
        Args:
            n (int): Döndürülecek eleman sayısı (varsayılan 5).
        Returns:
            list: İlk n eleman.
        """
        return self.data[:n]

    def list_tail(self, n=5):
        """
        Listenin son n elemanını döndürür.
        Args:
            n (int): Döndürülecek eleman sayısı (varsayılan 5).
        Returns:
            list: Son n eleman.
        """
        return self.data[-n:]

    def list_main(self, n=5):
        """
        Listenin ortadaki elemanlarını döndürür.
        Eğer listenin uzunluğu 2n veya daha küçükse tüm listeyi döndürür.
        Args:
            n (int): Kenarlardan kesilecek eleman sayısı (varsayılan 5).
        Returns:
            list: Ortadaki elemanlar.
        """
        if len(self.data) <= 2 * n:
            return self.data
        return self.data[n:-n]

    def list_unique_values(self):
        """
        Listenin benzersiz elemanlarını döndürür.
        Returns:
            list: Benzersiz elemanlar.
        """
        return list(set(self.data))

    def list_sort_asc(self):
        """
        Listeyi artan sırada sıralar.
        Returns:
            list: Artan sırada sıralanmış liste.
        """
        return sorted(self.data)

    def list_sort_desc(self):
        """
        Listeyi azalan sırada sıralar.
        Returns:
            list: Azalan sırada sıralanmış liste.
        """
        return sorted(self.data, reverse=True)

    def http_server(self, port=8000, ip='127.0.0.1', ssl_cert=None, ssl_key=None, username=None, password=None, directory=None):
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

    def http_send_request(self, url, method='GET', headers=None, data=None, destination=None):
        """
        Send an HTTP request to the given URL with the specified method, headers, and data,
        using the default User-Agent if not provided in headers.
        If destination is provided, download the file to the destination path.
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

    def http_get(self, url, params=None, headers=None, verify_ssl=True):
        """
        GET isteği gönderir.

        Parametreler:
        url (str): İstek URL'si.
        params (dict): URL parametreleri.
        headers (dict): İstek başlıkları.
        verify_ssl (bool): SSL doğrulama kontrolü.

        Dönüş:
        dict, str: JSON yanıtı veya düz metin.
        """
        if headers is None or "User-Agent" not in headers:
            headers = self.default_headers.copy()

        if params:
            url += '?' + parse.urlencode(params)

        req = request.Request(url, headers=headers)
        response = request.urlopen(req, timeout=10, context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def http_post(self, url, data=None, headers=None, verify_ssl=True):
        """
        POST isteği gönderir.

        Parametreler:
        url (str): İstek URL'si.
        data (dict): Gönderilecek veri.
        headers (dict): İstek başlıkları.
        verify_ssl (bool): SSL doğrulama kontrolü.

        Dönüş:
        dict, str: JSON yanıtı veya düz metin.
        """
        if headers is None or "User-Agent" not in headers:
            headers = self.default_headers.copy()

        if data:
            data = parse.urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='POST')
        response = request.urlopen(req, timeout=10, context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def http_put(self, url, data=None, headers=None, verify_ssl=True):
        """
        PUT isteği gönderir.

        Parametreler:
        url (str): İstek URL'si.
        data (dict): Gönderilecek veri.
        headers (dict): İstek başlıkları.
        verify_ssl (bool): SSL doğrulama kontrolü.

        Dönüş:
        dict, str: JSON yanıtı veya düz metin.
        """
        if headers is None or "User-Agent" not in headers:
            headers = self.default_headers.copy()

        if data:
            data = parse.urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='PUT')
        response = request.urlopen(req, timeout=10, context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

    def http_delete(self, url, headers=None, verify_ssl=True):
        """
        DELETE isteği gönderir.

        Parametreler:
        url (str): İstek URL'si.
        headers (dict): İstek başlıkları.
        verify_ssl (bool): SSL doğrulama kontrolü.

        Dönüş:
        dict, str: JSON yanıtı veya düz metin.
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

    def http_patch(self, url, data=None, headers=None, verify_ssl=True):
        """
        PATCH isteği gönderir.

        Parametreler:
        url (str): İstek URL'si.
        data (dict): Gönderilecek veri.
        headers (dict): İstek başlıkları.
        verify_ssl (bool): SSL doğrulama kontrolü.

        Dönüş:
        dict, str: JSON yanıtı veya düz metin.
        """
        if headers is None or "User-Agent" not in headers:
            headers = self.default_headers.copy()

        if data:
            data = parse.urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='PATCH')
        response = request.urlopen(req, timeout=10, context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content
