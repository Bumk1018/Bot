06.28

07.05
도로 영상(이미지의 연속)을 트래킹하는 알고리즘 오픈소스(YOLOv8과 Deep SORT)를 이용하여 구성
파이썬 3.10 버전 사용

* YOLOv8
- 이미지에서 사람, 차량, 신호등 등 객체의 위치와 클래스(종류)를 탐지
- bounding box, confidence score, class id를 출력
- 시간 속도에 최적화

* Deep SORT
- YOLO로 탐지한 객체들을 시간 순으로 추적
- 각 객체에 고유한 ID를 부여하여, 같은 사람이 어디로 이동했는지 추적
- Kalman Filter + Hungarian 알고리즘 + ReID 사용

* 흐름
1. images/ 폴더의 연속 이미지를 한 장씩 불러옴
2. YOLOv8으로 각 이미지에서 객체(예: 사람, 차)를 탐지함
3. 탐지된 객체들을 Deep SORT로 트래킹함 (ID 유지)
4. 프레임 위에 박스와 ID를 시각화함
5. 최종 결과를 output.mp4로 저장


