# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Josh M. Eisenbath <j.m.eisenbath@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
from ansible.module_utils.basic import env_fallback

try:
    import requests
    HAS_REQUESTS = True
    requests.packages.urllib3.disable_warnings()
except ImportError:
    HAS_REQUESTS = False
except Exception:
    raise Exception


def tripplite_argument_spec():
    return dict(
        poweralert_endpoint=dict(fallback=(env_fallback, ['POWERALERT_ENDPOINT']), required=False, type='str'),
        username=dict(fallback=(env_fallback, ['POWERALERT_USERNAME']), required=False, no_log=True, type='str'),
        password=dict(fallback=(env_fallback, ['POWERALERT_PASSWORD']), required=False, no_log=True, type='str'),
        api_version=dict(required=False, default='1.0.0')
    )


class Tripplite:

    def __init__(self, poweralert_endpoint, apiVersion):
        self.apiVersion = apiVersion
        self.poweralert_endpoint = poweralert_endpoint
        self.authHeaders = {"Accept-Version": self.apiVersion, "Content-Type": 'application/vnd.api+json'}
        self.authUrl = "https://{0}/api/oauth/token".format(self.poweralert_endpoint)
        self.logoutUrl = "https://{0}/api/oauth/token/logout".format(self.poweralert_endpoint)

    def get_auth_token(self, username, password):
        authdata = {'username': username, 'password': password, 'grant_type': 'password'}
        authdatajson = json.dumps(authdata)
        response = requests.post(self.authUrl, headers=self.authHeaders, data=authdatajson, verify=False)

        responsejson = json.loads(response.text)
        authtoken = responsejson['access_token']
        refreshtoken = responsejson['refresh_token']

        return authtoken, refreshtoken

    def log_out(self, token):
        apiheaders = {
            "Accept-Version": self.apiVersion,
            "Content-Type": 'application/vnd.api+json',
            "Authorization": "Bearer {0}".format(token)
        }

        logout = requests.post(self.logoutUrl, headers=apiheaders, verify=False)

        return logout.status_code, json.loads(logout.text)

    def _create_headers(self, token):
        apiheaders = {
            "Accept-Version": self.apiVersion,
            "Content-Type": 'application/vnd.api+json',
            "Authorization": "Bearer {0}".format(token),
            "By": 'name'
        }
        return apiheaders

    def api_post(self, uri, token, data):
        headers = self._create_headers(token)
        url = "https://{0}{1}?validation=false".format(self.poweralert_endpoint, uri)
        jsondata = json.dumps(data, indent=4)

        r = requests.post(url, headers=headers, verify=False, data=jsondata)

        return r.status_code, json.loads(r.text)

    def api_patch(self, uri, token, data):
        headers = self._create_headers(token)
        url = "https://{0}{1}?validation=false".format(self.poweralert_endpoint, uri)
        jsondata = json.dumps(data, indent=4)

        r = requests.patch(url, headers=headers, verify=False, data=jsondata)

        return r.status_code, json.loads(r.text)

    def api_get(self, uri, token):
        headers = self._create_headers(token)
        url = "https://{0}{1}?validation=false".format(self.poweralert_endpoint, uri)

        r = requests.get(url, headers=headers, verify=False)

        return r.status_code, json.loads(r.text)

    def api_delete(self, uri, token):
        headers = self._create_headers(token)
        url = "https://{0}{1}?validation=false".format(self.poweralert_endpoint, uri)

        r = requests.delete(url, headers=headers, verify=False)

        return r.status_code, json.loads(r.text)
