# -- coding:UTF-8 --
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import time
from config import write_json, read_json, random_name, check_cookie, allowed_file
import json
import os
import tools


app = Flask(__name__, static_folder = '../client/static', static_url_path = '')
CORS(app, resources = {
  r"/*": {
    'supports_credentials': 'true'
  }
})


@app.route('/')
def hello_world():
  return ''

# 登录 #
@app.route('/login', methods=['POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    user_data = read_json('json/user.json')
    expires_time = time.time() + 60 * 60
    if (username in user_data and user_data[username]['password'] != password):
      res = Response(json.dumps({ 'code': 0, 'message': '密码错误', 'data': 0 }), content_type='application/json')
    else:
      msg = '登录成功' if username in user_data else '注册成功'
      cookie_value = random_name(32)
      user_data[username] = {
        'password': password,
        'cookie': cookie_value,
        'expires': expires_time
      }
      write_json('json/user.json', user_data)
      res = Response(json.dumps({ 'code': 0, 'message': msg, 'data': 1 }), content_type='application/json')
      res.set_cookie(key = 'USERINFO', value = cookie_value, expires = expires_time )
    return res
  return 'NO POST'


# 退出 #
@app.route('/logout', methods=['POST'])
def logout():
  if request.method == 'POST':
    username = request.form.get('username')
    user_data = read_json('json/user.json')
    if (username in user_data):
      user_data[username] = {
        'password': user_data[username]['password'],
        'cookie': '',
        'expires': 0
      }
      write_json('json/user.json', user_data)
      res = Response(json.dumps({ 'code': 0, 'message': '退出成功', 'data': 1 }), content_type='application/json')
    else:
      res = Response(json.dumps({ 'code': 0, 'message': '退出失败', 'data': 0 }), content_type='application/json')
    return res
  return 'NO POST'


# 获取用户名 #
@app.route('/getUserInfo', methods=['GET'])
def get_user_info():
  if request.method == 'GET':
    cookie_value = request.cookies.get('USERINFO')
    username = check_cookie(cookie_value)
    if (username == ''):
      res = Response(json.dumps({
        'code': 302,
        'message': '未登录',
        'data': {
          'redirectUrl': 'http://127.0.0.1:5000/index.html/#/login'
        }
      }))
    else:
      res = Response(json.dumps({
        'code': 0,
        'data': {
          'username': username
        }
      }))
    return res
  return 'NO GET'


# 上传图片 #
@app.route('/upload', methods=['POST'])
def upload_file():
  if request.method == 'POST':
    dealType = request.form.get('type') # 处理方式
    style = request.form.get('style') # 黑白simple 彩色color
    
    if dealType == 'gray':
      red = request.form.get('red')
      green = request.form.get('green')
      blue = request.form.get('blue')
    elif dealType == 'log':
      logC = request.form.get('logC')
      logV = request.form.get('logV')
    elif dealType == 'gama':
      gama = request.form.get('gama')
    
    imagenames = []
    
    # 保存图片至original文件夹
    files = request.files.getlist('file')
    for file in files:
      # 设置图片名称
      name = random_name(18) + '.' + file.filename.rsplit('.', 1)[1]
      # 存储 原始图片
      basepath = os.path.dirname(__file__)
      original_path = os.path.join(basepath, 'original', name)
      file.save(original_path)
      # 返回图片url
      imagenames.append(name)
    
    # 图像处理
    for name in imagenames:
      if dealType == 'gray':
        tools.gray(name, float(red), float(green), float(blue))
      elif dealType == 'translate':
        tools.translate(name, style)
      elif dealType == 'log':
        tools.log(name, style, float(logC), float(logV))
      elif dealType == 'gama':
        tools.gama(name, style, float(gama))
      elif dealType == 'histogram':
        tools.histogram(name, style)
      elif dealType == 'median':
        tools.median(name)
      elif dealType == 'laplacian':
        tools.laplacian(name)
    
    return Response(json.dumps({ 'code': 0, 'message': 'success', 'data': { 'urls': imagenames }}), content_type='application/json')
  return 'NO POST'


# 获取图片 #
@app.route("/image/<imageid>")
def image(imageid):
  image = file("images/{}".format(imageid))
  resp = Response(image, mimetype="image/*")
  return resp


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)
  # app.run(debug=True)