#Robert Kowalchuk
#This script creates a number of objects in a circle 
# and modifies the color based off of it's position
import math
import colorsys

#Set Number of objects
ObjectNumber = 75
print ObjectNumber, "Objects will appear "

#Get the shape of type tube torus sphere box from user
Str_Object_Shape = raw_input("What shape should they be? torus, tube, sphere, or box ")
Str_Object_Shape = Str_Object_Shape.lower()
#Set the scale from 0.1 to 10.0
ObjectScale = 0.5
print ObjectScale, "Is the", Str_Object_Shape, "scale"

#Create the parent object
NodeTop = hou.node("/obj")

#Create i amount of objects
OffsetX = 0.0
OffsetY = 0.0
OffsetZ = 0.0

ContainerRadius = 8
ContainerAngleOffset = 360.0 / ObjectNumber
CurrentAngle = 0.0

for i in range(0, ObjectNumber):
    ContainerGeo = NodeTop.createNode("geo", "myGeo_00")
    ContainerGeo.children()[0].destroy()
    ContainerGeo.moveToGoodPosition()
    
    ObjectTemp = ContainerGeo.createNode(Str_Object_Shape, "My_{}Geo_00".format(Str_Object_Shape))
    ObjectTemp.moveToGoodPosition()

    #Set the shapes scale
    #Error check for tube
    if Str_Object_Shape != "tube":
        ObjectTemp.parm("scale").set(ObjectScale)
    else:
        ObjectTemp.parm("radscale").set(ObjectScale)

    #Arrange the object in a circle 
    ObjectTemp.parmTuple("t").set((OffsetX,OffsetY,OffsetZ))

    #Color the object
    NodeColor = ContainerGeo.createNode("color", "myColorNode")
    NodeColor.moveToGoodPosition()
    NodeColor.setInput(0, ObjectTemp)
    NodeColor.setDisplayFlag(True)
    NodeColor.parmTuple("color").set( colorsys.rgb_to_hsv(1,OffsetX,OffsetY) )

    #Update values for next object
    OffsetX += ContainerRadius*math.cos(CurrentAngle) 
    OffsetY += ContainerRadius*math.sin(CurrentAngle)
    CurrentAngle += ContainerAngleOffset