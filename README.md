# MaixPy_ATGM336H_5N_Module
这是一个适用于 ATGM336H-5N 卫星定位模块的 MaixPy 库

This is a MaixPy library of ATGM336H, which can be use in MAIX development kit.

ATGM336H-5N 是中科微基于其研发的 AT6558 GNSS Soc 开发的卫星定位模块，支持六种卫星导航系统，具有高灵敏度、低功耗、低成本的特点。本库封装了模块信息的处理功能，使用户可通过对象成员访问操作获取时间、经纬度、速度、航向等信息。

## Example

本示例在 MAIX GO 开发板上验证通过

```python
from fpioa_manager import fm
from machine import UART
from board import board_info
import utime, lcd
from ATGM336H_5N import ATGM336H_5N

lcd.init()

# 创建卫星定位模块使用的串口对象
fm.register(15,fm.fpioa.UART1_TX,force=True)
fm.register(17,fm.fpioa.UART1_RX,force=True)
uart1 = UART(UART.UART1, 9600,8,0,0,timeout=1000,read_buf_len=2048)

GNSS = ATGM336H_5N(uart1)

utime.sleep_ms(900)

while True:
    # 读取、解码、在 LCD 上显示并通过串口打印获取的定位信息
    GNSS.GNSS_Read()
    GNSS.GNSS_Parese()
    lcd.clear(lcd.WHITE)
    lcd.draw_string(10,40,"Date: "+GNSS.date,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(10,60,"UTC Time: "+GNSS.UTC_Time,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(10,80,"latitude: "+GNSS.latitude+GNSS.N_S,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(10,100,"longitude: "+GNSS.longitude+GNSS.E_W,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(10,120,"Speed: "+str(GNSS.speed_to_groud_kh),lcd.BLACK,lcd.WHITE)
    lcd.draw_string(10,140,"Course_over_ground: "+str(GNSS.course_over_ground),lcd.BLACK,lcd.WHITE)
    GNSS.print_GNSS_info()
    utime.sleep(5)

```

## 已知的局限

1. 定位模块输出信息使用 UART 缓冲区接收，再由程序读取。但当程序读取时缓冲区被修改，将导致接收到的信息存在乱码，一般而言在下次刷新就能够消除影响。在进行更多的修复之前，其他程序访问成员时应进行格式检查
2. 定位模块每秒输出一次定位信息并提供了 PPS 脉冲同步，但本库并未使用 PPS 引脚同步读取，而是使用 K210 芯片的串口缓冲机制。为了保证每次读取均能刷新定位信息，建议将读取时间间隔设定在 3s 或以上
3. 从 GNSS_Buffer 中截取 RMC 的代码存在未知 bug，导致截取到的信息并非完整的 RMC 信息、进入异常处理，不影响正常使用

## 对象成员

| 成员名             | 含义                                            |
| ------------------ | ----------------------------------------------- |
| __uart_port        | 模块使用的串口对象                              |
| GNSS_RX_Buffer     | 从串口接收的信息缓冲区                          |
| GNSS_Buffer        | 经解码提取后的信息缓冲区，含有 RMC 最小定位信息 |
| UTC_Time           | UTC 时间                                        |
| latitude           | 纬度                                            |
| N_S                | 北纬/南纬                                       |
| longitude          | 经度                                            |
| E_W                | 东经/西经                                       |
| speed_to_groud     | 对地速度（节）                                  |
| speed_to_groud_kh  | 对地速度（千米每小时）                          |
| course_over_ground | 方向角，与真北方向的夹角                        |
| isDecodeData       | 是否解码完成                                    |
| isParseData        | 是否解析完成                                    |
| DataIsUseful       | 数据是否被使用过                                |



## 对象方法

| 方法名                    | 含义         | 参数           |
| ------------------------- | ------------ | -------------- |
| \__init__(self,uart_port) | 初始化       | 使用的串口对象 |
| GNSS_Read(self)           | 读取信息     |                |
| GNSS_Parese(self)         | 解析信息     |                |
| print_GNSS_info(self)     | 串口打印信息 |                |

