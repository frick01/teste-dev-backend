from time import sleep
from smbus2 import SMBus


_I2C_NO_TRANSACTION			= 0
_I2C_SLAVE_ADDRESS_RECEIVED	= 1
_I2C_MODE_RECEIVED			= 2
_I2C_READ_ADDRESS			= 3
_I2C_READ_DATA				= 4
_I2C_MASTER_NACK			= 5

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


class I2cSlave(object):
 
    def __init__(self,bus_i2c,device_address):
        self.bus = SMBus(bus_i2c)
        self.device_address = device_address
        self._SSPBUF = 0x00 
        self.master_status = _I2C_NO_TRANSACTION
        
        self.master_cmd = 0x00
        self.SCRATCH_PAD = [0xFF,0XFF,device_address,0XFF]	

    def _read_data_master(self):
        
           
        return self.bus.read_i2c_block_data(self.device_address,0,3)

   
    def task_i2c_control(self):
        self.token = 0x00
        self._read_data_master() 
        self._SSPBUF = self._read_data_master()
        self.token = self._SSPBUF[1] & _MASK
        print(hex(self.token))  
     
        if self._SSPBUF[0] == self.device_address:
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
            checksum = self.device_address + self.SCRATCH_PAD[3]
            message = [self.device_address,self.SCRATCH_PAD[3],checksum] 
            self.bus.write_i2c_block_data(self.device_address, 0, message)
        
        elif command == EXECUTE_RESET :
            self.SCRATCH_PAD[0] = 0XFF
            self.SCRATCH_PAD[1] = 0x00
            self.SCRATCH_PAD[3] = 0x00
            print(self.SCRATCH_PAD)
            


#app = I2cSlave(19,0x1C)