import keyboard
import time
import os
import sys
import time
import math

from xarm.wrapper import XArmAPI



"""
Exercise 2: 
この演習では、キーボードの入力を受け取り、ロボットアームを動かすコードを書いてください。
なお、今回はロボットを正面から見て操作する前提で話を進めます。

ヒント：
Wキーを押すと、ロボットアームがx軸方向に5mm(手前)に移動します。
Sキーを押すと、ロボットアームがx軸方向に-5mm(奥)に移動します。
Aキーを押すと、ロボットアームがy軸方向に-5mm(左)に移動します。
Dキーを押すと、ロボットアームがy軸方向に5mm(右)に移動します。
上矢印キーを押すと、ロボットアームがz軸方向に5mm(上)に移動します。
下矢印キーを押すと、ロボットアームがz軸方向に-5mm(下)に移動します。
スペースキーを押したらOperateGripper関数を実行する。



また、スピードや、待機時間を変更することで、ロボットアームの動きを調整できるので、自由に変更してみてください。
(早すぎるのも怖いので、適度な速さで動かすようにしましょう。)
"""




################初期設定################

arm = XArmAPI("192.168.1.199") #IP指定してロボットアームと接続。

speed = 10 #モーターのスピードを設定する。
arm.set_mode(1) #サーボモードに設定する。
arm.set_state(0)



# グリッパーの設定。
code = arm.set_gripper_mode(0) 
enable = arm.set_gripper_enable(enable = True)
speedCode = arm.set_gripper_speed(3000)


#　グリッパーを開閉する設定。
isGripperOpen = True
def OperateGripper():
    global isGripperOpen
    if isGripperOpen == True:
        arm.set_gripper_position(350, wait=True)
        isGripperOpen = False
    else:
        arm.set_gripper_position(800, wait=True)
        isGripperOpen = True
   


#######################################


#新しい位置がワークスペース内にあるかどうかを確認する関数
#ロボットアームが環境の障害に衝突しないようにするため。
def CheckIfNewPositionInWorkspace(x,y,z):
    if (x > 680 ) or (x < 300 ) :
        print("x: ", x)
        return False
    if y < -250 or y > 520:
        print("y: ", y)
        return False
    if z < 94 or z > 500:
        print("z: ", z)
        return False
    return True




#x,y,z,roll,pitch,yawの位置を受け取り、その位置にロボットアームを移動する関数があると楽。
def SetPosition(x,y,z,roll,pitch,yaw):
    if CheckIfNewPositionInWorkspace(x,y,z):
        _, target_angle = arm.get_inverse_kinematics([x, y, z, roll, pitch, yaw])
        arm.set_servo_angle_j(angles=target_angle, speed=speed)
    else:
        print("position is out of workspace")



def main():
    isKeyPressed = False

    while True:
        position = []
        dirX = 0 
        dirY = 0 
        dirZ = 0

        if keyboard.is_pressed('down'):
            isKeyPressed = True
            dirZ -= 5 # Y軸方向に-1mm移動。下に動かす
        
            
        if keyboard.is_pressed('up'):
            isKeyPressed = True
            dirZ += 5 # Z軸方向に1mm移動。上に動かす



        if keyboard.is_pressed('left'):
            isKeyPressed = True
            dirY -= 5 # Y軸方向に-1mm移動。左に動かす
        

        if keyboard.is_pressed('right'):
            isKeyPressed = True
            dirY += 5 # Y軸方向に1mm移動。右に動かす


        if keyboard.is_pressed('w'):
            isKeyPressed = True
            dirX -= 5 # X軸方向に1mm移動。奥に動かす
        
            

        if keyboard.is_pressed('s'):
            isKeyPressed = True
            dirX += 5 # X軸方向に-1mm移動。手前に動かす
        
        
        
        if keyboard.is_pressed('a'):
            isKeyPressed = True
            dirY -= 5 # Y軸方向に-1mm移動。左に動かす
        

        if keyboard.is_pressed('d'):
            isKeyPressed = True
            dirY += 5 # Y軸方向に1mm移動。右に動かす
        
        if keyboard.is_pressed('space'):
            OperateGripper()
    

        if isKeyPressed:
            _, position  = arm.get_position()
            x,y,z,roll,pitch,yaw = position
            x += dirX
            y += dirY 
            z += dirZ
            
            SetPosition(x,y,z,roll,pitch,yaw)
            isKeyPressed = False

            
        if keyboard.is_pressed('esc'):
            
            print("Exiting...")
            break

        # 処理が反映される間隔を指定
        time.sleep(0.05)



if __name__ == "__main__":      
    main()
    arm.disconnect()