from I2cSlave import *
from time import sleep

_I2C_SLAVE_ADDRESS = 0x1C

_POWER_ON= 0x10
_POWER_OFF = 0x11





TARGET_VAL = 10


class DistanceSensorSlave(I2cSlave):

    def __init__(self,bus_i2c,device_address):

        super().__init__(bus_i2c,device_address)
        self.distance_cm = 0
        self.max_distance = 400
 

    def maps(self, val_in,max_in, max_out):
         
        return int(val_in * max_out / max_in)

    def distance_handler(self):             
       
        if self.distance_cm <= self.max_distance:
            self.distance_cm+=1
            sleep(0.750)
            
        elif self.distance_cm >= self.max_distance:
            
            self.distance_cm = 0

        return self.distance_cm

    def set_max_distance(self):

        self.max_distance = float(self.maps(self.SCRATCH_PAD[1],255,400))
           
    def task_generate_value(self,command):
        
        if command == _POWER_ON:


            self.set_max_distance()
            val = self.distance_handler()
            data = self.maps(val,self.max_distance, 255)
            print(data)
            self.SCRATCH_PAD[3]= int(data)
        
        elif command == _POWER_OFF:
            
            self.distance_m = 0


    def run(self):
        while True:
            self.task_generate_value(self.SCRATCH_PAD[0])
            self.task_i2c_control()
    
     


app = DistanceSensorSlave(19,0x1C)

app.run()







    

     
"""         

b = LumiSensorSlave(1)


for i in range(0,10000):
   

    val = b.value_simulater()
    data = b.maps(val,100, 255)
    
    with SMBus(19) as bus:

        bus.write_byte_data(0x1C, 0, data)    

        print(hex(data))


"""
