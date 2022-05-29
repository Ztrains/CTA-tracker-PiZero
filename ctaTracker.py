import os
import json

import requests


# API docs: https://www.transitchicago.com/developers/ttdocs/
cta_api_key = os.environ.get('CTA_API_KEY')
cta_api_url = 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={}&outputType=JSON'.format(cta_api_key)

belmont_map_id = 41320
southport_map_id = 40360

belmont_stop_id_north_red = 30255
belmont_stop_id_south_red = 30256
belmont_stop_id_north_bp = 30257
belmont_stop_id_south_bp = 30258

southport_stop_id_north = 30070
southport_stop_id_south = 30071

api_url_with_mapid = '{}&mapid={}'.format(cta_api_url, belmont_map_id)

response = requests.get(api_url_with_mapid)
json_response = json.loads(response.text)
ctatt = json_response['ctatt']

eta = ctatt['eta']
eta0 = eta[0]
#print(f'eta1 length: {len(eta0)}')
stpDe0 = eta0['stpDe']
arrT0 = eta0['arrT']

#print(f'eta1: {eta0}\n\n')
print(f'stpDe1: {stpDe0}')
print(f'Arrival Time: {arrT0}')
