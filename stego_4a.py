from PIL import Image
import math


def binarise(filename): 
    #converts payload file to a list of binary bits (string)
    f = open(filename,'r').read()
    b_file=[]
    for char in range(len(f)):
        for bit in format(ord(f[char]), '08b'):
            b_file.append(bit)
    return b_file



def decode(b_file): 
    #reverses binarise(), takes list, returns string
    result = []
    for byte in range(0,len(b_file),8):
        result.append(chr(int(''.join(b_file[byte:byte+8]),2)))
    return ''.join(result)



def inject(img_name, binfile, output_filename):
    with Image.open(img_name) as im:
        counter=0
        grid = im.load()
        
        # prevents counter from crashing if len(binfile) % 3 != 0 
        #(as there are 3 channels data is being saved to)
        if len(binfile) % 3 == 2: 
            binfile.append('3')
        elif len(binfile) % 3 == 1:
            binfile.append('3')
            binfile.append('3')

        for y in range(im.size[1]):
            for x in range(im.size[0]):
                pixel = grid[x,y]
                bitnum = (x + y*im.size[0]) * 3
                
                # darkens 255 values a bit (pun intended) to prevent data loss 
                #(as 255 can not be incremented further)
                if pixel[0] == 255: 
                    pixel = (pixel[0]-1,pixel[1],pixel[2])
                if pixel[1] == 255:
                    pixel = (pixel[0],pixel[1]-1,pixel[2])
                if pixel[2] == 255:
                    pixel = (pixel[0],pixel[1],pixel[2]-1)

                pixel = (   pixel[0] + int(binfile[bitnum]),
                            pixel[1] + int(binfile[bitnum + 1]),
                            pixel[2] + int(binfile[bitnum + 2])
                            )
                im.putpixel((x,y),pixel)
                counter+=3
                
                # breaks the loop if reached the end of the file and injects a breaker value of 3 at the last place 
                # to let extract() know where the binary data ends
                if counter == len(binfile): 
                    pixel = (pixel[0] + 2, pixel[1],pixel[2])
                    im.putpixel((x+1,y),pixel)
                    break
            if counter == len(binfile):
                break

        im.save(output_filename)


def extract(img_orig, img_msg): 
    # extracts binary data from img_msg using img_orig as a key
    binary = []
    with Image.open(img_orig) as orig, Image.open(img_msg) as msg:
        grid_orig = orig.load()
        grid_msg = msg.load()
        complete = False

        for y in range(orig.size[1]):
            for x in range(orig.size[0]):
                pixel_orig = grid_orig[x,y]
                pixel_msg = grid_msg[x,y]
                
                # same as in inject() on line 39, darkens values of 255
                if pixel_orig[0] == 255: 
                    pixel_orig = (pixel_orig[0]-1,pixel_orig[1],pixel_orig[2])
                if pixel_orig[1] == 255:
                    pixel_orig = (pixel_orig[0],pixel_orig[1]-1,pixel_orig[2])
                if pixel_orig[2] == 255:
                    pixel_orig = (pixel_orig[0],pixel_orig[1],pixel_orig[2]-1)

                for i in range(3):
                    if pixel_msg[i] - pixel_orig[i] == 1 or pixel_msg[i] - pixel_orig[i] == 0:
                        binary.append(str(pixel_msg[i] - pixel_orig[i]))
                    else:
                        print 'Extraction complete' # it is the value (3) used in inject() to trigger a break
                        complete = True
                        break
                if complete == True:
                    break
            if complete == True:
                break
    return binary


mode = ''
while mode != '1' and mode != '2':
    mode = raw_input('Select from following modes:\n[1] Inject file into image\n[2] Extract file from image\n\n')

if mode=='1':
    payload_name = raw_input('Enter name of payload file:\n')
    img_name = raw_input('Enter image file name:\n')
    outputname = 'STEGO_' + img_name
    print '\nInjecting...'
    inject(img_name, binarise(payload_name),outputname)
    print 'Injection complete! \n'
elif mode=='2':
    img_name = raw_input('Enter key image file name:\n')
    msg_img_name = raw_input('Enter message image file name:\n')
    print '\nExtracting...\n'
    result = open('result.txt','w+')
    result.write(decode(''.join(extract( img_name, msg_img_name))))
    result.close()
    print 'File extracted into result.txt.'
