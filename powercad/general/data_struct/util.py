'''
Author:      Brett Shook; bxs003@uark.edu

Desc:        Some basic utility functions
             Uniform random numbers
             Distance for n dimensions
             
Created:     Apr 30, 2011
Last Change: May 25, 2011

Copyright: 2011 University of Arkansas Board of Trustees 
'''

import random
import math
from numpy import sign
import matplotlib.pyplot as plt
import matplotlib.patches as patches
class Circle: # Todo: do this later
    '''
    A Filled Circle object mainly used for contours, most functions are used to interact with RECT
    '''
    def __init__(self,xc=0.0, yc=0.0, r=0.0):
        self.xc=xc # center X
        self.yc=yc # center Y
        self.r=r   # Radius

    def circle_func(self,pt):
        return (pt[0]-self.xc)**2+(pt[1]-self.yc)**2-self.r**2
    def encloses(self,pt):
        if self.circle_func(pt)<=0:
            return True
        else:
            return False

    def intersects(self, rect):
        #if rect.encloses(self.xc,self.yc): # Case 1 circle is inside rect
        return None
    def move_frame(self,pt):
        # move a point into a frame where circle's center is (0,0)
        x=pt[0]-self.xc
        y=pt[1]-self.yc
        return (x,y)

    def restore_frame(self,pt):
        x = pt[0] + self.xc
        y = pt[1] + self.yc
        return (x, y)

    def inter_line(self,line):
        '''Source: Weisstein, Eric W. "Circle-Line Intersection." From MathWorld--A Wolfram Web Resource. http://mathworld.wolfram.com/Circle-LineIntersection.html'''
        # Case 1: 2 points outside:
        if self.encloses(line.pt1) and self.encloses(line.pt2):
            print "no intersection, 2 pts are inside cirlce"
            return [] # 2 pts are inside circle, no intersection
        # move the line to the new xy frame begin at Center
        pt1 = self.move_frame(line.pt1)
        pt2 = self.move_frame(line.pt2)
        if self.encloses(line.pt1) or self.encloses(line.pt2): # check for intersection at one single poinr
            print "one point inside, one point outside single intersection"
            # using the coordinate to see which


        # Case: 2 points of line are outside the circle but there are intersects

        # Now we can use the formula from the above source
        dx=pt2[0]-pt1[0]
        dy=pt2[1]-pt1[1]

        dr=math.sqrt(dx**2+dy**2)
        print dx, dy,dr
        D=pt1[0]*pt2[1]-pt2[0]*pt1[1]
        print D
        delta=self.r**2*dr**2-D**2 # discriminant
        if delta>0:

            x_int = [(D*dy+sign(dy)*dx*math.sqrt(delta))/dr**2,(D*dy-sign(dy)*dx*math.sqrt(delta))/dr**2]
            y_int = [(-D*dx+abs(dy)*math.sqrt(delta))/dr**2,(-D*dx-abs(dy)*math.sqrt(delta))/dr**2]
            # move line back to old frame
            inter = [self.restore_frame([x,y]) for x,y in zip(x_int,y_int)]
            return inter
        elif delta ==0:
            return [(D*dy/dr**2-self.xc,-D*dx/dr**2-self.yc)]
        else:
            return None


class Line:
    def __init__(self,x1,y1,x2,y2):
        self.pt1=[x1,y1]
        self.pt2=[x2,y2]
class Rect:
    TOP_SIDE = 1
    BOTTOM_SIDE = 2
    RIGHT_SIDE = 3
    LEFT_SIDE = 4

    def __init__(self, top=0.0, bottom=0.0, left=0.0, right=0.0):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.top)+', '+str(self.bottom)+', '+str(self.left)+', '+str(self.right)

    def set_pos_dim(self, x, y, width, length):
        self.top = y+length
        self.bottom = y
        self.left = x
        self.right = x+width

    def intersects(self, rect):
        return not(self.left > rect.right or rect.left > self.right or rect.bottom > self.top or self.bottom > rect.top)

    def intersects_contact_excluded(self, rect):
        return not(self.left >= rect.right or rect.left >= self.right or rect.bottom >= self.top or self.bottom >= rect.top)

    def intersection(self, rect):
        if not self.intersects(rect):
            return None

        horiz = [self.left, self.right, rect.left, rect.right]
        horiz.sort()
        vert = [self.bottom, self.top, rect.bottom, rect.top]
        vert.sort()

        return Rect(vert[2], vert[1], horiz[1], horiz[2])

    def encloses(self, x, y):
        if x >= self.left and x <= self.right and y >= self.bottom and y <= self.top:
            return True
        else:
            return False

    def translate(self, dx, dy):
        self.top += dy
        self.bottom += dy
        self.left += dx
        self.right += dx

    def area(self):
        return (self.top - self.bottom)*(self.right - self.left)

    def width(self):
        return self.right - self.left

    def height(self):
        return self.top - self.bottom

    def center(self):
        return 0.5*(self.right+self.left), 0.5*(self.top+self.bottom)

    def center_x(self):
        return 0.5*(self.right+self.left)

    def center_y(self):
        return 0.5*(self.top+self.bottom)

    def normal(self):
        # Returns False if the rectangle has any non-realistic dimensions
        if self.top < self.bottom:
            return False
        elif self.right < self.left:
            return False
        else:
            return True

    def scale(self, factor):
        self.top *= factor
        self.bottom *= factor
        self.left *= factor
        self.right *= factor

    def change_size(self, amount):
        # Changes the size of the rectangle on all sides by the size amount
        self.top += amount
        self.bottom -= amount
        self.right += amount
        self.left -= amount

    def find_contact_side(self, rect):
        # Returns the side which rect is contacting
        # Return -1 if not in contact
        side = -1
        if self.top == rect.bottom:
            side = self.TOP_SIDE
        elif self.bottom == rect.top:
            side = self.BOTTOM_SIDE
        elif self.right == rect.left:
            side = self.RIGHT_SIDE
        elif self.left == rect.right:
            side = self.LEFT_SIDE
        return side

    def find_pt_contact_side(self, pt):
        # Returns the side which pt is contacting
        # Return -1 if pt not in contact
        hside = -1
        vside = -1
        if self.top == pt[1]:
            vside = self.TOP_SIDE
        elif self.bottom == pt[1]:
            vside = self.BOTTOM_SIDE
        if self.right == pt[0]:
            hside = self.RIGHT_SIDE
        elif self.left == pt[0]:
            hside = self.LEFT_SIDE
        return hside, vside

    def deepCopy(self):
        rect = Rect(self.top, self.bottom, self.left, self.right)
        return rect

# Seed the random module
def seed_rand(num):
    random.seed(num)

# Generate a random number in the range
def rand(num_range):
    return random.uniform(num_range[0], num_range[1])
def SolveVolume(dims):
        #mm -> m
        return dims[0]*dims[1]*dims[2]*1e-9
def distance(x1, x2):
    dist = 0
    for i in range(len(x1)):
        dist += math.pow(x2[i] - x1[i], 2)

    dist = math.sqrt(dist)
    return dist

def complex_rot_vec(theta_deg):
    theta = theta_deg*(math.pi/180)
    return complex(math.cos(theta), math.sin(theta))

def translate_pt(pt, *args):
    if len(pt) > len(args):
        return None

    ret_pt = []
    for i in xrange(len(args)):
        ret_pt.append(pt[i]+args[i])

    return tuple(ret_pt)

def get_overlap_interval(interval1, interval2):
    return (max(interval1[0], interval2[0]), min(interval1[1], interval2[1]))


def draw_rect_list(rectlist,ax,color,pattern):
    patch=[]
    for r in rectlist:
        p = patches.Rectangle((r.left, r.bottom), r.width(), r.height(),fill=True,
            edgecolor='black',facecolor=color,hatch=pattern)
        patch.append(p)
        ax.add_patch(p)
    #ax1.autoscale_view(tight=True)
    plt.xlim(0,60)
    plt.ylim(0, 60)
    plt.gca().set_aspect('equal', adjustable='box')


if __name__ == '__main__':

    l1=Line(1,3,2,2)
    c1=Circle(2,2,2)
    print c1.encloses([2,3])
    print c1.move_frame([0, 0])
    print c1.move_frame([5, 3])
    print c1.inter_line(l1)


    '''
    rect = Rect(2.0, 0.0, 0.0, 2.0)
    rect2 = Rect(2.0, 0.0, 0.0, 2.0)
    inter = rect.intersection(rect2)
    if inter is not None:
        print inter.area()
    else:
        print 'weird'
    '''
