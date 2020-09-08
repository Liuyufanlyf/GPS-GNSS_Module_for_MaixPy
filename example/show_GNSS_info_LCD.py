from fpioa_manager import fm
from machine import UART
from board import board_info
import utime, lcd
from ATGM336H_5N import ATGM336H_5N
lcd.init()
fm.register(15,fm.fpioa.UART1_TX,force=True)
fm.register(17,fm.fpioa.UART1_RX,force=True)
uart1 = UART(UART.UART1, 9600,8,0,0,timeout=1000,read_buf_len=2048)
GNSS = ATGM336H_5N(uart1)
utime.sleep_ms(900)
while True:
    GNSS.GNSS_Read()
    GNSS.GNSS_Parese()
    lcd.clear(lcd.WHITE)
    lcd.draw_string(10,40,"Date: "+GNSS.date,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(10,60,"UTC Time: "+GNSS.UTC_Time,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(10,80,"latitude:  "+GNSS.latitude+GNSS.N_S,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(10,100,"longitude: "+GNSS.longitude+GNSS.E_W,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(10,120,"Speed: "+str(GNSS.speed_to_groud_kh)+"km/h",lcd.BLACK,lcd.WHITE)
    lcd.draw_string(10,140,"Course_over_ground: "+str(GNSS.course_over_ground),lcd.BLACK,lcd.WHITE)
    #GNSS.print_GNSS_info()
    utime.sleep(3)
