import cv2
import sys


def main():
    if len(sys.argv) < 3:
        print("pass two images")
        return
        
    before = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    after = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)
    diff = cv2.absdiff(before, after)
    _, diff = cv2.threshold(diff, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite("./diff.jpg", diff)
    #cv2.imshow("Diff:", diff)
    #if cv2.waitKey() == ord('q'):
    #    cv2.destroyAllWindows()
    #return

main()