from setuptools import setup, find_packages
from distutils.version import StrictVersion
from importlib import import_module


def readme():
    with open('README.md') as f:
        return f.read()

extras = {
    'Numpy': ('numpy', '1.9', None),
    'MatPlot': ('matplotlib', '1.5', None),
    'SciPi': ('scipy', '0.15', None),
    'qcodes': ('qcodes', '0.1', None),
    'scikit-image': ('skimage', '0.11', 'scikit-image'),
    'pandas': ('pandas', '0.15', None),
    'attrs': ('attr', '16.2.0', 'attrs'),
    'h5py': ('h5py', '0.1', None),
}
extras_require = {k: '>='.join(v[0:2]) for k, v in extras.items()}

print('packages: %s' % find_packages())

setup(name='qtt',
      version='0.1.3',
      use_2to3=False,
      author='Pieter Eendebak',
      author_email='pieter.eendebak@tno.nl',
      maintainer='Pieter Eendebak',
      maintainer_email='pieter.eendebak@tno.nl',
      description='Python-based framework for analysis and tuning of quantum dots',
      long_description=readme(),
      url='http://qutech.nl',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering'
      ],
      license='Private',
      # if we want to install without tests:
      # packages=find_packages(exclude=["*.tests", "tests"]),
      packages=find_packages(),
      requires=['numpy', 'matplotlib', 'scipy', 'qcodes', 'pandas', 'attrs', 'qtpy', 'nose'], install_requires=[
          'numpy>=1.10',
          'scipy',
          'IPython>=0.1',
          'qcodes>=0.1.3'
          # nose is only for tests, but we'd like to encourage people to run tests!
          #'nose>=1.3',
      ],
      extras_require=extras_require,
      zip_safe=False,
      )

version_template = '''
*****
***** package {0} must be at least version {1}.
***** Please upgrade it (pip install -U {0}) in order to use {2}
*****
'''

missing_template = '''
*****
***** package {} not found
***** Please install it in order to use {}
*****
'''

# now test the versions of extras
for extra, (module_name, min_version, pip_name) in extras.items():
    try:
        module = import_module(module_name)
        if StrictVersion(module.__version__) < StrictVersion(min_version):
            print(version_template.format(module_name, min_version, extra))
    except ImportError:
        print(missing_template.format(module_name, extra))
