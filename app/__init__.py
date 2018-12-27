from flask import Flask

create_app = Flask(__name__)
create_app.config['SECRET_KEY'] = "uudye78tgde6refs55w7iwtsj"

from app.api.v1.views.user_views import user_mod
from app.api.v1.views.question_views import v1_mod

create_app.register_blueprint(user_mod, url_prefix="/api/v1/auth")
create_app.register_blueprint(v1_mod, url_prefix="/api/v1")
