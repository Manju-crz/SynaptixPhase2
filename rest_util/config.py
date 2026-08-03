"""
REST API Configuration - Base URLs and Global Settings
"""
BASE_URLS = {
    'JSONPLACEHOLDER': 'https://jsonplaceholder.typicode.com',
    'HTTPBIN': 'https://httpbin.org',
    'PETSTORE': 'https://petstore.swagger.io/v2',
    'REQRES': 'https://reqres.in/api',
}
TIMEOUTS = {
    'CRUD': 30,
    'FILE_UPLOAD': 120,
    'FILE_DOWNLOAD': 180,
    'REPORT_GENERATION': 180,
    'ANALYTICS': 120,
    'BATCH_OPERATIONS': 300,
    'DEFAULT': 30
}
DEFAULT_TIMEOUT = TIMEOUTS['DEFAULT']

DEFAULT_HEADERS = {
    'Accept': 'application/json',
    'User-Agent': 'Synaptix-RestClient/1.0'
}

VERIFY_SSL = True