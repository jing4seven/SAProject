# enums for api endpoints:

domain = 'http://localhost:8080/api$s'

API_ENDPOINTS =  {
	'SITE_CLIENT_LIST': domain % '/api/siteclient',
	'SITE_CLIENT': domain % 'api/siteclient/%s',
	'USER_LIST': domain % '/api/user/',
	'USER': domain % '/api/user/%s',
}
