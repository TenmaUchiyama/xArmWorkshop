import time

from xarm.wrapper import XArmAPI




"""
Exercise 1: 
この演習では、ロボットアームのエンドエフェクターを1周回して四角形を描いていただきます。

ヒント：
Position_Sampleの流れを参考に,Z軸方向に500mm, Y軸方向に500mm, Z軸方向に-500mm, Y軸方向に-500mmで順番に移動する。

"""



################初期設定################

arm = XArmAPI("192.168.1.199") #IP指定してロボットアームと接続。
arm.motion_enable(enable=True) #モーション有効化して動かせるようにする。
arm.set_mode(0) #ポジション制御モードに設定する。
arm.set_state(state=0) #ステート設定: 0 = スタートモーション

speed = 50 #アームのスピードを設定する。

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





#main関数の中にコードを記述していく。
def main():
    #初期位置の指定
    x = 500
    y = -100 
    z = 200

    if CheckIfNewPositionInWorkspace(x,y,z):
        print("Moving")
        arm.set_position(x,y,z, speed= speed, wait=True )
    else: 
        print("座標はワークスペース外です。")

    
  
    time.sleep(1) #移動後に1秒待つ。

  
    
    time.sleep(1) #移動後に1秒待つ。

   
    
    time.sleep(1) #移動後に1秒待つ。

    
    time.sleep(1) #移動後に1秒待つ。



    
    

    




if __name__ == "__main__":
    main()
    arm.disconnect()








