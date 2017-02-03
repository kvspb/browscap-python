from setuptools import setup, find_packages

setup(
    name='browscap-python',
    version='0.0.14',
    description='Python Browscap Library.',
    url='https://github.com/kvspb/browscap-python',

    author='Valery Komarov',
    author_email='komarov@valerka.net',

    license="BSD License",
    platforms=['any'],

    packages=find_packages(),

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
