from cemirutils import CemirUtils

data_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, "a", "b", "c"]
cem = CemirUtils(data_list)

print(data_list)  # Orijinal veri listesini yazdırır
print(cem.filter_greater_than(5))  # 5'ten büyük değerleri yazdırır: [9, 6]
print(cem.filter_less_than(4))  # 4'ten küçük değerleri yazdırır: [3, 1, 1, 2, 3]
print(cem.sum_values())  # Değerlerin toplamını yazdırır: 44
print(cem.average())  # Değerlerin ortalamasını yazdırır: 4.0
