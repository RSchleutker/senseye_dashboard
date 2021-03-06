from setuptools import find_packages, setup

setup(
    name='senseye_dashboard',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_wtf',
        'flask_table',
        'bokeh'
    ],
)