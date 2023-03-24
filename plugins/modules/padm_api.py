#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Josh M. Eisenbath <j.m.eisenbath@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
'''

EXAMPLES = r''' # '''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tripplite.poweralert.plugins.module_utils.padm import Tripplite, tripplite_argument_spec


def main():
    argument_spec = tripplite_argument_spec
    argument_spec.update(
        method=dict(required=False, choices=['get', 'post', 'patch'], default='get'),
        uri=dict(required=True, type='str'),
        data=dict(required=False, type='dict', default={}),
    )
    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
        required_if=[
            ('method', ['post', 'patch'], ['data'])
        ]
    )

    tripplite = Tripplite(module.params['poweralert_endpoint'], module.params['api_version'])
    try:
        token, refresh_token = tripplite.get_auth_token(module.params['username'], module.params['password'])
    except Exception as auth_exception:
        module.fail_json(msg='Failed to authenticate. Exception: {0}'.format(str(auth_exception)))

    if module.params['method'] == 'get':
        status, response_data = tripplite.api_get(module.params['uri'], token)
        tripplite.log_out(refresh_token)
        module.exit_json(changed=True, response_code=status, data=response_data)
    elif module.params['method'] == 'post':
        status, response_data = tripplite.api_post(module.params['uri'], token, module.params['data'])
        tripplite.log_out(refresh_token)
        module.exit_json(changed=True, response_code=status, data=response_data)
    elif module.params['method'] == 'patch':
        status, response_data = tripplite.api_patch(module.params['uri'], token, module.params['data'])
        tripplite.log_out(refresh_token)
        module.exit_json(changed=True, response_code=status, data=response_data)

    tripplite.log_out(refresh_token)
    module.exit_json(changed=False)


if __name__ == "__main__":
    main()
