from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import RadioField
from wtforms import BooleanField
from wtforms import DecimalField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange
from wtforms.validators import IPAddress


class PkForm(FlaskForm):
    pk1 = StringField(validators=[DataRequired()])
    pk2 = StringField(validators=[DataRequired()])
    submit = SubmitField(label='launch')


class LoginForm(FlaskForm):
    # username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    email = EmailField('邮箱', validators=[DataRequired()])
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    repeat = PasswordField('重复密码', validators=[DataRequired()])
    submit = SubmitField('注册')


class setting_safe_form(FlaskForm):
    # username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    repeat = PasswordField('重复密码', validators=[DataRequired()])
    submit = SubmitField('保存本页设置')


class setting_network_form(FlaskForm):
    wifi_name = StringField('WIFI接入点名称', validators=[DataRequired()])
    wifi_method = SelectField('WIFI加密方式', choices=[('1', 'WPA / WPA2'), ('2', 'WEP')])
    wifi_password = PasswordField('WIFI密码', validators=[DataRequired()])
    ip_address = StringField('IP地址', validators=[IPAddress()])
    submit = SubmitField('保存本页设置')


class setting_switch_form(FlaskForm):
    # fan_speed = SelectField('风扇速度', choices=[(1,1), (2,2), (2,3), (2,4), (2,5)])
    fan_switch = BooleanField(' ')
    pm25_switch = BooleanField(' ')
    thermometer_switch = BooleanField(' ')
    host_switch = BooleanField(' ')
    # oled_dispaly = DecimalField('屏幕显示时间', validators=NumberRange(min=1, max=60))

    submit = SubmitField('保存本页设置')


class setting_reset_form(FlaskForm):
    submit = SubmitField('重置')
