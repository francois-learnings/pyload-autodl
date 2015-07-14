try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

packages = ['autodl', 'autodl.plugins']
data_files = [('/etc/autodl', ['misc/conf/etc/config.json', 
               'misc/conf/etc/user_settings.json.sample'])]

config = {
    'description': 'pyload-autodl',
    'author': 'Francois Billant',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'fbillant@gmail.com',
    'version': '0.2.1',
    'install_requires': ['nose', 'selenium'],
    'packages': packages,
    'data_files': data_files,
    'name': 'autodl',
    'entry_points': {
        'console_scripts': [
            'autodl = autodl.__init__:main'
         ]
    }
}

setup(**config)

