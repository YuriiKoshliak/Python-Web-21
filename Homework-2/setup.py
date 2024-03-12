from setuptools import setup, find_packages


setup(
    name='python-power-project',
    version='0.2',
    description='helper-bot',
    url='None',
    author='Yulia Datsiuk, Yurii Koshliak, Olesya Shevchuk, Daniel Tishakov',
    author_email='None',
    license='MIT',
    packages=find_packages(),
    entry_points={'console_scripts': ['run-helper = src.main:entry_point']}
)