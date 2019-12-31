from api import Api

api = Api({'api_key':'apikey','endpoint':'endpoint','key_list':'data'})
get = api.get('/path')
print(get)