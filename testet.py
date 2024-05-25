from cemirutils import CemirUtils

cemir_utils = CemirUtils(None)  # Veri kullanmadan örnek oluşturduk

cemir_utils.http_server(port=35581, ip='127.0.0.1', ssl_cert=None, ssl_key=None, username='admin', password='12345', directory='C:\\Users\\cemem\\Downloads\\')
