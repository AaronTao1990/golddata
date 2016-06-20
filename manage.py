# -*- coding: utf-8 -*-
import os
from flask.ext.script import Manager, Shell
from app import create_app
from app import db
from flask.ext.migrate import Migrate, MigrateCommand
from app.models import Video

app = create_app(os.getenv('FLASK_CONFIG') or 'dev')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    """run deploy tasks"""
    from flask.ext.migrate import upgrade

    upgrade()

@manager.command
def tornado(host, port):
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(int(port))
    IOLoop.instance().start()

@manager.command
def post_article(count):
    from aaron.post_article import ArticlePoster
    from utils.accounts import Accounts

    accounts = Accounts('accounts.txt')
    post_article = ArticlePoster()
    for video in db.session.query(Video).filter(Video.posted==False).limit(int(count)):
        url = video.get_default_url()
        wemedia_data = accounts.get_random_account(video.vct, video.vsct)
        item = {
            'ks3_key' : url.replace('http://imedia-video.kss.ksyun.com/', ''),
            'ks3_url' : url,
            'poster_url' : video.cover,
            'wemedia_name' : wemedia_data[0],
            'wemedia_id' : wemedia_data[1],
            'web_url' : video.web_url,
            'duration' : video.duration,
            'vct' : 'vct//' + video.vct,
            'vsct' : 'vsct//' + video.vsct,
            'title' : video.title,
            'content' : video.content,
            'meta' : ['vct//' + video.vct, 'vsct//' + video.vsct]
        }
        post_article.post_article(item)
        video.posted=True
        db.session.commit()

if __name__ == '__main__':
    manager.run()
