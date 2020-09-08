from I2cSlave import *
from time import sleep


V_REF_3V3 = 0x33
V_REF_5V =  0x50

CONTROL_POWERON = 0x10
CONTROL_POWEROFF = 0x11

    
class SensorBattSlave(I2cSlave):
    def __init__(self,bus_i2c,device_address):
        super().__init__(bus_i2c,device_address)
        self.volt= 0.0
        self.vref = 3.3

    def maps(self, val_in,max_in, max_out):

        return int(val_in * max_out / max_in)

    def battery_handler(self):
       
        if self.volt==0.3*self.vref:
            self.volt+=0.01
            sleep(0.750)
        elif 0.3*self.vref < self.volt < 0.70*self.vref:
            self.volt+=0.1
            sleep(0.750)
        elif 0.7*self.vref <= self.volt < self.vref:
             self.volt-=0.3
             sleep(0.750)

        return self.volt

    def set_vref(self):

        if self.SCRATCH_PAD[1] == V_REF_3V3:
            self.vref = 3.3
        elif self.SCRATCH_PAD[1]== V_REF_5V:
            self.vref = 5.0

    def task_generate_value(self,command):
        
        if command == CONTROL_POWERON:

            self.set_vref()
            val = self.battery_handler()
            data = self.maps(val,100, 255)
            print(data)
            self.SCRATCH_PAD[3]= data
        
        elif command == CONTROL_POWEROFF:
            
            self.volt = 0

          

    def run(self):
        while True:
            self.task_generate_value(self.SCRATCH_PAD[0])
            self.task_i2c_control()


     

app=SensorBattSlave(19,0x1c)


app.run()
    