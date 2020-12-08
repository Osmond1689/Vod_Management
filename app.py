from flask import Flask,flash,abort,request,redirect,url_for,render_template,Response,send_from_directory
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, login_required,LoginManager, current_user,logout_user
from form.login_form import LoginForm
from form.upload_form import UploadForm
import os,json,time
from model.checkpasswd import User
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
app = Flask(__name__)
csrf = CSRFProtect(app)
#创建loginmanager管理类
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)
app.config["SECRET_KEY"] = os.urandom(24)
homepath=r"D:/app/Vod_Management/vod/"
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
        #app.logger.info(user_name )
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
@app.route('/index')
@login_required
def index():
    return render_template('index.html',username=current_user.username)
#文件管理ifram页面
@login_required
@app.route('/wjgl',methods=['GET', 'POST'])
def wjgl():
    form=UploadForm(CombinedMultiDict([request.form,request.files]))
    if request.method == "GET":
        return render_template('wjgl.html',form=form)
    elif form.validate():
        # 获取提交文件的数据
        #video_file = form.video_file.data
        for video_file in request.files.getlist('video_file'):

        # image_file.filename 是文件的名字
        #print(image_file.filename)

        # 获得文件的后缀
            file_name = secure_filename(video_file.filename)
        #print(file_name)

        # 保存文件到 images 文件夹
        # save(文件路径)
            video_file.save(f'{homepath}/{current_user.username}/{file_name}')

        flash('上传成功','success')
    else:
        flash('上传失败','danger')
    return redirect(url_for('wjgl'))
#文件查找，显示目录
@login_required
@app.route('/wjcz')
def wjcz():
    userpath=homepath+current_user.username
    filename=os.listdir(userpath)
    if current_user.username=='ICB':
        playpath='https://icbvod.yzbabyu.com/'+current_user.username
    else:
        playpath='https://vod.yzbabyu.com/'+current_user.username
    wjlb={}
    wjxq=[]
    for x in filename:
        wjxq.append({ "wjname":x,"wjsize":os.path.getsize(userpath+'/'+x),"wjtime":time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getctime(userpath+'/'+x))),"wjplay":playpath+'/'+x})
    wjlb['data']=wjxq
    return Response(json.dumps(wjlb), mimetype='application/json')
#文件上传
@login_required
@app.route('/wjsc')
def wjsc():
    pass
#密码修改
# @login_required
# @app.route('/mmxg')
# def mmxg():
#     return User.passwordxg('!QAZ2wsx')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)