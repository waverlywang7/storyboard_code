

import re
import cv2 
import numpy as np 
from PIL import Image
from pprint import pprint
import os
def detect_rectangles():
    # Let's load a simple image with 3 black squares 
    image = cv2.imread("/Users/waverlywang/Downloads/Grandpa-1.jpg")
    resized_image = cv2.resize(image, (960, 540))   # output is numpy array

    cv2.waitKey(0) 
    
    # Grayscale 
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY) 
    
    # Find Canny edges 
    edged = cv2.Canny(gray, 30, 200) 
    cv2.waitKey(0) 
    
    # Finding Contours 
    # Use a copy of the image e.g. edged.copy() 
    # since findContours alters the image 
    contours, hierarchy = cv2.findContours(edged,  
        cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    
    # cv2.imshow('Canny Edges After Contouring', edged) 
    # cv2.waitKey(0) 
    
    print("Number of Contours found = " + str(len(contours))) 
    
    # Draw all contours 
    # -1 signifies drawing all contours 

    # Loop through contours to find rectangles

    count = 0
    corners = []
    for contour in contours:
        # Approximate the contour to simplify it (reduce the number of points)
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True) #approx shapes. a collection of points



        
        # If the contour has 4 vertices (a rectangle), draw it

        if len(approx) == 4:
            area = cv2.contourArea(approx)
            if area > 52000:
                print(area, "area\n")
                count+=1
                LoC = []
                
                for corner in approx:
                    
                    x, y = corner.ravel()
                    rec_corners = LoC.append((x,y))

                    cv2.circle(resized_image, (x, y), 5, (0, 255, 0), -1)
          
                corners.append((LoC[0], LoC[2])) #only include the 1st and 3rd coordinates which is top left and bottom right corners
    # SO APPARENLTY 0,0 is in the top left corner of an image and y increases as you go down in images
    print(f"there are {count} rectangles")
    pprint(corners)

    # Display the image with detected rectangles
    cv2.imshow('Detected Rectangles', resized_image) 
    cv2.waitKey(0) 
    cv2.destroyWindow('Detected Rectangles') 
    cv2.waitKey(1) 
    return corners

CORNERS = [((641, 303), (954, 471)),
 ((323, 303), (636, 471)),
 ((5, 303), (318, 471)),
 ((641, 36), (954, 203)),
 ((323, 36), (636, 204)),
 ((5, 36), (318, 204))]

CORNERS.reverse()  # reverse the list because the CORNERS list is for some reason going backward


def crop_storyboard(image_path, starting_num):
    # takes in storyboard and outputs a bunch of storyboard panels and starting number for panel
    num = int(starting_num)

    base_name = os.path.basename(image_path)
    base_name = re.split(r"\.\s*", base_name)[0]

    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (960, 540))   # output is numpy array
    
    data = Image.fromarray(resized_image) 
    cropped_width, cropped_height = data.size

    for corner in CORNERS:
        print(CORNERS)
        (left, top), (right, bottom) = corner
  
        cropped_image = data.crop((int(left), int(top), int(right), int(bottom)))

      
        # make output folder in directory that held image
        output_folder = base_name + "_images"
        output_path = os.path.join(os.path.dirname(image_path), output_folder)
        if not os.path.exists(os.path.join(output_path)):
            os.makedirs(output_path)

        #make image
        jpeg_path = os.path.join(output_path, base_name + str(num) +'.jpg')
        num += 1

        # Save pages as images in the pdf
        cropped_width, cropped_height = cropped_image.size
        print(cropped_width, cropped_height)
        # cropped_image.save(jpeg_path, 'JPEG')
        cropped_image.save(jpeg_path, 'JPEG')

    print(f"I finished. Your images are at {os.path.join(os.path.dirname(image_path), output_folder)}")
    # Shows the image in image viewer






# import cv2
# import numpy as np
# # Opens a image in RGB mode

# # im = Image.open("/Users/waverlywang/Documents/art_school_apps/UCLA/UCLA_Storyboard_images/UCLA_Storyboard3.jpg")

# img = cv2.imread("/Users/waverlywang/Documents/art_school_apps/UCLA/UCLA_Storyboard_images/UCLA_Storyboard3.jpg")
# array = cv2.resize(img, (960, 540))   # output is numpy array
# data = Image.fromarray(array) 
      

# #TODO: save as jpeg and try again?


# # Setting the points for cropped image
# # top = 0
# # left = 0
# # right = 3834
# # bottom = 2263


# top = 42
# left = 58
# right = 326
# bottom = 209

# # top = 333
# # left = 58
# # right = 619
# # bottom = 209

# # top = 626
# # left = 58
# # right = 910
# # bottom = 209


# # top = 43
# # left = 303
# # right = 327
# # bottom = 454

# # top = 334
# # left = 303
# # right = 619
# # bottom = 454

# # top = 625
# # left = 303
# # right = 909
# # bottom = 454




 
# # Cropped image of above dimension
# # (It will not change original image)
# im1 = data.crop((left, top, right, bottom))
 
# # Shows the image in image viewer
# im1.show()


# # This is cool but not really what I'm looking for


# # img = cv2.imread("/Users/waverlywang/Documents/art_school_apps/UCLA/UCLA_Storyboard_images/UCLA_Storyboard3.jpg")
# # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # ret,thresh = cv2.threshold(gray,50,255,0)
# # contours,hierarchy = cv2.findContours(thresh, 1, 2)
# # print("Number of contours detected:", len(contours))

# # for cnt in contours:
# #    x1,y1 = cnt[0][0]
# #    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
# #    if len(approx) == 4:
# #       x, y, w, h = cv2.boundingRect(cnt)
# #       ratio = float(w)/h
# #       if ratio >= 0.9 and ratio <= 1.1:
# #          img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
# #          cv2.putText(img, 'Square', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
# #       else:
# #          cv2.putText(img, 'Rectangle', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
# #          img = cv2.drawContours(img, [cnt], -1, (0,255,0), 3)

# # imS = cv2.resize(img, (960, 540))  
# # cv2.imshow("Shapes", imS)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()