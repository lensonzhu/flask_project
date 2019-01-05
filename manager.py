import os
from flask import Flask,render_template,redirect,session,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_script import Shell

from flask_migrate import Migrate,MigrateCommand



basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)
db=SQLAlchemy(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)




class NameForm(FlaskForm):
    name=StringField('what is your name?',validators=[Required()])
    submit=SubmitField('Submit')


class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role',lazy='dynamic')
    def __repr__(self):
        return '<Role %r>'% self.name


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>'% self.username


def make_shell():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell))


@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    print('-------no problem')
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        print('------pass')
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['known']=False
            print('=========false')
        else:
            session['known']=True
            print('=========true')
        session['name']=form.name.data
        print('---------action')
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))


#bao cuo:404
@app.errorhandler(404)
def page_notfound(e):
    return render_template('402.html'),404

#bao cuo:500
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'),500


#5a number five and a jie
#@app.route('/',methods=['GET','POST'])
#def index():
#    form=NameForm()
#    if form.validate_on_submit():
#        old_name=session.get('name')
        # sure user name is or not exsit, and managed it.
#        if old_name is not None and old_name != form.name.data:
#            flash('Looks like you have changed your name!')
#        session['name']=form.name.data
        # redirect needn't add .html but a flash function index()
#        return redirect(url_for('index'))
#    return render_template('index.html',form=form,name=session.get('name'))

 #@app.route('/')
  #def index():
       #add a prasent time function
        #    return render_template('index.html',current_time=datetime.utcnow())

#chuan can:name
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

if __name__=='__main__':
#    db.create_all()
    manager.run()
