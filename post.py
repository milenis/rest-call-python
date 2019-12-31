from api import Api

api = Api({'api_key':'apikey','endpoint':'https://endpoint.com','key_list':'data'})
post_data = {
	u"name": "Andi",
	u"city": "Klaten"
}
post = api.post('/path',post_data)
print(post)