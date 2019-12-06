import rospy
from geometry_msgs.msg import Point,Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2
rospy.init_node('robot_cleaner', anonymous=True)

scan0   = 0.0
scan90  = 0.0
scan180 = 0.0
scan270 = 0.0
walk = 0
 
theta = 0.0
rotation =0.0
Direction = 0 
x = 1 # position x
y = 0 # position y
rotation = 0 # checkStateRotate

checkEdge0 = False
checkEdge90 = False
checkEdge180 = False
checkEdge270 = False

maze = [["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
	["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
	["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
        ["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
	["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
	["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
	["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
	["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
	["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
	["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"],
	["+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+","+"]]

def move():

    global x
    global y
    global Direction



    vel_msg = Twist()
    vel_msg.linear.x = 0.1
    velocity_publisher.publish(vel_msg)
				


    if Direction == 0 or Direction == -360 or Direction == 360:
	y = y + 1
    elif Direction == 90 or Direction == -270:
	x = x + 1
    elif Direction == 180 or Direction == -180:
        y = y - 1
    elif Direction == 270 or Direction == -90:
	x = x - 1

    rospy.sleep(2)
    saveMap()
    

def rotate():

     global checkEdge0
     vel_msg = Twist()
     vel_msg.angular.z = rotation
     velocity_publisher.publish(vel_msg)
     checkEdge0 = False
     rospy.sleep(2)
     vel_msg.angular.z = 0
     

def scanner(msg):
    global scan0 
    global scan90 
    global scan180 
    global scan270 
    scan0 = float(msg.ranges[0])
    scan90 = float(msg.ranges[90])
    scan180 = float(msg.ranges[180])
    scan270 = float(msg.ranges[270])
    print ('values at 0 degree',msg.ranges[0])
    print ('values at 90 degree',msg.ranges[90])
    print ('values at 180 degree',msg.ranges[180])
    print ('values at 270 degree',msg.ranges[270])


def checkEdge():

    global checkEdge0
    global checkEdge90
    global checkEdge180
    global checkEdge270 
    global rotation
    global Direction


    if scan0 > 0.345 or scan0 == 0.0:
        print ('values at 0 degree',scan0)
        move()
	Direction = Direction + 0

    if scan0 < 0.345 and scan0 !=0.0: 
        print ('values at 0 degree',scan0)
        checkEdge0 = True

    if checkEdge0 == True and scan0 < 0.345:
        if scan90 > scan270 and checkEdge0==True:
            rotation = 0.785
            rotate()
            Direction = Direction + 90	


        elif scan90 < scan270 and checkEdge0==True:
            rotation= -0.785
            rotate()
            Direction = Direction - 90



def saveMap():

    if maze[y][x] == "+":
       	maze[y][x] = " "
	print ("============  saveMap  =============")
	print ("maze[y][x] : ",maze[y][x])
	vel_msg = Twist()
	vel_msg.linear.x = 0
     	vel_msg.angular.z = 0
     	velocity_publisher.publish(vel_msg)
	for i in maze:
  	   print (i)
    elif maze[y][x] != "":
	pass
    elif maze[y][x] == "e":
	print("e")

	for i in maze:
  	   print (i)
		    



velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
#sub = rospy.Subscriber("/odometry/filtered", Odometry, newOdom)
sub = rospy.Subscriber('/scan', LaserScan, scanner)

if __name__ == '__main__':
    try:    
        while 1:
            
              checkEdge()
        
    except rospy.ROSInterruptException: pass
