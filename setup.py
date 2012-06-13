from setuptools import setup

setup(
    name='django-facebook',
    version='2.0',
    description="Facebook integration with Django",
    long_description=open('README.markdown').read(),
    author='Alex Leigh',
    author_email='leigh@atomatica.com',
    url='https://github.com/atomatica/django-facebook',
    packages=['facebook'],
    package_dir={'facebook': 'facebook'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
