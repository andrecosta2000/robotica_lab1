#Authors:
#Joca

import svgpathtools
import potrace
import cv2

class PATH:
    def __init__(self) -> None:
        self.n_paths: int = 0
        self.paths = None

    ### loads file
    def load_paths_png(self, file_name: str):
        """Loads paths from <file_name>.png image"""
        im1 = cv2.imread(file_name, 0)
        bmp = potrace.Bitmap(im1)
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