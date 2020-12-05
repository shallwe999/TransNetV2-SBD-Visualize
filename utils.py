import cv2
from PIL import Image, ImageTk


def print_tk_image(widget, frame, width, height, pos_x=0, pos_y=0):
    cv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    pil_img = Image.fromarray(cv_img).resize((width, height))  # 将图像转换成Image对象
    tk_img = ImageTk.PhotoImage(image=pil_img)
    widget.create_image(pos_x, pos_y, anchor='nw', image=tk_img)
    widget.update_idletasks()
    widget.update()
    return tk_img

def read_scenes(file_name, split_char=" "):
    scenes = []
    for line in open(file_name, "r"):
        data = line.strip("\n").split(split_char)
        scenes.append([int(data[0]), int(data[1])])
    return scenes

def read_predictions(file_name, split_char=" "):
    preds = []
    for line in open(file_name, "r"):
        data = line.strip("\n").split(split_char)
        preds.append([float(data[0]), float(data[1])])
    return preds


if __name__ == '__main__':
    read_scenes("/home/shallwe/Desktop/bbc_01_clip.mp4.scenes.txt")
    read_predictions("/home/shallwe/Desktop/bbc_01_clip.mp4.predictions.txt")
