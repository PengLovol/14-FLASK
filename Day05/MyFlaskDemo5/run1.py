from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy import or_

pymysql.install_as_MySQLdb()
#创建一个Ｆlsak应用程序,用于实现前后端交互以及与数据库连接的功能
app = Flask(__name__)
#制定连接的数据库
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:120913@localhost:3306/flask"
#指定执行完操作之后自动提交 ==db.session.commit()
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True


db = SQLAlchemy(app)

#根据现有的表结构构建模型类
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)
    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email
    def __repr__(self):
        return '<Users:%r>' % self.username

class Course(db.Model):
    __tablename__="course"
    id=db.Column(db.Integer,primary_key=True)
    cname=db.Column(db.String(30))
    #反向引用：返回与当前课程相关的teacher列表
    # backref:定义反向关系,本质上会向Teacher实体中增加一个course属性.该属性可替代course_id来访问Course模型.此时获得到的是模型对象,而不是外键值
    #一箭双雕：在Teacher实体中增加一个course属性,同时在Course实体中增加了teachers属性，以此实现两个表的互相查询
    teachers=db.relationship('Teacher',backref='course_id',lazy='dynamic')
    def __init__(self,cname):
        self.cname=cname



class Teacher(db.Model):
    __tablename__='teacher'
    id=db.Column(db.Integer,primary_key=True)
    tname=db.Column(db.String(30))
    tage=db.Column(db.Integer)
    # 增加一列:course_id,外键列，要引用主键表（course)的主键列(id)
    course_id=db.Column(db.Integer,db.ForeignKey('course.id'))

    def __int__(self,tname,tage):
        self.tname=tname
        self.tage=tage
    def __repr__(self):
        return "<Teacher %r>"% self.tname

# 将创建好的实体类映射回数据库
db.drop_all()
db.create_all()

@app.route('/insert_user')
def insert():
    user = Users('王hah',40,'wanghah@163.com')
    db.session.add(user)
    return "Insert OK"

@app.route('/query')
def query_views():
    #测试查询
    # print(db.session.query(Users))
    # print(db.session.query(Users.username,Users.email))
    # print(db.session.query(Users,Course))

    #通过查询执行函数获得最终查询结果
    # users=db.session.query(Users).all()
    # for u in users:
    #     print(u.username,u.age,u.email)

    #first():得到查询中的第一个结果
    # user=db.session.query(Users).first()
    # print(user)
    # course = db.session.query(Course).first()
    # print(course)

    # 使用查询过滤器函数对数据进行筛选

    # 查询年龄大于30的Users的信息
    # users = db.session.query(Users).filter(Users.age>30).all()
    # print(users)
    #查询年龄大于30并且id大于5的Users的信息
    # users1 = db.session.query(Users).filter(Users.age>30,Users.id > 5)
    # users2 = db.session.query(Users).filter(Users.age>30,Users.id > 5).all()
    # print(users1)
    # print(users2)

    # 查询年龄大于30 或者 id大于 5 的Users的信息
    # users = db.session.query(Users).filter(or_(Users.age>30,Users.id > 5)).all()
    # print(users)

    #查询email中包含字符'w'的用户的信息
    # users = db.session.query(Users).filter(Users.email.like('%w%')).all()
    # print(users)
    #查询id在1,2,3 之间的 用户的信息
    # users = db.session.query(Users).filter(Users.id.in_([1,2,3])).all()
    # print(users)

    # 查询 Users 表中所有数据的前3条
    # users = db.session.query(Users).limit(3).all()
    # print(users)
    # users = db.session.query(Users).limit(3).offset(1).all()
    # print(users)

    # 查询Users表中所有的数据,并按照id倒叙排序
    # users = db.session.query(Users).order_by('id desc').all()  #本版本会出错
    # users=db.session.query(Users).order_by(Users.id.desc()).all()
    # print(users)

    # 查询Users表中所有的数据,并按照 age 进行分组
    # users = db.session.query(Users.age).group_by('age').all()
    # print(users)

    # 基于Models实现的查询 : 查询id>3的所有用户的信息
    users = Users.query.filter(Users.id>3).all()
    print(users)
    return "Query OK"

#作业
#方法１：id传参方式是flask特有的一种方式；<a href="/query_by_id/{{ u.id }}">
@app.route('/query_all')
def query_all():
    #查询Users表中所有的数据
    users=db.session.query(Users).all()

    return render_template('01_users.html',params=locals())

@app.route('/query_by_id/<int:id>')
def query_by(id):
    user = db.session.query(Users).filter_by(id=id).first()
    return render_template('02_user.html',params=locals())

#方法2:该方法更加正规，根据http协议进行传参： <a href="/query_by_id_2?id={{ u.id }}">
@app.route('/query_all_2')
def query_all_2():
    #查询Users表中所有的数据
    users=db.session.query(Users).all()

    return render_template('01_users_2.html',params=locals())
@app.route('/query_by_id_2')
def query_by_2():
    # 接收前端通过地址栏传递过来的查询字符串
    id=request.args.get('id')
    # 根据id获取 user 的信息
    user = db.session.query(Users).filter_by(id=id).first()
    # 将user对象发送的02-user.html模板上进行显示
    return render_template('02_user.html',params=locals())

@app.route('/delete_user')
def delete_user():
    user = db.session.query(Users).filter_by(id=3).first()
    db.session.delete(user)
    return 'Delete OK'

@app.route('/update_user')
def update_user():
    #1)查
    user=Users.query.filter_by(id=5).first()
    #2）改
    user.username='Wang Wc'
    user.age=40
    # 3)保存
    db.session.add(user)
    return 'Update OK'

#删除功能
@app.route('/delete')
def delete_views():
    # 接收请求过来的id值
    id=request.args.get('id')
    #根据id值查询对应的模型对象
    user=Users.query.filter_by(id=id).first()
    #将模型对象删除
    db.session.delete(user)
    # request.headers : 获取请求消息头的信息
			                    # 获取 headers 中的 referer 请求消息头 : 请求的源地址
                                # referer = request.headers.get('referer', '')
    url=request.headers.get('referer','/query_all')
    print(url)
    return redirect(url)

#修改功能
@app.route('/update',methods=['GET','POST'])
def update_views():
    if request.method=='GET':
        # 获取前端传递过来的 id
        id=request.args.get('id')
        # 根据id查询出对应的实体对象
        user=Users.query.filter_by(id=id).first()
        # 将实体对象放到03-update.html模板中显示
        return render_template('03_update.html',params=locals())
    else:
        #接收前端传递过来的四个参数
        id=request.form['id'] #id=request.form.get('id')
        username=request.form['username']
        age=request.form['age']
        email=request.form['email']
        #查
        user=Users.query.filter_by(id=id).first()
        #改
        user.username=username
        user.age=age
        user.email=email
        #保存
        db.session.add(user)
        return redirect('/query_all_2')

#添加插入功能
@app.route('/insert',methods=['GET','POST'])
def insert_views():
    if request.method=='GET':
        return render_template('04_insert.html')
    else:
        username=request.form['username']
        age=request.form['age']
        email=request.form['email']
        user = Users(username,age,email)
        db.session.add(user)
        return redirect('/query_all_2')


if __name__=="__main__":
    app.run(debug=True)