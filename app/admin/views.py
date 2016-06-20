# -*- coding: utf-8 -*-
import flask_admin
from flask_admin import helpers, expose
import flask_login as login
from flask import url_for, redirect, request
from .forms import LoginForm, RegistrationForm, CreateUserForm, UserEditForm

from ..models import User, Role, Action, Signal
from werkzeug.security import generate_password_hash
from .. import db
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask import flash
from flask_admin.babel import gettext
import datetime
import logging

logger = logging.getLogger(__name__)

from blinker import Namespace
mysignals = Namespace()
action_signal = mysignals.signal('update_signal')

def action_signal_callback(sender, **kwargs):
    action = Action()
    action.user_id = login.current_user.id
    action.action_name = kwargs.get('signal_name')
    action.time = datetime.datetime.now()
    action.model_id = kwargs.get('model').id
    action.record = unicode(kwargs.get('model'))
    db.session.add(action)
    db.session.commit()

action_signal.connect(action_signal_callback)


class MyAdminIndexView(flask_admin.AdminIndexView):

    def __init__(self, *args, **kwargs):
        super(MyAdminIndexView, self).__init__(*args, **kwargs)

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

class VideoView(sqla.ModelView):

    edit_modal = True
    can_create = False
    can_edit = False
    column_exclude_list = []

    column_searchable_list = ['web_url']

    def is_accessible(self):
        return True
        #return login.current_user.can(Permission.EDIT_USER)

class AsyncTasksView(sqla.ModelView):

    edit_modal = True
    can_create = False
    can_edit = False
    column_exclude_list = []

    column_searchable_list = []

    def is_accessible(self):
        return True
        #return login.current_user.can(Permission.EDIT_USER)

'''
class UserView(sqla.ModelView):

    column_exclude_list = ['password']

    column_searchable_list = ['login']

    def is_accessible(self):
        return login.current_user.can(Permission.EDIT_USER)

    def after_model_change(self, form, model, is_created):
        if is_created:
            action_name = Signal.ADD_USER
        else:
            action_name = Signal.UPDATE_USER
        action_signal.send(self, current_user=login.current_user, signal_name=action_name, model=model)

    def get_query(self):
        if login.current_user.can(Permission.ADMINISTER):
            return super(UserView, self).get_query()
        else:
            role = Role.query.filter(Role.name=='User').first()
            return super(UserView, self).get_query().filter(User.role_id == role.id)

    def after_model_delete(self, model):
        action_signal.send(self, current_user=login.current_user, signal_name=Signal.DELETE_USER, model=model)

    def _feed_roles_choice(self, form):
        if login.current_user.is_administrator():
            roles = Role.query.all()
        else:
            roles = Role.query.filter(Role.permissions < login.current_user.role.permissions).all()
        form.role_id.choices = [(str(x.id), x.name) for x in roles]
        return form

    def edit_form(self, obj):
        form = UserEditForm(helpers.get_form_data(), obj=obj)
        return self._feed_roles_choice(form)

    def update_model(self, form, model):
        form.password.data = generate_password_hash(form.password.data)
        return super(UserView, self).update_model(form, model)

    def create_form(self):
        logger.info('in creating user...')
        form = CreateUserForm(helpers.get_form_data())
        self._template_args['form'] = form
        return self._feed_roles_choice(form)

    def create_model(self, form):
        form.password.data = generate_password_hash(form.password.data)
        return super(UserView, self).create_model(form)

class CrawlerTaskView(sqla.ModelView):

    edit_modal = True
    can_create = False
    can_edit = False

    column_searchable_list = ['wemedia_id', 'wemedia_name', 'url', 'wechat_id']

    column_filters = [
        filters.FilterEqual(CrawlerTask.site, 'site', options = (
            ('sogou', u'微信'),
            ('yourong.sogou', u'友荣'),
            ('baijia', u'百度百家'),
            ('toutiao', u'头条'),
            ('dy.qq', u'QQ订阅'),
            ('zhuanlan.sina', u'新浪专栏'),
            ('tech.sina', u'新浪科技'),
            ('blog.sina', u'新浪博客'),
            ('blog.163', u'网易播客'),
            ('yuedu.163', u'网易云阅读'),
            ('blog.sohu', u'搜狐博客'),
            ('mp.sohu', u'搜狐媒体平台'),
            ('ifeng.app', u'凤凰APP'),
            ('wemedia.ifeng', u'凤凰自媒体'),
        )),
        filters.FilterEqual(CrawlerTask.mp, 'mp', options = (
            (1, 'true'),
            (0, 'false')
        )),
        filters.FilterEqual(CrawlerTask.wemedia_name, 'wemedia_name')
    ]

    def is_accessible(self):
        self.can_delete = login.current_user.can(Permission.EDIT_TASK)
        return login.current_user.is_authenticated

    def after_model_change(self, form, model, is_created):
        if is_created:
            action_name = Signal.CREATE_TASK
        else:
            action_name = Signal.UPDATE_TASK
        action_signal.send(self, current_user=login.current_user, signal_name=action_name, model=model)

    def after_model_delete(self, model):
        action_signal.send(self, current_user=login.current_user, signal_name=Signal.DELETE_TASK, model=model)

    #def create_form(self):
    #    logger.info('in creating crawler task...')
    #    form = CreateCrawlerTaskForm(helpers.get_form_data())
    #    self._template_args['form'] = form
    #    return form

    #def create_model(self, form):
    #    site = get_site_for_url(form.url.data)
    #    form.site.data = site
    #    form.url.data = clean_url(form.url.data)
    #    return super(CrawlerTaskView, self).create_model(form)

class ActionsView(sqla.ModelView):

    can_create = False
    can_edit = False
    can_delete = False

    column_filters = [
        'user',
        'action_name',
        'model_id'
    ]

    column_searchable_list = [User.login, 'model_id', 'record']

    def is_accessible(self):
        return login.current_user.can(Permission.ADMINISTER)

    def get_query(self):
        if login.current_user.can(Permission.ADMINISTER):
            return super(ActionsView, self).get_query()
        else:
            return super(ActionsView, self).get_query().filter(Action.user_id==login.current_user.id)

    def get_count_query(self):
        if login.current_user.can(Permission.ADMINISTER):
            return super(ActionsView, self).get_count_query()
        else:
            return super(ActionsView, self).get_count_query().filter(Action.user_id==login.current_user.id)

class RegistWemediaView(sqla.ModelView):

    column_exclude_list = ['summary', 'logo']
    can_edit = False
    can_create = False

    def __init__(self, *args, **kwargs):
        super(RegistWemediaView, self).__init__(*args, **kwargs)
        self.register = Register()

    def is_accessible(self):
        return login.current_user.is_authenticated

    def create_form(self):
        logger.info('in creating regist wemedia...')
        form = RegistWemediaCreateForm(helpers.get_form_data())
        self._template_args['form'] = form
        return form

    def create_model(self, form):
        result, reason_or_id = self.register.regist(media_name=form.wemedia_name.data,
                             media_summary=form.summary.data,
                             media_pic=form.logo.data,
                             web_url=form.url.data)
        if result == 'success':
            form.wemedia_id.data = int(reason_or_id)
        else:
            flash(gettext('Failed to regist user. %(error)s', error=str(reason_or_id)), 'error')
            return False

        return super(RegistWemediaView, self).create_model(form)

    #def delete_model(self, model):
    #    result, reason = self.register.unregist(model.wemedia_id)
    #    if result != 'success':
    #        flash(gettext('Failed to unregist user. %(error)s', error=str(reason)), 'error')
    #        return False
    #    return super(RegistWemediaView, self).delete_model(model)

    def after_model_change(self, form, model, is_created):
        action_name = Signal.REGIST_WEMEDIA
        action_signal.send(self, current_user=login.current_user, signal_name=action_name, model=model)

    def after_model_delete(self, model):
        action_signal.send(self, current_user=login.current_user, signal_name=Signal.DELETE_WEMEDIA, model=model)
'''
