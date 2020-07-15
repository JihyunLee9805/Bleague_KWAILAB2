import cv2
import numpy as np
from PIL import Image
from time import sleep
#from e_drone.drone import*
#from e_drone.protocol import*
#frome picamera.array import PiRGBArray
#from picamera import PiCamera


#실시간으로 영상의 프레임 받아옴
#초록색이 인지된다면 -> 인지 print,초록 박스의 내부 중앙 좌표가 화면의 중앙이라면-> 직진
#                          중앙이 아니라면 ->좌우 확인 해서 x좌표 중앙에되게 하고 위아래 확인해서 y좌표로 이동->직
#       안된다면 -> 직진/회전 반복 진

class Autodrone:
    def __init__(self):
        self.drone="Drone"
        #self.drone=Drone()
        #self.camera=PiCamera()
        #self.camera=resolution(640,480)
        #self.camera.framerate=32
        #self.capture=PiRGBArray(self.camera,size=(640,480))
        #sleep(0.1)
        #self.drone.open()
        #self.takeOff()

    def forWhile(self,cmd):
        for i in range(3, 0, -1):
            print(cmd)
            sleep(1)

    def takeOff(self):
        self.drone.sendTakeOff()
        self.forWhile("TakeOff")
        self.drone.sendControlWhile(0, 0, 0, 0, 2000)
        self.forWhile("Hovering")
        self.goFront(1.0)

    def landing(self):
        self.drone.sendLanding()
        self.forWhile("Landing")
        self.drone.close()

    def goFront(self,x):
        self.drone.sendControlPosition(x,0,0,0.5,0,0)
        self.forWhile("goFront")

    def goUp(self,y):
        self.drone.sendControlPosition(0, 0, y, 0.5, 0, 0)
        self.forWhile("goUp")

    def goDown(self,y):
        self.drone.sendControlPosition(0, 0, -y, 0.5, 0, 0)
        self.forWhile("goDown")

    def goRight(self,x):
        self.drone.sendControlPosition(0, -x, 0, 0.5, 0, 0)
        self.forWhile("goRight")

    def goLeft(self,x):
        self.drone.sendControlPosition(0, x, 0, 0.5, 0, 0)
        self.forWhile("goLeft")

    def spinLeft(self,a):
        self.drone.sendControlPosition(0, 0, 0, 0, a, 0.5)
        self.forWhile("spinRight")


    def getMaxArea(self,contours,hierachy,img_internal):
        max = 0
        box = []
        maxIdx = 0
        for i in range(len(contours)):
            if hierachy[0][i][3] != -1:
                cv2.drawContours(img_internal, contours, i, 255, -1)
                area = cv2.contourArea(contours[i])
                if max < area:
                    max = area
                    maxIdx = i

        return max,maxIdx

    def getGreen(self): #input_str RGB2HSV
        lowerBound = np.array([22, 80, 22])
        upperBound = np.array([90, 170, 90])

        hsv = cv2.imread("./test.png", cv2.COLOR_BGR2HSV)
        img = cv2.inRange(hsv, lowerBound, upperBound)
        img = cv2.resize(img, dsize=(960, 720), interpolation=cv2.INTER_AREA)

        ret1, img = cv2.threshold(img, 125, 255, 0)

        contours, hierachy = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        img_internal = np.zeros(img.shape, img.dtype)

        box=[]
        max,maxIdx=self.getMaxArea(contours,hierachy,img_internal)

        #초록 내부 찾음
        if max>5000:
            cv2.drawContours(img_internal, contours, maxIdx, 255, -1)
            print("YES")
            cv2.imwrite("./check.png", img_internal)
            rect = cv2.minAreaRect(contours[maxIdx])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            print(box)
            cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
            cnt = contours[maxIdx]
            mmt = cv2.moments(cnt)
            print("box Center", str(int(mmt['m10'] / mmt['m00'])) + " " + str(int(mmt['m01'] / mmt['m00'])))
            #내부가 중앙에 옴
            if int(mmt['m10'] / mmt['m00']) >= 410 and int(mmt['m10'] / mmt['m00']) <= 510:
                self.goFront(0.5)
            #내부가 중앙이 아님
            else:
                print("Reset Center Position")
                self.drone.sendStop()#정지 모

        #초록 내부 찾지 못함
        else:
            print("Find Green Inner")
            self.FInner(img)

    def check(self,pos,low,high):
        if pos>=low and pos<=high:
            return True
        return False

    def FInner(self,img):
        contours, hierachy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
        canny=cv2.Canny(img,100,255)
        box = []
        max, maxIdx = self.getMaxArea(contours, hierachy, canny)
        if max>300:
            print("Set direction forward Green")
            cv2.drawContours(canny, contours, maxIdx, 255, -1)
            rect = cv2.minAreaRect(contours[maxIdx])
            box = cv2.boxPoints(rect)
            print(box)
            if self.check(box[1][0],0,50) and self.check(box[2][0],0,50):
                self.goLeft(0.2)

            if self.check(box[0][0],900,960) and self.check(box[3][0],900,960):
                self.goRight(0.2)

            if self.check(box[2][1],0,100) and self.check(box[3][1],0,100):
                self.goUp(0.2)

            if self.check(box[0][1],600,720) and self.check(box[1][1],600,720):
                self.goDown(0.2)

    def getRate(self,max):
        if max!=0:
            rate=(max/(960*720))*100
        else:
            rate=max
        return rate

    def getColorRate(self,frame):
        frame = cv2.resize(frame, dsize=(960, 720), interpolation=cv2.INTER_AREA)

        lower_blue = np.array([110, 100, 100])
        upper_blue = np.array([130, 255, 255])

        lower_green = np.array([50, 100, 100])
        upper_green = np.array([70, 255, 255])

        lower_red = np.array([-10, 100, 100])
        upper_red = np.array([10, 255, 255])

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        blue_range = cv2.inRange(hsv, lower_blue, upper_blue)
        green_range = cv2.inRange(hsv, lower_green, upper_green)
        red_range = cv2.inRange(hsv, lower_red, upper_red)

        _, blue_result = cv2.threshold(blue_range, 125, 255, 0)
        _, red_result = cv2.threshold(red_range, 125, 255, 0)
        _, green_result = cv2.threshold(green_range, 125, 255, 0)

        contours, hierachy = cv2.findContours(blue_result, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        max,_=self.getMaxArea(contours,hierachy,blue_result)
        bRate=self.getRate(max)
        contours, hierachy = cv2.findContours(green_result, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        max, _ = self.getMaxArea(contours, hierachy, green_result)
        gRate=self.getRate(max)
        contours, hierachy = cv2.findContours(red_result, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        max, _ = self.getMaxArea(contours, hierachy, red_result)
        rRate=self.getRate(max)

        return rRate,bRate,gRate



    def driving(self):
        for frame in self.camera.capture_continuous(self.capture,format('bgr'),use_video_port=True):
            img=frame.array
            #key=waitKey(0) & 0xFF
            self.capture.truncate(0)
            rRate,bRate,gRate=self.getColorRate(img)
            print(rRate,bRate,gRate)

            if(rRate>gRate): #좌회전+직진
                self.spinLeft(270)
                self.goFront(1.0)
            elif(bRate>gRate):#착지
                self.landing()
            elif(rRate<gRate and bRate<gRate):#링 감지
                self.getGreen()
            else: #아무것도 감지 안된 싱태
                self.goFront(0.3)
                self.spinLeft(180)




myDrone=Autodrone()
#myDrone.landing()
#myDrone.driving()
#myDrone.getGreen()
