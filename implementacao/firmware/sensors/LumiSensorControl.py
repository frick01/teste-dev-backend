__version__ = "0.0.0-auto.0"

#__repo__
from smbus2 import SMBus

from time import sleep


DEVICE_ADDRESS = 0x1C

_CONTROL_POWERON= 0x10
_CONTROL_POWEROFF = 0x11

_RESOLUTION = 0X19
WRITE = "write"
       
READ = "read"
class LumiSensor(object):

    """Class which provides interface to light sensor."""

    
    
    def __init__(self,bus_i2c,device_address):
        self.bus = SMBus(bus_i2c)
        self.device_address = device_address
        #self._enable()

    
    """    
    @property
    def lux(self):
        
        
        
        return self._compute_lux()
    """
    def _enable(self):
       self._write_control_register(_CONTROL_POWERON)

    
    def _disable(self):

        self._write_control_register(_CONTROL_POWEROFF)
    
        
    """ok"""
    def _write_control_register(self, reg, cont=0):
       

        if reg ==_CONTROL_POWERON or _CONTROL_POWEROFF:
            address_register = 0x00   
        elif reg == RESOLUTION:
            address_register = 0x01
        elif reg == DEVICE_ADDRES:
            address_register = 0x02
        print("addres_regiter:%x"%(address_register))
 
        for cont in range (0,3):
            print(cont)
            if cont == 0:
                self.set_mode(WRITE)
            elif cont == 1:
                self.send_commands(address_register)
            elif cont == 2:
                self.send_commands(reg)
             
            sleep(1)
    
    def set_mode(self,mode):

       
        if mode =="write":
        
            self.send_commands(0xAA)
        
        elif mode == "read":

            self.send_commands(0xAB)
  
    def send_commands(self,command):

        checksum = self.device_address+command
        packet= [self.device_address,command,checksum]
        self.bus.write_i2c_block_data(self.device_address, 0, packet)

    
    def read_data(self):

        packet_received =  self.bus.read_i2c_block_data(self.device_address,0,3)

        return packet_received
            
     
    def _compute_lux(self,data):


        lux = self.maps(data,255,100)

        return lux

    def get_luminosity(self):

        return self._compute_lux(self.read_data()[1])



    def maps(self, val_in,max_in, max_out):
         
        return int(val_in * max_out / max_in)

   
app = LumiSensor(19,0x1C)
        
app._write_control_register(0x10)

app.set_mode(READ)

while True:
    print(app.get_luminosity())
