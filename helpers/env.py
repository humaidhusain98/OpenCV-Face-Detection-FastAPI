import os
localUrl = os.getenv('localUrl')
prodUrl = os.getenv('prodUrl')
isDev = os.getenv('isDev')

if isDev=="True":
    url = prodUrl
else:
    url = localUrl