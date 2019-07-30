class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kitgiana@127.0.0.1:5432/july_payroll'  # dbtype://user:password@host:port/dab_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENVIRONMENT = 'Development'
    DEBUG = True

class Development(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kitgiana@127.0.0.1:5432/july_payroll'  # dbtype://user:password@host:port/dab_name
    ENVIRONMENT = 'Development'
    DEBUG = True

class Testing(Config): # Staging
    DEBUG = False

class Production(Config):
    SQLALCHEMY_DATABASE_URI = ''  # dbtype://user:password@host:port/dab_name
    DEBUG = False
    ENVIRONMENT = 'Production'



