from cemirutils import CemirUtilsHTTP

http = CemirUtilsHTTP()


# Show methods name
print(http.get_methods())


get_response = http.get("https://jsonplaceholder.typicode.com/posts/1", verify_ssl=True)
print("GET Response:", get_response)

# POST
post_data = {"title": "foo", "body": "bar", "userId": 1}
post_response = http.post("https://jsonplaceholder.typicode.com/posts", data=post_data, verify_ssl=True)
print("POST Response:", post_response)

# PUT
put_data = {"title": "foo", "body": "bar", "userId": 1}
put_response = http.put("https://jsonplaceholder.typicode.com/posts/1", data=put_data, verify_ssl=True)
print("PUT Response:", put_response)

# DELETE
delete_response = http.delete("https://jsonplaceholder.typicode.com/posts/1", verify_ssl=True)
print("DELETE Response:", delete_response)

# PATCH
patch_data = {"title": "foo"}
patch_response = http.patch("https://jsonplaceholder.typicode.com/posts/1", data=patch_data, verify_ssl=True)
print("PATCH Response:", patch_response)