==================================
Jeisenbath.Tripplite Release Notes
==================================

.. contents:: Topics

v1.2.0
======

Release Summary
---------------

Released 2025-01-30

Major Changes
-------------

- padm_dns module added to manage network static dns servers

New Modules
-----------

- jeisenbath.tripplite.padm_dns - Manages DNS servers for a Tripplite Poweralert device.

v1.1.0
======

Release Summary
---------------

Released 2024-11-17

Major Changes
-------------

- Add api_delete function to support absent state
- Add idempotence, check mode support, absent state to padm_snmp_user
- padm_api module - Add delete choice for method option

Bugfixes
--------

- Remove check mode support from padm_api

v1.0.1
======

Release Summary
---------------

Released 2024-07-22

Bugfixes
--------

- corrected import paths after changing collection namespace

v1.0.0
======

Release Summary
---------------

Released 2023-03-23

Major Changes
-------------

- Added module padm_api
- Added module padm_snmp_user

New Modules
-----------

- jeisenbath.tripplite.padm_api - Make an HTTP request to a PADM API.
- jeisenbath.tripplite.padm_snmp_user - Manages SNMP users for a Tripplite Poweralert device.
