class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENVIRONMENT = 'Development'
    DEBUG = True

class Development(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kitgiana@127.0.0.1:5432/july_payroll'  # dbtype://user:password@host:port/dab_name
    ENVIRONMENT = 'Development'
    SECRET_KEY = 'kmkldcc898f7cnck09fmiackm09'
    DEBUG = True

class Testing(Config): # Staging
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kitgiana@127.0.0.1:5432/july_payroll'  # dbtype://user:password@host:port/dab_name
    ENVIRONMENT = 'Development'
    SECRET_KEY = 'kmkldcc898f7cnck09fmiackm09'
    DEBUG = False

class Production(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://hikrnkqcvqgymz:78a1ed0cacb382c504f1e3c204084d2b45a6ccec1d8fe0153ff122ef7c876e41@ec2-75-101-131-79.compute-1.amazonaws.com:5432/dcndq7vpb5rtae'  # dbtype://user:password@host:port/dab_name
    DEBUG = False
    ENVIRONMENT = 'Production'
    SECRET_KEY = 'kmkldcc898f7cnck09fmiackm09'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
