import math
#计算角度差，a-b,取值均为（-2pi.2pi）,
def dif_ang(a, b):
  dif = a - b
  if dif < -math.pi:
    return dif + 2*math.pi#小于-pi加2pi
  elif dif >= math.pi:
    return dif - 2*math.pi#大于pi减2pi
  else:
    return dif

'''
def dif_ang(a, b):
    return ((a - b + np.pi) % (2 * np.pi)) - np.pi
'''


