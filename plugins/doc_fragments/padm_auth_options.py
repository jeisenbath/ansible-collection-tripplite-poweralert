# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Josh M. Eisenbath <j.m.eisenbath@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r"""
options:
    poweralert_endpoint:
        description: 
          - The IP address or FQDN of the Tripplite Poweralert device.
          - If not defined in the task, the value of E(POWERALERT_ENDPOINT) will be used instead.
        required: false
        type: str
    username:
        description: 
          - The username for the Tripplite Poweralert device.
          - If not defined in the task, the value of E(POWERALERT_USERNAME) will be used instead.
        required: false
        type: str
    password:
        description: 
          - The password to authenticate with to the Tripplite Poweralert device.
          - If not defined in the task, the value of E(POWERALERT_PASSWORD) will be used instead.
        required: false
        type: str
    api_version:
        description: The API version of the Tripplite Poweralert device.
        required: false
        default: "1.0.0"
        type: str
"""
