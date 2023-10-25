import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.highgui.HighGui;
import org.opencv.imgcodecs.Imgcodecs;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


/**
 * @Description: 用于接收python发送的视频流
 * @Author: Created by lzy on 2023/10/12.
 */


public class UdpReceive {

    // 调用OpenCV库文件
    static {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }

    public static void main(String[] args) throws Exception {

        // 创建UDP Socket对象
        DatagramSocket ds = new DatagramSocket(5005);
        int BUFSIZE = 65507;
        // 创建接收数据的缓冲区
        byte[] buf = new byte[BUFSIZE];
        // 初始化dataSize
        int dataSize = 0;

        while(true){
            // 创建接收数据的数据包
            DatagramPacket reciveHead = new DatagramPacket(buf, BUFSIZE);
            // 接收数据，如果没有数据，进入阻塞状态
            // 获取数据头/数据信息
            ds.receive(reciveHead);
            // 接收到的数据存储在recive的buf(字节数组)中，判断接收到的是文件头
            if (reciveHead.getLength() == 4){
                System.out.println("开始接收文件头");
                // buffer为接收到的数据，是一个字节类型的数组
                // 由于文件头是被压缩发送的，因此进行字节数组切片，只取recive.getData()--buf中的前四个字节
                byte[] buffer = Arrays.copyOfRange(reciveHead.getData(), 0, reciveHead.getLength());
                // 将buffer字节数组转换为int整型数
                dataSize = (0xff & buffer[0])
                        | (0xff00 & (buffer[1] << 8))
                        | (0xff0000 & (buffer[2] << 16))
                        | (0xff000000 & (buffer[3] << 24));
                System.out.println("data_size: " + dataSize);
            }else {
                System.out.println("不是文件头,请继续下次循环!");
                continue;
            }

            // 接收数据信息
            // 初始化recvdsize
            int recvdsize = 0;
            // 初始化dataTotal
            List<Byte> dataTotal = new ArrayList<>();
            System.out.println("接收发送的数据");
            // 重新接收数据
            int recvTimes = dataSize / BUFSIZE + 1;
            System.out.println("该图片接收次数为： " + recvTimes + " 次");

            // 遍历接收次数
            for (int i = 0; i < recvTimes; i++) {
                // 创建接收数据的数据包
                DatagramPacket reciveData = new DatagramPacket(buf, BUFSIZE);
                // 接收数据，如果没有数据，进入阻塞状态
                // 获取数据头/数据信息
                ds.receive(reciveData);
                // recive.getLength()代表传输的数据的字节长度，但是不会超过65507
                // 遍历每一个字节
                for (int j = 0; j < reciveData.getLength(); j++) {
                    // 将每个字节存入列表
                    dataTotal.add(reciveData.getData()[j]);
                }
            }
            recvdsize = dataTotal.size();

            // 将list转换为Byte数组
            Byte[] arr = new Byte[dataTotal.size()];
            // 现在arr中包含本次图像的字节数据
            dataTotal.toArray(arr);

            // 判断arr长度(接收到的数据的长度)是否等于图片长度，不是就继续下次循环
            if (arr.length != dataSize){
                System.out.println("一定又是哪接收出错了，导致没接收上，继续下轮循环！");
                continue;
            }
            System.out.println("received!");

            // 从arr(字节数组Byte[])中解码并显示数据
            // 将Byte数组转换成在[0,255]范围内
//            int[] arrNew = new int[arr.length];
//            for (int i = 0; i < arr.length; i++) {
//                arrNew[i] = arr[i] & 0xff;
//            }
            // 此时arrNew对应nparr = np.frombuffer(data_total, np.uint8),是一个一维的int[]数组

            // 将arr（字节数组Byte[]）转化为byte[]
            byte[] arrNew = new byte[arr.length];
            for (int i = 0; i < arr.length; i++) {
                arrNew[i] = arr[i];
            }

            // imdecode方法则是将压缩后的图像数据流解码成OpenCV格式的图像
            Mat matImage = Imgcodecs.imdecode(new MatOfByte(arrNew), Imgcodecs.IMREAD_COLOR);

            // 显示图像
            HighGui.imshow("receive frame", matImage);
            // 按下'q'退出循环
            if (HighGui.waitKey(1) == 81){
                HighGui.destroyAllWindows();
                break;
            }
        }
    }
}