import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEFAULT=None
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'aaron'


    KS3_AK = '/BuBx5t7pKxexhua31BW'
    KS3_SK = 'aEMoLuatE1hUaXVQThry1/NP84iJX1gkUToadqHT'
    KS3_HOST = 'kss.ksyun.com'
    KS3_BUCKET = 'imedia-video'


    USE_PROXY = False
    PROXY_HOST = 'http://proxy2.yidian.com'
    PROXY_PORT = 3038

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-db.sqlite')

    KS3_ASYNC_CB_GETDURATION = 'http://video-service.yidian-inc.com/getdurationcb'
    KS3_ASYNC_CB_TRANSCODE = 'http://video-service.yidian-inc.com/transcodecb'

class TestingConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')
    SQLALCHEMY_ECHO = True

    KS3_ASYNC_CB = 'http://video-service.yidian-inc.com/getdurationcb'

config = {
    'default' : Config,
    'dev' : DevelopmentConfig,
    'testing' : TestingConfig
}
