from setuptools import setup

setup(name='btstool',
      version='1.0',
      description='BTS script tools (encoding & decoding)',
      author='Magnus Olsson',
      author_email='magnus@minimum.se',
      python_requires='>=3',
      url='https://github.com/blastur/btstool',
      packages=['bts'],
      scripts=['bin/btsdump.py', 'bin/btsgen.py', 'bin/btstest', 'bin/hcidump.py', 'bin/btsdiff.py'],
)
