from turtle import *
from math import *
tracer(0)
mode("logo")
def teleport(x,y):
    up()
    goto(x,y)
    down()

def angle(r,l):
    alpha = atan(r/(l/2))

    angle = 180-(2*degrees(alpha))
    return angle
screensize(5000,5000)

def drawCircPath(l,a,n):
    forward(l/4)
    for i in range(n):
        left(a)
        forward(l/2)

def drawCanvas():
    setheading(90)
    for i in range(2):
        forward(300)
        right(90)
        forward(180)
        right(90)

def previewCirc(c,r,phase,n,scale,angleStart,angleEnd):
    clockwise = angleEnd - angleStart > 0
    l = (phase == 1 and 28*scale) or 42 * scale
    a = angle(r,l)

    if not clockwise:
         a = -a

    drawCanvas()

    teleport(c[0]/2,(-c[1]-r)/2)
    color("blue")
    circle(r/2)

    color("red")
    teleport(c[0]/2,-c[1]/2)
    up()
    setheading(angleStart)
    forward(r/2)
    if clockwise:
        left(90)
    else:
        right(90)
    down()
    pensize(5)
    dot(20)
    drawCircPath(l,a,n)

    color("green")
    teleport(c[0]/2,-c[1]/2)
    up()
    setheading(angleEnd)
    forward(r/2)
    if clockwise:
        left(90)
    else:
        right(90)
    down()
    dot(20)
    drawCircPath(l,a,n)

def previewLine(startPoint,endPoint,phase,n,scale):
    l = (phase == 1 and 28*scale) or 42*scale

    drawCanvas()

    teleport(startPoint[0]/2,-startPoint[1]/2)
    setheading(towards(endPoint[0]/2,-endPoint[1]/2))
    color("red")
    dot(20)
    pensize(5)
    for i in range(n):
        backward(l/2)

    teleport(endPoint[0]/2,-endPoint[1]/2)
    color("green")
    dot(20)
    for i in range(n):
        backward(l/2)

def lineWrite(phase,seg,scale,startPoint,endPoint,l,a,beat):
    tag = open(input("Name of the tag")+".json","w")
    unique_id = input("Select a unique ID for the set of decos (we don't want duplicates, now do we ?)")
    drawLayer = input('drawLayer ? (fg or bg)')
    drawOrder = input('drawOrder ?')
    #Head
    tag.write("[\n")
    tag.write('{"id":"'+unique_id+'Head","type":"deco","hide":false,"time":0,"angle":0,"sprite":"DoGPhase'+str(phase)+'Head.png","sx":'+str(scale)+',"sy":'+str(scale)+',"x":'+str(startPoint[0])+',"y":'+str(startPoint[1])+',"r":'+str(a)+',')
    tag.write('"drawLayer":"'+drawLayer+'","drawOrder":'+drawOrder+',')

    if phase == 1:
        tag.write('"ox":27,"oy":30')
    
    elif phase == 2:
        tag.write('"ox":34,"oy":54')
    tag.write('},')
    #Body
    for i in range(seg):
        tag.write('{"id":"'+unique_id+'Body'+str(i)+'","type":"deco","hide":false,"time":0,"angle":0,"sprite":"DoGPhase'+str(phase)+'Body.png","sx":'+str(scale)+',"sy":'+str(scale)+',"x":0,"y":'+str(l)+',')
        tag.write('"drawLayer":"'+drawLayer+'","drawOrder":'+drawOrder+',')

        if phase == 1:
            tag.write('"ox":23,')
    
        elif phase == 2:
            tag.write('"ox":29,')
        
        if i == 0:
            tag.write('"parentid":"'+unique_id+'Head"')
        else:
            tag.write('"parentid":"'+unique_id+'Body'+str(i-1)+'"')
        tag.write('},')
    #Tail
    tag.write('{"id":"'+unique_id+'Tail"'+',"type":"deco","hide":false,"time":0,"angle":0,"sprite":"DoGPhase'+str(phase)+'Tail.png","sx":'+str(scale)+',"sy":'+str(scale)+',"x":0,"y":'+str(l)+',')
    tag.write('"drawLayer":"'+drawLayer+'","drawOrder":'+drawOrder+',')
    
    if phase == 1:
            tag.write('"ox":21,')
    
    elif phase == 2:
        tag.write('"ox":22,')
    tag.write('"parentid":"'+unique_id+'Body'+str(seg-1)+'"},')

    #Movement
    tag.write('{"id":"'+unique_id+'Head","order":1,"type":"deco","time":0,"x":'+str(endPoint[0])+',"y":'+str(endPoint[1])+',"duration":'+str(beat)+'},')
    #Hiding
    tag.write('{"id":"'+unique_id+'Head","type":"deco","time":'+str(beat)+',"hide":true},') 

    for i in range(seg):
        tag.write('{"id":"'+unique_id+'Body'+str(i)+'","type":"deco","time":'+str(beat)+',"hide":true},')

    tag.write('{"id":"'+unique_id+'Tail","type":"deco","time":'+str(beat)+',"hide":true}]')
    print("Tag generated")

def circWrite(phase,seg,scale,circle,r,startAngle,endAngle,clockwise,l,a,beat):
    tag = open(input("Name of the tag")+".json","w")
    unique_id = input("Select a unique ID for the set of decos (we don't want duplicates, now do we ?)")
    drawLayer = input('drawLayer ? (fg or bg)')
    drawOrder = input('drawOrder ?')
    #Rotation center
    tag.write("[\n")
    tag.write('{"id":"'+unique_id+'RotationCenter","type":"deco","hide":true,"time":0,"angle":0,"x":'+str(circle[0])+',"y":'+str(circle[1])+',"r":'+str(startAngle)+'},')
    #Head
    
    tag.write('{"id":"'+unique_id+'Head","type":"deco","hide":false,"time":0,"angle":0,"sprite":"DoGPhase'+str(phase)+'Head.png","sx":'+str(scale)+',"sy":'+str(scale)+',"y":'+str(-r)+',')

    if clockwise:
        tag.write('"r":-90,"x":'+str(-l/2)+',')
    else:
        tag.write('"r":90,"x":'+str(l/2)+',')

    tag.write('"drawLayer":"'+drawLayer+'","drawOrder":'+drawOrder+',')

    if phase == 1:
        tag.write('"ox":27,"oy":30')
    
    elif phase == 2:
        tag.write('"ox":34,"oy":54')
    
    tag.write(',"parentid":"'+unique_id+'RotationCenter"')
    tag.write('},')
    #Body
    for i in range(seg):
        tag.write('{"id":"'+unique_id+'Body'+str(i)+'","type":"deco","hide":false,"time":0,"angle":0,"sprite":"DoGPhase'+str(phase)+'Body.png","sx":'+str(scale)+',"sy":'+str(scale)+',"x":0,"y":'+str(l)+',"r":'+str(a)+',')
        tag.write('"drawLayer":"'+drawLayer+'","drawOrder":'+drawOrder+',')

        if phase == 1:
            tag.write('"ox":23,')
    
        elif phase == 2:
            tag.write('"ox":29,')
        
        if i == 0:
            tag.write('"parentid":"'+unique_id+'Head"')
        else:
            tag.write('"parentid":"'+unique_id+'Body'+str(i-1)+'"')
        tag.write('},')
    #Tail
    tag.write('{"id":"'+unique_id+'Tail"'+',"type":"deco","hide":false,"time":0,"angle":0,"sprite":"DoGPhase'+str(phase)+'Tail.png","sx":'+str(scale)+',"sy":'+str(scale)+',"x":0,"y":'+str(l)+',"r":'+str(a)+',')
    tag.write('"drawLayer":"'+drawLayer+'","drawOrder":'+drawOrder+',')
    
    if phase == 1:
            tag.write('"ox":21,')
    
    elif phase == 2:
        tag.write('"ox":22,')
    tag.write('"parentid":"'+unique_id+'Body'+str(seg-1)+'"},')

    #Movement
    tag.write('{"id":"'+unique_id+'RotationCenter","order":1,"type":"deco","time":0,"r":'+str(endAngle)+',"duration":'+str(beat)+'},')
    #Hiding
    tag.write('{"id":"'+unique_id+'Head","type":"deco","time":'+str(beat)+',"hide":true},') 

    for i in range(seg):
        tag.write('{"id":"'+unique_id+'Body'+str(i)+'","type":"deco","time":'+str(beat)+',"hide":true},')

    tag.write('{"id":"'+unique_id+'Tail","type":"deco","time":'+str(beat)+',"hide":true}]')
    print("Tag generated")
    

def asking():
    phase = int(input("Phase of the Devourer (1 or 2)"))
    seg = int(input("Number of segments (Head and Tail excluded)"))
    scale = int(input("Scale at which the devourer will be drawn (2 recommended)"))

    movement = input("Type of movement : 'L' for a line and 'C' for a circle").upper()

    if movement == "L":
        startPointX = float(input("X coordinate of the Start Point"))
        startPointY = float(input("Y coordinate of the Start Point"))
        endPointX = float(input("X coordinate of the End Point (don't forget, the tail will trail behind)"))
        endPointY = float(input("Y coordinate of the End Point (don't forget, the tail will trail behind)"))
        beat = float(input("Number of beats to complete the animation"))

        l = (phase == 1 and 28*scale) or 42*scale
        a = 180 - degrees(acos((endPointY-startPointY)/dist((startPointX,startPointY),(endPointX,endPointY))))
        a = (endPointX-startPointX < 0 and -a) or a

        previewLine([startPointX,startPointY],[endPointX,endPointY],phase,seg+1,scale)
        update()
        w = input("Simulation displayed. Would you like to write the tag ? (y/n)").lower()
        if w == "y":
            lineWrite(phase,seg,scale,[startPointX,startPointY],[endPointX,endPointY],l,a,beat)

    elif movement == "C":
        cx = float(input("X coordinate of the center of the circle"))
        cy = float(input("Y coordinate of the center of the circle"))
        r = float(input("Radius of the circle"))

        startAngle = float(input("Start Angle"))
        endAngle = float(input("End Angle"))
        beat = float(input("Number of beats to complete the animation"))

        clockwise = startAngle - endAngle > 0
        l = (phase == 1 and 28*scale) or 42 * scale
        a = angle(r,l)

        if not clockwise:
            a = -a

        previewCirc([cx,cy],r,phase,seg+1,scale,startAngle,endAngle)
        update()
        w = input("Simulation displayed. Would you like to write the tag ? (y/n)").lower()
        if w == "y":
            circWrite(phase,seg,scale,[cx,cy],r,startAngle,endAngle,clockwise,l,a,beat)

#PLEASE OH GOD REMEMBER TO HIDE THE DECOS AT THE END OF THE TAG OR PENTATRATE WILL KILL YOU

#previewCirc([300,360],300,1,5,2,-90,180)
#previewLine([-50,300],[900,0],1,5,2)

asking()

done()