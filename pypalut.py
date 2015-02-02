import os
import sys
import math
import colorsys
from PIL import Image, ImageFilter

debug=True
#colors_all=[]

table=[]#vanilla table generated based on span
table_rgb=[]
table_hls=[]#the hls space verion
table_hsv=[]#the hsv space version
table_palette=[]#the palette being fitted
table_distance=[]#the distance of the palette from the table for comparrison

span = 8 # this is the cube root of the table ie 8*8*8
max_samples = 50000
#similar_threshold = 1.0

def load_image(im):
  try:
    my_im = Image.open(im)
    return my_im
  except:
    return "error"

def color_distance_rgb(c1,c2):
    #rgb distance
    rm = 0.5*(c1[0]+c2[0])
    #d = sum( (2+rm,4,3-rm)*( c1-c2 )**2 )**0.5

    a = 2.0+rm+4.0+3.0-rm
    b = (c1[0]-c2[0])+(c1[1]-c2[1])+(c1[2]-c2[2])
    d = (a*b**2.0)**0.5

    return d

def build_vanilla_table():
    global span
    global table
    tbsize = span**3
    tbsqr = span**2
    for i in range(tbsize):
        column = i%span
        row = math.floor(i/span)%span
        plane = math.floor(i/tbsqr)

        r = int(math.floor((column/(span-1.0))*255.0))
        g = int(math.floor((row/(span-1.0))*255.0))
        b = int(math.floor((plane/(span-1.0))*255.0))

        table.append((r,g,b))
        table_rgb.append( (r/255.0,g/255.0,b/255.0) )
        table_hls.append(colorsys.rgb_to_hls(r/255.0,g/255.0,b/255.0))
        table_hsv.append(colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0))

        table_palette.append((255,255,255))
        table_distance.append(1000.0)


        #print i%span # red 0-root colums
        #print math.floor(i/span)%span #green rows 0 - 63 (if span is 8 or 8*8)
        #print math.floor(i/tbsqr) # blue each squar
        #print (r,g,b)

def display_table(file=""):
    global span
    width = span**2
    im = Image.new("RGB", (width, span), (0,0,0))
    count = 0
    for i in table_palette:
        column = count%span
        row = math.floor(count/span)%span
        plane = math.floor(count/width)

        x = int((plane*span)+column)
        y = int(row)
        im.paste(i,(x,y,int(x+1),int(y+1)))
        count+=1
    #im.show()
    if file!="":
        im.save(file,"PNG")
    else:
        im.show()

def main_DEBUG(kwargs):
    build_vanilla_table()
    #display_table(kwargs[2])
    display_table()

def main(kwargs):

    global colors_all
    global debug
    global max_samples

    build_vanilla_table()

    my_im = load_image(kwargs[1])

    if my_im != "error":
        w,h = my_im.size
        fuzzy = 2 #int(math.floor( max(1,( (w*h)/max_samples ) ) ) )
        #fuzzy = (w*h)-max_samples
        #count=0
        if debug:
            print "image width:"+str(w)
            print "image height:"+str(h)
            print "number of pixels:"+str(w*h)
            print "fuzzy:"+str(fuzzy)
            print "fuzzy width:"+str(math.floor(w/fuzzy))
            print "fuzzy width:"+str(math.floor(h/fuzzy))
        l = my_im.load()
        for x in range(0,w-1,fuzzy):
            for y in range(0,h-1,fuzzy):
                c = l[x,y]
                #print c
                c_rgb = (c[0]/255.0,c[1]/255.0,c[2]/255.0) #convert to 0-1
                #chls = colorsys.rgb_to_hls(c[0]/255.0,c[1]/255.0,c[2]/255.0)
                #chsv = colorsys.rgb_to_hsv(c[0],c[1],c[2])

                #loop against the vanilla palette
                count = 0
                for tc in table_rgb:
                    distance = color_distance_rgb(c_rgb,tc)
                    #print distance
                    if(distance < table_distance[count]):
                        table_palette[count]=c
                        table_distance[count]=distance
                    count+=1


        display_table(kwargs[2])


    else:
        print "image not recognized"
        return



if __name__ == "__main__":
    main(sys.argv)
