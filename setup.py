from setuptools import setup, find_packages


def parse_requirements(file):
    required = []

    with open(file) as f:
        for req in f.read().splitlines():
            if not req.strip().startswith('#'):
                required.append(req)
    return required


requirements = parse_requirements('requirements.txt')
long_description = "pySpot helps to pass through the captive portals in public Wi-Fi networks"

setup(
    name="pySpot",
    version="0.1",
    description="Public Wi-Fi HotSpot ByPass",
    long_description=long_description,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS'
        'Topic :: Utilities',
        'Topic :: Security',
    ],

    packages=find_packages(),
    install_requires=requirements,

    python_requires='>3.11',

    scripts=['pySpot.py'],
)