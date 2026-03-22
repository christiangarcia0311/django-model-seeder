'''
Django Model Seeder
-------------------

A Django library powered by Data Seed PH for generating realistic, 
synthetic Philippine-based datasets directly into Django models

Information
-----------
@author: Christian G. Garcia
@github: github.com/christiangarcia0311/django-model-seeder
'''

from .seeder import ModelSeeder
from .loaders import BulkModelLoader
from .config_parser import ConfigParser

__version__ = '3.1.0'
__all__ = ['ModelSeeder', 'BulkModelLoader', 'ConfigParser']
