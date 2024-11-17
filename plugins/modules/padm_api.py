#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Josh M. Eisenbath <j.m.eisenbath@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: padm_api
short_description: Make an HTTP request to a PADM API
description:
    - Make an HTTP request to a Tripplite Poweralert device running the PADM API.
version_added: "1.0.0"
author:
    - "Josh Eisenbath (@jeisenbath)"
options:
    uri:
        description: The API URI to send the request.
        required: true
        type: str
    method:
        description: HTTP Method to send to URI.
        default: get
        type: str
        choices:
            - get
            - patch
            - post
            - delete
    data:
        description:
            - Data to post/patch to chosen URI.
            - Required when I(method=patch) or I(method=put).
        type: dict
extends_documentation_fragment:
    - jeisenbath.tripplite.padm_auth_options
requirements:
    - requests
'''

EXAMPLES = r'''
---
- name: Get API info from /api/devices
  jeisenbath.tripplite.padm_api:
    poweralert_endpoint: "{{ padm_device_fqdn }}"
    username: "{{ tripplite_username }}"
    password: "{{ tripplite_password }}"
    uri: /api/devices
    method: get
  delegate_to: localhost
'''

RETURN = r'''
response_code:
    description: HTTP response code of API request.
    returned: always
    type: str
data:
    description: Returned data from API request.
    returned: always
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jeisenbath.tripplite.plugins.module_utils.padm import Tripplite, tripplite_argument_spec


def main():
    argument_spec = tripplite_argument_spec()
    argument_spec.update(
        method=dict(required=False, choices=['get', 'post', 'patch', 'delete'], default='get'),
        uri=dict(required=True, type='str'),
        data=dict(required=False, type='dict'),
    )
    module = AnsibleModule(
        argument_spec,
        required_if=[
            ('method', ['post', 'patch'], ['data'])
        ]
    )

    tripplite = Tripplite(module.params['poweralert_endpoint'], module.params['api_version'])
    changed = False
    try:
        token, refresh_token = tripplite.get_auth_token(module.params['username'], module.params['password'])
    except Exception as auth_exception:
        module.fail_json(msg='Failed to authenticate. Exception: {0}'.format(str(auth_exception)))

    try:
        if module.params['method'] == 'get':
            response_code, response_data = tripplite.api_get(module.params['uri'], token)
        elif module.params['method'] == 'post':
            response_code, response_data = tripplite.api_post(module.params['uri'], token, module.params['data'])
        elif module.params['method'] == 'patch':
            response_code, response_data = tripplite.api_patch(module.params['uri'], token, module.params['data'])
        elif module.params['method'] == 'delete':
            response_code, response_data = tripplite.api_delete(module.params['uri'], token)
        changed = True
    except Exception as PadmException:
        module.fail_json(msg='PADM API failure: {0}'.format(PadmException))

    tripplite.log_out(refresh_token)
    module.exit_json(changed=changed, response_code=response_code, data=response_data)


if __name__ == "__main__":
    main()
