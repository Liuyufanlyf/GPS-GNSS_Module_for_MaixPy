from fpioa_manager import fm
from machine import UART
import utime

class ATGM336H_5N_GPS():
    def __init__(self,uart_port):
        self.__uart_port = uart_port
        self.GPS_RX_Buffer = ""
        self.GPS_Buffer = ""
        self.isGetData = False
        self.isParseData = False
        self.UTC_Time = ""
        self.latitude = ""
        self.N_S = ""
        self.longitude = ""
        self.E_W = ""
        self.speed_to_groud = 0
        self.course_over_ground = 0
        self.date = ""
        self.DataIsUseful = False

    def errorLog(self,num):
        while(True):
            print("ERROR %d\r\n",num)

    def GPS_Read(self):
        self.GPS_RX_Buffer = self.__uart_port.read(600)
        while self.GPS_RX_Buffer==None:
            self.GPS_RX_Buffer = self.__uart_port.read(600)
        self.GPS_Buffer = self.GPS_RX_Buffer.decode('ASCII')

        # 测试模块工作是否正常的代码，实际应用请注释掉以避免输出信息过多
        #print("This is GPS_RX_Buffer, origin data from uart:")
        #print(self.GPS_RX_Buffer)
        #print("This is GPS_Buffer, after decoding:")
        #print(self.GPS_Buffer)

        # 模块输出的信息很多，为了简便起见我们只选择 RMC 最小定位信息，此部分代码用于从 GPS_Buffer 中截取 RMC 部分
        GPS_BufferHead = self.GPS_Buffer.find("$GPRMC,")
        if GPS_BufferHead == -1:
            GPS_BufferHead = self.GPS_Buffer.find("GNRMC,")
        #print(GPS_BufferHead)
        if GPS_BufferHead == -1:
            print("Cannot read the RMC imformation")
        GPS_BufferTail = self.GPS_Buffer[GPS_BufferHead:].find("\r\n")
        #print(GPS_BufferTail)
        if GPS_BufferTail == -1:
            print("Not end with newline")

        self.GPS_Buffer=self.GPS_Buffer[GPS_BufferHead:GPS_BufferHead+GPS_BufferTail]
        self.isGetData=True

        # 测试模块工作是否正常的代码，实际应用请注释掉以避免输出信息过多
        #print("This is GPS_RX_Buffer, origin data from uart:")
        #print(self.GPS_RX_Buffer)
        #print("This is GPS_Buffer, including RMC info:")
        #print(self.GPS_Buffer)

    def GPS_Parese(self):
        if(self.isGetData == True):
            self.isGetData= False
            print("************")

        temp = self.GPS_Buffer.split(',')

        # RMC 信息中自带的标识符， A 代表有效， B 代表无效
        if temp[2] == 'A':
            self.DataIsUseful = True
        else:
            self.DataIsUseful = False
        self.UTC_Time = temp[1]
        self.UTC_Time = self.UTC_Time[0:1]+':'+self.UTC_Time[2:3]+':'+self.UTC_Time[4:]
        self.latitude = temp[3]
        self.latitude = self.latitude[0:1]+'°'+self.latitude[2:]
        self.N_S = temp[4]
        self.longitude = temp[5]
        self.longitude = self.longitude[0:2]+'°'+self.latitude[2:]
        self.E_W = temp[6]
        self.speed_to_groud = temp[7]
        self.course_over_ground = temp[8]
        self.date = temp[9]
        self.isParseData = True

    def print_GPS_info(self):
        if(self.isParseData):
            self.isParseData = False
            if(self.DataIsUseful):
                print("UTC_Time: %s",self.UTC_Time)
                print("latitude: %s %s",self.latitude,self.N_S)
                print("longitude: %s %s",self.longitude,self.E_W)
            else:
                print("GPS data is not usefull!")
                lcd.draw_string(100,180,"GPS data is not usefull!",lcd.RED,lcd.BLACK)