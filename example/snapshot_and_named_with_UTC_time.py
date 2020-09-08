# 2020.09.08

from fpioa_manager import fm
from machine import UART, Timer
from board import board_info
import time, lcd, image, sensor
from ATGM336H_5N import ATGM336H_5N

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames()

fm.register(15,fm.fpioa.UART1_TX,force=True)
fm.register(17,fm.fpioa.UART1_RX,force=True)
uart1 = UART(UART.UART1, 9600,8,0,0,timeout=1000,read_buf_len=2048)
GNSS = ATGM336H_5N(uart1)
#time.sleep_ms(500)

def GNSS_update(timer):
    GNSS.GNSS_Read()
    GNSS.GNSS_Parese()
    #lcd.clear(lcd.WHITE)
    #lcd.draw_string(10,40,"Date: "+GNSS.date,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(0,0,"UTC Time: "+GNSS.UTC_Time,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(0,20,"latitude:  "+GNSS.latitude+GNSS.N_S,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(0,40,"longitude: "+GNSS.longitude+GNSS.E_W,lcd.BLACK,lcd.WHITE)
    lcd.draw_string(0,60,"Speed: "+str(GNSS.speed_to_groud_kh)+"km/h",lcd.BLACK,lcd.WHITE)
    #lcd.draw_string(10,140,"Course_over_ground: "+str(GNSS.course_over_ground),lcd.BLACK,lcd.WHITE)
    GNSS.print_GNSS_info()

tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=3000, callback=GNSS_update)
        #tim = Timer(Timer.TIMER1, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=3000, callback=snapshot_and_save)
tim.start()

while True:
    i=0
    if GNSS.UTC_Time != "-1":
        path = "/sd/"+GNSS.UTC_Time[0:2]+GNSS.UTC_Time[3:5]+GNSS.UTC_Time[6:8]+".jpg"
        print(GNSS.UTC_Time)
    else:
        path = "/sd/"+str(i)+".jpg"
    img = sensor.snapshot()
    img.save(path)
    print("saved")
    img_read = image.Image(path)
    lcd.display(img_read)
    if i==9999999:
        i =0
    i+=1