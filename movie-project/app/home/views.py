# coding:utf8
from . import home
from flask import render_template, url_for, redirect, flash, session, request, abort
from flask import render_template, redirect, url_for
from app.home.forms import RegisterForm, LoginForm,UserDetailForm
from app.modules import User, UserLog
from app import app, db
from functools import wraps
from werkzeug.utils import secure_filename
import uuid,os,datetime


# 装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function

def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 登陆页面
@home.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if not user.check_pwd(data["pwd"]):
            flash("密码错误", 'err')
            return redirect(url_for("home.login"))
        session["user"] = user.name
        session["user_id"] = user.id
        userlog = UserLog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html", form=form)


@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))  # 注册
@home.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    from werkzeug.security import generate_password_hash
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            email=data["email"],
            phone=data["phone"],
            uuid=uuid.uuid4().hex
        )
        db.session().add(user)
        db.session.commit()
        flash("注册会员成功", 'ok')
    return render_template("home/register.html", form=form)


# 会员中心
@home.route("/user/",methods=['GET','POST'])
@user_login_req
def user():
    form = UserDetailForm()
    user = User.query.get(int(session["user_id"]))
    form.face.validators = []
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        file_face = secure_filename(form.face.data.filename)
        if not os.path.exists(app.config["FC_DIR"]):
            os.makedirs(app.config["FC_DIR"])
            os.chmod(app.config["FC_DIR"], "rw")
        user.face = change_filename(file_face)
        form.face.data.save(app.config["FC_DIR"] + user.face)
        name_count = User.query.filter_by(name=data["name"]).count()
        if data["name"] != user.name and name_count == 1:
            flash("昵称已存在！","err")
            return redirect(url_for())
        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("昵称已存在！", "err")
            return redirect(url_for())
        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"] != user.phone and phone_count == 1:
            flash("昵称已存在！", "err")
            return redirect(url_for())
        user.name = data["name"]
        user.phone = data["phone"]
        user.email = data["email"]
        user.info = data["info"]
        db.session.add(user)
        db.session.commit()
        flash("修改会员信息成功！", "ok")
        return redirect(url_for("home.user"))
    return render_template("home/user.html",form=form)


# 修改密码
@home.route("/pwd/")
@user_login_req
def pwd():
    return render_template("home/pwd.html")


# 评论
@home.route("/comments/")
def comments():
    return render_template("home/comments.html")


# 登陆日志
@home.route("/loginlog/")
def loginlog():
    return render_template("home/loginlog.html")


# 电影收藏
@home.route("/moviecol/")
@user_login_req
def moviecol():
    return render_template("home/moviecol.html")


@home.route("/")
def index():
    return render_template("home/index.html ")


# 动画
@home.route("/animation/")
def animation():
    return render_template("home/animation.html")


# 搜索
@home.route("/search/")
def search():
    return render_template("home/search.html")


# 播放
@home.route("/play/")
def play():
    return render_template("home/play.html")
