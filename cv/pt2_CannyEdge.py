# -*- coding: utf-8 -*- 
# Threshhold에 따른 Canny 변환 정도의 차이

import cv2
sample = cv2.imread('cv/insung.jpeg') #Local 절대경로


# Threshold가 낮아지냐 높아지냐가 중요한것같음 결국.
# Threshold가 낮으면 죄다 선으로 변해버림.
# Threshold가 높아야 좀 선같은 놈들만 선으로 변한다.

# High&Low Threshold 동시에 올리기
for i in range(0, 401, 50):
    canny_sample = cv2.Canny(sample, i, 50 + i)
    name = 'High&Low increase ' + str(i) + '~' + str(50 + i)

    cv2.imshow(name, sample)
    cv2.waitKey(300)
    cv2.imshow(name, canny_sample)
    cv2.waitKey(0) 

# High&Low Threshold 범위 늘리기
for i in range(0, 201, 50):
    canny_sample = cv2.Canny(sample, 200 - i, 200 + i)
    name = 'High&Low interval increase ' + str(200 - i) + '~' + str(200 + i)

    cv2.imshow(name, sample)
    cv2.waitKey(300)
    cv2.imshow(name, canny_sample)
    cv2.waitKey(0) 


# High Threshold가 낮아지는 경우 => 어쨌든 낮아지는거니까 선이 많아짐
for i in range(0, 301 ,50):
    canny_sample = cv2.Canny(sample, 0, 300 - i)
    name = 'High decrease ' + str(0) + '~' + str(300 - i)

    cv2.imshow(name, sample)
    cv2.waitKey(300)
    cv2.imshow(name, canny_sample)
    cv2.waitKey(0) 


# Low Threshold가 높아지는 경우 => 어쨌든 높아지는 거니까 선이 적어짐
for i in range(0, 301, 50):
    canny_sample = cv2.Canny(sample, i, 300)
    name = 'Low increase ' + str(i) + '~' + str(300)

    cv2.imshow(name, sample)
    cv2.waitKey(300)
    cv2.imshow(name, canny_sample)
    cv2.waitKey(0) 


# 이렇게 네 경우에 대해 테스트 하면 가장 적당한게 보이는 것같음. 셋 중 하나 골라서 그거 베이스로 조정하면 될 듯.

# 최종적으로 할거 이미지를 canny => 선으로 변환, hough => 선의 함수 구하기, 원그리는것처럼 해서 선 칠하기.
