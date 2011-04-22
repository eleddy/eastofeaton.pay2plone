from setuptools import setup, find_packages

version = '0.1a'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='eastofeaton.pay2plone',
      version=version,
      description="Accept payment and create a plone site",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='plone, zope, e-commerce',
      author='Cris Ewing',
      author_email='cris@crisewing.com',
      url='https://github.com/cewing/eastofeaton.pay2plone',
      license='gpl',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['eastofeaton'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
