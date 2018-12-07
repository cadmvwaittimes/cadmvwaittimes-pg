from distutils.core import setup


setup(
    name='CaDMV',
    version='0.0.1',
    author='Josh Saunders',
    author_email='saunders.josh.work@gmail.com',
    packages=['cadmv', 'cadmv.test', 'cadmv.helper'],
    # scripts=['bin/stowe-towels.py', 'bin/wash-towels.py'],
    # url='http://pypi.python.org/pypi/TowelStuff/',
    # license='LICENSE.txt',
    description='Useful CA DMV-related stuff.',
    # long_description=open('README.txt').read(),
    # install_requires=[
    #     "Django >= 1.1.1",
    #     "caldav == 0.1.4",
    # ],
)
