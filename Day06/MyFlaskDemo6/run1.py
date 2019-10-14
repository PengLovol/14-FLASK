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
    teachers=db.relationship('Teacher',backref='course',lazy='dynamic')
    def __init__(self,cname):
        self.cname=cname
    def __repr__(self):
        return "<Course %r>" % self.cname

# class Teacher(db.Model):
#     __tablename__ = 'teacher'
#     id = db.Column(db.Integer, primary_key=True)
#     tname = db.Column(db.String(30))
#     tage = db.Column(db.Integer)
#
#     # 增加一列 : course_id,外键列,要引用自主键表(course)的主键列(id)
#     course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
#
#     def __init__(self, tname, tage):
#         self.tname = tname
#         self.tage = tage
#
#     def __repr__(self):
#         return "<Teacher %r>" % self.tname

class Teacher(db.Model):
    __tablename__='teacher'
    id = db.Column(db.Integer,primary_key=True)
    tname = db.Column(db.String(30))
    tage = db.Column(db.Integer)

    # 增加一列:course_id,外键列，要引用主键表（course)的主键列(id)
    course_id=db.Column(db.Integer,db.ForeignKey('course.id'))

    # 增加反向引用,与 Wife 实体类做一对一引用.允许在Teacher中得到一个Wife的信息.同时,在Wife中也能的到一个Teacher的信息
    # uselist=False , 查询出来的是一个对象,而不是一个列表
    wife = db.relationship('Wife', backref='teacher', uselist=False)

    def __init__(self,tname,tage):
        self.tname=tname
        self.tage=tage
    def __repr__(self):
        return "<Teacher %r>"% self.tname

#和Teache实现一对一关系
class Wife(db.Model):
    __tablename__='wife'
    id=db.Column(db.Integer,primary_key=True)
    wname=db.Column(db.String(30))
    wage=db.Column(db.Integer)
    # 增加一个列:表示引用自teacher表的主键
    teacher_id=db.Column(db.Integer,db.ForeignKey('teacher.id'))
    def __init__(self,wname,wage):
        self.wname=wname
        self.wage = wage

    def __repr__(self):
        return "<Wife %r>" % self.wage

#新增student表 ，实现多对多关系：课程和学生是多对多关系
class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer,primary_key=True)
    sname = db.Column(db.String(30))
    sage=db.Column(db.Integer)
    # 增加关联属性以及反向引用
    courses=db.relationship('Course',
                            secondary='student_course',
                            lazy='dynamic',
                            backref=db.backref(
                                'students',
                                lazy='dynamic'
                            )
                            )


    def __init__(self,sname,sage):
        self.sname = sname
        self.sage=sage

    def __repr__(self):
        return "<Student %r>" % self.sname
#新增student_course表：关联表
student_course=db.Table(
    'student_course',
    db.Column('id',db.Integer,primary_key=True),
    db.Column('student_id',db.Integer,db.ForeignKey('student.id')),
    db.Column('course_id',db.Integer,db.ForeignKey('course.id'))
)


# 将创建好的实体类映射回数据库
# db.drop_all()
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

#Day06
@app.route('/add_course')
def add_course():
    course1 = Course('PYTHON 基础')
    course2 = Course('PYTHON 高级')
    course3 = Course('PYTHON WEB 基础')
    course4 = Course('PYTHON WEB 开发')

    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.add(course4)
    return "Add Course OK"

@app.route('/add_teacher')
def add_teacher():
    teacher = Teacher('李老师',40)
    # teacher.course_id = 1
    # 根据course_id查询出一个Course实体,再将Course实体赋值给teacher
    course=Course.query.filter_by(id=3).first()
    # course = db.session.query(Course).filter_by(id=1).first()
    # print(course)
    teacher.course = course
    db.session.add(teacher)

    return "Add teacher OK"

#练习1.png
@app.route('/register_teacher',methods=['POST','GET'])
def register_teacher():
    if request.method=='GET':
        courses=Course.query.all()
        return render_template('05_register.html',params=locals())
    else:
        # 获取提交过来的三个数据
        tname=request.form['tname']
        tage=request.form['tage']
        course_id=request.form['course_id']
        # 根据提交过来的course_id查询出对应的course对象
        course=Course.query.filter_by(id=course_id).first()
        # 创建teacher对象并将course对象赋值给teacher对象
        teacher=Teacher(tname,tage)
        teacher.course=course
        # 将teacher对象保存进数据库
        db.session.add(teacher)
        return redirect('/show_teacher')


@app.route('/query_teacher')
def query_teacher():
    # 通过 course 查询对应所有的 teacher
    # 查询 id 为1 的course对象
    course=Course.query.filter_by(id=1).first()
    print(course)
    # 根据course对象查询所有的teacher对象
    teachers=course.teachers.all()

    print(teachers)

    # 通过teacher查询course
    teacher=Teacher.query.filter_by(tname='李老师').first()
    course=teacher.course
    print(course)
    print('老师:%s,课程:%s' % (teacher.tname, course.cname))
    return "Query OK"

#练习2.png
@app.route('/show_teacher')
def show_teacher():
    teachers=Teacher.query.all()
    return render_template('05_showteacher.html',params=locals())
@app.route('/teacher_delete')
def teacher_delete():
    id=request.args.get('id')
    teacher=Teacher.query.filter_by(id=id).first()
    db.session.delete(teacher)
    return redirect('/show_teacher')

@app.route('/query_teacher_course')
def query_teacher_course():
    results = db.session.query(Teacher,Course).filter(Teacher.course_id == Course.id).all()

    for result in results:
        print("姓名:%s,课程:%s" % (result.Teacher.tname,result.Course.cname))
    return "Query OK"

#新增wife表，实现一对一关系
@app.route('/add_wife')
def add_wife():
    # 查询 李老师 的信息
    teacher=Teacher.query.filter_by(tname='李老师').first()
    # 创建 wife 对象
    wife = Wife('李夫人',36)
    # 将 王老师 对象 赋值给 wife
    wife.teacher=teacher
    # 将 wife 保存回数据库
    db.session.add(wife)
    return "Add wife OK"

@app.route('/query_wife')
def query_wife():
    # 通过 teacher 找 wife
    teacher=Teacher.query.filter_by(tname='李老师').first()
    wife=teacher.wife
    print("%s的媳妇是:%s" % (teacher.tname,wife.wname))
    # 通过 wife 找 teacher
    wife=Wife.query.filter_by(wname='李夫人').first()
    teacher=wife.teacher
    print("%s的老公是：%s" % (wife.wname,teacher.tname))
    return "Query OK"

#练习3.png
@app.route('/register_wife',methods=['GET','POST'])
def register_wife():
    if request.method=='GET':
        #查询Teacher列表,发送到模板上
        teachers = Teacher.query.all()
        return render_template('06_register_wife.html',params=locals())
    else:
        # 接收 teacher 的 value
        teacher_id=request.form['teacher']
        wife=Wife.query.filter_by(teacher_id=teacher_id).first()
        if wife:
            errMsg="EXIST"
            print(errMsg)
            # 判断 wife 表中的 teacher_id 列是否已经有了value的值
            teachers = Teacher.query.all()
            return render_template('06_register_wife.html',params=locals())
        else:
            # 接收剩余数据
            wname=request.form['wname']
            wage=request.form['wage']
            # 根据teacher_id查询teacher对象
            wife_teacher=Teacher.query.filter_by(id=teacher_id).first()
            # 创建wife对象并保存回数据库
            wife_new=Wife(wname,wage)
            wife_new.teacher=wife_teacher
            db.session.add(wife_new)
            return redirect('/show_all_wife')

#显示左右wife信息
@app.route('/show_all_wife')
def show_all_wife():
    allWife=Wife.query.all()
    return render_template('06_show_all_wife.html',params=locals())
#增加删除功能
@app.route('/wife_delete')
def wife_delete():
    wife_id=request.args.get('id')
    wife=Wife.query.filter_by(id=wife_id).first()
    db.session.delete(wife)
    return redirect('/show_all_wife')


#多对多：往关联表中插入数据
@app.route('/add_student_course')
def add_student_course():
    # 查询 张三丰 的信息
    stu = Student.query.filter_by(sname='陈敏').first()
    # 查询 PYTHON基础 的信息
    cour = Course.query.filter_by(id=3).first()
    # 将cour课程追加到stu的courses列表中
    stu.courses.append(cour)
    db.session.add(stu)
    return "Add OK"

#查询
@app.route('/query_student_course')
def query_student_course():
    # 查询陈敏所选的所有课程
    student = Student.query.filter_by(id=1).first()
    courses = student.courses.all()
    print('学员姓名:%s' % student.sname)
    for cour in courses:
        print('所选课程:%s' % cour.cname)

    return "Query OK"

#我的小练习：可视化关联表
@app.route('/register_course_student',methods=['GET','POST'])
def register_course_student():
    if request.method == 'GET':
        courses = Course.query.all()
        students = Student.query.all()
        return render_template('07_register_course_student.html', params=locals())
    else:
        #由表单提交得到相关信息
        student_id=request.form['student']
        course_id=request.form['course']
        student=Student.query.filter_by(id=student_id).first()
        print(student.sname)
        print(student.sage)
        courseNew=Course.query.filter_by(id=course_id).first()


        #遍历该学生所选过的课程，避免重复
        coursesAll=student.courses.all()
        # print(course.cname)
        # for cour in courses:
        #     print(cour.cname)
        # return 'OK'

        for cour in coursesAll:
            if courseNew.cname==cour.cname:
                errMsg = "重复选择课程"
                print(errMsg)
                return render_template('/07_reback.html',params=locals())

        student.courses.append(courseNew)
        coursesUpdate=student.courses.all()
        return render_template('/07_show_course_student.html',params=locals())



#显示所有学生的课程表
@app.route('/show_database_courseStu')
def show_database_courseStu():
    students=Student.query.all()
    return render_template('/07_show_databse_courseStdu.html',params=locals())






if __name__ == "__main__":
    app.run(debug=True)