# Tripplite Power Alert Device Manager Collection for Ansible
<!-- Add CI and code coverage badges here. Samples included below. -->

<!-- Describe the collection and why a user would want to use it. What does the collection do? -->

## Included Content

<!--start collection content-->
### Modules
|Name                                 | Description                                        |
|-------------------------------------|----------------------------------------------------|
| jeisenbath.tripplite.padm_api       | Interface with Power Alert Device Manager REST API |
| jeisenbath.tripplite.padm_snmp_user | Manage SNMP users                                  |
| jeisenbath.tripplite.padm_dns       | Manage Network DNS servers                         |

## External requirements

<!-- List any external resources the collection depends on, for example minimum versions of an OS, libraries, or utilities. Do not list other Ansible collections here. -->
```bash
pip install -r requirements.yml
```

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install jeisenbath.tripplite
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: jeisenbath.tripplite
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install jeisenbath.tripplite --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `1.0.0`:

```bash
ansible-galaxy collection install jeisenbath.tripplite,v1.0.0
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## More Information

Documentation for the [Power Alert Device Manager API](https://assets.tripplite.com/owners-manual/padm20-api-documentation.html).

## Licensing

<!-- Include the appropriate license information here and a pointer to the full licensing details. If the collection contains modules migrated from the ansible/ansible repo, you must use the same license that existed in the ansible/ansible repo. See the GNU license example below. -->

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Community Code of Conduct

Please see the official [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html#code-of-conduct).

