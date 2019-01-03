from flask import Flask

app=Flask(__name__)

#@app.route('/user/<name>')
#def index(name):
#    return '<h2>hello world,%s !</h2>'%name

#if __name__ == '__main__':
#    app.run(debug=True)
@app.route('/')
def index():
    from flask import request
    user_agent=request.headers.get('User-Agent')
    return '<p>browser is %s</p>' %user_agent


if __name__=='__main__':
    app.run(debug=True)
