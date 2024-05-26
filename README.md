<meta charset="UTF-8">

# CemirUtils

CemirUtils, basit veri işleme işlevlerini içeren bir Python yardımcı kütüphanesidir.

## Kurulum

Öncelikle CemirUtils kütüphanesini Python projesine eklemek için aşağıdaki adımları izleyin:

```bash
pip install cemirutils
````


## Kullanım

Kütüphane, farklı veri işleme işlevlerini sağlayan `CemirUtils` sınıfını içerir. Örneğin:


```python
from cemirutils import CemirUtils

# Mevcut tüm metodların isimlerini yazdır
cemir_utils = CemirUtils(None)
print(cemir_utils.getmethods())


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


data_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
cem = CemirUtils(data_list)
print(data_list)
print(cem.head(2))  # Listenin ilk 5 elemanını yazdırır.
print(cem.tail(4))  # Listenin son 5 elemanını yazdırır.
print(cem.main())  # Listenin ortadaki elemanlarını yazdırır.
print(cem.unique_values())  # Listenin benzersiz elemanlarını yazdırır.
print(cem.sort_asc())  # Listenin artan sırada sıralanmış halini yazdırır.
print(cem.sort_desc())  # Listenin azalan sırada sıralanmış halini yazdırır.
print(data_list)  # Orijinal veri listesini yazdırır
print(cem.filter_greater_than(5))  # 5'ten büyük değerleri yazdırır: [9, 6]
print(cem.filter_less_than(4))  # 4'ten küçük değerleri yazdırır: [3, 1, 1, 2, 3]
print(cem.sum_values())  # Değerlerin toplamını yazdırır: 44
print(cem.average())  # Değerlerin ortalamasını yazdırır: 4.0


## Zaman işlemleri
utils = CemirUtils(None)
print(utils.days_between_dates("2024-05-01", "2024-05-25"))  # 24
print(utils.hours_minutes_seconds_between_times("08:30:00", "15:45:30"))  # (7, 15, 30)
print(utils.time_until_date("2024-05-27 23:59:59"))  # Kalan gün, saat, dakika, saniye
print(utils.add_days_and_format("2024-05-01", 30))  # "2024-05-31 (Cuma)"
print(utils.is_weekend("2024-05-25"))  # True
print(utils.is_leap_year(2024))  # True
print(utils.days_in_month(2024, 2))  # 29
print(utils.next_weekday("2024-05-25", 0))  # 2024-05-27
print(utils.time_since("2022-01-01 00:00:00"))  # (2, 4, 24, 14, 30, 15)
print(utils.business_days_between_dates("2024-05-01", "2024-05-25"))  # 17


# Veri listesindeki her bir elemanı verilen skaler değer ile çarpar.
ceml = CemirUtils([1, 2, 3])
ceml.multiply_by_scalar(2)  # Output: [2, 4, 6]


ceml = CemirUtils([1, 2, 3])
# Veri listesindeki her bir elemanı verilen skaler değer ile çarpar
result = ceml.multiply_by_scalar(2)
print(result)  # Output: [2, 4, 6]


ceml = CemirUtils([1, 2, 3])
# Veri listesindeki en büyük değeri döner.
ceml.get_max_value()  # Output: 3


ceml = CemirUtils([1, 2, 2, 3])
# Verilen değerin veri listesinde kaç kez geçtiğini sayar.
result = ceml.get_frequency(2)
print(result)  # Output: 2


cemd = CemirUtils({'a': 1, 'b': 2, 'c': 3})
# Sözlükteki veya sözlük listesindeki anahtarları döndürür.
cemd.get_keys()  # Output: ['a', 'b', 'c']


ceml = CemirUtils([[1, 2], [3, 4], [5]])
# Çok katmanlı listeyi tek katmana indirger.
ceml.flatten_list()  # Output: [1, 2, 3, 4, 5]

````