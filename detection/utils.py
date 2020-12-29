import shutil
import os

def move_files(src, dest):
    """Move all files from src to dest

    Parameters
    ----------
    src : str
        Source directory 
    dest : str
        Destination directory 
    """
    if not os.path.exists(dest):
        print(dest + " not exist." + "Creating " + dest)
        os.mkdir(dest)

    for f in os.listdir(src):
        shutil.move( os.path.join(src, f), os.path.join(dest, f) )


def gen_txt(txt_path, ip_dir):
    """Generate text files for yolo. (e.g train.txt or test.txt)

    Parameters
    ----------
    txt_path : str
        Text file path
    ip_dir : str
        Directory to get images from
    """
    txt = open(txt_path, "a+")
    
    for f in os.listdir(ip_dir):
        if ".jpg" in f:
            txt.write( os.path.join(ip_dir, f) + "\n" )

    txt.close()

