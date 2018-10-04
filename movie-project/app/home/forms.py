# coding:utf8
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired,EqualTo,Email,Regexp

class RegisterForm(FlaskForm):
    """会员注册表单"""
    name = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称")
        ],
        description="昵称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入昵称！",
            # "required": 'required'
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱"),
            Email("邮箱格式不正确")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入邮箱！",
            # "required": 'required'
        }
    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机号"),
            Regexp("1[3458]\\d[9]",message="手机格式不正确")
        ],
        description="手机",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入手机号！",
            # "required": 'required'
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            # "required": 'required'
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )
