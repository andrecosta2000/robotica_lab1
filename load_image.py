#Authors:
#Joca
#Ricardo


import cv2 as cv
import matplotlib.pyplot as plt
import math
import numpy as np
from shapely.geometry import Polygon, Point, LineString

class PATH:
    def __init__(self) -> None:
        self.n_paths: int = 0
        self.paths = None
        self.points: list = []

    def remove_duplicate_lines(self):
        #Guarda os novos contornos
        unique_contours = []
        #Corro os 3 contornos
        
        for contour1 in self.points:
            #Guarda os pontos que so existem num contorno
            print("Contour1", contour1)
            unique_points = set()
            #Vou comparar os contornos para ver se é o mesmo
            for contour2 in self.points:
                if contour1.all()==contour2.all():
                    continue
            #Vou buscar 
            for point in contour2:
                print(contour2)
                if point not in unique_points:
                    unique_points.add(point)
            
                for point in contour1:
                    if point not in unique_points:
                        unique_points.add(point)
                contour_unique = np.array(list(unique_points))
                unique_contours.append(contour_unique) 
        print("Esta a correr a função")
        self.point = unique_contours
        # ##############################################2ºFunção(nao funciona) 
    def remove_duplicate_lines(self):
        unique_contours=[]
        aux=[]

        for idx in range(len(self.points)):
        # Check the hierarchy of the contour
            if self.hierarchy[0][idx][2] < 0:
            # The contour is not a duplicate, so add it to the list of unique contours
                unique_contours.append(self.points[idx])
            else:
                aux.append(self.points[idx])
        
        for n in range(len(aux)):
            initial_p=aux[n][0]
            final_p=aux[n][len(aux[n])-1]
            print(initial_p, final_p)
            for i, point in enumerate(unique_contours):
                print(i,point)
                dist1=math.dist(initial_p,point[0])
                dist2=math.dist(final_p,point[len(point)-1])
                #if(dist1<35): #means that the contour starts at the first point of the parent contour
                    #find
                #if(dist2<35): #means that the contour starts at the last point of the parent contour

        self.points=unique_contours

    def remove_point_contour_ext(self):
        j=0
        i=2

        aux=np.zeros([len(self.points),2])
        flag=False

        for j in range(len(self.points)):
            first=0
            last=0
            for i in range(len(self.points[j])-2):
                dis1=math.dist(self.points[j][i], self.points[j][i+1])
                dis2=math.dist(self.points[j][i], self.points[j][i+2])
                
                if(flag):
                    if(int(dis2) < 35 and dis2<dis1):
                        last=i+2 #it should be plus 1 however when doing, i.e, points[:last] it would not have in consideration the last value
                else:
                    if(int(dis2)< 35 and dis2<dis1):
                        first=i+1
                        flag=True
                        
            if(last == 0 and first==0): 
                self.points[j]=self.points[j]
                last=len(self.points[j])
            elif last!=0:
                self.points[j]=self.points[j][first:last]
            else:
                last=first+1
                self.points[j]=self.points[j][:last]
            aux[j][0]=first
            aux[j][1]=last
        
        self.remove_duplicate_lines()
        
       
    def removepoints(self, file_name: str):
        font = cv.FONT_HERSHEY_COMPLEX
        img3 = cv.imread(file_name, cv.IMREAD_COLOR)


        for i in range(len(self.points)):
            self.points[i]=np.reshape(np.array(self.points[i]),(-1,2))

        self.remove_point_contour_ext() #removes the points that are similar on the external contour

        #if(len(self.points)>1):
            #self.reorder_contour()


        num=0
         #---para escrever os pontos na imagem
        for j in range(len(self.points)):
            for i in range(len(self.points[j])):
                x = self.points[j][i][0]
                y = self.points[j][i][1]
                string = str(x) + " " + str(y) + " " + str(num)
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
        ret, thresh = cv.threshold(imgray, 127, 255,cv.THRESH_BINARY_INV)
        
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        self.hierarchy=hierarchy

        for cnt in contours :
  
            approx = cv.approxPolyDP(cnt, 0.0009*cv.arcLength(cnt, True), True)
            # draws boundary of contours 
            cv.drawContours(img2, [approx], -1, (0, 255, 0), 2) 
            # Used to flatted the array containing
            # the co-ordinates of the vertices.
            n = approx.ravel()
            self.points.append(n)
            

        #plt.imshow(img2)
        #plt.show()


        self.removepoints(file_name)


path=PATH()
path.load_paths_png('images/test_draw_2.png')


