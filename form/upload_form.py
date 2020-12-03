from flask_wtf import FlaskForm
#from wtforms import FileField 
from flask_wtf.file import FileAllowed,FileField
from wtforms import SubmitField
   
   
class UploadForm(FlaskForm): 
    video_file = FileField(validators=[FileAllowed(['mp4','flv','jpeg'])])
    submit = SubmitField(u'提交')