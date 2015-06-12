try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {
    'description': 'autodl',
    'author': 'Francois Billant',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'fbillant@gmail.com',
    'version': '0.1.3',
    'install_requires': ['nose', 'selenium'],
    'packages': ['autodl', 'autodl.plugins'],
    'name': 'autodl',
    'entry_points': {
        'console_scripts': [
            'autodl = autodl.__init__:main'
         ]
    }
}

setup(**config)

