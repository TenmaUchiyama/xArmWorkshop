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
arm.set_mode(1) #サーボモードに設定する。サーボモードは角度の情報しか受け取れないので、座標位置情報は受け取れない
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
    if x > 680  or x < 300:
        return False
    if y < -230 or y > 420:
        return False
    if z < 94 or z > 550:
        return False
    return True



#x,y,z,roll,pitch,yawの位置を受け取り、その位置にロボットアームを移動する関数があると楽。
# rol pitch yaaw
def SetPosition(x,y,z,roll,pitch,yaw):
    if CheckIfNewPositionInWorkspace(x,y,z):# その新しいポジションがワークスペース内にあったらモーターがどう角度を制御するかを逆運動学で計算
        _, target_angle = arm.get_inverse_kinematics([x, y, z, roll, pitch, yaw]) #Inverse Kinematicsで、座標から7つそれぞれのモーターの角度を計算する
        arm.set_servo_angle_j(angles=target_angle, speed=speed) # モーターの角度を指定して操作する。
    else:
        print("position is out of workspace")



def main():
    isKeyPressed = False
    # 現在位置の把握
    _,current_position = arm.get_position() #現在のアームの位置を取得する。 return: [x,y,z,roll,pitch,yaw]
    x,y,z,roll,pitch,yaw = current_position #展開して各変数に代入する。
    
    while True:

        if keyboard.is_pressed('up'): # 下矢印キーが押されたときの処理
           print("up key pressed")
           z+=5 
           SetPosition(x,y,z,roll,pitch,yaw)

        if keyboard.is_pressed('down'): # 上矢印キーが押されたときの処理
           print("down key pressed")
           z-=5
           SetPosition(x,y,z,roll,pitch,yaw)
     
        if keyboard.is_pressed('w'): # wキーが押されたときの処理: 前進
            print("w key pressed")
            x+=5
            SetPosition(x,y,z,roll,pitch,yaw)
        
        if keyboard.is_pressed('s'): # sキーが押されたときの処理：奥
            print("w key pressed")
            x-=5
            SetPosition(x,y,z,roll,pitch,yaw)
        
        if keyboard.is_pressed('a'): # aキーが押されたときの処理：右
            print("w key pressed")
            y-=5
            SetPosition(x,y,z,roll,pitch,yaw)
        
        if keyboard.is_pressed('d'): # dキーが押されたときの処理：左
            print("w key pressed")
            y+=5
            SetPosition(x,y,z,roll,pitch,yaw)

        if keyboard.is_pressed('space'): # スペースキーが押されたときの処理
            print("space key pressed")
            OperateGripper()
    

        if keyboard.is_pressed('esc'): # escキーが押されたときの処理
            print("Exiting...")
            break

        # 処理が反映される間隔を指定
        time.sleep(0.05)



if __name__ == "__main__":      
    main()
    arm.disconnect()