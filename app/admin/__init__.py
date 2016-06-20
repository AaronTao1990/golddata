from . import views
from ..models import Video, AsyncTask
from .. import db
import flask_admin

admin = flask_admin.Admin(name='Admin', index_view=views.MyAdminIndexView(), base_template='my_master.html', template_mode='bootstrap2')
#admin.add_view(views.RegistWemediaView(RegistWemedia, db.session))
#admin.add_view(views.CrawlerTaskView(CrawlerTask, db.session))
#admin.add_view(views.UserView(User, db.session))
#admin.add_view(views.ActionsView(Action, db.session))
admin.add_view(views.VideoView(Video, db.session))
admin.add_view(views.AsyncTasksView(AsyncTask, db.session))
