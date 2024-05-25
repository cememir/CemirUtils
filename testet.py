from cemirutils import CemirUtils

data_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
data_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

ceml = CemirUtils(data_list)
cemd = CemirUtils(data_dict)

# Veri listesinin çıktısını yazdır
print(data_list)

# Bir değerin frekansını bul
print(ceml.get_frequency(2))

# Listeyi tersine çevir
print(ceml.reverse_list())

# Sözlük verisi ile işlemler
try:
    print(ceml.multiply_by_scalar(2))
except TypeError as e:
    print(e)

try:
    print(ceml.get_max_value())
except TypeError as e:
    print(e)

try:
    print(ceml.get_min_value())
except TypeError as e:
    print(e)

# Sözlükte belirli bir anahtar-değer çiftini filtrele
print(cemd.filter_by_key("b", 2))

# Sözlükteki anahtarları al
print(cemd.get_keys())

# Çok katmanlı listeyi düzleştirme işlemi, burada hata beklenir çünkü veri tipi sözlük
try:
    # Çok katmanlı liste oluştur
    nested_list = [[1, 2], [3, 4], [5, 6]]
    cem_nested = CemirUtils(nested_list)
    print(cem_nested.flatten_list())
except TypeError as e:
    print("eee", e)

# Sözlükleri birleştirme işlemi
print(cemd.merge_dicts({'e': 5}, {'f': 6}))
