# Created by Alexander Wheadon
# 02/08/17
# Assignment 1

import os
# default config
class BaseConfig(object):
	# debug mode disabled unless changed
	DEBUG = False
	#secret session key
	SECRET_KEY = 'b\'9;6\\xbeKt\\xdcv\\xad6\\x1b\\xd2\\x06Z?\\xe7\\x0ci\\x86\\xe7\\xfc\\x99\\x91S\''
	#Data base location as specified by enviroment variable
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	#disable alchemy track modifications to prevent warning
	SQLALCHEMY_TRACK_MODIFICATIONS = False
#local testing config
class DevelopmentConfig(BaseConfig):
	DEBUG = True
#heroku configuration
class ProductionConfig(BaseConfig):
	DEBUG = False
