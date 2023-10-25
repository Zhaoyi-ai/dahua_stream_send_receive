import cv2

cap = cv2.VideoCapture('rtsp://admin:admin123@192.168.13.117:554/cam/realmonitor?channel=1&subtype=0')
print("cap:" + str(cap))

while True:
    ret,frame = cap.read()
    print("current status:" + str(ret))
    cv2.imshow("current frame",frame)
    cv2.imwrite('frame.jpg', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#关闭所有图像窗口
cv2.destroyAllWindows()
#释放摄像头
cap.release()