import time
from xarm.wrapper import XArmAPI

"""
ロボットアームのエンドエフェクタを初期値に戻すための処理。
"""
arm = XArmAPI("192.168.1.199")
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(0)




code, angles = arm.get_servo_angle(is_radian=False)

print(angles)