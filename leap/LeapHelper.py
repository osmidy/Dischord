import sys
sys.path.append('..')
from kivy.core.window import Window

sys.path.insert(0, "lib")
import Leap

'''
Static class for processing inputs from the Leap Motion,
and converting them for use within the Kivy framework.
    Author: Olivier Midy
'''

class LeapHelper(object):
    ibox_height = 200 # millimeters
    pixel_to_mm_ratio_vertical = Window.height / 200
    pixel_to_mm_ratio_horizontal = Window.width / 350
    
    '''
    Convert Leap millimeter measurements to kivy pixel coordinates.
    Takes in hand coordinates and interaction box of a Leap frame
    Returns a tuple of (x, y) 
    '''
    @staticmethod
    def position_as_pixels(handX, handY):
        # TODO: Use depth to get size or something...       
        vertical_buffer = 200 # buffer region above surface of the Leap Motion
                
        # Get pixels
        x = LeapHelper.pixel_to_mm_ratio_horizontal * handX
        y = LeapHelper.pixel_to_mm_ratio_vertical * handY - vertical_buffer
        
        # Translate pixel locations to be based around center of screen
        x += Window.width / 2
        
        return (x, y)