import os
import sys
import time
import math

from xarm.wrapper import XArmAPI


"""
Servo_Sampleでは、サーボモードで単純にロボットアームを上方向に10cm移動するコードを書いています。
サーボは基本的に小さい値を連続的に指定してやることで、滑らかに柔軟な動きに対応できるようになるものになります。

処理の流れ：
1. 現在のアームの位置を取得する。
2. その位置からZ軸方向に10cm(100mm)移動する。
3. 新しい位置がワークスペース内にあるかどうかを確認する。
4. ワークスペース内にある場合、その位置に移動するための各モーターの角度をInverse Kinematicsで計算する。
5. 各モーターの角度を設定する。


"""


################初期設定################

arm = XArmAPI("192.168.1.199") #IP指定してロボットアームと接続。
arm.motion_enable(enable=True) #モーション有効化して動かせるようにする。
arm.set_mode(1) #サーボモードに設定する。
arm.set_state(state=0) #ステート設定: 0 = スタートモーション

speed = 50 #モーターのスピードを設定する。

#######################################


#新しい位置がワークスペース内にあるかどうかを確認する関数
#ロボットアームが環境の障害に衝突しないようにするため。
def CheckIfNewPositionInWorkspace(x,y,z):
    if x > 680  or x < 300:
        return False
    if y < -230 or y > 420:
        return False
    if z < 94 or z > 500:
        return False
    return True



def main():
   
    _,current_position = arm.get_position() #現在のアームの位置を取得する。 return: [x,y,z,roll,pitch,yaw]
    x,y,z,roll,pitch,yaw = current_position #展開して各変数に代入する。
   
    for i in range(100): 
        z -= 1 # Z軸に1mm増やす
        if CheckIfNewPositionInWorkspace(x,y,z): #新しい座標がWorkspace内にあるか調べる。
            _, target_angle = arm.get_inverse_kinematics([x, y, z, roll, pitch, yaw]) #Inverse Kinematicsで、座標から7つそれぞれのモーターの角度を計算する
        
            arm.set_servo_angle_j(angles=target_angle, speed=speed) # モーターの角度を指定して操作する。
        else:
            print(" position is out of workspace")

        

        time.sleep(0.01) # これがないと早すぎてしまうので、ここでスピードを調整する。
        






if __name__ == "__main__":
    main() 
    arm.disconnect()

