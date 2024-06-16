from cemirutils.utils import IPGeolocation

ip_geolocator = IPGeolocation()

## CSV -> SQLite
# ip_geolocator.create_sqlite_db()

#
ip_address = "185.122.202.210"
# # IP adresinin lokasyon bilgisini al (Zip dosyasını tekrar indir)
location_info = ip_geolocator.get_ip_location(ip_address, force_download=False)
print(location_info)