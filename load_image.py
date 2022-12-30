import cv2 as cv
import matplotlib.pyplot as plt
import math
import numpy as np

class PATH:
    def __init__(self) -> None:
        self.n_paths: int = 0
        self.paths = None
        self.points: list = []

    def remove_duplicate_points_1cnt(self):
        j=0        
        first=0
        flag=False
        last=len(self.points[0])

        for j,_ in enumerate(self.points[0]):
            if(j<len(self.points[0])-2):

                dis1=math.dist(self.points[0][j], self.points[0][j+1])
                dis2=math.dist(self.points[0][j], self.points[0][j+2])
                
                if(flag):
                    if(int(dis2) < 100 and dis2<dis1):
                        last=j+2 #it should be plus 1 however when doing, i.e, points[:last] it would not have in consideration the last value
                else:
                    if(int(dis2)< 100 and dis2<dis1):
                        first=j+1 #since its the nex
                        flag=True
                        
        if(last == 0 and first==0): 
            first=0
            last=len(self.points[0])
        elif (last == 0 and first !=0) :
            last=last+1
        self.points[0]=self.points[0][first:last]

       
    def removepoints(self, file_name: str):
        font = cv.FONT_HERSHEY_COMPLEX
        img3 = cv.imread(file_name, cv.IMREAD_COLOR)
        unique_contours=[]
        flag=False

      
        iter=0
        unique_contours=self.points[0].tolist() #since we can't remove the pen, we are assuming that only one parent contour is returned from function findcontours
        for a1 in (self.points[1:]):
            for idx1  in range (len(a1)-1):
                mindist=100000
                flag=False
                for idx2 in range(len(unique_contours)-1): #point from parent contour that is closer to each point of child contours 
                    dist=math.dist(a1[idx1],unique_contours[idx2])
                    if(dist<mindist):
                        mindist=dist
                        iter=idx2
                dist1=math.dist(unique_contours[iter-1],a1[idx1+1])
                dist2=math.dist(unique_contours[iter+1],a1[idx1+1])
                if(dist1< 300 or dist2 < 300 or math.dist(unique_contours[iter],a1[idx1+1])<500 or math.dist(a1[idx1],unique_contours[iter])==0):
                    #means that the point is already on the parent contour
                    flag=True
                
                if(flag==False):
                    if(dist1>dist2): #means that the 
                        unique_contours.insert(iter+1,a1[idx1]) # a similar value is on the list however, when adding the next value it would modify the line
                        unique_contours.insert(iter+2,a1[idx1+1]) # it isnt on the list so we add it
                        if(math.dist(unique_contours[iter-1],a1[idx1+2])>500):
                            unique_contours.insert(iter+3,a1[idx1])
                    else:
                        unique_contours.insert(iter,a1[idx1]) # a similar value is on the list however, when adding the next value it would modify the line
                        unique_contours.insert(iter+1,a1[idx1+1]) # it isnt on the list so we add it
                        if(math.dist(unique_contours[iter-1],a1[idx1+2])>500):
                            unique_contours.insert(iter+2,a1[idx1])

            
        
        num=0
        self.points=np.reshape(np.array(unique_contours),(-1,2))
        

        for j in range(len(self.points)):
            x = self.points[j][0]
            y = self.points[j][1]
            string = str(x) + " " + str(y) + " " + str(num)
                # text on remaining co-ordinates.
            cv.putText(img3, string, (x, y), 
                    font, 1, (255, 0, 0))
            num += 1

        

        cv.polylines(img3, [self.points] , False, (0,0,255), 2)
       
            
        # String containing the co-ordinates.
        
        plt.imshow(img3)
        plt.show()

    def load_paths_png(self, file_name: str):
        """Loads paths from <file_name>.png image"""
        im1 = cv.imread(file_name)
        font = cv.FONT_HERSHEY_COMPLEX
        imgray = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
        imgray = cv.GaussianBlur(imgray, (5, 5), 0)
        img2 = cv.imread(file_name, cv.IMREAD_COLOR)
        img3 = cv.imread(file_name, cv.IMREAD_COLOR)
        ret, thresh = cv.threshold(imgray, 127, 255,cv.THRESH_BINARY_INV)
        
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for cnt in contours :
  
            approx = cv.approxPolyDP(cnt, 0.0009*cv.arcLength(cnt, False), False)
            # draws boundary of contours
            cv.drawContours(img2, [approx], -1, (0, 255, 0), 2) 
            # Used to flatted the array containing
            # the co-ordinates of the vertices.
            n = approx.ravel()
            self.points.append(n)

        num=0
        for i in range(len(self.points)):
            self.points[i]=np.reshape(np.array(self.points[i]),(-1,2))


        for j in range(len(self.points)):
            for i in range(len(self.points[j])):
                x = self.points[j][i][0]
                y = self.points[j][i][1]
                string = str(x) + " " + str(y) + " " + str(i)
                    # text on remaining co-ordinates.
                if( j==0):
                    cv.putText(img2, string, (x, y), 
                        font, 1, (255, 0, 0))
                elif j==1 :
                    cv.putText(img2, string, (x, y), 
                        font, 1, (0, 0, 255))
                else:
                    cv.putText(img2, string, (x, y), 
                        font, 1, (0, 255, 0))
                num += 1
        

        plt.imshow(img2)
        plt.show()

        if(len(self.points)>1):
            self.removepoints(file_name)
        else:
            self.remove_duplicate_points_1cnt()
            for j in range(len(self.points)):
                for i in range(len(self.points[j])):
                    x = self.points[j][i][0]
                    y = self.points[j][i][1]
                    string = str(x) + " " + str(y) + " " + str(i)
                        # text on remaining co-ordinates.
                    if( j==0):
                        cv.putText(img3, string, (x, y), 
                            font, 1, (255, 0, 0))
                    elif j==1 :
                        cv.putText(img3, string, (x, y), 
                            font, 1, (0, 0, 255))
                    else:
                        cv.putText(img3, string, (x, y), 
                            font, 1, (0, 255, 0))
                    num += 1
                    cv.polylines(img3, self.points , False, (0,0,255), 2)
            plt.imshow(img3)
            plt.show()


        #self.removepoints(file_name)


path=PATH()
path.load_paths_png('images/test_draw_2_r.png')

