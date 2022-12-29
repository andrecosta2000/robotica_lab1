#Authors:
#Joca
#Ricardo


import cv2 as cv
import matplotlib.pyplot as plt
import math
import numpy as np

class PATH:
    def __init__(self) -> None:
        self.n_paths: int = 0
        self.paths = None
        self.points: list = []

    def remove_point_contour_ext(self):
        j=0
        i=2
        
        first=0
        flag=False

        for i in range(len(self.points)):
            last=len(self.points[i])
            first=0
            for j,_ in enumerate(self.points[i]):
                if(j<len(self.points[i])-2):

                    dis1=math.dist(self.points[i][j], self.points[i][j+1])
                    dis2=math.dist(self.points[i][j], self.points[i][j+2])
                    
                    if(flag):
                        if(int(dis2) < 100 and dis2<dis1):
                            last=j+2 #it should be plus 1 however when doing, i.e, points[:last] it would not have in consideration the last value
                            print("Last", j,i)
                    else:
                        if(int(dis2)< 100 and dis2<dis1):
                            first=j+1 #since its the nex
                            print("Firs", j,i)
                            flag=True
                            
            if(last == 0 and first==0): 
                first=0
                last=len(self.points[i])
            elif (last == 0 and first !=0) :
                last=last+1
            print(first,last)
            self.points[i]=self.points[i][first:last]
       
    def removepoints(self, file_name: str):
        font = cv.FONT_HERSHEY_COMPLEX
        img3 = cv.imread(file_name, cv.IMREAD_COLOR)

        self.remove_point_contour_ext()

        for i in range(len(self.n_points)):
            self.points[i]=np.reshape(np.array(self.points[i]),(-1,2))

        
        """
        i = 0
        aux=np.array(self.points).reshape(-1,2)       

        for i in range(len(aux)):
            x = aux[i][0]
            y = aux[i][1]
            string = str(x) + " " + str(y) + " " + str(i)
                # text on remaining co-ordinates.
            cv.putText(img3, string, (x, y), 
                    font, 1, (255, 0, 0)) """

        
        #---para escrever os pontos na imagem
        for j in range(len(self.points)):
            for i in range(len(self.points[j])):
                x = self.points[j][i][0]
                y = self.points[j][i][1]
                string = str(x) + " " + str(y) + " " + str(i)
                    # text on remaining co-ordinates.
                cv.putText(img3, string, (x, y), 
                        font, 1, (255, 0, 0))
        #cv.polylines(img3, self.points , False, (0,0,255), 2)
       
            
        
        #plt.imshow(img3)
        #print(self.points[0][0])
        #plt.show()

    def load_paths_png(self, file_name: str):
        """Loads paths from <file_name>.png image"""
        im1 = cv.imread(file_name)
        font = cv.FONT_HERSHEY_COMPLEX
        imgray = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
        imgray = cv.GaussianBlur(imgray, (5, 5), 0)
        img2 = cv.imread(file_name, cv.IMREAD_COLOR)
        ret, thresh = cv.threshold(imgray, 127, 255,cv.THRESH_BINARY_INV)
        
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        self.n_points = []

        for cnt in contours :
  
            approx = cv.approxPolyDP(cnt, 0.0009*cv.arcLength(contours[0], True), True)
            # draws boundary of contours 
            cv.drawContours(img2, [approx], -1, (0, 255, 0), 2) 
            # Used to flatted the array containing
            # the co-ordinates of the vertices.
            n = approx.ravel()
            i = 0
            self.points.append(n)
            

        #plt.imshow(img2)
        #plt.show()
        for i in range(len(self.points)):
            self.points[i]=np.reshape(np.array(self.points[i]),(-1,2))

        self.remove_point_contour_ext()
 
