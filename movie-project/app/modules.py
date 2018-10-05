# coding:utf8
from datetime import datetime
from app import db


# 用户模型
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机
    info = db.Column(db.String(100), unique=True)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间
    uuid = db.Column(db.DATETIME, unique=True)  # 唯一标识符
    userlogs = db.relationship('UserLog', backref="user")  # 会员日志外键关系
    comments = db.relationship('Comment', backref="user")  # 评论外键关联关系
    moviecols = db.relationship('Moviecol', backref="user")  # 收藏外键关联关系

    def __repr__(self):
        return "<User %r>" % self.name


# 日志模型
class UserLog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    user_id = db.Column(db.INTEGER, db.ForeignKey("user.id"))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return "<UserLog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.DATE)  # 放映时间
    length = db.Column(db.String(100))  # 播放时间
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间
    comments = db.relationship("Comment", backref="movie")  # 评论外键关联关系
    moviecols = db.relationship("Moviecol", backref="movie")  # 收藏外键关联关系
    tag = db.relationship("Tag", backref="movie")  # 标签外键关联关系

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 上映预告
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 标题
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 上映预告
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 角色列表
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否是管理员账号
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))  # 是否是管理员账号
    adminlogs = db.relationship("Adminlog", backref="admin")  # 管理员登陆日志外键关联关系
    oplogs = db.relationship("Oplog", backref="admin")  # 管理员操作日志外键关联关系
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间
    role = db.relationship("Role",backref="admin")

    def __repr__(self):
        return "<Admin %r>" % self.name

    # 定义密码验证函数
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash  # 由于密码是加密的，所以要引入相应的加密函数
        return check_password_hash(self.pwd, pwd)


# 管理员登陆日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))  # 所属管理员
    ip = db.Column(db.String(100))  # 登陆ip
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 管理员登陆日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.INTEGER, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))  # 所属管理员
    ip = db.Column(db.String(100))  # 登陆ip
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


if __name__ == "__main__":
    # db.create_all()
    """
      role = Role(
        name="超级管理员",
        auths=""
    )
    db.session.add(role)
    db.session.commit()
    """
    from werkzeug.security import generate_password_hash

    admin = Admin(
        name="miacheng",
        pwd=generate_password_hash("123321"),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()
