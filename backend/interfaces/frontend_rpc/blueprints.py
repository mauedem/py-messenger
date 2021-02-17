from flask import Blueprint

from interfaces.frontend_rpc import views

# Auth Blueprint
auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
auth_blueprint.add_url_rule(
    '/register/', methods=['POST'],
    view_func=views.RegisterUserView.as_view(
        'register_user_view'
    )
)
