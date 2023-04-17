from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in farmley_app/__init__.py
from farmley_app import __version__ as version

setup(
	name="farmley_app",
	version=version,
	description="Farmley Internal Feature Request",
	author="Vishal Dhayagude",
	author_email="vishal.v@farmley.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
