
__all__ = ["Package"]

import subprocess
from pluto.base import Resource

class DebianPackageProvider(object):
    def install(self, package):
        return self._dpkg("install", package)

    def remove(self, package):
        return self._dpkg("remove", package)

    def purge(self, package):
        return self._dpkg("purge", package)

    def check_installed(self, package):
        return 0 == subprocess.call("dpkg -s %s" % package,
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def _dpkg(self, command, package):
        return subprocess.check_call("apt-get -y %s %s" % (command, package),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

class Package(Resource):
    package_name = ResourceArgument()
    version = ResourceArgument()

    provider = DebianPackageProvider()

    def action_install(self):
        if not self.provider.check_installed(self.real_package_name):
            self.provider.install(self.real_package_name)
            self.changed()

    def action_upgrade(self):
        # TODO: Need to support changed
        self.provider.install(self.real_package_name)

    def action_remove(self):
        if self.provider.check_installed(self.real_package_name):
            self.provider.remove(self.real_package_name)
            self.changed()

    def action_purge(self):
        if self.provider.check_installed(self.real_package_name):
            self.provider.purge(self.real_package_name)
            self.changed()

    @property
    def real_package_name(self):
        return self.package_name or self.name
