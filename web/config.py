# -- coding:UTF-8 --
import json
import random
import time

# 读json #
def write_json(filename, data):
  with open(filename, 'w') as f:
    json.dump(data, f)


# 写json #
def read_json(filename):
  with open(filename, 'r') as f:
    data = json.load(f)
  return data


# 生成随机名称 #
def random_name(num):
  seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  name = []
  for i in range(num):
    name.append(random.choice(seed))
  return ''.join(name)


# 获取没过期的cookie对应的username #
def check_cookie(value):
  user_data = read_json('json/user.json')
  username = ''
  for key in user_data:
    if (user_data[key]['cookie'] == value and user_data[key]['expires'] >= time.time()):
      username = key
  return username

# 检查图片格式
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg'])