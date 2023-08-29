import configparser
import requests
import sys

config = configparser.ConfigParser()
config.read('config.ini')
auth_header = {
    'X-Emby-Authorization': 'MediaBrowser Client="Jellyfin Web", Device="LibSwitcher", DeviceId="'
                            + config['c']['device_id'] + '", Token="' + config['c']['token'] + '"'}
user_url = 'http://' + config['c']['server'] + '/Users/' + config['c']['user']
r = requests.get(user_url, headers=auth_header)
print(r.status_code)
user_settings = r.json()
if config['c']['library'] in user_settings['Policy']['EnabledFolders']:
    user_settings['Policy']['EnabledFolders'].remove(config['c']['library'])
if len(sys.argv) == 2 and sys.argv[1] == 'restore':
    user_settings['Policy']['EnabledFolders'].append(config['c']['library'])

r = requests.post(user_url + '/Policy',
                  headers={**auth_header, 'Content-Type': 'application/json'},
                  json=user_settings['Policy']
                  )
print(r.status_code)
