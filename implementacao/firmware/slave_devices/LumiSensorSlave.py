from time import sleep
from smbus2 import SMBus
from threading import Thread
#serial comunicates states
_I2C_NO_TRANSACTION			= 0
_I2C_SLAVE_ADDRESS_RECEIVED	= 1
_I2C_MODE_RECEIVED			= 2
_I2C_READ_ADDRESS			= 3
_I2C_READ_DATA				= 4
_I2C_MASTER_NACK			= 5


_I2C_SLAVE_ADDRESS = 0x1C

_POWER_ON= 0x10
_POWER_OFF = 0x11



_MODE_WRITE_SCRATCH_PAD = 0XAA
_MODE_READ_SCRATCH_PAD = 0xAB
_MODE_RESET_SCRATCH_PAD = 0XAC



_MASTER_W_DATA = 0x20
_MASTER_R_ADDRES = 0x05
_MASTER_R_DATA = 0x21

_MASK = 0X25


EXECUTE_WRITE_SCRATCH_PAD = 0XA1
EXECUTE_READ_SCRATCH_PAD = 0XA2
EXECUTE_RESET = 0xA3
EXECUTE_NONE = 0xA0

RESOLUTION = 0X02

_TCONV_8_BIT = 0.100
_TCONV_9_BIT = 0.250
_TCONV_10BIT = 0.550
_TCONV_12BIT = 0.750

MAX_LUX = 100
MIN_LUX = 0

TARGET_VAL = 10


class LumiSensorSlave(object):
 
    def __init__(self,bus_i2c,device_address):
        self.bus = SMBus(bus_i2c)
        self.device_address = device_address
        self.lux = MIN_LUX
        self._SSPBUF = 0x00 
        
        self.master_status = _I2C_NO_TRANSACTION
        self.master_cmd = 0x00
        self.SCRATCH_PAD = [_POWER_OFF,RESOLUTION,device_address,0]	

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



    def _read_data_master(self):
        
        #self._SSPBUF = self.bus.read_byte_data(self.device_address, 0)
        
        return self.bus.read_i2c_block_data(self.device_address,0,3)
        #self.bus.close()

   
    def task_i2c_control(self):
        self.token = 0x00
        self._read_data_master() 
        self._SSPBUF = self._read_data_master()
        self.token = self._SSPBUF[1] & _MASK
        print(hex(self.token))  
     
        if self._SSPBUF[0] == _I2C_SLAVE_ADDRESS:
            self.master_status = _I2C_SLAVE_ADDRESS_RECEIVED  
            print("_I2C_SLAVE_ADDRESS_RECEIVED ")  

            temp = self._SSPBUF[1]
            if self.master_status == _I2C_SLAVE_ADDRESS_RECEIVED:  
                self.master_index = 0
                self.master_status = _I2C_MODE_RECEIVED
                print("_I2C_MODE_RECEIVED")
                self.master_mode = temp
                                                                       
                if self.master_mode == _MODE_WRITE_SCRATCH_PAD: #comando 0xAA
                    print("_MODE_WRITE_SCRATCH_PAD")
                    while(self._read_data_master()[1] == 0XAA):
                        print("aguardando endereçp do scratchpad")
                    self.scratch_pad_addr = self._read_data_master()[1]
                    while(self._read_data_master()[1] == self.scratch_pad_addr ):
                        print("aguardando valor")
                    self.scratch_pad_val = self._read_data_master()[1]
                    self.master_cmd = EXECUTE_WRITE_SCRATCH_PAD  

                elif self.master_mode == _MODE_READ_SCRATCH_PAD:#We 've got the EEPROM address
                    print("_MODE_READ_SCRATCH_PAD")        
                    self.master_cmd = EXECUTE_READ_SCRATCH_PAD
                elif self.master_mode ==_MODE_RESET_SCRATCH_PAD:
                    self.master_cmd = EXECUTE_RESET
                    print("_MODE_RESET_SCRATCH_PAD")

                self.scratchpad_control(self.master_cmd)

          
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
            


    def run(self):
        while True:
            self.task_generate_value(self.SCRATCH_PAD[0])
            self.task_i2c_control()
    
         


app = LumiSensorSlave(19,0x1C)

app.run()
#Thread_1=Thread(target=app..start()
#Thread_2=Thread(target=app.).start()






    

     
"""         

b = LumiSensorSlave(1)


for i in range(0,10000):
   

    val = b.value_simulater()
    data = b.maps(val,100, 255)
    
    with SMBus(19) as bus:

        bus.write_byte_data(0x1C, 0, data)    

        print(hex(data))


"""
