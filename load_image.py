#Authors:
#Joca

#import svgpathtools
#import potrace
import cv2
import matplotlib.pyplot as plt

class PATH:
    def __init__(self) -> None:
        self.n_paths: int = 0
        self.paths = None

    ### loads file
    def load_paths_png(self, file_name: str):
        """Loads paths from <file_name>.png image"""
        font = cv2.FONT_HERSHEY_COMPLEX
        im1 = cv2.imread(file_name)
        imgray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:
            approx = cv2.approxPolyDP(i,0.009*cv2.arcLength(i,True),True)
            cv2.drawContours(imgray,[approx],0,(0,0,255),5)
            n=approx.ravel()
            k=0
            for j in n:
                if(k%2==0):
                    x = n[k]
                    y = n[k+1]
                    print(x,y)
                    string=str(x)+""+str(y)
                    if(k==0):
                        cv2.putText(imgray,"Arrow tip",(x,y),font,0.5,(255,0,0))
                    else:
                        cv2.putText(imgray,string,(x,y),font,0.5,(0,255,0))
                k=k+1
            cv2.imshow('image2',imgray)
            if cv2.waitKey(0) & 0xFF ==ord('q'):
                cv2.destroyAllWindows()

                            #im2= cv2.drawContours(im1, contours, -1, (0,255,0), 0)
        #plt.imshow(im2)
        #plt.show()
        #bmp = potrace.Bitmap(im1)
        #print(bmp.)
        
        self.paths = bmp.trace()
    
    def load_paths_svg(self, file_name: str):
        """Loads paths from <file_name>.svg image"""
        self.paths, attribute_dictionary_list = svgpathtools.svg2paths(file_name)
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
path.generate_arm_positions()
""" for path in path.paths:
    for segment in path:
        print(segment)
        print('(', segment.start.real, ' , ', segment.start.imag,')', '->', '(', 
            segment.end.real, ' , ', segment.end.imag,')') """