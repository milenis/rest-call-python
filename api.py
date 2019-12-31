from json.encoder import JSONEncoder
import requests, json

class ApiRequest(object):
	"""Basic Api request with using requests library

	"""
	json_encoder_class = JSONEncoder

	def __init__(self, endpoint):
		self.endpoint = endpoint

	def get(self, headers=None, url_parameters={}):
		return requests.get(
			self.endpoint,
			params=url_parameters,
			headers=headers
		)

	def post(self, headers=None, url_parameters={}, payload={}):
		return requests.post(
			self.endpoint,
			data=json.dumps(payload, cls=self.json_encoder_class),
			params=url_parameters,
			headers=headers
		)

	def put(self, headers=None, url_parameters={}, payload={}):
		return requests.put(
			self.endpoint,
			data=json.dumps(payload, cls=self.json_encoder_class),
			params=url_parameters,
			headers=headers
		)

	def delete(self, headers=None, url_parameters={}):
		return requests.delete(
			self.endpoint,
			params=url_parameters,
			headers=headers
		)

	def options(self, headers=None, url_parameters={}):
		return requests.options(
			self.endpoint,
			params=url_parameters,
			headers=headers
		)

class ApiErrorException(Exception):
	pass

class Api(object):

	def __init__(self, config):
		self.api_key = config['api_key']
		self.endpoint = config['endpoint']
		self.key_list = config['key_list']

	# @classmethod
	def __grab(self, json_results):
		return json_results.get(self.key_list)

	@staticmethod
	def __status(response_json):
		"""Checking the status of response api

		:param response_json:
		:return:
		"""
		if not response_json:
			raise ApiErrorException('Response Api is None, cannot fetch the status of api')

		status = response_json.get('status')

		assert status is not None, \
			'Response Status is not Available'

		assert status.get('code') == requests.codes.ok, \
			'Response status not clear, should be any error occurred: {}'.format(status.get('description'))

	def __get(self, service_endpoint, params=None):
		"""Separate GET request into individual method,
		because it's will be used multiple times, short-code=better

		:param service_endpoint: `str` specific api endpoint
		:param params: `dict` url parameter to include
		:return: `dict` results of returned api
		"""
		req_params = {
			'headers': {
				'Accept': 'application/json',
				'key': self.api_key
			}
		}
		if params is not None:
			req_params['url_parameters'] = params

		api = ApiRequest(endpoint=service_endpoint)
		response = api.get(**req_params)

		return self.__grab(response.json())

	def __post(self, service_endpoint, params=None, payload=None):
		"""Separate POST request into individual method,
		because it's will be used multiple times, short-code=better

		:param service_endpoint: `str` specific api endpoint
		:param params: `dict` url parameter to include
		:return: `dict` results of returned api
		"""
		req_params = {
			'headers': {
				'Accept': 'application/json',
				'key': self.api_key
			}
		}
		if params is not None:
			req_params['url_parameters'] = params

		api = ApiRequest(endpoint=service_endpoint)
		response = api.post(
			headers={
				'key': self.api_key,
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'charset': 'utf8'
			},
			payload=payload
		)
		return self.__grab(response.json())

	@staticmethod
	def __parser(response_json):
		"""Get the actual result of json response

		:param response_json:
		:return:
		"""
		return response_json.get('results') if response_json is not None else None

	def get(self,path):
		"""Get methode

		:return:
		"""
		request = self.__get('{}%s'.format(self.endpoint) %path)

		self.__status(request)

		return self.__parser(request)

	def post(self, path, payload):
		"""POST methode

		:return:
		"""

		request = self.__post('{}%s'.format(self.endpoint) %path, None,payload)

		self.__status(request)

		return self.__parser(request)