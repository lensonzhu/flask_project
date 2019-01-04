from flask import Flask,render_template,redirect,session,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime


app=Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'

manage=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)

#bao cuo:404
@app.errorhandler(404)
def page_notfound(e):
    return render_template('404.html'),404

#bao cuo:500
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'),500


from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name=StringField('what is your name?',validators=[Required()])
    submit=SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        old_name=session.get('name')
        # sure user name is or not exsit, and manage it.
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name']=form.name.data
        # redirect needn't add .html hou_zui:(inderx.html)
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'))

 #@app.route('/')
  #def index():
       #add a prasent time function
        #    return render_template('index.html',current_time=datetime.utcnow())

#chuan can:name
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

if __name__=='__main__':
    manage.run()
