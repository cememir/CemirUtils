class CemirUtils:
    def __init__(self, data):
        """
        CemirUtils sınıfının yapıcı fonksiyonu.
        Verilen veriyi sınıfın 'data' değişkenine atar ve sadece int ve float olanları filtreler.

        Parametre:
        data (list): İşlenecek veri listesi.
        """
        self.data = [x for x in data if isinstance(x, (int, float))]

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

