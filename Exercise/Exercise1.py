import keyboard
import time
import os
import sys
import time
import math

from xarm.wrapper import XArmAPI




"""
Exercise 1: 
この演習では、サンプルコードをベースに、ロボットアームのエンドエフェクターを1周回して四角形を描いてください。

ヒント：
Sampleの流れを参考に,Z軸方向に300m, y軸方向に300mm, Z軸方向に-300mm, X軸方向に-300mmで順番に移動する。


+z(上) +x(正面) +y(左)

"""



################初期設定################

arm = XArmAPI("192.168.1.199") #IP指定してロボットアームと接続。
arm.motion_enable(enable=True) #モーション有効化して動かせるようにする。
arm.set_mode(0) #サーボモードに設定する。
arm.set_state(state=0) #ステート設定: 0 = スタートモーション

speed = 100 #モーターのスピードを設定する。

#######################################


#新しい位置がワークスペース内にあるかどうかを確認する関数
#ロボットアームが環境の障害に衝突しないようにするため。
def CheckIfNewPositionInWorkspace(x,y,z):
    if x > 680  or x < 300:
        return False
    if y < -330 or y > 420:
        return False
    if z < 94 or z > 550:
        return False
    return True





def main():
    #初期位置の指定
    x = 500
    y = -100 
    z = 200
    # 初期ポイントに行く
    if CheckIfNewPositionInWorkspace(x,y,z):
        print("Moving")
        arm.set_position(x,y,z, speed= speed, wait=True )
    else: 
        print("Position is out of workspace")
    
    time.sleep(1) # 移動後に1秒待つ

    z+=200
    #移動先がワークスペース内か調べる
    if CheckIfNewPositionInWorkspace(x,y,z):
        print("Moving")
        arm.set_position(x,y,z, speed= speed, wait=True )
    else: 
        print("Position is out of workspace")
    
    time.sleep(1) # 移動後に1秒待つ

    y-=200
    if CheckIfNewPositionInWorkspace(x,y,z):
        print("Moving")
        arm.set_position(x,y,z, speed= speed, wait=True )
    else: 
        print("Position is out of workspace")

    
    time.sleep(1) # 移動後に1秒待つ

    z-=200
    if CheckIfNewPositionInWorkspace(x,y,z):
        print("Moving")
        arm.set_position(x,y,z, speed= speed, wait=True )
    else: 
        print("Position is out of workspace")

    
    time.sleep(1) # 移動後に1秒待つ

    y+=200
    if CheckIfNewPositionInWorkspace(x,y,z):
        print("Moving")
        arm.set_position(x,y,z, speed= speed, wait=True )
    else: 
        print("Position is out of workspace")
    
    time.sleep(1) # 移動後に1秒待つ





    



    
    

    




if __name__ == "__main__":
    main()
    arm.disconnect()








