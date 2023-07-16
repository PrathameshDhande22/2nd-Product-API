""" Example of API """

import json
import requests

url = "https://twondproductapi.onrender.com/api/v1"
""" body = {
    "name": "python request",
    "email": "python@gmail.com",
    "phoneno": 1234567890,
    "age": 21,
    "address": "Gokuldham Society",
    "city": "Dadar",
    "state": "Maharashtra",
    "pincode": 400001,
    "password": "request",
}

jsonbody=json.dumps(body)


# register yourself
data = requests.post(url + "/register", data=jsonbody) """

params = {"email": "python@gmail.com", "password": "request"}

# login yourself
data = requests.get(url + "/login", params=params)

accesstoken = data.json()["Access Token"]


# view all products
products = requests.get(url + "/prod")

print(products.json())

# view yourself
myself = requests.get(url + "/me", headers={"Authorization": accesstoken})
print(myself.json())
