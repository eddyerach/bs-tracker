from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np
from deep_sort_pytorch.deep_sort import build_tracker
from deep_sort_pytorch.utils.draw import draw_boxes
from deep_sort_pytorch.utils.parser import get_config


parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='test.mp4')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='KNN')
args = parser.parse_args()
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
if args.algo == 'CNT':
    backSub = cv.bgsegm.BackgroundSubtractorCNT()
if args.algo == 'LSBP':
    backSub = cv.bgsegm.createBackgroundSubtractorLSBP()
else:
    backSub = cv.createBackgroundSubtractorKNN()
    backSub.setDetectShadows(True) #Set shadows detection
    backSub.setHistory(50) #Sets the number of last frames that affect the background mode
    backSub.setShadowThreshold(0.5)
capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
if not capture.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)

cfg = get_config()
cfg.merge_from_file("./deep_sort_pytorch/configs/yolov3.yaml")
cfg.merge_from_file("./deep_sort_pytorch/configs/deep_sort.yaml")
deepsort_person = build_tracker(cfg, use_cuda=1)

while True:
    ret, frame = capture.read()
    if frame is None:
        break
    
    fgMask = backSub.apply(frame)
    
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(15,15))

    fgMask = cv.morphologyEx(fgMask, cv.MORPH_CLOSE, kernel)# 
    cnts = cv.findContours(fgMask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    #cv.imshow('Frame', frame)
    #cv.imshow('FG Mask', fgMask)

    for cnt in cnts:
        if cv.contourArea(cnt) > 15000:
            x, y, w, h = cv.boundingRect(cnt)
            bbox_xywh = np.array([[x+(w/2),y+(h/2),w,h]])
            print(bbox_xywh)
            cv.rectangle(fgMask, (x,y), (x+w,y+h), (255, 0, 0) , 5)
            outputs_person = deepsort_person.update(
                            bbox_xywh, [0.5], frame)
            print(outputs_person)
            if len(outputs_person) > 0:
                bbox_xyxy_person = outputs_person[:, :4]
                identities_person = outputs_person[:, -1]
            
                frame = draw_boxes(
                    frame, bbox_xyxy_person, identities_person)


    cv.imshow('cnts', frame)
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break