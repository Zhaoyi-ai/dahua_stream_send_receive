import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.highgui.HighGui;
import org.opencv.imgcodecs.Imgcodecs;

public class Test {

    // 调用OpenCV库文件
    static {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }

    public static void main(String args[]) {

        // 加载本地OpenCV库
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
        Mat mat = Imgcodecs.imread("src/main/java/1.png");
        //显示图像
        HighGui.imshow("原图", mat);

        // 按下'q'退出循环
        if (HighGui.waitKey(10000000) == 81){
            System.out.println("lzy");
        }

//        System.out.println(System.getProperty("java.library.path"));
//        System.out.println(System.getProperty("sun.arch.data.model"));

    }
}
