# Aqui deverá colocar a documentação gerada:
  - API
  - Diagrama do código
  * O que mais julgar necessário

## ESTE ARQUIVO PODERÁ SER TOTALMENTE ALTERADO, CASO O DESENVOLVEDOR DESEJAR


# Usando o I2C-Stub para emular um dispositivo I2C
O módulo i2c-stub é um driver I2C / SMBus falso.

Pré-requisitos:
- i2c-tools instalado

Uso:
-carregue o módulo i2c-stub;

$ modprobe i2c-stub chip_addr=0x1c

-o parâmetro chip_addr especifica o endereço do dispositivo escravo;

-use i2cset para pré-carregar alguns dados nos endereço

$ i2cset 19 0x1C 0x07 0x04 b

$ i2cset 19 0x1C 0x22 0x64 w

-i2cset é usado para definir os registros I2C.

-O primeiro parâmetro passado refere-se ao número do barramento I2C associado ao i2c-stub
-Este número pode ser anotado executando o comando i2cdetect -l;
-Neste caso o número do barramente retornado foi 19;
-Os dois últimos parâmetros referem-se ao valor a escrever e ao tamanho da escrita.

-carregue o módulo de driver do chip de destino.
$ echo al3320a 0x1c > /sys/class/i2c-adapter/i2c-19/new_device

observe seu comportamento no log do kernel.
Você pode usar o dmesg para isso.

$ modprobe i2c-stub chip_addr=0x1c