from setuptools import setup, find_packages

setup(
    name='changelog',
    url='https://github.com/kirankoduru/changelog',
    version='0.1.0',
    license='BSD',
    description='Create a suggested CHANGELOG from your git repos logs',
    author='Kiran Koduru',
    author_email='kiranrkoduru@gmail.com',
    keywords="git log changelog python",
    packages=find_packages(),
    test_suite='changelog.tests',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'changelog=changelog.command_line:main'
        ]
    },
)
