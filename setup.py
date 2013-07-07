import re
from setuptools import setup
import codecs
import pmpd as pmpd

def long_description():
    """Pre-process the README so that PyPI can render it properly."""
    with codecs.open('README.rst', encoding='utf8') as f:
        rst = f.read()
    code_block = '(:\n\n)?\.\. code-block::.*'
    rst = re.sub(code_block, '::', rst)
    return rst

setup(
    name='pmpd',
    version=pmpd.__version__,
    author=pmpd.__author__,
    author_email='jared@pyscape.com',
    packages=['pmpd'],
    url='http://pypi.python.org/pypi/pmpd/',
    license=pmpd.__licence__,
    description='pmpd [puhmp-eed] is a command line interface to deploy projects that use git.',
    long_description=long_description(),
    entry_points={
        'console_scripts': [
            'pmpd = pmpd.__main__:main',
        ],
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Version Control',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Shells',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ]
)
