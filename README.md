# Fleet Ansible


## Description
This is an ansible desigined to turn an Enterprise Linux VM into a fleet dm without containers based on the [fleetdm docs](https://fleetdm.com/docs/deploying/upgrading-fleet#install-the-latest-version-of-fleet) with the following modifications

* using percona's build of mysql
* no json logging for the fleet dm service to work better with shift-mon
* fix SELinux errors
* add query packs

## Installation
I need to write docs...


## Support
Please submit an issue to this project if you find any bugs with this role if you fleetdm has successfully been deployed please file issue with fleetdm

## Roadmap
- [ ] write playbook that deploys the software
- [ ] add cool query packs by default
- [ ] see if I can create a CI pipeline for creating installers for all platforms
- [ ] bring your own certificates

## Authors and acknowledgment
Thanks to shift systems for writing the role. If you need a place to store your query results long term look at deploying [shift-mon](https://gitlab.com/shiftsystems/shift-rmm) or contact sales@shiftsystems.net

## License
Apache 2 licensed