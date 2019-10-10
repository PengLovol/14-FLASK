from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return  '这是首页'

@app.route('/login')
def login():
    return '这是登陆页面'

@app.route('/register')
def register():
    return '这是注册页面'

@app.route('/show1/<name>')
def show1(name):
    return "<h1>姓名为:%s</h1>" % name

# 定义带两个参数的路由
@app.route('/show2/<name>/<age>')
def show2(name,age):
    return "<h1>姓名为:%s,年龄为:%s" % (name,age)
# 定义带两个参数的路由,其中,age参数指定为整数
@app.route('/show3/<name>/<int:age>')
def show3(name,age):
    # age : 为 整型,并非 字符串
    return "传递进来的参数是name:%s,age:%d" % (name,age)


@app.route('/post',methods=['POST','GET'])
def post():
    return '这是post请求方式进来的'





if __name__=="__main__":
    app.run(debug=True)
