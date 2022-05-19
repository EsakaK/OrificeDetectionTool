import cv2
import torch
import torch.nn.functional as F
import numpy as np
import cv2
from lib.Network_Res2Net_GRA_NCD import Network
from mask2img import generate_mask_img
from PIL import Image
import torchvision.transforms as transforms

class Detector(object):
    def __init__(self):
        self.img_size = 352
        self.model = Network(imagenet_pretrained=False)
        self.model.load_state_dict(torch.load('./snapshots/Net_epoch_150.pth'))
        self.model.cuda()
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((self.img_size, self.img_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    def load_data(self,rgb_image):
        image = Image.fromarray(rgb_image)
        image = self.transform(image).unsqueeze(0)
        return image,np.array(rgb_image)

    def predict(self,image,shape):
        image = image.cuda()
        res5, res4, res3, res2 = self.model(image)
        res = res2
        res = F.upsample(res, size=shape[:-1], mode='bilinear', align_corners=False)
        res = res.sigmoid().data.cpu().numpy().squeeze()
        res = (res - res.min()) / (res.max() - res.min() + 1e-8)
        return res

    def mask2img(self,res,rgb_image):
        res = res*255
        ret, thresh = cv2.threshold(res, 50, 255, 0)
        mask_img = generate_mask_img(thresh)
        img_with_with_mask = mask_img*0.5  + rgb_image
        img_with_with_mask = img_with_with_mask.astype(np.uint8)
        return img_with_with_mask

    def write_frame(self,frame):
        image, rgb_image = self.load_data(frame)
        res = self.predict(image,rgb_image.shape)
        img_with_mask = self.mask2img(res,rgb_image)
        return img_with_mask

    def video_detecing(self):
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        while True:
            flag, frame = cap.read()
            frame = cv2.flip(frame,1)
            if not flag:
                break
            frame_detected = self.write_frame(frame)
            cv2.imshow('orifice',frame_detected)
            if ord('q') == cv2.waitKey(30):
                break
        cv2.destroyAllWindows()
        cap.release()

if __name__ == '__main__':
    V = Detector()
    V.video_detecing()
