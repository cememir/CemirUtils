from cemirutils import CemirUtilsHTTP

http = CemirUtilsHTTP()


# Mevcut tüm metodların isimlerini yazdır
print(http.get_methods())

get_response = http.get("https://jsonplaceholder.typicode.com/posts/1", verify_ssl=True)
print("GET Response:", get_response)

# POST isteği
post_data = {"title": "foo", "body": "bar", "userId": 1}
post_response = http.post("https://jsonplaceholder.typicode.com/posts", data=post_data, verify_ssl=True)
print("POST Response:", post_response)

# PUT isteği
put_data = {"title": "foo", "body": "bar", "userId": 1}
put_response = http.put("https://jsonplaceholder.typicode.com/posts/1", data=put_data, verify_ssl=True)
print("PUT Response:", put_response)

# DELETE isteği
delete_response = http.delete("https://jsonplaceholder.typicode.com/posts/1", verify_ssl=True)
print("DELETE Response:", delete_response)

# PATCH isteği
patch_data = {"title": "foo"}
patch_response = http.patch("https://jsonplaceholder.typicode.com/posts/1", data=patch_data, verify_ssl=True)
print("PATCH Response:", patch_response)