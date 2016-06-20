# -*- coding: utf-8 -*-
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
import flask_login as login
import logging
import logging.handlers
from logging import Formatter

db = SQLAlchemy()
login_manager = login.LoginManager()


def init_log():
    # logging初始化工作
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # nor的初始化工作

    # 添加TimedRotatingFileHandler到nor
    # 定义一个1分钟换一次log文件的handler
    filehandler = logging.handlers.TimedRotatingFileHandler(
            "log/video_service.log", 'D', 1, 0)
    filehandler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
            ))
    # 设置后缀名称，跟strftime的格式一样
    filehandler.suffix = "%Y%m%d-%H%M.log"
    root_logger.addHandler(filehandler)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #from .tasks import tasks as tasks_blueprint
    #app.register_blueprint(tasks_blueprint, url_prefix='/tasks')

    from .admin import admin
    admin.init_app(app)

    init_log()

    return app

