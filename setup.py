from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in accounts/__init__.py
from accounts import __version__ as version

setup(
	name="accounts",
	version=version,
	description="An acccounting app using Frappe framework",
	author="Summayya",
	author_email="summayya@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
