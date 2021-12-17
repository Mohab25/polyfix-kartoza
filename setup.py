import setuptools

setuptools.setup(
    name='kartoza_polyfix',
    version='0.1.6.3',
    description='a python package to fix polygon spikes',
    long_description='a python package to fix polygon spikes, built on top of fiona and shapely',
    author='kartoza',
    install_requires=[
        'Fiona>=1.8.20',
        'shapely>=1.8.0'
    ],
    
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),

)
