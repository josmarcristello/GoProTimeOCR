import cv2
import pytesseract
import os
import re
from graphviz import Digraph

dot = Digraph()

with dot.subgraph() as c:
    c.attr(rank='same')
    c.node('A', 'Start')
    c.node('B', 'Load Image \n (using cv2.imread)')
    c.node('C', 'Convert to HSV \n (using cv2.cvtColor)')
    c.node('D', 'Threshold for Yellow Colors \n (using cv2.inRange)')
    c.node('E', 'Bitwise-AND Original and Mask \n (using cv2.bitwise_and)')

with dot.subgraph() as c:
    c.attr(rank='same')
    c.node('F', 'Convert to Grayscale \n (using cv2.cvtColor)')
    c.node('G', 'Crop Image \n (using array slicing)')
    c.node('H', 'Apply Thresholding \n (using cv2.threshold)')
    c.node('I', 'Invert Colors \n (using cv2.bitwise_not)')
    c.node('J', 'Threshold Inverted Image \n (using cv2.threshold)')

dot.node('K', 'Resize Image \n (using cv2.resize)')
dot.node('L', 'OCR with EasyOCR \n (using easyocr.Reader.readtext)')
dot.node('M', 'End')

dot.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH', 'HI', 'IJ', 'JK', 'KL', 'LM'])

dot.render('media/flowchart.gv', view=True)  # save the graph to a file and open it