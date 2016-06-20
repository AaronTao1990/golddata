# -*- coding: utf-8 -*-
from utils.netcall import fetch_html
import json
from optparse import OptionParser
import urllib

class UserValidator(object):

    def __init__(self):
        self.api_find_user_by_id = 'http://10.111.0.207:9100/users/get-by-id?is_admin=1&id=%s'
        self.check_user_api = 'http://10.111.0.207:9100/users/check-media-name?media_name=%s'
        self.search_user_api = 'http://10.111.0.207:9100/users/search-users?media_name=%s'

    def is_valid_user_by_id(self, wemedia_id):
        url = self.api_find_user_by_id % wemedia_id
        resp = fetch_html(url)
        try:
            data = json.loads(resp)
        except Exception:
            return False
        else:
            if data.get('status') != 'success':
                return False
            user = data.get('result', {}).get('user_info', {})
            if user.get('type') not in [1, 4]:
                return False
            return True

    def is_user_exists(self, wemedia_name):
        resp = fetch_html(self.check_user_api % urllib.quote(wemedia_name))
        try:
            data = json.loads(resp)
            if data['result']['is_exist'] == 'true':
                return True
            else:
                return False
        except Exception:
            return False

    def get_media_id_by_name(self, wemedia_name):
        resp = fetch_html(self.search_user_api % urllib.quote(wemedia_name))
        data = None
        try:
            data = json.loads(resp)
        except Exception:
            return None
        ids = []
        for user in data.get('result', {}).get('users', []):
            if wemedia_name.decode('utf-8') == user.get('media_name') and user.get('status') in [1, 2] and user.get('type') in [1,2,3,4,5]:
                ids.append(user.get('id'))
        if len(ids) == 1:
            return ids[0]
        else:
            return None

    def get_media_name_by_id(self, wemedia_id):
        url = self.api_find_user_by_id % wemedia_id
        resp = fetch_html(url)
        try:
            data = json.loads(resp)
        except Exception:
            return None
        else:
            if data.get('status') != 'success':
                return None
            user = data.get('result', {}).get('user_info', {})
            if user.get('type') not in [1, 4]:
                return None
            return user.get('media_name')

def get_user_id_by_media_name(wemedia_name):
    user_validator = UserValidator()
    print user_validator.get_media_id_by_name(wemedia_name)


def main(wemedia_name, wemedia_id,args):
    get_user_id_by_media_name(wemedia_name)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-i', '--id', dest='wemedia_id',
                      default='9894',
                      help='wemedia id')
    parser.add_option('-n', '--name', dest='wemedia_name',
                      default='麦子熟了',
                      help='wemedia name')
    (options, args) = parser.parse_args()
    main(options.wemedia_name, options.wemedia_id, args)
