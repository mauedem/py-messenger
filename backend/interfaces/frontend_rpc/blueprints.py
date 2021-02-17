from flask import Blueprint

from interfaces.frontend_rpc import views

# Auth Blueprint
auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
auth_blueprint.add_url_rule(
    '/register/', methods=['POST'],
    view_func=views.CreateUserView.as_view(
        'register_user_view'
    )
)
auth_blueprint.add_url_rule(
    '/login/', methods=['POST'],
    view_func=views.AuthorizeUserView.as_view(
        'authorize_user_view'
    )
)
auth_blueprint.add_url_rule(
    '/authenticate/', methods=['POST'],
    view_func=views.AuthenticateUserView.as_view(
        'authenticate_user_view'
    )
)
