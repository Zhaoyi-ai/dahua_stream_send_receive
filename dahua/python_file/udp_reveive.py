import socket
import struct
import cv2
import numpy as np


ip_port = ('192.168.13.202', 5005) # 目标计算机的IP以及端口，5005端口为UDP协议的实时传输端口号
BUFSIZE = 65507
# socket.AF_INET：用于internet进程间通讯
# socket.SOCK_DGRAM：套接字类型，SOCK_STREAM（流式套接字，主要用于 TCP 协议）
udp_server_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind()将套接字绑定到特定地址
# bind接收一个元组,用于绑定本地的ip地址和端口号，ip如果''则会绑定本机的任意一个ip, 端口如果不指定,系统会随机分配
udp_server_client.bind(ip_port)
# print("udp_server_client: " + str(udp_server_client))
# print("type: " + str(type(udp_server_client)))


def receive():

    # while True:
    try:
        while True:
            # 获取数据头信息，第一个参数为信息，第二个参数是发送方ip地址
            # buffer为接收到的数据，是一个字节字符串
            buffer, _ = udp_server_client.recvfrom(BUFSIZE)
            # buffer type: <class 'bytes'>
            print("buffer type: " + str(type(buffer)))
            # buffer: b'g{\x00\x00'
            print("buffer: " + str(buffer))
            # len: 4
            print("len: " + str(len(buffer)))  # 可能为4或60000+，4代表文件头
            if len(buffer) == 4:
                # print(buffer)  # b'g{\x00\x00'   # 每次都不一样的
                # 解包，看看有多大（unpack返回的是只有一个元素的元组，如(64282,)，元素个数貌似取决于fmt）
                # data_size代表图片长度
                data_size = struct.unpack('i', buffer)[0]
                # 31591
                print(data_size)
                print("data_size: " + str(type(data_size)))
            else:
                print('不是文件头，请继续下次循环！')
                # cv2.destroyAllWindows()
                continue

            # 重写接收程序
            recv_times = data_size // BUFSIZE + 1
            # 1
            print(recv_times)  # 按目前的BUFSIZE，为1或2，大部分为2
            data_total = b''
            recvd_size = 0
            for count in range(recv_times):
                data, _ = udp_server_client.recvfrom(BUFSIZE)
                recvd_size += len(data)
                data_total += data
            # 判断data_total长度是否等于图片长度，不是就继续下次循环
            # print(len(data_total))
            if len(data_total) != data_size:
                print('一定又是哪接收出错了，导致没接收上，继续下轮循环！')
                continue
            print('received!')
            # fromstring，frombuffer:从字节符串中解码出数据
            nparr = np.frombuffer(data_total, np.uint8) # frombuffer fromstring
            print("nparr: " + str(nparr))  # [255 216 255 ...  15 255 217] # 每次不一样的
            print("nparr type: " + str(type(nparr)))
            print("nparr len: " + str(len(nparr)))
            # imdecode:将图像数据从存储格式中解析出来并转化为OpenCV中的图像格式
            img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # print("img_decode: " + str(img_decode))
            print("img_decode len: " + str(len(img_decode)))
            print("img_decode type: " + str(type(img_decode)))
            cv2.imshow('receive frame', img_decode)
            # 保存截图
            # cv2.imwrite('{}.jpg'.format(time.clock()), img_decode)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # cv2.destroyAllWindows()
                break
    except:
        print('出现异常，继续调用receive()函数！')


if __name__ == '__main__':
    receive()