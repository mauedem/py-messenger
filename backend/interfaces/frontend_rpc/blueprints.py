from flask import Blueprint

from interfaces.frontend_rpc import views

# Auth Blueprint
auth_blueprint = Blueprint('auth', __name__, url_prefix='/private_api/auth')
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
auth_blueprint.add_url_rule(
    '/logout/', methods=['POST'],
    view_func=views.LogoutUserView.as_view(
        'logout_user_view'
    )
)

# Telegram Blueprint
tg_blueprint = Blueprint('tg', __name__, url_prefix='/private_api/tg')
tg_blueprint.add_url_rule(
    '/authorize/', methods=['POST'],
    view_func=views.TelegramAuthorizeUserView.as_view(
        'telegram_authorize_user_view'
    )
)
tg_blueprint.add_url_rule(
    '/dialogs/', methods=['GET'],
    view_func=views.TelegramGetUserDialogsView.as_view(
        'telegram_get_user_dialogs_view'
    )
)
tg_blueprint.add_url_rule(
    '/messages/', methods=['GET'],
    view_func=views.TelegramGetDialogMessagesView.as_view(
        'telegram_get_dialog_messages_view'
    )
)
tg_blueprint.add_url_rule(
    '/get_photo/', methods=['GET'],
    view_func=views.TelegramGetPhotoView.as_view(
        'telegram_get_photo_view'
    )
)
tg_blueprint.add_url_rule(
    '/send_message/', methods=['POST'],
    view_func=views.TelegramSendMessageView.as_view(
        'telegram_send_messages_view'
    )
)
