import time
from xarm.wrapper import XArmAPI

"""
ロボットアームのエンドエフェクタを初期値に戻すための処理。
"""
arm = XArmAPI("192.168.1.199")
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(0)



initialPosition = [79.700091, -66.500117, -81.000018, 22.399785, 186.499825, 59.599528, 113.000051]

for i in range(1,8):
    arm.set_servo_angle(servo_id=8-i, angle= initialPosition[8-i-1],speed=20, wait=False)

