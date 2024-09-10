from flask import Flask ,session ,g
from flask_sqlalchemy import SQLAlchemy
import config
from exts import db
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from models import UserModel
from flask_migrate import Migrate

app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

#cooike身份验证
@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)

#在模板中注册user对象
@app.context_processor
def my_context_processor():
    return {'user': g.user}


if __name__ == '__main__':
    app.run()
