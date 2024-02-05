import os
from PIL import Image  # install by > python3 -m pip install --upgrade Pillow  # ref. https://pillow.readthedocs.io/en/latest/installation.html#basic-installation
from os import listdir
import re
from pdf2image import convert_from_path


# Name of the folder containing the files

def images_to_pdf(folder_path):
    # takes in a path to folder that holds images and converts them to pdf and 
    # puts them in directory that held folder of images

    base_name = os.path.basename(folder_path)
    base_name = re.split(r"\.\s*", base_name)[0]
    # Get a list of filenames
    #filenames = sorted(listdir(folder_path))
    filenames = listdir(folder_path)
    filenames.remove(".DS_Store")
    filenames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    print(filenames)
    images = [
        Image.open(os.path.join(folder_path, f))
        for f in filenames
    ]


    pdf_path = os.path.join(os.path.dirname(folder_path), f"{base_name}"+".pdf")
        
    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )
    print(f"I finished. Your pdf is at {pdf_path}")


 
def pdf_to_image(pdf_path):
     # takes path to pdf and bunch of images and puts them in a folder in the path
    # Store Pdf with convert_from_path function
    images = convert_from_path(pdf_path)  #converts pdf to images

    base_name = os.path.basename(pdf_path)
    base_name = re.split(r"\.\s*", base_name)[0]

    for i in range(len(images)):
  
        output_folder = base_name + "_images"
        output_path = os.path.join(os.path.dirname(pdf_path), output_folder)
        jpeg_path = os.path.join(output_path, base_name+ str(i) +'.jpg')
        if not os.path.exists(os.path.join(output_path)):
            os.makedirs(output_path)
        # Save pages as images 
        images[i].save(jpeg_path, 'JPEG')

    print(f"I finished. Your images are at {os.path.join(os.path.dirname(pdf_path), output_folder)}")