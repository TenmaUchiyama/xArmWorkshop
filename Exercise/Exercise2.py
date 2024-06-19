import keyboard
import time

from xarm.wrapper import XArmAPI



"""
Exercise 2: 
この演習では、キーボードの入力を受け取り、ロボットアームを動かすコードを書いてください。
なお、今回はロボットを正面から見て操作する前提で話を進めます。

ヒント：
Wキーを押すと、ロボットアームがx軸方向に-5mm(奥)移動します。
Sキーを押すと、ロボットアームがx軸方向に5mm(手前)移動します。
Aキーを押すと、ロボットアームがy軸方向に-5mm(左)移動します。
Dキーを押すと、ロボットアームがy軸方向に5mm(右)移動します。
上矢印キーを押すと、ロボットアームがz軸方向に5mm(上)移動します。
下矢印キーを押すと、ロボットアームがz軸方向に-5mm(下)移動します。
スペースキーを押したらOperateGripper関数を実行する。

また、待機時間を変更することで、ロボットアームの動きの速さを調整できるので、自由に変更してみてください。
(速すぎるのも怖いので、適度な速さで動かすようにしましょう。)

Servo_Sample.pyの流れを参考にし、それぞれのキーが押された時にロボットアームをどのうに動かすかを考えてみてください。
"""




################初期設定################

arm = XArmAPI("192.168.1.199") #IP指定してロボットアームと接続。
arm.motion_enable(enable=True) #モーション有効化して動かせるようにする。
arm.set_mode(1) #サーボモードに設定する。
arm.set_state(state=0) #ステート設定: 0 = スタートモーション

speed = 10 #モーターのスピードを設定する。



# グリッパーの初期設定。
arm.set_gripper_mode(0)
arm.set_gripper_enable(True)
arm.set_gripper_speed(3000)

isGripperOpen = False

def OperateGripper():
    global isGripperOpen
    if(isGripperOpen):
        arm.set_gripper_position(320, wait=True)
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
    if z < 94 or z > 500:
        return False
    return True




#x,y,z,roll,pitch,yawの位置を受け取り、その位置にロボットアームを動かす一連の処理を関数にまとめておくと楽。
def SetPosition(x,y,z,roll,pitch,yaw):
    if CheckIfNewPositionInWorkspace(x,y,z):
        _, target_angle = arm.get_inverse_kinematics([x, y, z, roll, pitch, yaw])
        arm.set_servo_angle_j(angles=target_angle, speed=speed)
    else:
        print(" position is out of workspace")



while True:
    _,current_position = arm.get_position() #現在のアームの位置を取得する。 return: [x,y,z,roll,pitch,yaw]
    x,y,z,roll,pitch,yaw = current_position #展開して各変数に代入する。

    if keyboard.is_pressed('down'):
        z = z - 5
        SetPosition(x,y,z,roll,pitch,yaw)
        print("down key pressed")

    if keyboard.is_pressed('up'):
        z = z + 5
        SetPosition(x,y,z,roll,pitch,yaw)
        print("up key pressed")

    if keyboard.is_pressed("w"):
        x = x - 5
        SetPosition(x,y,z,roll,pitch,yaw)
        print("w key pressed")
    
    if keyboard.is_pressed("s"):
        x = x + 5
        SetPosition(x,y,z,roll,pitch,yaw)
        print("s key pressed")

    if keyboard.is_pressed("a"):
        y = y - 5
        SetPosition(x,y,z,roll,pitch,yaw)
        print("a key pressed")

    if keyboard.is_pressed("d"):
        y = y + 5
        SetPosition(x,y,z,roll,pitch,yaw)
        print("d key pressed")

    if keyboard.is_pressed("space"):
        OperateGripper()
        print("s key pressed")
        
    if keyboard.is_pressed('esc'):
        
        print("Exiting...")
        break

    # 処理が反映される間隔を指定
    time.sleep(0.05)

