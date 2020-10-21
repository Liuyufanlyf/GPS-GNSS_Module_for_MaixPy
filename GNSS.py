from fpioa_manager import fm
from machine import UART
import utime

# GNSS 基类，基于 ATGM336H-5N
class GNSS():
    def __init__(self, uart_port):
        self.__uart_port = uart_port
        self.GNSS_RX_Buffer = ""
        self.GNSS_Buffer = ""
        self.UTC_Time = ""
        self.latitude = -1
        self.N_S = ""
        self.longitude = -1
        self.E_W = ""
        self.speed_to_groud = ""
        self.speed_to_groud_kh = 0
        self.course_over_ground = ""
        self.date = ""
        self.isDecodeData = False
        self.isParseData = False
        self.DataIsUseful = False

    def GNSS_Read(self):
        self.GNSS_RX_Buffer = self.__uart_port.read(1200)
        while type(self.GNSS_RX_Buffer)!=bytes:
            self.GNSS_RX_Buffer = self.__uart_port.read(1200)

        # 当电子线路连接不可靠，如使用杜邦线时接收到的信息可能因为含有非 ASCII 字符，引发 UnicodeError
        # AttributeError 引发原因未知
        while self.isDecodeData==False:
            try:
                self.GNSS_Buffer = self.GNSS_RX_Buffer.decode('ASCII')
                self.isDecodeData = True
            except UnicodeError:
                self.GNSS_RX_Buffer = self.__uart_port.read(1200)
            except AttributeError:
                self.GNSS_RX_Buffer = self.__uart_port.read(1200)

        # 测试模块工作是否正常的代码，实际应用请注释掉以避免输出信息过多
        #print("This is GNSS_RX_Buffer, origin data from uart:")
        #print(self.GNSS_RX_Buffer)
        #print("This is GNSS_Buffer, after decoding:")
        #print(self.GNSS_Buffer)

        # 本类只解码 RMC 最小定位信息，此部分代码用于从 GNSS_Buffer 中截取 RMC 部分
        GNSS_BufferHead = self.GNSS_Buffer.find("$GPRMC,")
        if GNSS_BufferHead == -1:
            GNSS_BufferHead = self.GNSS_Buffer.find("GNRMC,")
        if GNSS_BufferHead == -1:
            print("Cannot read the RMC imformation")
            self.isDecodeData = False
        else:
            GNSS_BufferTail = self.GNSS_Buffer[GNSS_BufferHead:].find("\r\n")
            if GNSS_BufferTail == -1:
                print("Not end with newline")
                self.isDecodeData = False

            self.GNSS_Buffer=self.GNSS_Buffer[GNSS_BufferHead:GNSS_BufferHead+GNSS_BufferTail]

        # 测试模块工作是否正常的代码，实际应用请注释掉以避免输出信息过多
        # print("This is GNSS_RX_Buffer, origin data from uart:")
        # print(self.GNSS_RX_Buffer)
        # print("This is GNSS_Buffer, including RMC info:")
        # print(self.GNSS_Buffer)

    def GNSS_Parese(self):
        if(self.isDecodeData == True):
            self.isDecodeData= False
            print("*****************************************")

            temp = self.GNSS_Buffer.split(',')

            try:
                # RMC 信息中自带的标识符， A 代表有效， V 代表无效
                if temp[2] == 'A':
                    self.DataIsUseful = True
                elif temp[2] == 'V':
                    self.DataIsUseful = False
                else:
                    raise GNSSException("Data decode fail","Not a 'A' or 'V'")

                if temp[1] == "":
                    self.UTC_Time = "-1"
                else:
                    self.UTC_Time = temp[1]
                    self.UTC_Time = self.UTC_Time[0:2]+':'+self.UTC_Time[2:4]+':'+self.UTC_Time[4:6]

                if temp[3] == "":
                    self.latitude = -1
                else:
                    try:
                        # 提供 ddmmmmm 格式的字符串输出和 ddddddd 格式的浮点数输出
                        #self.latitude = self.latitude[0:2]+'°'+self.latitude[2:]+'\''
                        self.latitude = float(temp[3][0:2])+float(temp[3][2:])/60.0
                    except Exception:
                        raise GNSSException("latitude exception", "convert to float failed")
                    else:
                        if self.latitude < 0 or self.latitude > 90:
                            raise GNSSException("latitude exception", "latitude out of range")
                            

                self.N_S = temp[4]
                if self.N_S != 'N' or self.N_S != 'S':
                    raise GNSSException("N_S error", "not N or S")

                if temp[5] == "":
                    self.longitude = "-1"
                else:
                    try:
                        # 提供 ddmmmmm 格式的字符串输出和 ddddddd 格式的浮点数输出
                        #self.longitude = self.longitude[0:3]+'°'+self.latitude[3:]
                        self.longitude = float(temp[5][0:3])+float(temp[5][3:])/60.0
                    except Exception:
                        raise GNSSException("longtitude exception", "convert to float failed")
                    else:
                        if self.longitude < 0 or self.longitude > 180:
                            raise GNSSException("longtitude exception", "longtitude out of range")

                self.E_W = temp[6]
                if self.E_W != 'E' or self.E_W != 'W':
                    raise GNSSException("E_W error", "not E or W")
                
                # RMC 中的速度以节为单位
                if temp[7] != "":
                    try:
                        self.speed_to_groud = float(temp[7])
                        self.speed_to_groud_kh = self.speed_to_groud*1.852
                    except ValueError:
                        raise GNSSException("speed decode fail","valueError")
                else:
                    self.speed_to_groud = -1
                    self.speed_to_groud_kh = -1

                if temp[8] != "":
                    try:
                        self.course_over_ground = float(temp[8])
                    except ValueError:
                        raise GNSSException("speed decode fail","valueError")
                else:
                    self.course_over_ground = -1

                if temp[9] == "":
                    self.date = "-1"
                else:
                    self.date = temp[9]
                    self.date = self.date[4:6]+'.'+self.date[2:4]+'.'+self.date[0:2]

                self.isParseData = True
            except IndexError:
                raise GNSSException("index error","index error")

    def print_GNSS_info(self):
        if(self.isParseData):
            self.isParseData = False
            if(self.DataIsUseful):
                print("latitude: %f %s",self.latitude,self.N_S)
                print("longitude: %f %s",self.longitude,self.E_W)
                print("Date: %s",self.date,end=' ')
                print("UTC_Time: %s",self.UTC_Time)
                print("speed: %f km/h",self.speed_to_groud_kh)
                print("course_over_groud: %f°",self.course_over_ground)
            else:
                print("GNSS data is not usefull!")

# 完整的定位信息解读，而非只有 RMC 信息
class GNSS_complex(GNSS):
    def __init__(self, uart_port):
        super().__init__(uart_port)

    
        

# 此异常类用于处理错误的定位信息，包括解码失败和不合常理的位置信息 
class GNSSException(Exception):
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason