import os
import re
import moviepy
from moviepy.editor import *

def vid_to_gif(path):
    videoClip = VideoFileClip(path)
    finalClip = videoClip.fx( vfx.resize, width = 280)  # resize

    base_name = os.path.basename(path)
    base_name = re.split(r"\.\s*", base_name)[0]


    gif_path = os.path.join(os.path.dirname(path), f"{base_name}"+".gif")

    finalClip.write_gif(gif_path, loop=True)