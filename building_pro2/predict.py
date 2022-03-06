import numpy as np
import torch
import cv2 as cv

COLORS = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 127, 255), (0, 255, 0), (0, 0, 255),
(127, 0, 255), (127, 255, 127), (127, 127, 255), (170, 170, 170), (108, 172, 255), (0, 102, 102), (204, 204, 255)]
model = torch.hub.load('ultralytics/yolov5', 'custom', path='static/best.pt', force_reload=True)

# print(len(COLORS))
def predict_image(img):
    
    detections = model(img)
    results = detections.pandas().xyxy[0].to_dict(orient='records')
    for result in results:
        name = result['name']
        id = result['class']
        confidence = result['confidence']
        xmin = int(result['xmin'])
        ymin = int(result['ymin'])
        xmax = int(result['xmax'])
        ymax = int(result['ymax'])
        cv.rectangle(img, (xmin, ymin+2), (xmax, ymax), COLORS[id], 1)
        text = '{} {}%'.format(name, int(confidence * 100))
        cv.putText(img, text, (xmin, ymin), cv.FONT_ITALIC, 0.5, COLORS[id], 1)
        torch.cuda.empty_cache()
    return img