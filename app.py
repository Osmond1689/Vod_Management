from flask import Flask,flash,abort,request,redirect,url_for
from flask import render_template
from flask_wtf.csrf import CSRFProtect
#import sys
#sys.path.append('/root/python/ftp-manage')
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user
from form.login_form import LoginForm
import os
from model.checkpasswd import User
app = Flask(__name__)
csrf = CSRFProtect(app)
#创建loginmanager管理类
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)
app.config["SECRET_KEY"] = os.urandom(24)

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route('/login',methods=('GET', 'POST'))
def login():
    form = LoginForm()
    #日志
    # app.logger.info(form.validate_on_submit())
    if form.validate_on_submit():
        user_name = request.form.get('accountNumber', None)
        password = request.form.get('password', None)
    #    app.logger.info(user_name)
        user = User(user_name)
        #print(user)
        if user.verify_password(password):
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
        #    return redirect(url_for('main'))
        else:
            flash(u'用户名或密码有误')
    return render_template('login.html',form=form)   

@app.route('/')
@app.route('/index',methods=['get','post'])
@login_required
def index():
    return render_template('index.html',username=current_user.username)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=80,debug=True)