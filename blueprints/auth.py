from flask import Blueprint, render_template, request ,redirect, session
from .forms import RegisterForm, LoginForm
from models import UserModel
from exts import db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            username = form.username.data
            user = UserModel(email=email, password=password, username=username)
            db.session.add(user)
            db.session.commit()
            return redirect("/auth/login")
        else:
            print(form.errors)
            return "fail"


@bp.route("/login/confirm", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱不存在")
                return "fail"
            if user.password == password:
                #保存登录信息
                session["user_id"] = user.id
                return redirect("/")
            else:
                print("密码错误")
                return "fail"
        else:
            print(form.errors)
            return "fail——02"

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")