'''

- set port
- serial write to new program (C++/Arduino) to 

detect.py

# coordinates of setpoint's center
x_cp_sp = width // 2
y_cp_sp = height // 2
area_sp = width * height # setpoint area
# detected centerpoint's coordinates
x_cp_det = (x2 + x1)/2
y_cp_det = (y1 + y2)/2
'''
x_tol_err = 10 # tolerated x error
y_tol_err = 10 # tolerated y error

class yolo_serial:
    def __init__(self, x_cp_det, y_cp_det, x_cp_sp, y_cp_sp):
        # detect.py: map(int, xyxy)
        # serial.py: def __init__(self, xyxy)
        # x1, y1, x2, y2 = map(int, xyxy)

        # calculate position error
        # conditions: if x_detect > x_cp_sp... if necessary
        x_err = x_cp_det - x_cp_sp
        y_err = y_cp_det - y_cp_sp

        self.x = x_err
        self.y = y_err
        '''
        if the bounding box's area is << area_sp:
            approach the target --> send signal to legs
        
        if the bounding box's area approaches area_sp (error+= 5-10 px):
            if x_err >> x_tol_err:
                turn head toward the target --> send signal to head
            elif x_err << x_tol_err:
                ready to grip
        '''

        # self.publish = 
        # usage: yolo_serial(x1, y1, x2, y2).publish

# class color_serial:
    '''
    applicable conditions
    '''

# yolo = yolo_serial(20,30,40,50).x
# print(yolo)