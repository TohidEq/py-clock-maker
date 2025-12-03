from PIL import Image, ImageDraw
from IPython.display import display
import math
import random
import glob, os

from datetime import datetime

from draw_frame import draw_frame
from draw_pointer import draw_pointer

from plyer import notification

def export_frame(configs_dic, base_dir="./clockimgs/", frame_dir="frames/" ):
    #          ./clockimgs/frames/
    full_dir = os.path.join(base_dir , frame_dir)
    os.makedirs(full_dir, exist_ok=True) # create path if not exists

    start = datetime(2000, 1, 1)
    now = datetime.now()
    delta = now - start

    file_name = str(delta.total_seconds()) + "-" + str(random.randint(1000, 9000)) + ".png"

    img = draw_frame(configs_dic)
    img.save(os.path.join(full_dir + file_name))

    notification.notify(
        title="Frame exported at:",
        message=os.path.join(full_dir + file_name),
        timeout=10
    )




def export_pointer(configs_dic,hms="h",base_dir="./clockimgs/", pointer_dir="hms/", save_dir="h/"):
    #       "./clockimgs/hms/h/"
    full_dir = os.path.join(base_dir ,pointer_dir , save_dir)
    os.makedirs(full_dir, exist_ok=True) # create path if not exists

    # REMOVE every png with formats like:
    #           >> h-0.png m-1.png s-2.png
    c = 0
    for file_path in glob.glob(os.path.join(full_dir, f"{hms}-*.png")):

        if os.path.isfile(file_path):
            os.remove(file_path)
            c += 1
            print(f"Deleted: {file_path}")
    if c>0:
        notification.notify(
            title=f"{c} images delete at:",
            message=full_dir,
            timeout=10
        )


    for i in range(0,60+1):
      file_name = hms+"-"+str(i)+".png"
      img = draw_pointer(i,configs_dic)
      img.save(os.path.join(full_dir + file_name))


    notification.notify(
        title=f"{hms}-Pointers exported at:",
        message=os.path.join(full_dir + file_name),
        timeout=10
    )




