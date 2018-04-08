# Robert Kowalchuk
""" This script creates an equal distribution of randomized objects based on user input """

import math
import random

random.seed()
List_Positions = []

# This function creates an empty object from the given parent node and returns itself
def Create_Object(ParentNode = None, Name = "geo_00"):
    ContainerObject = ParentNode.createNode("geo", Name)
    ContainerObject.children()[0].destroy()
    ContainerObject.moveToGoodPosition()

    return ContainerObject

# This function adds an object to a parent object and attemps to connect those objects and returns itself
def Add_Object(ParentObject = None, Type = "box"):
    TempObject = ParentObject.createNode(Type, "{}_00".format(Type))
    TempObject.moveToGoodPosition()

    numberChildren = len(ParentObject.children()) - 1
    if( numberChildren > 0 ):
        TempObject.setInput(0, ParentObject.children()[numberChildren - 1])

    TempObject.setDisplayFlag(True)   

    return TempObject

# This function adds a grid to the given parent object and attaches it to the given object and returns itself
def Add_Grid(ParentObject = None, Name = "Grid_00", Size = (10, 10)):
    GridObject = Add_Object(ParentObject, "grid")
    GridObject.parm("sizex").set(Size[0])
    GridObject.parm("sizey").set(Size[1])

    return GridObject

# This function adds a cone to the given parent object and attaches it to the given object and returns itself
def Add_Cone(ParentObject = None, Name = "Cone_00"):
    ConeObject = Add_Object(ParentObject, "cone")

    return ConeObject

# This function adds a torus to the given parent object and attaches it to the given object and returns itself
def Add_Torus(ParentObject = None, Name = "Torus_00"):
    TorusObject = Add_Object(ParentObject, "torus")

    return TorusObject

# This function adds a box to the given parent object and attaches it to the given object and returns itself
def Add_Box(ParentObject = None, Name = "Box_00"):
    BoxObject = Add_Object(ParentObject, "box")

    return BoxObject

# This function adds a sphere to the given parent object and attaches it to the given object and returns itself
def Add_Sphere(ParentObject = None, Name = "Sphere_00"):
    SphereObject = Add_Object(ParentObject, "sphere")

    return SphereObject

# This function adds a color node to the given parent object and attaches it to the given object and returns itself
def Add_Color(ParentObject = None, Name = "Color_00"):
    ColorObject = Add_Object(ParentObject, "color")

    return ColorObject

# This function takes an object and modifies it scale by the specified value
def Set_Scale(ModifyObject = None, Scale = 1.0):
    ModifyObject.parm("scale").set(Scale)

# This function takes an object and modifies it's position by the specified value
#  This function is inteded to be used with the container objects and not the actual geometry obects
def Set_Position(ModifyObject = None, Position = (0,0,0)):
    ModifyObject.parmTuple("t").set(Position)

# Add a position to the list of positions
#  Does not check if position is unique
def Update_PositionList(Position = (0,0,0)):
    List_Positions.append(Position)
    return Position

# Check to see if the given position has already been used
def Is_PositionUnique(Position = (0, 0, 0)):
    for i in List_Positions:
        if i == Position:
            return False

    return True

# Return a random position based off of the given MaxNumber
def Random_Position(MaxNumber = 10):
    Position = (random.random()*MaxNumber, (random.random()*(MaxNumber/10)) + (MaxNumber/10), random.random()*MaxNumber)

    return Position

#Return a random scale based off of the given MaxNumber
def Random_Scale(MaxNumber = 5):
    Scale = random.random()*MaxNumber

    return Scale

# Take in an color node object and randomize it's RGB color values
def Set_RandomColor(ColorObject = None):
    ColorObject.parmTuple("color").set((random.random(), random.random(), random.random()))



# Get user input from the command line asking for the number of objects as a string value
Str_Number_Objects = raw_input("How many objects? . . . ")
Number_Objects = int(Str_Number_Objects)

# Get a reference to the obj node that is already in the scene in houdini
NodeObj = hou.node("/obj")

# Create a ground plane and scale it based on the number of objects
TempContainer = Create_Object(NodeObj)
TempObject = Add_Grid(TempContainer, "Grid_00", (Number_Objects, Number_Objects))

# Add a random color to the ground plane
TempColor = Add_Color(TempContainer)
Set_RandomColor(TempColor)  

# Set the position of the ground plane so it wil encompase the majority of the created objects
TempPosition = (Number_Objects/2.0,0,Number_Objects/2.0)
Set_Position(TempContainer, TempPosition)

TempScale = 0.0

# create the amount of objects specified by the user
Limits = (Number_Objects/3, (Number_Objects/3) * 2)
for i in range(0, Number_Objects):
    # If we are traversing the first third of the desired number of objects 
    if i < Limits[0]:
        # Create the containing object and then the object that lives inside that container
        TempContainer = Create_Object(NodeObj)
        TempObject = Add_Box(TempContainer)

        # Add a color object to the continer and connect it to the last object that was added
        TempColor = Add_Color(TempContainer)
        Set_RandomColor(TempColor)
        
        # Scale the initial object inside the container 
        TempScale = Random_Scale()
        Set_Scale(TempObject, TempScale)

        # Position the contianer somewhere around the grid without reusing a position
        while(True):
            TempPosition = Random_Position(Number_Objects)
            if(Is_PositionUnique(TempPosition)):
                Set_Position(TempContainer, TempPosition)
                Update_PositionList(TempPosition)
                break
        
    # The second third
    elif i < Limits[1]:
        TempContainer = Create_Object(NodeObj)
        TempObject = Add_Sphere(TempContainer)

        TempColor = Add_Color(TempContainer)
        Set_RandomColor(TempColor)
        
        TempScale = Random_Scale()
        Set_Scale(TempObject, TempScale)

        while(True):
            TempPosition = Random_Position(Number_Objects)
            if(Is_PositionUnique(TempPosition)):
                Set_Position(TempContainer, TempPosition)
                Update_PositionList(TempPosition)
                break
    
    # The last third
    else:
        TempContainer = Create_Object(NodeObj)
        TempObject = Add_Torus(TempContainer)

        TempColor = Add_Color(TempContainer)
        Set_RandomColor(TempColor)
        
        TempScale = Random_Scale()
        Set_Scale(TempObject, TempScale)

        while(True):
            TempPosition = Random_Position(Number_Objects)
            if(Is_PositionUnique(TempPosition)):
                Set_Position(TempContainer, TempPosition)
                Update_PositionList(TempPosition)
                break

