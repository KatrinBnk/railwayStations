from .stations import stations_bp
from .trains import trains_bp
from .login import login_bp
from .register import register_bp, register_admin_bp, register_staff_bp
from .book_ticket import booking_bp, confirm_booking_bp
from .return_ticket import return_bp, confirm_return_bp
from .tickets import ticket_details_bp, view_tickets_bp
from .seats import seats_bp

from backend.routes.admin import register_blueprints_admin

def register_blueprints(app):
    app.register_blueprint(stations_bp)
    app.register_blueprint(trains_bp)
    app.register_blueprint(seats_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(register_admin_bp)
    app.register_blueprint(register_staff_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(return_bp)
    app.register_blueprint(confirm_booking_bp)
    app.register_blueprint(confirm_return_bp)
    app.register_blueprint(view_tickets_bp)
    app.register_blueprint(ticket_details_bp)

    register_blueprints_admin(app)



