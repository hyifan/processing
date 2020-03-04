# -- coding: utf-8 --
import cv2
import numpy as np


'''
灰度图像
'''
def gray(name, red, green, blue):
	img = cv2.imread('original/' + name)
	img_output = red * img[:,:,0] + green * img[:,:,1] + blue * img[:,:,2]
	cv2.imwrite('images/' + name, img_output)


'''
图像反转
'''
def translate(name, style):
	if style == 'simple':
		# 灰度图像
		img = cv2.imread('original/' + name, 0)
		img_output = np.ones(img.shape) * 255 - img
	else:
		# 彩色图像
		img = cv2.imread('original/' + name)
		img_output = np.zeros(img.shape)
		img_output[:,:,0] = np.ones(img[:,:,0].shape) * 255 - img[:,:,0]
		img_output[:,:,1] = np.ones(img[:,:,1].shape) * 255 - img[:,:,1]
		img_output[:,:,2] = np.ones(img[:,:,2].shape) * 255 - img[:,:,2]
	cv2.imwrite('images/' + name, img_output)


'''
对数变换
'''
def log(name, style, logC, logV):
	if style == 'simple':
		# 灰度图像
		img = cv2.imread('original/' + name, 0)
		img = img / 255 # 归一化为范围[0,1]
		img_output = logC * np.log10(1 + logV * img)
		img_output = img_output * 255 # 转换为范围[0,255]
	else:
		# 彩色图像
		img = cv2.imread('original/' + name)
		img = img / 255 # 归一化为范围[0,1]
		img_output = np.zeros(img.shape)
		img_output[:,:,0] = logC * np.log10(1 + logV * img[:,:,0])
		img_output[:,:,1] = logC * np.log10(1 + logV * img[:,:,1])
		img_output[:,:,2] = logC * np.log10(1 + logV * img[:,:,2])
		img_output = img_output * 255 # 转换为范围[0,255]
	cv2.imwrite('images/' + name, img_output)


'''
伽马变换
'''
def gama(name, style, gama):
	if style == 'simple':
		# 灰度图像
		img = cv2.imread('original/' + name, 0)
		img = img / 255 # 归一化为范围[0,1]
		img_output = np.power(img, gama)
		img_output = img_output * 255 # 转换为范围[0,255]
	else:
		# 彩色图像
		img = cv2.imread('original/' + name)
		img = img / 255 # 归一化为范围[0,1]
		img_output = np.zeros(img.shape)
		img_output[:,:,0] = np.power(img[:,:,0], gama)
		img_output[:,:,1] = np.power(img[:,:,1], gama)
		img_output[:,:,2] = np.power(img[:,:,2], gama)
		img_output = img_output * 255 # 转换为范围[0,255]
	cv2.imwrite('images/' + name, img_output)


'''
直方图均衡
'''
def histogram(name, style):
	if style == 'simple':
		# 灰度图像
		img = cv2.imread('original/' + name, 0)
		img_output = cv2.equalizeHist(img) # 直方图均衡
	else:
		# 彩色图像
		img = cv2.imread('original/' + name)  # 加载BGR图片
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # BGR转HSV
		img_v = img_hsv[:, :, 2] # 获取V分量
		img_equal_v = cv2.equalizeHist(img_v) # 对V分量进行直方图均衡
		img_hsv[:, :, 2] = img_equal_v # 将均衡后的V分量赋值给原图
		img_output = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR) # HSV转BGR
	cv2.imwrite('images/' + name, img_output)


'''
中值滤波器
'''
def median(name):
	img = cv2.imread('original/' + name)
	img_output = cv2.medianBlur(img, 3)
	cv2.imwrite('images/' + name, img_output)


'''
Laplacian算子
'''
def laplacian(name):
	kernel = np.array([[-1, -1, -1],[-1, 8, -1],[-1, -1, -1]])
	img = cv2.imread('original/' + name, 0)
	img_edge = cv2.filter2D(img, -1, kernel)
	img_output = cv2.add(img, img_edge)
	cv2.imwrite('images/' + name, img_output)