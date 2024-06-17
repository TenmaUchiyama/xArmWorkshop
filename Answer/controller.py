from DualSense import DualSenseController
import time
from xarm.wrapper import XArmAPI

arm = XArmAPI("192.168.1.199") #IP指定してロボットアームと接続。



speed = 10 #モーターのスピードを設定する。


def init():
        
    
    arm.set_mode(1) #サーボモードに設定する。
    arm.set_state(0)


    # グリッパーの設定。
    arm.set_gripper_mode(0) 
    arm.set_gripper_enable(enable = True)
    arm.set_gripper_speed(3000)

init()
                                    

dualsense = DualSenseController()
vibration_on = False
on_change_vibration_state = False


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
    global vibration_on
    global on_change_vibration_state
    if CheckIfNewPositionInWorkspace(x,y,z):
        _, target_angle = arm.get_inverse_kinematics([x, y, z, roll, pitch, yaw])
        arm.set_servo_angle_j(angles=target_angle, speed=speed)
        vibration_on = False
        on_change_vibration_state = True
    else:
        print("position is out of workspace")
        vibration_on=True
        on_change_vibration_state = True


while not dualsense.state.touchBtn: 
    
    left_joy = dualsense.get_joystick_left_val()
    right_joy = dualsense.get_joystick_right_val() 

    dirX = left_joy[1]
    dirY = left_joy[0]
    dirZ = -right_joy[1]
    

    print(dirX)
    _, position  = arm.get_position()
    x,y,z,roll,pitch,yaw = position
    SetPosition(x+dirX,y+dirY,z+dirZ,roll,pitch,yaw)


    # 処理が反映される間隔を指定
    time.sleep(0.05)

    if arm.has_error:

        init() 
        time.sleep(1)


    if dualsense.state.R1:
        OperateGripper()
        dualsense.light.setColorI(0,255,0)
    

    if on_change_vibration_state:

        if vibration_on: 
            dualsense.setLeftMotor(200)
            dualsense.setRightMotor(200)
            dualsense.light.setColorI(255,0,0)
        else:
            dualsense.setLeftMotor(0)
            dualsense.setRightMotor(0)
            dualsense.light.setColorI(0,0,255)

        on_change_vibration_state = False
arm.disconnect()
dualsense.close()



