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
        arm.set_gripper_position(320, wait=False)
        isGripperOpen = False
    else:
        arm.set_gripper_position(320, wait=False)
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

def PlusPosition(d_x,d_y,d_z):
    global x, y, z
    # x
    if d_x < 0:
        d_x = -d_x
        for i in range(d_x):
            x -= 1
            SetPosition(x,y,z,roll,pitch,yaw)
    else:
        for i in range(d_x):
            x += 1
            SetPosition(x,y,z,roll,pitch,yaw)
    
    # y
    if d_y < 0:
        d_y = -d_y
        for i in range(d_y):
            y -= 1
            SetPosition(x,y,z,roll,pitch,yaw)
    else:
        for i in range(d_y):
            y += 1
            SetPosition(x,y,z,roll,pitch,yaw)
    
    # z
    if d_z < 0:
        d_z = -d_z
        for i in range(d_z):
            z -= 1
            SetPosition(x,y,z,roll,pitch,yaw)
    else:
        for i in range(d_z):
            z += 1
            SetPosition(x,y,z,roll,pitch,yaw)


_,current_position = arm.get_position() #現在のアームの位置を取得する。 return: [x,y,z,roll,pitch,yaw]
x,y,z,roll,pitch,yaw = current_position #展開して各変数に代入する。

while True:

    if keyboard.is_pressed('down'):
        print("down key pressed")
        PlusPosition(0, 0, -5)

    if keyboard.is_pressed('up'):
        print("up key pressed")
        PlusPosition(0, 0, 5)

    if keyboard.is_pressed("w"):
        print("w key pressed")
        PlusPosition(-5, 0, 0)
    
    if keyboard.is_pressed("a"):
        print("a key pressed")
        PlusPosition(0, -5, 0)
    
    if keyboard.is_pressed("s"):
        print("s key pressed")
        PlusPosition(5, 0, 0)
    
    if keyboard.is_pressed("d"):
        print("d key pressed")
        PlusPosition(0, 5, 0)

    if keyboard.is_pressed("space"):
        OperateGripper()
        
    if keyboard.is_pressed('esc'):
        
        print("Exiting...")
        break

    # 処理が反映される間隔を指定
    time.sleep(0.05)

