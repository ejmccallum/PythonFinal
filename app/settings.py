"""
Settings for the app.
"""

END_POINT = (
    'https://us-west-2.aws.data.mongodb-api.com/'
    'app/data-vzvec/endpoint/data/v1'
)
API_KEY = 'tjxJi07wQZp9QB1u6WUa463MJxvvSXqd0xNymUGFMvYaSTpLxvolHALGIQ76MTqh'
DATA_SOURCE = 'Cluster0'
DB_NAME = 'Gradebook'
COLLECTION = 'Mathmatics'
HEADERS = {'Content-Type': 'application/json',
           'Access-Control-Request-Headers': '*',
           'api-key': f'{API_KEY}'}

PAYLOAD = {
    "collection": COLLECTION,
    "database": DB_NAME,
    "dataSource": DATA_SOURCE
}
