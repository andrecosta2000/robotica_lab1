#Authors:
#Joca
#Ricardo

#import svgpathtools
#import potrace
import cv2 as cv
import matplotlib.pyplot as plt

class PATH:
    def __init__(self) -> None:
        self.n_paths: int = 0
        self.paths = None

    ### loads file
    def load_paths_png(self, file_name: str):
        """Loads paths from <file_name>.png image"""
        im1 = cv.imread(file_name)
        font = cv.FONT_HERSHEY_COMPLEX
        imgray = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
        imgray = cv.GaussianBlur(imgray, (5, 5), 0)
        img2 = cv.imread(file_name, cv.IMREAD_COLOR)
        ret, thresh = cv.threshold(imgray, 127, 255,cv.THRESH_BINARY_INV)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        #bmp = potrace.Bitmap(im1)
        #print(bmp.)    
        #ima=cv.drawContours(im1, contours, -1, (0,255,0), 0)
        for cnt in contours :
  
            approx = cv.approxPolyDP(cnt, 0.00009*cv.arcLength(cnt, True), True)
        
            # draws boundary of contours.
            cv.drawContours(img2, [approx], -1, (0, 255, 0), 2) 
        
            # Used to flatted the array containing
            # the co-ordinates of the vertices.
            n = approx.ravel() 
            i = 0
        
            for j in n :
                if(i % 2 == 0):
                    x = n[i]
                    y = n[i + 1]
        
                    # String containing the co-ordinates.
                    string = str(x) + " " + str(y) 
        
                    if(i == 0):
                        # text on topmost co-ordinate.
                        cv.putText(img2, "Arrow tip", (x, y),
                                        font, 0.5, (255, 0, 0)) 
                    else:
                        # text on remaining co-ordinates.
                        cv.putText(img2, string, (x, y), 
                                font, 0.5, (0, 255, 0)) 
                i = i + 1
        
        # Showing the final image.
        #cv.imshow('image2', img2)
        plt.imshow(img2)
        plt.show()
        # Exiting the window if 'q' is pressed on the keyboard.
        cv.waitKey(0)
        # Exiting the window if 'q' is pressed on the keyboard
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
#path.generate_arm_positions()
""" for path in path.paths:
    for segment in path:
        print(segment)
        print('(', segment.start.real, ' , ', segment.start.imag,')', '->', '(', 
            segment.end.real, ' , ', segment.end.imag,')') """