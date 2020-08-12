import cv2
sample = cv2.imread('resource/sample.png')
sample = cv2.resize(sample, dsize=(1396//2, 784//2), interpolation=cv2.INTER_AREA)

sample = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)

# cv2.imshow('gray', gray)


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
