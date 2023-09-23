import os
import cv2
import argparse

# 把所有的图片和标签放在visem文件夹里，处理好的图片都在all文件夹里
# all文件夹自行分割
def main():
    img_path = 'VISEM0.1+SVIA+Bristol_same/images/'
    anno_path = 'VISEM0.1+SVIA+Bristol_same/labels/'
    cut_path = 'VISEM0.1+SVIA+Bristol_same/all/'
    if not os.path.exists(cut_path):
        os.makedirs(cut_path)
    imagelist = os.listdir(img_path)
    for image in imagelist:
        image_pre, ext = os.path.splitext(image)
        img_file = img_path + image
        img = cv2.imread(img_file)
        txt_file = anno_path + image_pre + '.txt'

        if not os.path.exists(txt_file):
            print(f"No label file for {img_file}. Skipping this image.")
            continue

        with open(txt_file, 'r') as f:
            lines = f.readlines()

        obj_i = 0
        for line in lines:
            obj_i += 1
            data = line.strip().split()
            cls = data[0]
            b = [float(x) for x in data[1:]]

            img_height, img_width = img.shape[:2]
            x1 = int(b[0]*img_width - b[2]*img_width/2)
            y1 = int(b[1]*img_height - b[3]*img_height/2)
            x2 = int(b[0]*img_width + b[2]*img_width/2)
            y2 = int(b[1]*img_height + b[3]*img_height/2)

            img_cut = img[y1:y2, x1:x2, :]
            path = os.path.join(cut_path, cls)
            os.makedirs(path, exist_ok=True)
            save_file = os.path.join(cut_path, cls, '{}_{:0>2d}.jpg'.format(image_pre, obj_i))
            if img_cut is None or img_cut.size == 0:
                print("Error: img_cut is empty")
            else:
                cv2.imwrite(save_file, img_cut)

            print(f"Saved image: {save_file}")


if __name__ == '__main__':
    main()
