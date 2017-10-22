from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='nirdizati.encoders',
      version='0.1',
      description='Encoders for Nirdizati training',
      long_description=readme(),
      url='https://github.com/nirdizati/nirdizati-encoders',
      author='TKasekamp',
      packages=['nirdizati.encoders'],
      install_requires=['pandas==0.19.2', 'numpy==1.12.0', 'untangle==1.1.0'],
      zip_safe=False)
