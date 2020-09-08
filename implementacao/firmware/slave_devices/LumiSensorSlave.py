from I2cSlave import *

_I2C_SLAVE_ADDRESS = 0x1C

_POWER_ON= 0x10
_POWER_OFF = 0x11


RESOLUTION = 0X02

_TCONV_8_BIT = 0.100
_TCONV_9_BIT = 0.250
_TCONV_10BIT = 0.550
_TCONV_12BIT = 0.750

MAX_LUX = 100
MIN_LUX = 0

TARGET_VAL = 10


class LumiSensorSlave(I2cSlave):

    def __init__(self,bus_i2c,device_address):

        super().__init__(bus_i2c,device_address)
        self.lux = 0
 

    def maps(self, val_in,max_in, max_out):
         
        return int(val_in * max_out / max_in)

    def value_simulater(self):             
        if self.lux <10:
            self.lux+=0.535
            sleep(_TCONV_12BIT)
        elif 10  < self.lux < 10.3:        
            self.lux+=0.0253
            sleep(_TCONV_12BIT)
        elif  10.3 < self.lux < 12:
            self.lux+=0.3
            sleep(_TCONV_12BIT)
            
        elif  12 < self.lux < 100:
            self.lux+=1
            sleep(_TCONV_12BIT)
        return self.lux
           
    def task_generate_value(self,command):
        
        if command == _POWER_ON:

            #for i in range(0,10000):
            
            val = self.value_simulater()
            data = self.maps(val,100, 255)
            print(data)
            self.SCRATCH_PAD[3]= data
        
        elif command == _POWER_OFF:
            
            self.lux = 0

    """      
    def scratchpad_control(self,command):

        if command  == EXECUTE_WRITE_SCRATCH_PAD:

            self.SCRATCH_PAD[self.scratch_pad_addr]=self.scratch_pad_val
            print(self.SCRATCH_PAD)
        elif command == EXECUTE_READ_SCRATCH_PAD:
            checksum = _I2C_SLAVE_ADDRESS + self.SCRATCH_PAD[3]
            message = [_I2C_SLAVE_ADDRESS,self.SCRATCH_PAD[3],checksum] 
            self.bus.write_i2c_block_data(self.device_address, 0, message)
        
        elif command == EXECUTE_RESET :
            self.SCRATCH_PAD[0] = _CONTROL_POWEROFF
            self.SCRATCH_PAD[1] = 0x00
            self.SCRATCH_PAD[3] = 0x00
            print(self.SCRATCH_PAD)
            
   
    """ 

    def run(self):
        while True:
            self.task_generate_value(self.SCRATCH_PAD[0])
            self.task_i2c_control()
    
     


app = LumiSensorSlave(19,0x1C)

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
