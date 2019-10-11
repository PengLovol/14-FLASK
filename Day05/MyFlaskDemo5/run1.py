from flask import Flask,render_template,request
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

    def __init__(self,cname):
        self.cname=cname

# 将创建好的实体类映射回数据库
# db.create_all()

@app.route('/insert')
def insert_views():
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
    users = db.session.query(Users).filter(Users.id.in_([1,2,3])).all()
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

if __name__=="__main__":
    app.run(debug=True)