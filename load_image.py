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
        counter =[]

        self.points[0]=self.points[0].tolist()
        final_iter=self.n_points[0]

        while (j < final_iter ):
            while (i < final_iter):
                distance = math.sqrt((self.points[0][j]-self.points[0][i])**2 + (self.points[0][j+1]-self.points[0][i+1])**2)
                if distance < 35: #we choose this threshold since it gave the best results
                    counter=i
                    self.points[0].pop(i)
                    self.points[0].pop(i)
                    final_iter-=2
                i += 2
            j+=2
            i=j+2
        
        self.points[0]=self.points[0][:counter]
       
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
        cv.polylines(img3, self.points , False, (0,0,255), 2)
       
            
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
        
        self.n_points = []

        for cnt in contours :
  
            approx = cv.approxPolyDP(cnt, 0.0009*cv.arcLength(cnt, True), True)
            # draws boundary of contours 
            cv.drawContours(img2, [approx], -1, (0, 255, 0), 2) 
            # Used to flatted the array containing
            # the co-ordinates of the vertices.
            n = approx.ravel()
            i = 0
            self.points.append(n)
            self.n_points.append(len(n))
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

        plt.imshow(img2)
        plt.show()


        self.removepoints("images/test_draw_1.png")
        print(self.points)
        return self.points

    def load_paths_svg(self, file_name: str):
        """Loads paths from <file_name>.svg image"""
        #self.paths, attribute_dictionary_list = svgpathtools.svg2paths(file_name)

    def generate_arm_positions(self):
        """Generate arm positions for m paths with varying #positions [[[pos_1x1]...[pos_1xk]]...[[pos_mx1]...[pos_mxb]]]"""
        positions=1
        n_paths=self.paths.__sizeof__()
        i=0
        print("here")
        """for path in self.paths:
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
                    print('(', segment.start.real, ' , ', segment.start.imag,')', 
                    '->', '(', segment.end.real, ' , ', segment.end.imag,')') """
        return positions, n_paths


#potrace.potrace.CornerSegment

path = PATH()
path.load_paths_png("images/test_draw_1.png")
#path.generate_arm_positions()
""" for path in path.paths:
    for segment in path:
        print(segment)
        print('(', segment.start.real, ' , ', segment.start.imag,')', '->', '(', 
            segment.end.real, ' , ', segment.end.imag,')') """