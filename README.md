# MaixPy_ATGM336H_5N_Module
这是一个适用于 ATGM336H-5N 卫星定位模块的 MaixPy 库

This is a MaixPy library of ATGM336H, which can be use in MAIX development kit.

ATGM336H-5N 是中科微基于其研发的 AT6558 GNSS Soc 开发的卫星定位模块，支持六种卫星导航系统，具有高灵敏度、低功耗、低成本的特点。本库封装了模块信息的处理功能，使用户可通过对象成员访问操作获取时间、经纬度、速度、航向等信息。

## Example

本示例在 MAIX GO 开发板上验证通过

```
from fpioa_manager import fm
from machine import UART
from board import board_info
import utime, lcd
from ATGM336H_5N_GPS import ATGM336H_5N_GPS

lcd.init()

# 创建 GPS 模块使用的串口对象
fm.register(15,fm.fpioa.UART1_TX,force=True)
fm.register(17,fm.fpioa.UART1_RX,force=True)
uart1 = UART(UART.UART1, 9600,8,0,0,timeout=1000,read_buf_len=4096)

GPS = ATGM336H_5N_GPS(uart1)

while True:
    GPS.GPS_Read()
    GPS.GPS_Parese()

    # 在 LCD 上显示时间、经纬度信息
    lcd.draw_string(10,120,"UTC Time: "+GPS.UTC_Time,lcd.RED,lcd.BLACK)
    lcd.draw_string(10,140,"latitude: "+GPS.latitude+GPS.N_S,lcd.RED,lcd.BLACK)
    lcd.draw_string(10,160,"longitude: "+GPS.longitude+GPS.E_W,lcd.RED,lcd.BLACK)

    # 串口打印 GPS 相关信息
    GPS.print_GPS_info()
    
    utime.sleep(10)
```

