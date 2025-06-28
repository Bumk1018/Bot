import os
import random
from PIL import Image
import torch
import urllib.request

# 모델 다운로드 (필요시)
if not os.path.exists('yolov5s.pt'):
    url = 'https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt'
    urllib.request.urlretrieve(url, 'yolov5s.pt')

# 장치 설정
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# 모델 로드
model = torch.hub.load('yolov5', 'custom', path='yolov5s.pt', source='local', device=device)

# 테스트 이미지 중 하나 선택
test_dir = 'test_images'
image_files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if not image_files:
    raise Exception("test_images 폴더에 이미지가 없습니다.")

random_img = random.choice(image_files)
image_path = os.path.join(test_dir, random_img)
print(f"선택된 이미지: {image_path}")

# 이미지 열기 및 탐지
img = Image.open(image_path)
results = model(img)
results.print()
results.show()
results.save()
