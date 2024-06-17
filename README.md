<meta charset="UTF-8">

# CemirUtils

### Linux ve Pythonda sık kullanılan tüm komut ve kütüphaneleri tek yerden, basit veri işleme işlevlerini içeren bir Python yardımcı kütüphanesidir.

## Kurulum

```bash
wget https://bootstrap.pypa.io/get-pip.py

## PIP Kurulumu
python3.9 get-pip.py pip cemirutils
sudo python3.9 get-pip.py pip cemirutils

## Güncelleme
pip install -U pip cemirutils
python3.9 -m pip install -U pip cemirutils

sudo pip install -U pip cemirutils
sudo python3.9 -m pip install -U pip cemirutils

## Kontrol
pip show cemirutils
pip freeze | grep cemir
````


# Kullanım Örnekleri

## Dekoratörler

```python
from cemirutils import CemirUtilsFunctionNotification

utils = CemirUtilsFunctionNotification(
    smtp_server="mail.makdos.com",
    smtp_port=587,
    smtp_user="notify@makdos.com",
    smtp_password="nope"
)


@utils.notify(to_email="musluyuksektepe@gmail.com", subject="Function Called")
def important_action():
    return {"status": "Important action completed."}


# SMTP sunucusu çalışıyor olmalı
important_action()

```

## Dekoratörler

```python
import time
from datetime import datetime

from cemirutils import CemirUtilsDecorators

@CemirUtilsDecorators.timeit
@CemirUtilsDecorators.log
def timeit_log(x, y):
    time.sleep(1)
    return x + y

timeit_log(3, 5)

# Output: 
# Calling function 'timeit_log' with arguments (3, 5) and keyword arguments {}
# Function 'timeit_log' returned 8
# Function 'timeit_log' took 1.0018 seconds

@CemirUtilsDecorators.retry(retries=5, delay=2)
def may_fail_function():
    if time.time() % 2 < 1:
        raise ValueError("Random failure!")
    return "Success"

may_fail_function()

# Output: 
# Attempt 1 failed: Random failure!
# Attempt 2 failed: Random failure!
# Attempt 3 failed: Random failure!
# Attempt 4 failed: Random failure!
# Attempt 5 failed: Random failure!
# Function 'may_fail_function' failed after 5 attempts

@CemirUtilsDecorators.cache
def slow_function(x):
    time.sleep(2)  # Zaman alacak bir işlem yapalım.
    return x * x

print(slow_function(4))
print(slow_function(4))  # Bu sefer önbellekten sonuç dönecek

# Output: 
# 16
# Returning cached result for slow_function with args (4,) and kwargs {}
# 16

@CemirUtilsDecorators.cache_with_expiry(expiry_time=5)
def cached_function(x):
    time.sleep(3)  # Örnek olarak zaman alacak bir işlem yapalım.
    return x * x

print(datetime.now(), cached_function(4))
time.sleep(1)
print(datetime.now(), cached_function(4))  # Süre dolmuş, tekrar hesaplanacak

# Output: 
# 2024-06-17 13:02:29.906200 16
# Returning cached result for cached_function with args (4,) and kwargs {}
# 2024-06-17 13:02:33.920453 16

@CemirUtilsDecorators.deprecate("Please use new_function instead.")
def old_function(x, y):
    return x + y

old_function(3, 5)

# Output: 
# WARNING: old_function is deprecated. Please use new_function instead.

@CemirUtilsDecorators.debug
def add_numbers(a, b):
    return a + b

add_numbers(3, 5)

# Output: 
# DEBUG: Calling function 'add_numbers' with arguments (3, 5) and keyword arguments {}
# DEBUG: Function 'add_numbers' returned 8

@CemirUtilsDecorators.before_after
def test_beforeafter(data):
    print(f"1 Performing database operation with data: {data}")
    return "2 Success"

print(test_beforeafter("Muslu Y."))

# Output: 
# Starting transaction
# 1 Performing database operation with data: Muslu Y.
# Committing transaction
# 2 Success


#  max_call = Belirli bir zaman dilimi içinde bir fonksiyonun kaç kez çağrılabileceğini belirtir.
#  period = Örneğin, period=10 olarak ayarlandığında, 10 saniyelik bir süre içinde max_call sayısınca (örn: 5) fonksiyon çağrısına izin verilir.
@CemirUtilsDecorators.rate_limit(max_calls=5, period=10)
def limited_function():
    return {"status": "ok"}


# Test the rate-limited function
try:
    print(datetime.now(), limited_function())
    print(datetime.now(), limited_function())
    print(datetime.now(), limited_function())
    time.sleep(4)
    print(datetime.now(), limited_function())  # This call should succeed
    print(datetime.now(), limited_function())
    print(datetime.now(), limited_function())
    print(datetime.now(), limited_function())  # This call should raise a rate limit error
except RuntimeError as e:
    print(e)

#Output:

# 2024-06-17 13:19:42.270686 {'status': 'ok'}
# 2024-06-17 13:19:42.270686 {'status': 'ok'}
# 2024-06-17 13:19:42.270686 {'status': 'ok'}
# 2024-06-17 13:19:46.281105 {'status': 'ok'}
# 2024-06-17 13:19:46.281105 {'status': 'ok'}
# Rate limit exceeded
```


## Email göndermek, dosya eklemek


```python
from cemirutils import CemirUtilsEmail

# Kullanım
email_util = CemirUtilsEmail(
    smtp_host="smtp.gmail.com",
    smtp_port=465,
    smtp_user="musluyuksektepe@gmail.com",
    smtp_pass="nopass",
    smtp_ssl=True
)

email_util.send_email(
    to_email="cememir2017@gmail.com",
    subject="Test Subject",
    body_html="<html><body><h1>This is a test email in HTML.</h1></body></html>",
    attachments=["2024.pdf", "not_found.log"],
    zip_files=False  # Dosyaları zipleyip eklemek için
)

```


## Tetiklenen uygun koşulların satır numaralarını ve koşul ifadelerini göster

```python
from cemirutils import CemirUtilsConditions

cemir_utils = CemirUtilsConditions()

@cemir_utils.condition_collector
def test_function(x, y, z):
    if x > 15:
        # print("x is greater than 15")
        pass
    elif x < 15 and y > 10:
        # print("x is less than 15 and y is greater than 10")
        pass
    else:
        # print("x is not within the expected range or y is not greater than 10")
        pass

    if y == 20:
        # print("y is exactly 20")
        pass
    elif y >= 15:
        # print("y is greater than or equal to 15")
        pass
    else:
        # print("y is less than 15")
        pass

    if z == "hello":
        # print("z is 'hello'")
        pass
    elif z == "world":
        # print("z is 'world'")
        pass
    else:
        # print("z is something else")
        pass

    if x == 10:
        # print("x is 10")
        pass
    elif x >= 10:
        # print("x is greater than or equal to 10")
        pass
    else:
        # print("x is less than 10")
        pass

    if y % 2 == 0:
        # print("y is even")
        pass
    else:
        # print("y is odd")
        pass

    if z.startswith("hq"):
        # print("z starts with 'h'")
        pass
    elif z.startswith("w"):
        # print("z starts with 'w'")
        pass
    else:
        # print("z starts with another letter")
        pass


test_function(10, 20, "hello")

# Output:
# x is less than 15 and y is greater than 10
# y is exactly 20
# z is 'hello'
# x is 10
# y is even
# z starts with another letter

# Line 10: elif x < 15 and y > 10:
# Line 15: if y == 20:
# Line 22: if z == "hello":
# Line 29: if x == 10:
# Line 36: if y % 2 == 0:
# Line 45: else:
```


## IPGeolocation işlemleri.

```python
from cemirutils import IPGeolocation

ip_geolocator = IPGeolocation()

## CSV -> SQLite
# ip_geolocator.create_sqlite_db()

#
ip_address = "121.0.11.0"
# # IP adresinin lokasyon bilgisini al (Zip dosyasını tekrar indir)
location_info = ip_geolocator.get_ip_location(ip_address, force_download=False)
print(location_info)
```

## PostgreSQL için CRUD işlemleri.
```python
from datetime import datetime
from cemirutils import CemirPostgreSQL

utils = CemirPostgreSQL(dbname='test_db3', dbhost='127.0.0.1', dbuser='postgres', dbpassword='', dbport=5435, dbcreate_db_if_not_exists=True)

# print(utils.psql_create_table('test_table_flat', 'id SERIAL PRIMARY KEY, name VARCHAR(100), surname VARCHAR(100)'))
# print(utils.psql_create_table('test_table_json', 'id SERIAL PRIMARY KEY, dates DATE, content JSONB'))

# print(utils.psql_insert('test_table_flat', ('id', 'name', 'surname'), (3, 'Muslu', 'Yüksektepe'), get_id=True))
print(utils.insert('test_table_json', ('id', 'dates', 'content'), (2, datetime.now(), {"age": 40, "city": "İzmir"}), get_id=True))
print(utils.read('test_table_json'))

print(utils.update('test_table_json', {'dates': datetime.now(), 'content': '{"age": 40, "city": "Sivas"}'}, 'id = 1', get_id=True))
print(utils.read('test_table_json'))

asd = utils.read(table_name='test_table_json', columns="content", condition="content ->> 'age' = '40'")
# asd = utils.read(table_name='test_table_json', columns="content", condition="content ->> 'age' like '%4%'")
print(type(asd), asd)

# asdd = Dict2Dot(asd[0])
# print(type(asd), asdd.id)


print(utils.delete('test_table_json', 'id = 1'))
print(utils.read('test_table_json'))
```



## Kütüphane, farklı veri işleme işlevlerini sağlayan `CemirUtils` sınıfını içerir.


### Linux komutlarını Python üzerinden çağırarak işlem yapmak için kullanılır.
```python
from cemirutils import CemirUtils
utils = CemirUtils()

# Dosya ve dizinleri listeleme örneği
print(utils.linux_ls("."))


# Dosya oluşturma örneği
print(utils.linux_touch("new_file.txt"))

# Dosyayı gzip ile sıkıştırma örneği
print(utils.linux_gzip("new_file.txt"))

# Dosya içeriğini görüntüleme örneği
print(utils.linux_cat("new_file.txt"))

# Dosya kopyalama örneği
print(utils.linux_cp("new_file.txt", "destination.txt"))

# Dosya taşıma örneği
print(utils.linux_mv("new_file.txt", "/tmp/"))

# Dosya silme örneği
# print(utils.linux_rm("new_file.txt"))

# Yeni bir dizin oluşturma örneği
print(utils.linux_mkdir("new_directory"))

# Boş bir dizini silme örneği
print(utils.linux_rmdir("new_directory"))

# Dosyadan alanları ayırma örneği
print(utils.linux_cut("\t", "1,3", "data.txt"))


# Dizin içinde dosya arama örneği
print(utils.linux_find("/", "new_file.txt"))

# Dosyada desen arama örneği
print(utils.linux_grep("a", "new_file.txt"))
```

## HTTP istek örnekleri

```python
from cemirutils import CemirUtils

# Mevcut tüm metodların isimlerini yazdır
cemir_utils = CemirUtils(None)
print(cemir_utils.get_methods())


get_response = cemir_utils.http_get("https://jsonplaceholder.typicode.com/posts/1", verify_ssl=True)
print("GET Response:", get_response)

# POST isteği
post_data = {"title": "foo", "body": "bar", "userId": 1}
post_response = cemir_utils.http_post("https://jsonplaceholder.typicode.com/posts", data=post_data, verify_ssl=True)
print("POST Response:", post_response)

# PUT isteği
put_data = {"title": "foo", "body": "bar", "userId": 1}
put_response = cemir_utils.http_put("https://jsonplaceholder.typicode.com/posts/1", data=put_data, verify_ssl=True)
print("PUT Response:", put_response)

# DELETE isteği
delete_response = cemir_utils.http_delete("https://jsonplaceholder.typicode.com/posts/1", verify_ssl=True)
print("DELETE Response:", delete_response)

# PATCH isteği
patch_data = {"title": "foo"}
patch_response = cemir_utils.http_patch("https://jsonplaceholder.typicode.com/posts/1", data=patch_data, verify_ssl=True)
print("PATCH Response:", patch_response)

```

## List ve Dict işlemleri

```python
from cemirutils import CemirUtils

data_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
cem = CemirUtils(data_list)
print(data_list)
print(cem.list_head(2))  # Listenin ilk 5 elemanını yazdırır.
print(cem.list_tail(4))  # Listenin son 5 elemanını yazdırır.
print(cem.list_main())  # Listenin ortadaki elemanlarını yazdırır.
print(cem.list_unique_values())  # Listenin benzersiz elemanlarını yazdırır.
print(cem.list_sort_asc())  # Listenin artan sırada sıralanmış halini yazdırır.
print(cem.list_sort_desc())  # Listenin azalan sırada sıralanmış halini yazdırır.
print(cem.list_filter_greater_than(5))  # 5'ten büyük değerleri yazdırır: [9, 6]
print(cem.list_filter_less_than(4))  # 4'ten küçük değerleri yazdırır: [3, 1, 1, 2, 3]
print(cem.list_sum_values())  # Değerlerin toplamını yazdırır: 44
print(cem.list_average())  # Değerlerin ortalamasını yazdırır: 4.0


ceml = CemirUtils([[1, 2], [3, 4], [5]])
# Çok katmanlı listeyi tek katmana indirger.
print(ceml.list_flatten())  # Output: [1, 2, 3, 4, 5]


ceml = CemirUtils([1, 2, 3])
# Veri listesindeki her bir elemanı verilen skaler değer ile çarpar
print(ceml.list_multiply_by_scalar(2))  # Output: [2, 4, 6]


ceml = CemirUtils([1, 2, 3])
# Veri listesindeki en büyük değeri döner.
print(ceml.list_get_max_value())  # Output: 3


ceml = CemirUtils([1, 2, 2, 3])
# Verilen değerin veri listesinde kaç kez geçtiğini sayar.
print(ceml.list_get_frequency(2)) # Output: 2


# Sözlükteki veya sözlük listesindeki anahtarları döndürür.
data = [{'a': 1}, {'b': 2}, {'a': 3}, {"name": "sivas", "age": 10}]
cemd = CemirUtils(data)

print(cemd.dict_get_keys())
print(cemd.dict_filter_by_key('name'))
print(cemd.dict_merge({'a': 1}, {'b': 2}))
```

## Zaman işlemleri

```python
from cemirutils import CemirUtils

utils = CemirUtils(None)
print(utils.time_days_between_dates("2024-05-01", "2024-05-25"))  # 24
print(utils.time_hours_minutes_seconds_between_times("08:30:00", "15:45:30"))  # (7, 15, 30)
print(utils.time_until_date("2024-05-27 23:59:59"))  # Kalan gün, saat, dakika, saniye
print(utils.time_add_days_and_format("2024-05-01", 30))  # "2024-05-31 (Cuma)"
print(utils.time_is_weekend("2024-05-25"))  # True
print(utils.time_is_leap_year(2024))  # True
print(utils.time_days_in_month(2024, 2))  # 29
print(utils.time_next_weekday("2024-05-25", 0))  # 2024-05-27
print(utils.time_since("2022-01-01 00:00:00"))  # (2, 4, 24, 14, 30, 15)
print(utils.time_business_days_between_dates("2024-05-01", "2024-05-25"))  # 17


````



PING/ICMP takip ve dbye kayıt ettirmek.

```shell
sudo nano /usr/bin/ping_logger.py

from cemirutils import CemirUtils
utils = CemirUtils(data=False, dbname='test_db3', dbuser='postgres', dbpassword='asd', dbport=5435, dbcreate_db_if_not_exists=True)
utils.tcp_listen_for_icmp(print_query=True, insert_db=True)
```

```shell
sudo nano /etc/systemd/system/ping_logger.service

[Unit]
Description=Ping Logger Service
After=network.target

[Service]
ExecStart=/usr/bin/python3.9 /usr/bin/ping_logger.py
WorkingDirectory=/usr/bin/
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
```

```shell
sudo chmod +x /usr/bin/ping_logger.py
sudo systemctl daemon-reload
sudo systemctl enable ping_logger
sudo systemctl restart ping_logger
sudo systemctl status ping_logger
journalctl -xe
```
