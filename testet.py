from cemirutils import CemirUtils

data_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
cem = CemirUtils(data_list)
print(data_list)
print(cem.head(2))  # Listenin ilk 5 elemanını yazdırır.
print(cem.tail(4))  # Listenin son 5 elemanını yazdırır.
print(cem.main())  # Listenin ortadaki elemanlarını yazdırır.
print(cem.unique_values())  # Listenin benzersiz elemanlarını yazdırır.
print(cem.sort_asc())  # Listenin artan sırada sıralanmış halini yazdırır.
print(cem.sort_desc())  # Listenin azalan sırada sıralanmış halini yazdırır.
