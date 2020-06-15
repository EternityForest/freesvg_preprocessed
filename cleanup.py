
import os, cairosvg,shutil,xml,gzip,traceback,zlib

svg = os.path.join(os.path.abspath(os.path.dirname(__file__)),"svg")
svgz = os.path.join(os.path.abspath(os.path.dirname(__file__)),"svgz")
png = os.path.join(os.path.abspath(os.path.dirname(__file__)),"png")
junk = os.path.join(os.path.abspath(os.path.dirname(__file__)),"junk")
junk0 = os.path.join(os.path.abspath(os.path.dirname(__file__)),"junk0")
junkinvalid = os.path.join(os.path.abspath(os.path.dirname(__file__)),"junkinvalid")
junknameless = os.path.join(os.path.abspath(os.path.dirname(__file__)),"junkbignameless")

webp= os.path.join(os.path.abspath(os.path.dirname(__file__)),"webp")

from PIL import Image

try:
    os.mkdir(png)
except:
    pass
try:
    os.mkdir(junk)
except:
    pass
try:
    os.mkdir(webp)
except:
    pass
try:
    os.mkdir(svgz)
except:
    pass

try:
    os.mkdir(junk0)
except:
    pass


try:
    os.mkdir(junkinvalid)
except:
    pass

try:
    os.mkdir(junknameless)
except:
    pass



def isNameless(fn):
    fn = fn.split(".")
    for i in fn[0]:
        if not i in '0123456789':
            return False
    return True

#Just gzip these. Text is the reason.
preserve={    
    "3D-Multicolored-United-States-Map-Dots.svg":"Took a very long time to convert"
}


#Allow working straight from the zip file
if os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)),"source.zip")):
    print("Found source zip")
    from zipfile import ZipFile
    z=ZipFile(os.path.join(os.path.abspath(os.path.dirname(__file__)),"source.zip"))
    
    for i in z.namelist():
        n = i
        i=os.path.basename(i)
        if not i.endswith('.svg'):
            continue
        
        if os.path.exists(os.path.join(png,i+".png")):
            continue
        if os.path.exists(os.path.join(svgz,i+"z")):
            continue
        if os.path.exists(os.path.join(webp,i+".webp")):
            continue
        if os.path.exists(os.path.join(svg,i)):
            continue
        if z.getinfo(n).file_size==0:
            continue
            
                
        print("Imported "+n)
        z.extract(n, path=svg)
        shutil.move(os.path.join(svg,"svg",i), os.path.join(svg,i))
try:
    os.remove(os.path.join(svg,"svg"))
except:
    pass
        



ts = 0
ts_raster=0

COMPRESS_ABOVE = 96000
RASTER_ABOVE = 10**6*6
WEBP_ABOVE = 512000
MAX_NAMELESS = 386000
MAX_NAMELESS_COMPRESSED = 128000

for i in os.listdir(svg):
    if os.path.getsize(os.path.join(svg,i)) > COMPRESS_ABOVE:
        ts += os.path.getsize(os.path.join(svg,i))
    if os.path.getsize(os.path.join(svg,i)) > RASTER_ABOVE:
        ts_raster += os.path.getsize(os.path.join(svg,i))
print("Size of svg files above compress threshold:",ts)
print("Size of svg files above raster threshold:",ts_raster)


#Restore things from junk that previous non-svgz versions shouldn't have junked, according
#To the current settings
#NOTE: This has no way of pulling compressed files back out of compression.
#If you have huge stuff there that belongs as a raster, you  may have to start over straight
#From the zip
for i in os.listdir(junk):
    if os.path.exists(os.path.join(svg,i)):
        continue
    if os.path.exists(os.path.join(svgz,i+"z")):
        continue
    
    #Find files under 6MB that were junked by a previous version, and try compressing them instead.
    #If bigger than the current raster threshold, then they are where they should be.
    if os.path.getsize(os.path.join(junk,i)) > RASTER_ABOVE:
        continue
    
    if isNameless(i):
         if os.path.getsize(os.path.join(junk,i)) > MAX_NAMELESS:
            shutil.move(os.path.join(junk,i), os.path.join(junknameless,i))
            continue
    
    lossyversion = None
    if os.path.exists(os.path.join(webp,i+".webp")):
        lossyversion= os.path.join(webp,i+".webp")
    
    if os.path.exists(os.path.join(webp,i+".png")):
        lossyversion = os.path.join(webp,i+".png")
    
    if not lossyversion:
        continue
    
    print("Restoring "+i+" from junk as compressed")
   
    with gzip.open(os.path.join(svgz,i)+"z", 'wb') as f:
        with open(os.path.join(junk,i),'rb') as f_in:
            f.write(f_in.read())
            
    os.remove(os.path.join(junk,i))
    os.remove(lossyversion)
   
   
for i in os.listdir(webp):
    #Keep small nameless files that aren't taking up space
    if isNameless(i):
         if os.path.getsize(os.path.join(webp,i)) > MAX_NAMELESS_COMPRESSED:
            shutil.move(os.path.join(webp,i), os.path.join(junknameless,i))
            continue
        
for i in os.listdir(png):
    #Keep small nameless files that aren't taking up space
    if isNameless(i):
         if os.path.getsize(os.path.join(png,i)) > MAX_NAMELESS_COMPRESSED:
            shutil.move(os.path.join(png,i), os.path.join(junknameless,i))
            continue
        
for i in os.listdir(svgz):
    #Keep small nameless files that aren't taking up space
    if isNameless(i):
         if os.path.getsize(os.path.join(svgz,i)) > MAX_NAMELESS_COMPRESSED:
            shutil.move(os.path.join(svgz,i), os.path.join(junknameless,i))
            continue
        
        
for i in os.listdir(svg):
    #Keep small nameless files that aren't taking up space
    if isNameless(i):
         if os.path.getsize(os.path.join(svg,i)) > MAX_NAMELESS:
            shutil.move(os.path.join(svg,i), os.path.join(junknameless,i))
            continue
        
    #If the compressed version exists use that
    if os.path.exists(os.path.join(png,i+".png")):
        os.remove(os.path.join(svg,i))
        continue
    if os.path.exists(os.path.join(svgz,i+"z")):
        os.remove(os.path.join(svg,i))
        continue
    if os.path.exists(os.path.join(webp,i+".webp")):
        os.remove(os.path.join(svg,i))
        continue
    
    if os.path.getsize(os.path.join(svg,i)) > RASTER_ABOVE and not i in preserve:
        try:
            print(os.path.join(svg,i)+'Converting to png')
            cairosvg.svg2png(url=os.path.join(svg,i), write_to=os.path.join(png,i)+".png")
            print(os.path.join(svg,i)+'Converted to png')

            if os.path.getsize(os.path.join(png,i)+".png") > WEBP_ABOVE:
                im = Image.open(os.path.join(png,i)+".png")
                rgb_im = im.convert('RGBA')
                print(os.path.join(svg,i)+'Converting to webp')
                rgb_im.save(os.path.join(webp,i)+'.webp',method=6)
                print(os.path.join(svg,i)+'Converted to webp')

                os.remove(os.path.join(png,i)+".png")
        except MemoryError:
            print("Could not convert(MemoryError)"+os.path.join(svg,i)+', excluding from results')
            shutil.move(os.path.join(svg,i), os.path.join(junk,i))
        except xml.etree.ElementTree.ParseError:
            print("Could not convert(ParseError)"+os.path.join(svg,i)+', excluding from results')
            shutil.move(os.path.join(svg,i), os.path.join(junkinvalid,i))
        except:
            print(i)
            print(traceback.format_exc())
       
        try:
            shutil.move(os.path.join(svg,i), os.path.join(junk,i))
        except Exception as e:
            print(e)
        print(i)
        
    elif os.path.getsize(os.path.join(svg,i)) > COMPRESS_ABOVE:
        print("Gzipping "+i)
        with gzip.open(os.path.join(svgz,i)+"z", 'wb') as f:
            with open(os.path.join(svg,i),'rb') as f_in:
                f.write(f_in.read())
        try:
            shutil.move(os.path.join(svg,i), os.path.join(junk,i))
        except Exception as e:
            print(e)
                
    elif os.path.getsize(os.path.join(svg,i)) ==0:
        print(os.path.join(svg,i)+' was 0 bytes, excluding from results')
        shutil.move(os.path.join(svg,i), os.path.join(junk0,i))
        
