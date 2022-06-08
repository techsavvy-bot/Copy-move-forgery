import os
import cv2
from sklearn.cluster import DBSCAN
import numpy as np

from myapp.settings import BASE_DIR


def siftDetector(image):
    sift = cv2.SIFT_create()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    key_points, descriptors = sift.detectAndCompute(gray, None)
    return key_points, descriptors


def locateForgery(image, key_points, descriptors, eps=40, min_sample=2):
    clusters = DBSCAN(eps=eps, min_samples=min_sample).fit(
        descriptors)  # Find clusters using DBSCAN
    # Identify the number of clusters formed
    size = np.unique(clusters.labels_).shape[0]-1
    # Create another image for marking forgery
    forgery = image.copy()
    if (size == 0) and (np.unique(clusters.labels_)[0] == -1):
        print('No Forgery Found!!')
        # If no clusters are found return
        return None
    if size == 0:
        size = 1
    # List of list to store points belonging to the same cluster
    cluster_list = [[] for i in range(size)]
    for idx in range(len(key_points)):
        if clusters.labels_[idx] != -1:
            cluster_list[clusters.labels_[idx]].append(
                (int(key_points[idx].pt[0]), int(key_points[idx].pt[1])))
    for points in cluster_list:
        if len(points) > 1:
            for idx1 in range(1, len(points)):
                # Draw line between the points in a same cluster
                cv2.line(forgery, points[0], points[idx1], (255, 0, 0), 5)
    return forgery


def twoImageForgery():
    image1 = cv2.imread(os.path.join(f'{BASE_DIR}/media/', 'image1.png'))
    image2 = cv2.imread(os.path.join(f'{BASE_DIR}/media/', 'image2.png'))
    gray1 = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
    arr1 = np.array(gray1)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)
    arr2 = np.array(gray2)
    # print(arr1==arr2)
    normalarr=(arr1==arr2)
    newarr = np.zeros((arr1.shape[0], arr1.shape[1]))
    count = 0
    print(type(newarr))
    for i in range(0, newarr.shape[0]):
        for j in range(0, newarr.shape[1]):
            if normalarr[i][j] == True:
                count = count + 1
                newarr[i][j]=255
            # else:
            #     newarr[i][j]=0
    print(newarr)
    if count != 0:
        return 1
    else:
        return 0    

    cv2.imwrite("static/output2.png",newarr)
    # print(np.array_equal(arr1,arr2))
    # print(arr1.shape[1])

    # key_points, descriptors = siftDetector(image1)
    # img_1 = cv2.drawKeypoints(gray1,key_points,image1)
    # cv2.imwrite("output.jpg",img_1)

    # im2 = locateForgery(image1, key_points, descriptors)
    # print(im2)
    # if im2 is not None:
        # cv2.imwrite("../static/output.jpg", im2)
