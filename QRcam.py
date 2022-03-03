import cv2
import numpy as np


def QR_getter(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    qrcoder = cv2.QRCodeDetector()
    ok, point = qrcoder.detect(gray)
    # print(point, sep='\n')
    if not ok:
        return None,image
    w = image
    cv2.drawContours(w, np.int32(point), 0, (0, 0, 255), 1)
    # cv2.waitKey()
    return point, w
