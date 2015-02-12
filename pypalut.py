import os
import sys
import math
import colorsys
from PIL import Image, ImageFilter

class pypalut:
    span = 8 # the cube root of th lut size span^3
    im = "error" # the read in image
    output = "" #the file to save
    w = 1
    h = 1 #the width and height of read in image

    colors_all=[] #the colors from the image

    table=[]#0-1255 values

    table_rgb=[]#0-1 values
    #table_hls=[]#the hls space verion NOT USED YET
    #table_hsv=[]#the hsv space version NOT USED YET

    table_palette=[]#the palette being fitted
    table_distance=[]#distance of all color to table colors

    fuzzy = 5 #grab every nth pixel
    debug = True #give me the play by play

    display_pixel_size = 10 #when shwoing the resulting palette, multiply pixels by this

    def __init__(self,img,out="",size=8,fuz=5,dbg=True,dps = 10):
        self.span=4
        #self.span = size
        self.build()
        self.fuzzy=fuz
        self.debug = dbg
        self.display_pixel_size = dps

        self.load(img)
        self.generate(self.im)
        self.im = self.process(out,True)
        #pass 2
        self.clear_tables()
        self.span=16#size
        self.display_pixel_size = 4
        self.build()
        self.load_buffer(self.im)
        self.generate(self.im)
        self.process(out)


    def generate(self,img,buffer=False):
        if self.debug:
            print "generate: generate lut from palette"

        l = self.im.load()
        for x in range(0,self.w-1,self.fuzzy):
            for y in range(0,self.h-1,self.fuzzy):
                c = l[x,y]
                c_rgb = (c[0]/255.0,c[1]/255.0,c[2]/255.0) #convert to 0-1
                #chls = colorsys.rgb_to_hls(c[0]/255.0,c[1]/255.0,c[2]/255.0)
                #chsv = colorsys.rgb_to_hsv(c[0],c[1],c[2])
                self.colors_all.append(c)

                #loop against the vanilla palette
                count = 0
                for tc in self.table_rgb:

                    distance = self.distance(tc,c_rgb);

                    if(distance < self.table_distance[count]):
                        self.table_palette[count]=c
                        self.table_distance[count]=distance

                    count+=1

        #self.process()

    def process(self,out,multipass=False):
        if self.debug:
            print "process: mange resulting lut"
        width = self.span**2
        swatch = 1
        if out=="" and not multipass:
            swatch = self.display_pixel_size
        img = Image.new("RGB", (width*swatch, self.span*swatch), (0,0,0))
        count = 0
        for i in self.table_palette:
            column = count%self.span
            row = math.floor(count/self.span)%self.span
            plane = math.floor(count/width)

            x = int(((plane*self.span)+column)*swatch)
            y = int(row*swatch)
            img.paste(i,(x,y,int(x+swatch),int(y+swatch)))
            count+=1

        if out!="":
            img.save(self.output,"PNG")
        else:
            if not multipass:
                img.show()

        return img

    def distance(self,c1,c2):
        v = (c1[0]-c2[0],c1[1]-c2[1],c1[2]-c2[2])
        return math.sqrt( (v[0]*v[0])+(v[1]*v[1])+(v[2]*v[2]) )

    def clear_tables(self):
        del self.colors_all[:] #the colors from the image

        del self.table[:]#0-1255 values

        del self.table_rgb[:]#0-1 values
        #del self.table_hls[:]#the hls space verion NOT USED YET
        #del self.table_hsv[:]#the hsv space version NOT USED YET

        del self.table_palette[:]#the palette being fitted
        del self.table_distance[:]#distance of all color to table colors


    def build(self):
        if self.debug:
            print "generate: generate default lut"
        tbsize = self.span**3
        tbsqr = self.span**2
        for i in range(tbsize):
            column = i%self.span
            row = math.floor(i/self.span)%self.span
            plane = math.floor(i/tbsqr)

            r = int(math.floor((column/(self.span-1.0))*255.0))
            g = int(math.floor((row/(self.span-1.0))*255.0))
            b = int(math.floor((plane/(self.span-1.0))*255.0))

            self.table.append((r,g,b))
            self.table_rgb.append( (r/255.0,g/255.0,b/255.0) )
            #self.table_hls.append(colorsys.rgb_to_hls(r/255.0,g/255.0,b/255.0))
            #self.table_hsv.append(colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0))

            self.table_palette.append((255,255,255))
            self.table_distance.append(1000.0)


    def load(self, img):
        if self.debug:
            print "load: load image off disk"
        try:
            self.im = Image.open(img)
            self.w,self.h = self.im.size
            if self.debug:
                print "image info:"+str(self.w)+","+str(self.h)+" : "+str(self.w*self.h)
                print "fuzzy numbers:"+str(self.fuzzy)+" : "+str(math.floor(self.w/self.fuzzy))+","+str(math.floor(self.h/self.fuzzy))+" : "+str((math.floor(self.w/self.fuzzy))*(math.floor(self.h/self.fuzzy)))
            #self.generate()

        except:
            return "loading error"

    def load_buffer(self,buffer,fuzzy=1):
        if self.debug:
            print "load buffer: use generated image"
        self.w,self.h = buffer.size
        self.fuzzy = 1
        if self.debug:
            print "image info:"+str(self.w)+","+str(self.h)+" : "+str(self.w*self.h)
            print "fuzzy numbers:"+str(self.fuzzy)+" : "+str(math.floor(self.w/self.fuzzy))+","+str(math.floor(self.h/self.fuzzy))+" : "+str((math.floor(self.w/self.fuzzy))*(math.floor(self.h/self.fuzzy)))



def main(kwargs):
    lut = pypalut(kwargs[1],"",8,10);


if __name__ == "__main__":
    main(sys.argv)
