from flask import Flask,render_template,request,make_response,redirect
import time

app=Flask(__name__,template_folder='t',static_url_path='/static',static_folder='s')

@app.route('/')
def index():
    return render_template('01_index.html')

@app.route('/request')
def request_views():
    # 将request中的成员打印在终端上
    # print(dir(request))
    # print(request.scheme)
    # 获取请求方案(协议)
    scheme=request.scheme
    # 获取请求方式
    method=request.method
    # 获取get请求方式提交的数据
    args = request.args
    # 获取post请求方式提交的数据
    form = request.form
    # 获取任意一种请求方式提交的数据
    values = request.values
    # 获取 cookies
    cookies = request.cookies
    # 获取 path (请求路径)
    path = request.path
    # 获取 headers (请求消息头)
    headers = request.headers
    # 获取 headers 中的 User-Agent请求消息头
    ua = request.headers['User-Agent']
    # 获取 headers 中的 referer 请求消息头 : 请求的源地址
    referer = request.headers.get('referer', '')
    # 获取 full_path
    full_path = request.full_path
    # 获取 url
    url = request.url

    return render_template('02_request.html',params=locals())

@app.route('/form')
def form_views():
    return render_template('03_form.html')

@app.route('/form_do')
def  form_do():
    if request.method=='GET':
#         获取form表单提交过来的数据
        uname=request.args.get('uname')
        upwd=request.args.get('upwd')
        print('用户名称：%s,用户密码：%s'%(uname,upwd))
    return "获取表单数据成功！"

@app.route('/post',methods=['GET','POST'])
def post():
    if request.method == 'GET':
        return render_template('04_form.html')
    else:
        uname = request.form.get('uname')
        upwd = request.form.get('upwd')
        uemail = request.form.get('uemail')
        trueName = request.form.get('trueName')
        print("姓名:%s,密码:%s,邮件:%s,真实姓名:%s" % (uname, upwd, uemail, trueName))
        # return "Post OK"
        #重定向到'/'
        return redirect('/')
# @app.route('/post_do',methods=['POST'])
# def post_do():
#     uname = request.form.get('uname')
#     upwd = request.form.get('upwd')
#     uemail = request.form.get('uemail')
#     trueName = request.form.get('trueName')
#     print("姓名:%s,密码:%s,邮件:%s,真实姓名:%s" % (uname, upwd, uemail, trueName))
#     return "Post OK"

@app.route('/response')
def response_views():
    #相应普通字符串给客户端-使用响应对象
    #创建响应对象，并赋值响应的字符串
    # resp=make_response('使用响应对象响应回去的内容')

    #创建响应对象，并赋值响应的模板
    resp=make_response(render_template('04_form.html'))
    #将响应对象进行返回
    return resp

@app.route('/file',methods=['GET','POST'])
def file_views():
    if request.method=='GET':
        return render_template('05_file.html')
    else:
        #接收名称为uimg的图片（文件）
        f=request.files['uimg']
        #获取上传的图片的名称
        filename=f.filename
        # filenameSplit=filename.split('.')
        date=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        filename=date[0:10]+'_'+date[12:16]+'_'+str(filename)
        # print(filenameSplit)
        print('文件名称：'+filename)
        #再将图片保存进static
        f.save('s/img/'+filename)
        return "Upload OK"


if __name__=="__main__":
    app.run(debug=True)