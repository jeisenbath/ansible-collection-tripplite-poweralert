#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Josh M. Eisenbath <j.m.eisenbath@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: padm_snmp_user
short_description: Manages SNMP users for a Tripplite Poweralert device
description:
    - Manages SNMP v2 users for a Tripplite Poweralert device running PADM API.
    - Creates or removes, enables or disabled users and manages their community string.
version_added: 1.0.0
author:
    - "Josh Eisenbath (@jeisenbath)"
options:
    state:
        description: Determine if the managed user is present or absent.
        required: true
        type: str
        choices:
            - present
            - absent
    snmp_user:
        description: SNMP Username to manage.
        required: true
        type: str
    snmp_community:
        description: SNMP v2 Community string to configure for the snmp user.
        type: str
    update_community:
        description:
            - Whether or not the community string should be updated.
        type: bool
        required: false
        default: false
    enabled:
        description: Determine if the managed snmp user is enabled/disabled.
        type: bool
extends_documentation_fragment:
    - jeisenbath.tripplite.padm_auth_options
requirements:
    - requests
'''

EXAMPLES = r'''
---
- name: Add and enable a user
  jeisenbath.tripplite.padm_snmp_user:
    poweralert_endpoint: "{{ padm_device_fqdn }}"
    username: "{{ tripplite_username }}"
    password: "{{ tripplite_password }}"
    state: present
    snmp_user: "{{ snmp_v2_user }}"
    snmp_community: "{{ snmp_v2_ro_community_string }}"
    enabled: true
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
        state=dict(required=True, choices=['present', 'absent']),
        snmp_user=dict(required=True, type='str'),
        snmp_community=dict(required=False, type='str'),
        update_community=dict(required=False, type='bool', default=False),
        enabled=dict(required=False, type='bool'),
    )
    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ['snmp_community', 'enabled'])
        ]
    )

    tripplite = Tripplite(module.params['poweralert_endpoint'], module.params['api_version'])
    changed = False
    response_code = ""
    response_data = {}
    try:
        token, refresh_token = tripplite.get_auth_token(module.params['username'], module.params['password'])
    except Exception as auth_exception:
        module.fail_json(msg='Failed to authenticate. Exception: {0}'.format(str(auth_exception)))

    user_url = '/api/snmpv1v2users/{0}'.format(module.params['snmp_user'])
    get_user_resp, get_user_data = tripplite.api_get(user_url, token)
    if module.params['state'] == 'present':
        if get_user_resp == 200:
            if (
                (get_user_data['data']['attributes']['enabled'] and not module.params['enabled']) or
                (not get_user_data['data']['attributes']['enabled'] and module.params['enabled']) or
                module.params['update_community']
            ):
                params = {
                    "data": {
                        "type": "snmpv1v2users",
                        "attributes": {
                            "community": module.params['snmp_community'],
                            "enabled": module.params['enabled']
                        }
                    }
                }
                if not module.check_mode:
                    response_code, response_data = tripplite.api_patch(
                        "{0}?username={1}".format(user_url, module.params['snmp_user']), token, params
                    )
                changed = True
        elif get_user_resp == 404:  # 404 == user not found
            params = {
                "data": {
                    "type": "snmpv1v2users",
                    "attributes": {
                        "proto": "SNMP_PROTOCOL_V2",
                        "community": module.params['snmp_community'],
                        "name": module.params['snmp_user'],
                        "role": "Manager",
                        "enabled": module.params['enabled'],
                        "ip": "",
                        "mask": "",
                        "contact": "",
                        "description": ""
                    }
                }
            }
            if not module.check_mode:
                response_code, response_data = tripplite.api_post('/api/snmpv1v2users', token, params)
            changed = True
    elif module.params['state'] == 'absent':
        if get_user_resp == 200:
            if not module.check_mode:
                response_code, response_data = tripplite.api_delete('/api/snmpv1v2users/{0}'.format(module.params['snmp_user']), token)

            changed = True

    tripplite.log_out(refresh_token)
    module.exit_json(changed=changed, response_code=response_code, data=response_data, getuser_resp=get_user_resp, getuser=get_user_data)


if __name__ == "__main__":
    main()
