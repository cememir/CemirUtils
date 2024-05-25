from cemirutils import CemirUtils

cemir_utils = CemirUtils(None)  # Veri kullanmadan örnek oluşturduk

# GET isteği
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
patch_response = cemir_utils.http_patch("https://jsonplaceholder.typicode.com/posts/1", data=patch_data,
                                        verify_ssl=True)
print("PATCH Response:", patch_response)

