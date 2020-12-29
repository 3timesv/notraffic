from pathlib import Path
from tqdm import tqdm
import cv2
import pandas as pd
import sys
from seaborn import color_palette


classes = ['articulated_truck', 'bicycle', 'bus', 'car',
           'motorcycle', 'motorized_vehicle', 'non-motorized_vehicle',
           'pedestrian', 'pickup_truck',
           'single_unit_truck', 'work_van']


def make_color_map():

    names = sorted(set(classes))
    n = len(names)

    if n == 0:
        return {}
    cp = color_palette("Paired", n)

    cp[:] = [tuple(int(255*c) for c in rgb) for rgb in cp]

    return dict(zip(names, cp))


def plot_bboxes(txt_path, img_path):
    """plot_bboxes.

    Parameters
    ----------
    txt_path :
        txt_path
    img_path :
        img_path
    """

    txt_file = open(txt_path, "r")
    lines = txt_file.readlines()
    
    image = cv2.imread(img_path)

    color_map = make_color_map()
    for line in lines:
        txt = line.split(" ")
        data = {}
        data["obj_class"] = int(txt[0])
        data["x_center"] = float(txt[1])
        data["y_center"] = float(txt[2])
        data["width"] = float(txt[3])
        data["height"] = float(txt[4].replace("\n", ""))
        
        draw_bbox(data, image, color_map)
    show_plot(image)

def show_plot(image):
    """show_plot.

    Parameters
    ----------
    image :
        image
    """

    #cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    #cv2.resizeWindow("image", 600, 400)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_bbox(data, image, color_map, remodify = True):
    """draw_bbox.

    Parameters
    ----------
    data :
        data
    image :
        image
    remodify :
        remodify
    """
    
    if remodify:
        data = remodify_data(data, image)

    x1y1 = (data["x1"], data["y1"]) 
    x2y2 = (data["x2"], data["y2"])

    _ = cv2.rectangle(image, x1y1, 
            x2y2,
            color = color_map[ data["class_name"] ], 
            thickness = 2)

    textsize, baseline = cv2.getTextSize(data["class_name"],
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 0.4,
            thickness = 1)

    cv2.rectangle(image, x1y1, (x1y1[0] + textsize[0], x1y1[1] + textsize[1]),
            color_map[data["class_name"]], -1)

    cv2.putText(image, data["class_name"], (x1y1[0], x1y1[1] + baseline * 2),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)


def modify_data(data, image_path):
    """modify_data.

    Parameters
    ----------
    data :
        data
    image_path :
        image_path
    """

    obj_class = classes.index( data["class_name"] )
    image = cv2.imread(str(image_path))
    h, w = image.shape[:2]

    width = data["x2"] - data["x1"] 
    height = data["y2"] - data["y1"] 
    x_center = ( data["x1"] + ( width / 2 ) ) / w
    y_center = ( data["y1"] + ( height / 2 ) ) / h
    width /= w
    height /= h

    modified_data = {"x_center": x_center,
            "y_center": y_center,
            "width": width,
            "height": height,
            "obj_class": obj_class,
            "class_name": data["class_name"]}

    return modified_data


def remodify_data(data, image):
    """remodify_data.

    Parameters
    ----------
    data :
        data
    image :
        image
    """

    h, w = image.shape[:2]

    x1 = ( data["x_center"] * w ) - ( (data["width"] * w) / 2 )
    y1 = ( data["y_center"] * h ) - ( (data["height"] * h) / 2 )
    x2 = data["width"] * w + x1
    y2 = data ["height"] * h + y1

    modified_data = {"x1": int(x1),
            "y1": int(y1),
            "x2": int(x2),
            "y2": int(y2),
            "class_name": classes[ data["obj_class"]]}

    return modified_data

def write_txt(data, path):
    """write_txt.

    Parameters
    ----------
    data :
        data
    path :
        path
    """

    img_path = path/(data["id"] + ".jpg")
    txt_path = path/(data["id"] + ".txt")

    d = modify_data(data, img_path)

    txt_file = open(str(txt_path), "a+")
    
    txt_file.write("{} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(d["obj_class"],
        d["x_center"],
        d["y_center"],
        d["width"],
        d["height"]) )
    txt_file.close()

def main():
    """Main Function
    """

    csv_path = sys.argv[1]
    df = pd.read_csv(csv_path, names = ["id", "class_name", "x1", "y1", "x2", "y2"],
            dtype = {"id": str })

    path = Path( sys.argv[2] )
    
    for i in tqdm(range(len(df))):
        row = df.iloc[i]
        write_txt(row, path)

if __name__ == "__main__":
    main()
