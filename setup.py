#coding=utf-8
from setuptools import setup, find_packages, Extension

setup(  
    name = "Web", 
    version = "1.1", 
    keywords = ("Web",), 
    description = "light Web framework", 
    long_description = "light Web framework",
    license = "MIT Licence", 
    
    url = "https://github.com/vtheno/lightWeb", 
    author = "vtheno", 
    author_email = "a2550591@gmail.com", 
    
    packages = find_packages(), 
    include_package_data = True, 
    platforms = "any", 
    setup_requires = ['setuptools','cython'],
    install_requires = [], 
    scripts = [], 
    entry_points = { } ,
    ext_modules = [
        Extension('Web.parse',sources=["ext/parse.pyx"]),
    ],
) 
