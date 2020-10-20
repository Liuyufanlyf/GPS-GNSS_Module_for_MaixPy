# GPS(GNSS)_Module_for_MaixPy

本项目是一个 [MaixPy]() 库，适用于输出格式符合 CASIC 多模卫星导航接收机协议规范的全球定位系统模组。对特定型号可能有所差别，目前验证了 ATGM336H-5N 模组和合宙 Air530 模组。

ATGM336H-5N 是中科微基于其研发的 AT6558 GNSS Soc 开发的卫星定位模块，支持六种卫星导航系统，具有高灵敏度、低功耗、低成本的特点。

合宙 Air530 模块是一款高性能、高集成度的多模卫星定位导航模块。体积小、功耗低，可用于车载导航、智能穿戴、无人机等 GNSS 定位的应用中。很遗憾的是，该模组目前已停产。

本库封装了模块信息的处理功能，使用户可通过对象成员访问操作获取时间、经纬度、速度、航向等信息。

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

