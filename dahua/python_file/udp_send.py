import socket
import cv2
import struct


# Channels代表通道号，channel = 1：正常摄像头画面 channel = 2：热成像摄像头画面
# subtype代表码流类型 subtype = 0：主码流 subtype = 1：子码流，主码流比子码流清晰，子码流适用于低带宽的网络传输
cap = cv2.VideoCapture('rtsp://admin:admin123@192.168.13.117:554/cam/realmonitor?channel=1&subtype=1')
# cap:< cv2.VideoCapture 0000023669D81870>
print("cap:" + str(cap))


# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_FPS, 30)


# 配置 UDP 服务器
UDP_IP = "192.168.13.202"  # 目标计算机的 IP 地址
UDP_PORT = 5005
# socket.AF_INET：用于internet进程间通讯
# socket.SOCK_DGRAM：套接字类型，SOCK_STREAM（流式套接字，主要用于 TCP 协议）
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:

    ret, frame = cap.read()
    # current status:True
    print("current status:" + str(ret))
    print("frame len: " + str(len(frame)))
    ## frame--type:<class 'numpy.ndarray'>，三维矩阵
    cv2.imshow("send frame", frame)

    # 将算法植入此处


    # 将图像编码为JPEG格式
    # imencode：将图像数据(<class 'numpy.ndarray'>)编码为指定格式的图像文件并返回一个二进制表示
    # jpeg_image:[255 216 255 ...  63 255 217]
    # print("frame" + str(frame))
    _, jpeg_image = cv2.imencode('.jpg', frame)
    # jpeg_image:[255 216 255 ... 115 255 217]
    print("jpeg_image:" + str(jpeg_image))
    # jpeg_image type:<class 'numpy.ndarray'>
    print("jpeg_image type:" + str(type(jpeg_image)))
    # jpeg_image len: 31591
    print("jpeg_image len: " + str(len(jpeg_image)))

    # tobytes()：将原始数据转换为python字节码
    # data--type:<class 'bytes'>
    # len(data) = len(jpeg_image)
    data = jpeg_image.tobytes()
    # print("data: " + str(data))
    # len data： 31591
    print("len data： " + str(len(data)))

    # 【定义文件头、数据】
    # struct.pack:将输入的值（len(data)）根据对应的格式('i')进行压缩，并返回对应压缩后的二进制串。
    # fread--type:<class 'bytes'>
    fread = struct.pack('i', len(data))
    # fread:
    # b'g{\x00\x00'
    # type fread:  <class 'bytes'>
    # 4
    print("fread: ")
    print(fread)
    print("type fread: ", str(type(fread)))
    print(len(fread))#--4

    # 【发送文件头、数据】
    # sendto:向指定目的地发送数据
    # fread为要发送的数据，(UDP_IP, UDP_PORT)是要发送数据的目标地址，可以是IP地址和端口号的元组
    # 发送IP头（20），UDP头（8）
    sock.sendto(fread, (UDP_IP, UDP_PORT))

    # 每次发送x字节，计算所需发送次数
    pack_size = 65507  # 每次发送65507字节
    send_times = len(data) // pack_size + 1  # 向下取整再+1
    for count in range(send_times):
        if count < send_times - 1:
            # 除最后一次之外
            sock.sendto(data[pack_size * count:pack_size * (count + 1)], (UDP_IP, UDP_PORT))
        else:
            # 最后一次
            sock.sendto(data[pack_size * count:], (UDP_IP, UDP_PORT))

    # 按下'q'退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# 关闭所有图像窗口
cv2.destroyAllWindows()
# 释放摄像头
cap.release()