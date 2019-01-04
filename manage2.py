from flask import Flask
from flask import redirect
from flask.ext.script import Manager


app=Flask(__name__)

manager=Manager(app)

@app.route('/')
def index():
    return '<p>hello word</p>'


#@app.route('/')
#def index():
#    return redirect('http://www.idu.com')

#@app.route('/user/<name>')
#def index(name):
#    return '<h2>hello world,%s !</h2>'%name

#if __name__ == '__main__':
#    app.run(debug=True)
#@app.route('/')
#def index():
#    from flask import request
#    user_agent=request.headers.get('User-Agent')
#    return '<p>browser is %s</p>' %user_agent


if __name__=='__main__':
    manager.run()
