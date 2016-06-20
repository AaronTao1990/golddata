from . import db, login_manager
from flask.ext.login import UserMixin, AnonymousUserMixin
import datetime

class Permission:
    EDIT_TASK = 0x01
    EDIT_USER = 0x02
    ADMINISTER = 0x80

class Signal:
    REGIST_WEMEDIA = 'regist_wemedia'
    DELETE_WEMEDIA = 'delete_wemedia'

    UPDATE_TASK = 'update_task'
    CREATE_TASK = 'create_task'
    DELETE_TASK = 'delete_task'

    LOGIN_USER = 'login_user'
    DELETE_USER = 'delete_user'
    UPDATE_USER = 'update_user'
    ADD_USER = 'add_user'

class Action(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action_name = db.Column(db.String(20))
    time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    model_id = db.Column(db.Integer)
    record = db.Column(db.String(300))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __lt__(self, other):
        return self.permissions < other.permissions

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.EDIT_TASK, True),
            'Moderator': (Permission.EDIT_TASK |
                          Permission.EDIT_USER,
                          False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

    def __unicode__(self):
        return self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))
    actions = db.relationship('Action', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __unicode__(self):
        return self.login

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

class AsyncTaskType:
    TRANSCODING = 0x01
    RETRIVE_DURATION = 0x02
    CAPTURE_SCREEN = 0x03

class AsyncTaskStatus:
    STATUS_IN_PROGRESS = 0x01
    STATUS_SUCCESS = 0x02
    STATUS_FAILED = 0x03

class AsyncTask(db.Model):
    __tablename__ = 'task_async'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    key = db.Column(db.String(100))
    task_id = db.Column(db.String(10), index=True)
    callback = db.Column(db.String(100))
    status = db.Column(db.Integer, default=AsyncTaskStatus.STATUS_IN_PROGRESS)
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())


class VideoType:
    CRAWLER = 0x01
    USER_UPLOAD = 0x02
    RSS = 0x03

class Video(db.Model):
    __tablename__ = 'video'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    title = db.Column(db.String(200))
    content = db.Column(db.String())
    cover = db.Column(db.String(200))
    stream_url = db.Column(db.String(200), index=True)
    web_url = db.Column(db.String(200), index=True)
    posted = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime(timezone=True))
    duration = db.Column(db.Integer)
    vct = db.Column(db.String(200))
    vsct = db.Column(db.String(200))
    h_ceph_url = db.Column(db.String(200))
    h_cloud_url = db.Column(db.String(200))
    h_height = db.Column(db.Integer)
    h_brate = db.Column(db.Integer)
    m_ceph_url = db.Column(db.String(200))
    m_cloud_url = db.Column(db.String(200))
    m_height = db.Column(db.Integer)
    m_brate = db.Column(db.Integer)
    l_ceph_url = db.Column(db.String(200))
    l_cloud_url = db.Column(db.String(200))
    l_height = db.Column(db.Integer)
    l_brate = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    status = db.Column(db.Boolean)

    def get_default_url(self):
        if self.h_cloud_url:
            return self.h_cloud_url
        elif self.m_cloud_url:
            return self.m_cloud_url
        elif self.l_cloud_url:
            return self.l_cloud_url
        else:
            raise Exception('no url found')

login_manager.anonymous_user = AnonymousUser
@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))
