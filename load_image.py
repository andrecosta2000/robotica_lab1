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
        unique_contours=[]
        flag=False
        last=len(self.points[0])
        first=0

        

        #self.remove_point_contour_ext(file_name) #removes the repeated points from the external contour
        self.remove_point_contour_ext()

        for a2 in self.points[1:]:
            print("another")
            for point in a2:
                print(point)
                unique_contours.append(point)
            aux=np.array(unique_contours).ravel()

        for idx in range(len(unique_contours)-1):
            for j in range(idx+1,len(unique_contours)):
                if(math.dist(unique_contours[idx],unique_contours[j])<100):
                    print(unique_contours[idx],unique_contours[j])

        for a1 in self.points[0]:
            flag=False
            for point in unique_contours:
                if math.dist(a1,point) < 100:
                    flag=True
            if(flag==False):
                unique_contours.append(a1)
            if(flag==False):
                unique_contours.append(a1)  

                #unique_contours.append(a1)
    
    
        self.points = np.array(aux)
        """flag=False
        last=len(unique_contours)
        first=0

        self.points = np.array(unique_contours)

        print(len(self.points[0]))
        for j in range(len(self.points)-2):
            
            dis1=math.dist(self.points[j], self.points[j+1])
            dis2=math.dist(self.points[j], self.points[j+2])
            
            if(flag):
                if(int(dis2) < 100 and dis2<dis1):
                    last=j+1 #it should be plus 1 however when doing, i.e, points[:last] it would not have in consideration the last value
                    print("Last", j)
            else:
                if(int(dis2)< 100 and dis2<dis1):
                    first=j+1 #since its the next
                    print("Firs", j)
                    flag=True
                        

        if(last == 0 and first==0): 
                first=0
                last=len(self.points)
        elif (last ==0 and first !=0) :
            last=last+1
        print(first, last)    
        self.points=self.points[first:last]

"""
        """
        first_idx = 0
        last_idx = len(unique_contours)
        extreme = 0
        
        for idx, _ in enumerate(unique_contours):
            if(idx<len(unique_contours)-2):
                if math.dist(unique_contours[idx],unique_contours[idx+2]) < 200 :
                    extreme += 1
                    if (extreme == 1 and len(self.points)==2):
                        first_idx = idx+1
                    elif (extreme == 2):
                        last_idx = idx+1
                        break
        
        for idx, _ in enumerate(unique_contours):
            if math.dist(unique_contours[idx],unique_contours[first_idx]) < 100 and idx != first_idx:
                first_idx += 1
                break
"""
        #unique_contours = unique_contours[first_idx:last_idx+1]

        

        #for i in range(len(unique_contours)):
            #unique_contours[i]=np.reshape(np.array(unique_contours[i]),(-1,2))


        num=0

        for i in range(len(self.points)):
            x = self.points[i][0]
            y = self.points[i][1]
            string = str(x) + " " + str(y) + " " + str(num)
                # text on remaining co-ordinates.
            if( i==0):
                cv.putText(img3, string, (x, y), 
                    font, 1, (255, 0, 0))
            elif i==1 :
                cv.putText(img3, string, (x, y), 
                    font, 1, (0, 0, 255))
            else:
                cv.putText(img3, string, (x, y), 
                    font, 1, (0, 255, 0))
            num += 1




        """for i in range(len(self.points)):
            self.points[i]=np.reshape(np.array(self.points[i]),(-1,2))

        self.remove_point_contour_ext() #removes the points that are similar on the external contour


        num=0
         #---para escrever os pontos na imagem
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
                num += 1"""
        
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
  
            approx = cv.approxPolyDP(cnt, 0.0009*cv.arcLength(contours[0], False), False)
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
            self.remove_point_contour_ext()
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
path.load_paths_png('images/test_draw_2.png')


