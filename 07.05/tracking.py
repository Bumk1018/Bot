# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18540zIVZTDm8DXuUGGJ7eqPmgvjNdkfF
"""

import os
import sys
import subprocess

# 1. 필요한 패키지 설치
def install_packages():
    packages = ['ultralytics', 'deep_sort_realtime', 'opencv-python']
    for pkg in packages:
        subprocess.run([sys.executable, "-m", "pip", "install", pkg])

install_packages()

# 2. 모듈 import
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# 3. 모델 로드 (YOLOv8n은 가장 가볍고 빠름)
model = YOLO('yolov8n.pt')
tracker = DeepSort(max_age=30)

# 4. 이미지 파일 목록 수정 시간 기준 정렬
image_folder = 'images'
image_paths = sorted([
    os.path.join(image_folder, f)
    for f in os.listdir(image_folder)
    if f.lower().endswith(('.jpg', '.png'))
], key=lambda x: os.path.getmtime(x))

# 5. 출력 비디오 설정
if not image_paths:
    raise FileNotFoundError("images 폴더에 이미지가 없습니다.")

first_frame = cv2.imread(image_paths[0])
h, w = first_frame.shape[:2]
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 10, (w, h))  # fps = 10

# 6. 각 프레임 처리 및 트래킹
for path in image_paths:
    frame = cv2.imread(path)
    results = model.predict(frame, conf=0.3, verbose=False)[0]

    detections = []
    for r in results.boxes:
        x1, y1, x2, y2 = r.xyxy[0].cpu().numpy()
        conf = float(r.conf[0])
        cls = int(r.cls[0])
        detections.append(([x1, y1, x2 - x1, y2 - y1], conf, cls))

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        l, t, r, b = map(int, track.to_ltrb())
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(frame, f'ID {track_id}', (l, t - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    out.write(frame)
    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) == 27:  # ESC 키로 종료
        break

# 7. 종료 처리
out.release()
cv2.destroyAllWindows()