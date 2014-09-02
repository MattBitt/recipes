from PIL import Image
import os

def resize_picture(pic_path, temp_name, pic_name, pic_size):
    temp_name = os.path.join(pic_path, temp_name)
    pname = os.path.join(pic_path, pic_name)
    
    if not os.path.isfile(pname):
        return None
    else:
        try:
            i = Image.open( temp_name )
            i = i.resize( pic_size, Image.ANTIALIAS)
            i.save( pname )
            return 1
        except:
            print "Image function returning none"
            return None

        
        
if __name__ == '__main__':
    img_path = 'c:\\Users\\mbittinger\\Documents\\python\\'
    img_name = 'pic1.jpg'
    if resize_picture(img_path, img_name, (640,480)) == None:
        print "Error"
    else:
        print "Success"
    img_name = 'pic2.jpg'
    if resize_picture(img_path, img_name, (640,480)) == None:
        print "Error"
    else:
        print "Success"
    img_name = 'pic3.jpg'
    if resize_picture(img_path, img_name, (640,480)) == None:
        print "Error"
    else:
        print "Success"