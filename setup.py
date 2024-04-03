from setuptools import setup

setup(
    name='fast-deploy',
    version='0.1',
    py_modules=['fast_deploy'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        fast-deploy=fast_deploy:cli
    ''',
)
