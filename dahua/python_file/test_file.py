import socket
import struct
import cv2
import numpy as np

img = cv2.imread("frame.jpg")
cv2.imshow("img", img)

if True:
    print(cv2.waitKey(0))
    print(type(cv2.waitKey(0)))

    print(0xFF)
    print(type(0xFF))

    print(cv2.waitKey(0) & 0xFF)
    print(type(cv2.waitKey(0) & 0xFF))

    print(ord('q'))
    print(type(ord('q')))

    cv2.destroyAllWindows()



