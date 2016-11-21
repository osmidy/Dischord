import sys
sys.path.append('..')
import math

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
    Takes in hand from a Leap frame
    Returns a tuple of (x, y) 
    '''
    @staticmethod
    def position_as_pixels(hand):
        handX, handY = hand.palm_position.x, hand.palm_position.y
        # TODO: Use depth to get size or something...       
        vertical_buffer = 200 # bottom out range of hand motion at 200 mm above Leap motion surface
                
        # Get pixels
        x = LeapHelper.pixel_to_mm_ratio_horizontal * handX
        y = LeapHelper.pixel_to_mm_ratio_vertical * handY - vertical_buffer
        
        # Translate horizontal locations to be based around center of screen
        x += Window.width / 2
        
        return (x, y)
        
    '''
    Return whether or not hand is hovering (approximately) above the 
    given kivy pixel, point
    '''
    @staticmethod
    def point_is_hovered(hand, point):
        # Hover range is represented as a rectangular area around the point
        pointX, pointY = point[0], point[1]
        minX = pointX - 75
        maxX = pointX + 75
        minY = pointY - 25 # TODO: remove magic number for actual radius of flame
        maxY = pointY + 90
        
        handX, handY = LeapHelper.position_as_pixels(hand)
        
        if handX < minX or handX > maxX or handY < minY or handY > maxY:
            return False
            
        return True
