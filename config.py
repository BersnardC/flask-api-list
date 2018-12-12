# config.py


class Config(object):

    """
    Commo configurations
    """

    pass


class DevelopmentConfig(Config):

    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = False
    ASSETS_DEBUG = True
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 50
    
class ProductionConfig(Config):

    """
    Production configurations
    """

    DEBUG = False
    ASSETS_DEBUG = False
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 50


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
