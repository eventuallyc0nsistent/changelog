from setuptools import setup, find_packages

setup(
    name='changelog',
    version='0.1.0',
    license='BSD',
    description='Create a suggested CHANGELOG from your git repositories logs',
    author='Kiran Koduru',
    author_email='kiranrkoduru@gmail.com',
    keywords="git log changelog python",
    platforms=['Any'],
    packages=find_packages(),
    test_suite='changelog.tests',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'changelog.command_line:main'
        ]
    },
)
