#Authors:
#Joca
#Ricardo

#import svgpathtools
#import potrace
import cv2 as cv
import matplotlib.pyplot as plt
import math
import numpy as np
#from svg.path import 

class PATH:
    def __init__(self) -> None:
        self.n_paths: int = 0
        self.paths = None
        self.points: list = []

    ### loads file
    def removepoints(self, file_name: str):
        i=0
        font = cv.FONT_HERSHEY_COMPLEX
        img3 = cv.imread(file_name, cv.IMREAD_COLOR)
        
        j=0
        i=2
        #self.points.reshape(-1,2)
        counter=0
        if(len(self.n_points) == 1): #means that we only have one contour
            #mediumpoint=int(int(self.n_points[0])/2)+4
            #self.points=self.points[0:mediumpoint]
            while (j < int(self.n_points[0]) ):
                while (i < int(self.n_points[0]) ):
                    distance = math.sqrt((self.points[j]-self.points[i])**2 + (self.points[j+1]-self.points[i+1])**2)
                    if distance < 100:
                        print(distance, self.points[j], self.points[j+1], self.points[i], self.points[i+1])
                        #self.points=self.points[:i]
                        counter+=1
                       
                        #print(self.points)
                        #print(len(self.points))
                    i += 2
                j+=2
                i=j+2
            print(counter)
            #mediumpoint=int(counter/2)
            self.points=self.points[:(int(self.n_points[0])-2*counter)]

        """while (j<len(self.points)):
            i=j+2
            while(i<len(self.points) ):
                distance = np.sqrt((self.points[j]-self.points[i])**2 + (self.points[j+1]-self.points[i+1])**2)
                if distance < 100:
                    self.points.pop(i)
                    self.points.pop(i)
                    #print(self.points)
                    #print(len(self.points))
                else: 
                    i += 2
            j += 2"""
        j = 0
        i = 0
        print(len(self.points))
        #cv.drawContours(img3, self.points, -1 , (0, 255, 0), 2)
        aux=np.array(self.points).reshape(-1,2)
        #print(aux)
        
        
            
        for i in range(len(self.points)-1):
            x = aux[i][0]
            y = aux[i][1]
            string = str(x) + " " + str(y)
                # text on remaining co-ordinates.
            cv.putText(img3, string, (x, y), 
                    font, 1, (255, 0, 0)) 
        
            
        """for i in range(0,self.n_points[0],2):
            for j in range(1,len(self.points)):
                for n in range(self.n_points[j]-1):
                    distance = np.sqrt((self.points[0][i, 0,0]-self.points[j][n, 0,0])**2 + (self.points[0][i,0,1 ]-self.points[j][n, 0,1])**2)
                    if distance < 100:
                        print(self.points[j][n])
                        self.points[j]=np.concatenate((self.points[j][0:i-1],self.points[j][i+1:self.n_points[j]]), axis=0)
                        self.n_points[j]-=1
                        print(self.points[j])
                        #self.n_points[j]-=2
           """
        image = cv.polylines(img3, [aux],
                      False, (0,255,0), 2)
        #cv.drawContours(img3, self.points, 1, (255, 0, 0), 2)
        #cv.drawContours(img3, self.points, 2, (0, 0, 255), 2)      
        # String containing the co-ordinates.
        
        plt.imshow(img3)
        #print(self.points[0][0])
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
        #contours2, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        """if len(contours2)>1:
            print(contours1)
            contours1.ravel(contours2[1])"""
        #bmp = potrace.Bitmap(im1)
        #print(bmp.)    
        
        aux = []
        self.n_points = []

        for cnt in contours :
  
            approx = cv.approxPolyDP(cnt, 0.001*cv.arcLength(cnt, False), True)
            # draws boundary of contours.
            cv.drawContours(img2, [approx], -1, (0, 255, 0), 2) 
            # Used to flatted the array containing
            # the co-ordinates of the vertices.
            n = np.array(approx.ravel())
            i = 0
            
            aux.append(n)
            self.n_points.append(len(n))
            print(aux)
            for j in n :
                if(i % 2 == 0):
                    x = n[i]
                    y = n[i + 1]

                    # String containing the co-ordinates.
                    string = str(x) + " " + str(y) 
        
                    if(i == 0):
                        # text on topmost co-ordinate.
                        cv.putText(img2, "Arrow tip", (x, y),
                                        font, 1, (255, 0, 0)) 
                    else:
                        # text on remaining co-ordinates.
                        cv.putText(img2, string, (x, y), 
                                font, 1, (0, 255, 0)) 
                
                i = i + 1
        #self.points=aux
        for sublist in aux:
            for item in sublist:
                self.points.append(item)

        # Showing the final image.
        plt.imshow(img2)
        #print(self.points[0][0])
        plt.show()
        
        

        #self.paths = bmp.trace()
    
    def load_paths_svg(self, file_name: str):
        """Loads paths from <file_name>.svg image"""
        #self.paths, attribute_dictionary_list = svgpathtools.svg2paths(file_name)
    def generate_arm_positions(self):
        """Generate arm positions for m paths with varying #positions [[[pos_1x1]...[pos_1xk]]...[[pos_mx1]...[pos_mxb]]]"""
        positions=1
        n_paths=self.paths.__sizeof__()
        i=0
        for path in self.paths:
            i=i+1
            #print(path)
            for segment in path:
                if isinstance(segment, potrace.BezierSegment):
                    print('-> BezierSegment')
                    print(segment.c1.x, '\t', segment.c1.x)
                    print(segment.c2.x, '\t', segment.c2.y)
                    print(segment.end_point.x, '\t',  segment.end_point.y)
                if isinstance(segment, potrace.CornerSegment):
                    print('-> CornerSegment')
                    print(segment.c.x, '\t', segment.c.x)
                    print(segment.end_point.x, '\t', segment.end_point.y)
                """ print('(', segment.start.real, ' , ', segment.start.imag,')', 
                    '->', '(', segment.end.real, ' , ', segment.end.imag,')') """
        return positions, n_paths


#potrace.potrace.CornerSegment

path = PATH()
path.load_paths_png("images/test_draw_1.png")
path.removepoints("images/test_draw_1.png")
#path.generate_arm_positions()
""" for path in path.paths:
    for segment in path:
        print(segment)
        print('(', segment.start.real, ' , ', segment.start.imag,')', '->', '(', 
            segment.end.real, ' , ', segment.end.imag,')') """