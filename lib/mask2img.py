import cv2
import os
from PIL import Image
import matplotlib.image as mpimg
import numpy as np

def union_image_mask(image_path, mask_path):
    # 读取原图
    image = cv2.imread(image_path)

    # 读取分割mask，这里本数据集中是白色背景黑色mask
    mask_3d = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    ret, thresh = cv2.threshold(mask_3d, 20, 255, 0)

    mask_img = generate_mask_img(thresh)

    img_with_with_mask = mask_img*0.5 + image
    # 保存图像
    file_name = os.path.split(image_path)[-1]
    cv2.imwrite("./Image_Results/"+file_name, img_with_with_mask)

def generate_mask_img(mask):
    mask_img = np.zeros((mask.shape[0],mask.shape[1],3),dtype=np.uint8)
    mask_img[mask==255] = (200,0,0)
    return mask_img


def all_mask(images_path,masks_path):
    for image_name_with_et in os.listdir(images_path):
        img_name = image_name_with_et[:-4]
        img_path = os.path.join(images_path,img_name+'.jpg')
        mask_path = os.path.join(masks_path,img_name+'.png')
        union_image_mask(img_path,mask_path)


if __name__ == '__main__':
    all_mask(r'E:\dataset\C_teeth_v2\val\Imgs',r'E:\Git_repos\SINet-V2\res')