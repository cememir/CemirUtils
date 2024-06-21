# Documentation

## Class: `CemirUtilsAMP`

### Methods
- `fetch_html(self, url)`
- `convert_to_amp(self, html_content)`
- `convert_img_tags(self, html_content)`
- `convert_video_tags(self, html_content)`
- `save_to_file(self, content, filename)`
## Class: `CemirUtilsHTTP`

### Methods
- `__init__(self)`
  **Docstring:**
  ```
  CemirUtilsHTTP
  ```
- `get_methods(self)`
  **Docstring:**
  ```
  CemirUtilsHTTP sınıfının mevcut tüm metodlarının isimlerini yazdırır.
  ```
- `server(self, port, ip, ssl_cert, ssl_key, username, password, directory)`
## Class: `CemirUtilsHTTPRequestHandler`

### Methods
- `__init__(self)`
- `do_GET(self)`
- `check_basic_auth(self, username, password)`
- `send_request(self, url, method, headers, data, destination)`
  **Docstring:**
  ```
  Send an HTTP request to the given URL with the specified method, headers, and data,
using the default User-Agent if not provided in headers.
If destination is provided, download the file to the destination path.
  ```
- `get(self, url, params, headers, verify_ssl)`
  **Docstring:**
  ```
  GET isteği gönderir.

Parametreler:
url (str): İstek URL'si.
params (dict): URL parametreleri.
headers (dict): İstek başlıkları.
verify_ssl (bool): SSL doğrulama kontrolü.

Dönüş:
dict, str: JSON yanıtı veya düz metin.
  ```
- `post(self, url, data, headers, verify_ssl)`
  **Docstring:**
  ```
  POST isteği gönderir.

Parametreler:
url (str): İstek URL'si.
data (dict): Gönderilecek veri.
headers (dict): İstek başlıkları.
verify_ssl (bool): SSL doğrulama kontrolü.

Dönüş:
dict, str: JSON yanıtı veya düz metin.
  ```
- `put(self, url, data, headers, verify_ssl)`
  **Docstring:**
  ```
  PUT isteği gönderir.

Parametreler:
url (str): İstek URL'si.
data (dict): Gönderilecek veri.
headers (dict): İstek başlıkları.
verify_ssl (bool): SSL doğrulama kontrolü.

Dönüş:
dict, str: JSON yanıtı veya düz metin.
  ```
- `delete(self, url, headers, verify_ssl)`
  **Docstring:**
  ```
  DELETE isteği gönderir.

Parametreler:
url (str): İstek URL'si.
headers (dict): İstek başlıkları.
verify_ssl (bool): SSL doğrulama kontrolü.

Dönüş:
dict, str: JSON yanıtı veya düz metin.
  ```
- `patch(self, url, data, headers, verify_ssl)`
  **Docstring:**
  ```
  PATCH isteği gönderir.

Parametreler:
url (str): İstek URL'si.
data (dict): Gönderilecek veri.
headers (dict): İstek başlıkları.
verify_ssl (bool): SSL doğrulama kontrolü.

Dönüş:
dict, str: JSON yanıtı veya düz metin.
  ```
## Class: `CemirUtilsLoopTimer`

### Methods
- `__init__(self)`
## Class: `LoopTimerContext`

### Methods
- `__init__(self, timer)`
- `__enter__(self)`
- `__exit__(self)`
- `check_loop(self)`
- `extract_loops(self, code)`
- `loop_timer_decorator(self, func)`
- `loop(self, func)`
## Class: `CemirUtilsDecorators`

### Methods
- `__init__(self)`
- `webhook_request(url, headers)`
- `timeit(func)`
- `log(func)`
- `retry(retries, delay)`
- `cache(func)`
- `deprecate(message)`
- `debug(func)`
- `cache_with_expiry(expiry_time)`
- `before_after(func)`
- `rate_limit(max_calls, period)`
  **Docstring:**
  ```
  :param max_calls: Belirli bir zaman dilimi içinde bir fonksiyonun kaç kez çağrılabileceğini belirtir.
:param period: Örneğin, period=5 olarak ayarlandığında, 5 saniyelik bir süre içinde max_call sayısınca fonksiyon çağrısına izin verilir.
:return:
  ```
## Class: `CemirUtilsFunctionNotification`

### Methods
- `__init__(self, smtp_server, smtp_port, smtp_user, smtp_password)`
- `notify(self, to_email, subject)`
- `send_notification(self, to_email, subject, func_name, result)`
## Class: `CemirUtilsEmail`

### Methods
- `__init__(self, smtp_host, smtp_port, smtp_user, smtp_pass, smtp_ssl)`
- `html_to_plain(self, html)`
- `zip_attachments(self, attachments)`
- `send_email(self, to_email, subject, body_html, attachments, zip_files)`
## Class: `CemirUtilsConditions`

### Methods
- `__init__(self)`
- `condition_collector(self, func)`
## Class: `Dict2Dot`

### Methods
- `__getattr__(self, key)`
## Class: `IPGeolocation`

### Methods
- `__init__(self)`
- `ip_to_int(self, ip)`
- `int_to_ip(self, ip_int)`
- `download_database(self, force_download)`
  **Docstring:**
  ```
  IP2Location veritabanını indirir.

Args:
    force_download (bool): Zip dosyasını yeniden indirme zorunluluğu.
  ```
- `create_sqlite_db(self)`
  **Docstring:**
  ```
  SQLite veritabanını oluşturur ve Csv dosyasını içine aktarır.
  ```
- `get_ip_location(self, ip_address, force_download)`
  **Docstring:**
  ```
  Verilen IP adresinin lokasyon bilgisini döndürür.

Args:
    ip_address (str): IP adresi.
    force_download (bool): Zip dosyasını yeniden indirme zorunluluğu.

Returns:
    str: IP adresinin lokasyon bilgisi.
  ```
## Class: `CemirPostgreSQL`

### Methods
- `__init__(self, dbhost, dbport, dbuser, dbpassword, dbname, timeout, dbcreate_db_if_not_exists)`
- `get_methods(self)`
  **Docstring:**
  ```
  CemirPostgreSQL sınıfının mevcut tüm metodlarının isimlerini yazdırır.
  ```
- `parse_output(self, output)`
  **Docstring:**
  ```
  psql komutunun çıktısını parse ederek dict yapısına çevirir.

Args:
    output (str): psql komutunun çıktısı.

Returns:
    dict: Dict formatında çıktı.
  ```
- `execute_query(self, query, dbname)`
  **Docstring:**
  ```
  Veritabanına SQL sorgusu gönderir ve sonucu döndürür.

Args:
    query (str): SQL sorgusu.
    dbname (str, optional): Veritabanı adı. Eğer verilmezse, self.dbname kullanılır.

Returns:
    str: Sorgu sonucu veya JSON formatında hata bilgisi.
  ```
- `raw(self, query, print_query)`
- `insert(self, table_name, columns, values, get_id)`
  **Docstring:**
  ```
  Veritabanına yeni kayıt ekler.

Args:
    table_name (str): Tablo adı.
    columns (tuple): Kolon adları (örnek: ("id", "name", "data")).
    values (tuple): Kolon değerleri (örnek: (1, "John Doe", {"age": 30, "city": "Istanbul"})).
    get_id (bool): İşlem yapılan ID

Returns:
    str: Sorgu sonucu veya JSON formatında hata bilgisi.
  ```
- `create_database(self, dbname)`
  **Docstring:**
  ```
  Belirtilen ad ile yeni bir veritabanı oluşturur.

Args:
    dbname (str): Oluşturulacak veritabanının adı.

Returns:
    str: Sorgu sonucu veya JSON formatında hata bilgisi.
  ```
- `create_table(self, table_name, schema)`
  **Docstring:**
  ```
  Veritabanında tablo oluşturur.

Args:
    table_name (str): Tablo adı.
    schema (str): Tablo şeması (örnek: "id SERIAL PRIMARY KEY, name VARCHAR(100), data JSONB").

Returns:
    str: Sorgu sonucu veya JSON formatında hata bilgisi.
  ```
- `read(self, table_name, columns, condition)`
- `update(self, table_name, updates, condition, get_id)`
  **Docstring:**
  ```
  Veritabanındaki kaydı günceller.

Args:
    table_name (str): Tablo adı.
    updates (dict): Güncellemeler (örnek: {"name": "Jane Doe"}).
    condition (str): Koşul (örnek: "id = 1").
    get_id (bool): İşlem yapılan ID
Returns:
    str: Sorgu sonucu veya JSON formatında hata bilgisi.
  ```
- `delete(self, table_name, condition)`
  **Docstring:**
  ```
  Veritabanındaki kaydı siler.

Args:
    table_name (str): Tablo adı.
    condition (str): Koşul (örnek: "id = 1").

Returns:
    str: Sorgu sonucu veya JSON formatında hata bilgisi.
  ```
## Class: `CemirUtils`

### Methods
- `__init__(self, data)`
  **Docstring:**
  ```
  CemirUtils sınıfının yapıcı fonksiyonu.
Verilen veriyi sınıfın 'data' değişkenine atar.

Parametre:
data (list, dict): İşlenecek sayısal veri listesi veya sözlük.
  ```
- `get_methods(self)`
  **Docstring:**
  ```
  CemirUtils sınıfının mevcut tüm metodlarının isimlerini yazdırır.
  ```
- `linux_ls(self, path)`
  **Docstring:**
  ```
  List files and directories in the given path.
  ```
- `linux_cat(self, filename)`
  **Docstring:**
  ```
  Display the contents of a file.
  ```
- `linux_touch(self, filename)`
  **Docstring:**
  ```
  Create an empty file or update the access and modification times of a file.
  ```
- `linux_cp(self, source, destination)`
  **Docstring:**
  ```
  Copy files or directories from source to destination.
  ```
- `linux_mv(self, source, destination)`
  **Docstring:**
  ```
  Move or rename files or directories from source to destination.
  ```
- `linux_rm(self, path)`
  **Docstring:**
  ```
  Remove files or directories.
  ```
- `linux_mkdir(self, directory)`
  **Docstring:**
  ```
  Create a new directory.
  ```
- `linux_rmdir(self, directory)`
  **Docstring:**
  ```
  Remove an empty directory.
  ```
- `linux_cut(self, delimiter, fields, filename)`
  **Docstring:**
  ```
  Extract fields from a file based on a delimiter.
  ```
- `linux_gzip(self, filename)`
  **Docstring:**
  ```
  Compress or decompress files using gzip.
  ```
- `linux_find(self, path, filename)`
  **Docstring:**
  ```
  Search for files in a directory hierarchy.
  ```
- `linux_grep(self, pattern, filename)`
  **Docstring:**
  ```
  Search for a pattern in a file.
  ```
- `time_days_between_dates(self, date1, date2)`
  **Docstring:**
  ```
  İki tarih arasındaki gün sayısını hesaplar.


Args:
    date1 (str): İlk tarih (YYYY-MM-DD formatında).
    date2 (str): İkinci tarih (YYYY-MM-DD formatında).


Returns:
    int: İki tarih arasındaki gün sayısı.
  ```
- `time_hours_minutes_seconds_between_times(self, time1, time2)`
  **Docstring:**
  ```
  İki zaman arasındaki saat, dakika ve saniye farkını hesaplar.


Args:
    time1 (str): İlk zaman (HH:MM:SS formatında).
    time2 (str): İkinci zaman (HH:MM:SS formatında).


Returns:
    tuple: Saat, dakika ve saniye farkı.
  ```
- `time_until_date(self, future_date)`
  **Docstring:**
  ```
  Belirli bir tarihe kadar kalan yıl, ay, gün, saat, dakika ve saniye hesaplar.


Args:
    future_date (str): Gelecek tarih (YYYY-MM-DD HH:MM:SS formatında).


Returns:
    tuple: Kalan gün, saat, dakika ve saniye.
  ```
- `time_add_days_to_date(self, date, days)`
  **Docstring:**
  ```
  Belirtilen tarihe gün sayısı ekleyerek yeni bir tarih hesaplar.

Args:
    date (str): Başlangıç tarihi (YYYY-MM-DD formatında).
    days (int): Eklenecek gün sayısı.

Returns:
    datetime: Yeni tarih.
  ```
- `time_add_days_and_format(self, date, days)`
  **Docstring:**
  ```
  Belirtilen tarihe gün sayısı ekleyip yeni tarihi istenilen dilde gün adı ile birlikte formatlar.


Args:
    date (str): Başlangıç tarihi (YYYY-MM-DD formatında).
    days (int): Eklenecek gün sayısı.

Returns:
    str: Formatlanmış yeni tarih ve gün adı.
  ```
- `time_is_weekend(self, date)`
  **Docstring:**
  ```
  Bir tarihin hafta sonu olup olmadığını kontrol eder.


Args:
    date (str): Tarih (YYYY-MM-DD formatında).


Returns:
    bool: Hafta sonu ise True, değilse False.
  ```
- `time_is_leap_year(self, year)`
  **Docstring:**
  ```
  Bir yılın artık yıl olup olmadığını kontrol eder.


Args:
    year (int): Yıl.


Returns:
    bool: Artık yıl ise True, değilse False.
  ```
- `time_days_in_month(self, year, month)`
  **Docstring:**
  ```
  Bir ay içindeki gün sayısını döndürür.


Args:
    year (int): Yıl.
    month (int): Ay.


Returns:
    int: Ay içindeki gün sayısı.
  ```
- `time_next_weekday(self, date, weekday)`
  **Docstring:**
  ```
  Bir tarihten sonraki belirli bir günün tarihini döndürür (örneğin, bir sonraki Pazartesi).


Args:
    date (str): Başlangıç tarihi (YYYY-MM-DD formatında).
    weekday (int): Hedef gün (0 = Pazartesi, 1 = Salı, vb.).


Returns:
    datetime: Bir sonraki hedef günün tarihi.
  ```
- `time_todatetime(date)`
  **Docstring:**
  ```
  Bir tarihi datetime türüne çevirir

Args:
    date (str): Tarih (YYYY-MM-DD formatında).


Returns:
    str: Formatlanmış tarih.
  ```
- `time_since(self, past_date)`
  **Docstring:**
  ```
  Belirli bir tarihten geçen yıl, ay, gün, saat, dakika ve saniyeyi hesaplar.

Parametre:
past_date (str): Geçmiş tarih (yyyy-mm-dd HH:MM:SS formatında)

Dönüş:
dict: Geçen yıl, ay, gün, saat, dakika ve saniyeleri içeren sözlük.
  ```
- `time_business_days_between_dates(self, date1, date2)`
  **Docstring:**
  ```
  İki tarih arasındaki iş günü sayısını hesaplar.


Args:
date1 (str): İlk tarih (YYYY-MM-DD formatında).
date2 (str): İkinci tarih (YYYY-MM-DD formatında).


Returns:
    int: İki tarih arasındaki iş günü sayısı.
  ```
- `str_replace_multiple(self, text, replacements)`
  **Docstring:**
  ```
  Verilen metinde çoklu değiştirme işlemi yapar.


Args:
    text (str): Değiştirilecek metin.
    replacements (dict): Değiştirilecek değer çiftleri (anahtar: eski değer, değer: yeni değer).

Returns:
    str: Değiştirilmiş metin.
  ```
- `str_replace_with_last(self, text, values)`
  **Docstring:**
  ```
  Verilen metinde belirtilen tüm değerleri son değer ile değiştirir.


Args:
    text (str): Değiştirilecek metin.
    values (tuple): Değiştirilecek değerler.

Returns:
    str: Değiştirilmiş metin.
  ```
- `list_multiply_by_scalar(self, scalar)`
  **Docstring:**
  ```
  Veri listesindeki her bir elemanı verilen skaler değer ile çarpar.

Parametre:
scalar (int, float): Çarpılacak skaler değer.

Dönüş:
list: Skaler değer ile çarpılmış veri listesi.
  ```
- `list_get_frequency(self, value)`
  **Docstring:**
  ```
  Verilen değerin veri listesinde kaç kez geçtiğini sayar.

Parametre:
value: Sayılacak değer.

Dönüş:
int: Değerin listede kaç kez geçtiği.
  ```
- `list_reverse(self)`
  **Docstring:**
  ```
  Veri listesini tersine çevirir.

Dönüş:
list: Tersine çevrilmiş veri listesi.
  ```
- `list_get_max_value(self)`
  **Docstring:**
  ```
  Veri listesindeki en büyük değeri döner.

Dönüş:
int, float: Veri listesindeki en büyük değer.
  ```
- `list_get_min_value(self)`
  **Docstring:**
  ```
  Veri listesindeki en küçük değeri döner.

Dönüş:
int, float: Veri listesindeki en küçük değer.
  ```
- `dict_filter_by_key(self, key)`
  **Docstring:**
  ```
  Sözlükte veya sözlüklerin bulunduğu listede belirtilen anahtara sahip elemanları filtreler.

Parametreler:
key: Filtreleme yapılacak anahtar.

Dönüş:
dict, list: Filtrelenmiş veri.
  ```
- `dict_get_keys(self)`
  **Docstring:**
  ```
  Sözlükteki veya sözlüklerin bulunduğu listedeki anahtarları döner.

Dönüş:
list: Anahtarlar listesi.
  ```
- `dict_merge(self)`
  **Docstring:**
  ```
  Verilen sözlükleri birleştirir.

Parametreler:
*dicts (dict): Birleştirilecek sözlükler.

Dönüş:
dict: Birleştirilmiş sözlük.
  ```
- `list_filter_greater_than(self, threshold)`
  **Docstring:**
  ```
  Belirtilen eşik değerinden büyük olan öğeleri filtreler.

Parametre:
threshold (int/float): Eşik değer.

Dönüş:
list: Eşik değerinden büyük olan öğeleri içeren liste.
  ```
- `list_filter_less_than(self, threshold)`
  **Docstring:**
  ```
  Belirtilen eşik değerinden küçük olan öğeleri filtreler.

Parametre:
threshold (int/float): Eşik değer.

Dönüş:
list: Eşik değerinden küçük olan öğeleri içeren liste.
  ```
- `list_flatten(self)`
  **Docstring:**
  ```
  Çok katmanlı listeyi tek katmana indirger.

Dönüş:
list: Tek katmanlı liste.
  ```
- `list_sum_values(self)`
  **Docstring:**
  ```
  Listedeki tüm sayısal değerlerin toplamını hesaplar.

Dönüş:
int/float: Listedeki sayısal değerlerin toplamı.
  ```
- `list_average(self)`
  **Docstring:**
  ```
  Listedeki sayısal değerlerin ortalamasını hesaplar.

Dönüş:
float: Listedeki sayısal değerlerin ortalaması. Liste boşsa 0 döner.
  ```
- `list_head(self, n)`
  **Docstring:**
  ```
  Listenin ilk n elemanını döndürür.
Args:
    n (int): Döndürülecek eleman sayısı (varsayılan 5).
Returns:
    list: İlk n eleman.
  ```
- `list_tail(self, n)`
  **Docstring:**
  ```
  Listenin son n elemanını döndürür.
Args:
    n (int): Döndürülecek eleman sayısı (varsayılan 5).
Returns:
    list: Son n eleman.
  ```
- `list_main(self, n)`
  **Docstring:**
  ```
  Listenin ortadaki elemanlarını döndürür.
Eğer listenin uzunluğu 2n veya daha küçükse tüm listeyi döndürür.
Args:
    n (int): Kenarlardan kesilecek eleman sayısı (varsayılan 5).
Returns:
    list: Ortadaki elemanlar.
  ```
- `list_unique_values(self)`
  **Docstring:**
  ```
  Listenin benzersiz elemanlarını döndürür.
Returns:
    list: Benzersiz elemanlar.
  ```
- `list_sort_asc(self)`
  **Docstring:**
  ```
  Listeyi artan sırada sıralar.
Returns:
    list: Artan sırada sıralanmış liste.
  ```
- `list_sort_desc(self)`
  **Docstring:**
  ```
  Listeyi azalan sırada sıralar.
Returns:
    list: Azalan sırada sıralanmış liste.
  ```

## Functions
- `cprint(data, indent)`
  **Docstring:**
  ```
  İç içe veri türlerine göre renklendirme yaparak çıktı verir.

Args:
    data (any): Yazdırılacak veri.
    indent (int): Girinti seviyesi.

Returns:
    None
  ```
- `print_with_indent(string, indent_level)`
- `colorize_numbers(string)`
- `replace_with_color(match)`
- `wrapper()`
- `decorator(func)`
- `wrapper()`
- `wrapper()`
- `wrapper()`
- `decorator(func)`
- `wrapper()`
- `wrapper()`
- `decorator(func)`
- `wrapper()`
- `wrapper()`
- `decorator(func)`
- `wrapper()`
- `wrapper()`
- `decorator(func)`
- `wrapper()`
- `decorator(func)`
- `wrapper()`
- `wrapper()`
- `trace_function(frame, event, arg)`
