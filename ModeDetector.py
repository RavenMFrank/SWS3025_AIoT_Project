import torch
import numpy as np
from torch import Tensor
from torchvision import transforms
import torch.nn.functional as F
from pathlib import Path
import arrow
from PIL import Image

default_transform = transforms.Compose([transforms.Resize(256),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            mean=[0.485, 0.456, 0.406],
                                            std=[0.229, 0.224, 0.225])
                                        ])


class ModeDetector:
    def __init__(self, modeMap=None, modelPath: str = "ml/model.pth", data_path: str = "ml/images",
                 transform=default_transform):
        if modeMap is None:
            modeMap = ["computer", "none", "reading"]
        self.modeMap = modeMap
        self.model = torch.load(modelPath)
        self.transform = transform
        self.data_path = data_path
        self.dataset = None

    def detect(self, img_path, numerical_output=False) -> Tensor | str | list[str]:
        img = Image.open(img_path)
        input_img = self.transform(img).unsqueeze(0)
        pred_softmax = F.softmax(self.model(input_img), dim=1)
        if numerical_output:
            return pred_softmax
        else:
            return self.modeMap[pred_softmax.argmax()]

    def detect_batch(self, numerical_output=False):
        pred = []
        for item in Path(self.data_path).glob('*'):
            if item.is_file():
                pred.append(self.detect(item, True).argmax())
        if numerical_output:
            return pred
        else:
            return self.modeMap[np.bincount(pred).argmax()]

    def clear(self):
        self.dataset = None
        max_minutes = 10
        # 获取当前时间
        now = arrow.now()
        # 遍历文件夹中的所有文件
        for item in Path(self.data_path).glob('*'):
            if item.is_file():  # 如果是文件（不是子文件夹）
                item_time = arrow.get(item.stat().st_mtime)
                # 如果文件的修改时间小于当前时间减去最大时间
                if item_time < now.shift(minutes=-max_minutes):
                    item.unlink()
