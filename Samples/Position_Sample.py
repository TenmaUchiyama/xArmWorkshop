import os
import sys
import time
import math

from xarm.wrapper import XArmAPI


"""
Position_Sampleでは、ポジションモードで単純にロボットアームを上方向に100m移動するコードを書いています。


処理の流れ：
1. 指定先の座標を決定する。
2. arm.set_positionを使ってロボットアームのエンドエフェクタを動かす。
"""


################初期設定################
arm = XArmAPI("192.168.1.199") #IP指定してロボットアームと接続。
arm.motion_enable(enable=True) #モーション有効化して動かせるようにする。

arm.set_mode(0) #ポジション制御モードに設定する。

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
    x = 400
    y = 200 
    z = 400

    z += 100
    if CheckIfNewPositionInWorkspace(x,y,z): #新しい値がworkspaceに存在するかを調べる。
        arm.set_position(x,y,z, speed= speed, wait=True ) #ポジションを指定する。

    





if __name__ == "__main__":
    main() 
    arm.disconnect()

