import cv2
import sys


def main():
    if len(sys.argv) < 3:
        print("pass two images")
        return
        
    before = cv2.imread(sys.argv[1])
    after = cv2.imread(sys.argv[2])
    diff = cv2.absdiff(before, after)
    # diff = cv2.adaptiveThreshold(diff, 255, cv2.ADAPTIVE_THRESH_MEAN_C,  cv2.THRESH_BINARY, 5, 1)
    _, diff = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY)
    # diff = cv2.dilate(diff, None, iterations=2)
    cv2.imwrite("thresh.jpg", diff)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("diff", diff)
    # cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest_contour_idx, biggest_contour_val = max(enumerate(contours), key=lambda e: len(e[1]))
    print(cv2.contourArea(biggest_contour_val))
    throw_place = tuple(max(biggest_contour_val, key=lambda p: p[0][1])[0])
    # print(throw_place)
    cv2.circle(after, throw_place, 5, (0, 255, 0), 5)
    #cv2.drawContours(after, contours, biggest_contour_idx, (0, 255, 0), 5)
    cv2.imwrite("diff.jpg", after)


main()
