#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Josh M. Eisenbath <j.m.eisenbath@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: padm_dns
short_description: Manages DNS servers for a Tripplite Poweralert device
description:
    - Manages the network config DNS servers for a Tripplite Poweralert device running PADM API.
version_added: 1.2.0
author:
    - "Josh Eisenbath (@jeisenbath)"
options:
    manual_dns:
        description: Enable or disable statically defined DNS servers.
        type: bool
        required: false
    primary_dns:
        description: The primary DNS server.
        type: str
        required: false
    secondary_dns:
        description: The secondary DNS server.
        type: str
        required: false
    tertiary_dns:
        description: The tertiary DNS server.
        type: str
        required: false
    apply:
        description:
            - Send a POST to /api/apply_changes to apply changes and restart.
            - Recommended to set to I(apply=false) and notify a handler if configuring multiple changes.
        type: bool
        required: false
        default: True
extends_documentation_fragment:
    - jeisenbath.tripplite.padm_auth_options
requirements:
    - requests
'''

EXAMPLES = r'''
---
- name: Update static DNS servers
  jeisenbath.tripplite.padm_dns:
    poweralert_endpoint: "{{ padm_device_fqdn }}"
    username: "{{ tripplite_username }}"
    password: "{{ tripplite_password }}"
    manual_dns: true
    primary_dns: 127.0.0.1
    secondary_dns: 8.8.8.8
    tertiary_dns: 8.8.4.4
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
        manual_dns=dict(required=False, type='bool'),
        primary_dns=dict(required=False, type='str'),
        secondary_dns=dict(required=False, type='str'),
        tertiary_dns=dict(required=False, type='str'),
        apply=dict(required=False, type='bool', default=True),
    )
    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )

    tripplite = Tripplite(module.params['poweralert_endpoint'], module.params['api_version'])
    changed = False
    response_code = ""
    response_data = {}
    try:
        token, refresh_token = tripplite.get_auth_token(module.params['username'], module.params['password'])
    except Exception as auth_exception:
        module.fail_json(msg='Failed to authenticate. Exception: {0}'.format(str(auth_exception)))

    dns_url = '/api/network_config/dns'
    get_dns_resp, get_dns_data = tripplite.api_get(dns_url, token)
    if get_dns_resp == 200:
        dns_attributes = {}

        if module.params['manual_dns'] is not None and module.params['manual_dns'] != get_dns_data['data']['attributes']['manual_dns']:
            dns_attributes['manual_dns'] = module.params['manual_dns']
        if module.params['primary_dns'] and module.params['primary_dns'] != get_dns_data['data']['attributes']['primary_dns']:
            dns_attributes['primary_dns'] = module.params['primary_dns']
        if module.params['secondary_dns'] and module.params['secondary_dns'] != get_dns_data['data']['attributes']['secondary_dns']:
            dns_attributes['secondary_dns'] = module.params['secondary_dns']
        if module.params['tertiary_dns'] and module.params['tertiary_dns'] != get_dns_data['data']['attributes']['tertiary_dns']:
            dns_attributes['tertiary_dns'] = module.params['tertiary_dns']

        if dns_attributes:
            changed = True
            if not module.check_mode:
                params = {
                    "data": {
                        "type": "dns",
                        "id": "dns",
                        "attributes": dns_attributes,
                    }
                }
                response_code, response_data = tripplite.api_patch(dns_url, token, params)
                get_dns_resp, get_dns_data = tripplite.api_get(dns_url, token)
                if module.params['apply']:
                    tripplite.api_post('/api/apply_changes', token, {})

    tripplite.log_out(refresh_token)
    module.exit_json(changed=changed, response_code=response_code, data=get_dns_data)


if __name__ == "__main__":
    main()
