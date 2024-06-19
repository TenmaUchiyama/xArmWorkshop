import pydualsense
import math 




class DualSenseController(pydualsense.pydualsense): 

    
    def __init__(self):
        super().__init__()

        #初期化する
        self.init()
      
        self.joystick_left_val = [0, 0]
        self.joystick_right_val = [0, 0]
      
        #イベントハンドラを追加する
        self.left_joystick_changed += self.on_joystick_left
        self.right_joystick_changed += self.on_joystick_right
       


    def on_joystick(self,stateX,stateY):
        #128マックスだから、128で割って0-5に正規化する。また、小数点第一位までに丸める
        stateX_norm = math.floor(( stateX / 128)* 50) / 10
        stateY_norm = math.floor(( stateY / 128)* 50) / 10
    
        self.is_joystick_in = not (-1 < stateX_norm < 1 and -1 < stateY_norm < 1)

        return [stateX_norm, stateY_norm]


    def on_joystick_left(self, stateX, stateY):
        self.joystick_left_val = self.on_joystick(stateX,stateY)


    def on_joystick_right(self, stateX, stateY):
        self.joystick_right_val = self.on_joystick(stateX,stateY)
    
    def get_joystick_left_val(self):
        return self.joystick_left_val
    
    def get_joystick_right_val(self):
        return self.joystick_right_val
    


   
    






