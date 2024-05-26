import base64
import json
import ssl

from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib import request, parse


class CemirUtils:
    def __init__(self, data):
        """
        CemirUtils sınıfının yapıcı fonksiyonu.
        Verilen veriyi sınıfın 'data' değişkenine atar.

        Parametre:
        data (list, dict): İşlenecek sayısal veri listesi veya sözlük.
        """
        self.data = data

    def getmethods(self):
        """
        CemirUtils sınıfının mevcut tüm metodlarının isimlerini yazdırır.
        """
        return [method for method in dir(CemirUtils) if callable(getattr(CemirUtils, method)) and not method.startswith("__")]


    def replace_multiple(self, text, replacements):
        """
        Verilen metinde çoklu değiştirme işlemi yapar.


        Args:
            text (str): Değiştirilecek metin.
            replacements (dict): Değiştirilecek değer çiftleri (anahtar: eski değer, değer: yeni değer).


        Returns:
            str: Değiştirilmiş metin.
        """
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def replace_with_last(self, text, values):
        """
        Verilen metinde belirtilen tüm değerleri son değer ile değiştirir.


        Args:
            text (str): Değiştirilecek metin.
            values (tuple): Değiştirilecek değerler.


        Returns:
            str: Değiştirilmiş metin.
        """
        if not values:
            return text
        last_value = values[-1]
        for value in values[:-1]:
            text = text.replace(value, last_value)
        return text

    def multiply_by_scalar(self, scalar):
        """
        Veri listesindeki her bir elemanı verilen skaler değer ile çarpar.

        Parametre:
        scalar (int, float): Çarpılacak skaler değer.

        Dönüş:
        list: Skaler değer ile çarpılmış veri listesi.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.multiply_by_scalar(2)
        [2, 4, 6]
        """
        if isinstance(self.data, list):
            return [x * scalar for x in self.data]
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def get_frequency(self, value):
        """
        Verilen değerin veri listesinde kaç kez geçtiğini sayar.

        Parametre:
        value: Sayılacak değer.

        Dönüş:
        int: Değerin listede kaç kez geçtiği.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 2, 3])
        >>> ceml.get_frequency(2)
        2
        """
        if isinstance(self.data, list):
            return self.data.count(value)
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def reverse_list(self):
        """
        Veri listesini tersine çevirir.

        Dönüş:
        list: Tersine çevrilmiş veri listesi.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.reverse_list()
        [3, 2, 1]
        """
        if isinstance(self.data, list):
            return self.data[::-1]
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def get_max_value(self):
        """
        Veri listesindeki en büyük değeri döner.

        Dönüş:
        int, float: Veri listesindeki en büyük değer.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.get_max_value()
        3
        """
        if isinstance(self.data, list):
            return max(self.data)
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def get_min_value(self):
        """
        Veri listesindeki en küçük değeri döner.

        Dönüş:
        int, float: Veri listesindeki en küçük değer.

        Örnek:
        >>> ceml = CemirUtils([1, 2, 3])
        >>> ceml.get_min_value()
        1
        """
        if isinstance(self.data, list):
            return min(self.data)
        else:
            raise TypeError("Veri tipi liste olmalıdır.")

    def filter_by_key(self, key, value):
        """
        Sözlükte veya sözlüklerin bulunduğu listede belirtilen anahtar ve değere sahip elemanları filtreler.

        Parametreler:
        key: Filtreleme yapılacak anahtar.
        value: Filtreleme yapılacak değer.

        Dönüş:
        dict, list: Filtrelenmiş veri.

        Örnek:
        >>> cemd = CemirUtils({'a': 1, 'b': 2, 'c': 3})
        >>> cemd.filter_by_key('b', 2)
        {'b': 2}

        >>> ceml = CemirUtils([{'a': 1}, {'b': 2}, {'a': 3}])
        >>> ceml.filter_by_key('a', 1)
        [{'a': 1}]
        """
        if isinstance(self.data, dict):
            return {k: v for k, v in self.data.items() if k == key and v == value}
        elif isinstance(self.data, list):
            return [item for item in self.data if isinstance(item, dict) and item.get(key) == value]
        else:
            raise TypeError("Veri tipi sözlük veya sözlük listesi olmalıdır.")

    def get_keys(self):
        """
        Sözlükteki veya sözlüklerin bulunduğu listedeki anahtarları döner.

        Dönüş:
        list: Anahtarlar listesi.

        Örnek:
        >>> cemd = CemirUtils({'a': 1, 'b': 2, 'c': 3})
        >>> cemd.get_keys()
        ['a', 'b', 'c']

        >>> ceml = CemirUtils([{'a': 1}, {'b': 2}, {'a': 3}])
        >>> ceml.get_keys()
        ['a', 'b', 'a']
        """
        if isinstance(self.data, dict):
            return list(self.data.keys())
        elif isinstance(self.data, list):
            return [key for item in self.data if isinstance(item, dict) for key in item.keys()]
        else:
            raise TypeError("Veri tipi sözlük veya sözlük listesi olmalıdır.")

    def flatten_list(self):
        """
        Çok katmanlı listeyi tek katmana indirger.

        Dönüş:
        list: Tek katmanlı liste.

        Örnek:
        >>> ceml = CemirUtils([[1, 2], [3, 4], [5]])
        >>> ceml.flatten_list()
        [1, 2, 3, 4, 5]
        """
        if isinstance(self.data, list) and all(isinstance(i, list) for i in self.data):
            return [item for sublist in self.data for item in sublist]
        else:
            raise TypeError("Veri tipi çok katmanlı liste olmalıdır.")

    def merge_dicts(self, *dicts):
        """
        Verilen sözlükleri birleştirir.

        Parametreler:
        *dicts (dict): Birleştirilecek sözlükler.

        Dönüş:
        dict: Birleştirilmiş sözlük.

        Örnek:
        >>> ceml = CemirUtils({})
        >>> ceml.merge_dicts({'a': 1}, {'b': 2})
        {'a': 1, 'b': 2}
        """
        if all(isinstance(d, dict) for d in dicts):
            merged = {}
            for d in dicts:
                merged.update(d)
            return merged
        else:
            raise TypeError("Tüm parametreler sözlük olmalıdır.")

    def filter_greater_than(self, threshold):
        """
        Belirtilen eşik değerinden büyük olan öğeleri filtreler.

        Parametre:
        threshold (int/float): Eşik değer.

        Dönüş:
        list: Eşik değerinden büyük olan öğeleri içeren liste.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.filter_greater_than(5)
        [9, 6]
        """
        return [x for x in self.data if x > threshold]

    def filter_less_than(self, threshold):
        """
        Belirtilen eşik değerinden küçük olan öğeleri filtreler.

        Parametre:
        threshold (int/float): Eşik değer.

        Dönüş:
        list: Eşik değerinden küçük olan öğeleri içeren liste.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.filter_less_than(4)
        [3, 1, 1, 2, 3]
        """
        return [x for x in self.data if x < threshold]

    def sum_values(self):
        """
        Listedeki tüm sayısal değerlerin toplamını hesaplar.

        Dönüş:
        int/float: Listedeki sayısal değerlerin toplamı.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.sum_values()
        44
        """
        return sum(self.data)

    def average(self):
        """
        Listedeki sayısal değerlerin ortalamasını hesaplar.

        Dönüş:
        float: Listedeki sayısal değerlerin ortalaması. Liste boşsa 0 döner.

        Örnek:
        >>> cem = CemirUtils([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        >>> cem.average()
        4.0
        """
        return sum(self.data) / len(self.data) if self.data else 0

    def head(self, n=5):
        """
        Listenin ilk n elemanını döndürür.
        Args:
            n (int): Döndürülecek eleman sayısı (varsayılan 5).
        Returns:
            list: İlk n eleman.
        """
        return self.data[:n]

    def tail(self, n=5):
        """
        Listenin son n elemanını döndürür.
        Args:
            n (int): Döndürülecek eleman sayısı (varsayılan 5).
        Returns:
            list: Son n eleman.
        """
        return self.data[-n:]

    def main(self, n=5):
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

    def unique_values(self):
        """
        Listenin benzersiz elemanlarını döndürür.
        Returns:
            list: Benzersiz elemanlar.
        """
        return list(set(self.data))

    def sort_asc(self):
        """
        Listeyi artan sırada sıralar.
        Returns:
            list: Artan sırada sıralanmış liste.
        """
        return sorted(self.data)

    def sort_desc(self):
        """
        Listeyi azalan sırada sıralar.
        Returns:
            list: Azalan sırada sıralanmış liste.
        """
        return sorted(self.data, reverse=True)

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
        if headers is None:
            headers = {}

        if params:
            url += '?' + parse.urlencode(params)

        req = request.Request(url, headers=headers)
        response = request.urlopen(req, timeout=10,
                                   context=None if verify_ssl else request._create_unverified_context())
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
        if headers is None:
            headers = {}

        if data:
            data = parse.urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='POST')
        response = request.urlopen(req, timeout=10,
                                   context=None if verify_ssl else request._create_unverified_context())
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
        if headers is None:
            headers = {}

        if data:
            data = parse.urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='PUT')
        response = request.urlopen(req, timeout=10,
                                   context=None if verify_ssl else request._create_unverified_context())
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
        if headers is None:
            headers = {}

        req = request.Request(url, headers=headers, method='DELETE')
        response = request.urlopen(req, timeout=10,
                                   context=None if verify_ssl else request._create_unverified_context())
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
        if headers is None:
            headers = {}

        if data:
            data = parse.urlencode(data).encode('utf-8')

        req = request.Request(url, data=data, headers=headers, method='PATCH')
        response = request.urlopen(req, timeout=10,
                                   context=None if verify_ssl else request._create_unverified_context())
        content = response.read().decode('utf-8')

        if 'application/json' in response.getheader('Content-Type'):
            return json.loads(content)
        else:
            return content

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
