from setuptools import setup, find_packages

with open('./README.rst') as readme:
    long_description = readme.read()

setup(
    name='changelog-suggest',
    url='https://github.com/kirankoduru/changelog',
    version='0.1.0',
    license='MIT',
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
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    long_description=long_description
)
