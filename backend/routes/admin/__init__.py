from .dates import dates_bp
from .delete_user import delete_user_bp
from .register_staff import register_staff_bp
from .stations import stations_bp
from .stops import stops_bp
from .trains import train_bp

def register_blueprints_admin(app):
    app.register_blueprint(dates_bp, url_prefix='/admin')
    app.register_blueprint(delete_user_bp, url_prefix='/admin')
    app.register_blueprint(register_staff_bp, url_prefix='/admin')
    app.register_blueprint(stations_bp, url_prefix='/admin')
    app.register_blueprint(stops_bp, url_prefix='/admin')
    app.register_blueprint(train_bp, url_prefix='/admin')