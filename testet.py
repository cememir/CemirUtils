from cemirutils import IPGeolocation

ip_geolocator = IPGeolocation()

## CSV -> SQLite
# ip_geolocator.create_sqlite_db()

#
ip_address = "121.0.11.0"
# # IP adresinin lokasyon bilgisini al (Zip dosyasını tekrar indir)
location_info = ip_geolocator.get_ip_location(ip_address, force_download=False)
print(location_info)