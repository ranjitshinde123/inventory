import requests
# import pandas as pd
import json

d=input("enter the ")
url = ("http://sheet.gstincheck.co.in/check/16b30b08fa1fb7a99d49cf16fcb935cc/"+d)

r = requests.get(url)
a=r.json()
e=a['flag']
print(e)
if e==True:
    b = a['data']['lgnm']
    c = a['data']['pradr']['adr']
    print('Name:', b)
    print("address:", c)
else:
    print("GST Number is invalid Please Fill valid GST Number")