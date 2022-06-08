import cv2
import numpy as np
import os
from myapp.settings import BASE_DIR

def forgery():
    quantization = 16
    tsimilarity = 5  
    tdistance = 20  
    vector_limit = 20 
    block_counter = 0
    block_size = 8

    image = cv2.imread(os.path.join(f'{BASE_DIR}/media/', 'temp.png'))

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    temp = []
    arr = np.array(gray)

    prediction_mask = np.zeros((arr.shape[0], arr.shape[1]))
    column = arr.shape[1] - block_size
    row = arr.shape[0] - block_size
    dcts = np.empty((((column+1)*(row+1)), quantization+2))

    # ----------------------------------------------------------------------------------------

    print("scanning & dct starting...")

    for i in range(0, row):
        for j in range(0, column):

            blocks = arr[i:i+block_size, j:j+block_size]
            imf = np.float32(blocks) / 255.0 
            dst = cv2.dct(imf)  
            blocks = np.uint8(np.float32(dst) * 255.0)  
           
            solution = [[] for k in range(block_size + block_size - 1)]
            for k in range(block_size):
                for l in range(block_size):
                    sum = k + l
                    if (sum % 2 == 0):
                        
                        solution[sum].insert(0, blocks[k][l])
                    else:
                        
                        solution[sum].append(blocks[k][l])

            for item in range(0, (block_size*2-1)):
                temp += solution[item]

            temp = np.asarray(temp, dtype=np.float)
            temp = np.array(temp[:16])
            temp = np.floor(temp/quantization)
            temp = np.append(temp, [i, j])

            np.copyto(dcts[block_counter], temp)

            block_counter += 1
            temp = []

    print("scanning & dct over!")

    dcts = dcts[~np.all(dcts == 0, axis=1)]
    dcts = dcts[np.lexsort(np.rot90(dcts))]


    print("euclidean operations starting...")

    sim_array = []
    for i in range(0, block_counter):
        if i <= block_counter-10:
            for j in range(i+1, i+10):
                pixelsim = np.linalg.norm(dcts[i][:16]-dcts[j][:16])
                pointdis = np.linalg.norm(dcts[i][-2:]-dcts[j][-2:])
                if pixelsim <= tsimilarity and pointdis >= tdistance:
                    sim_array.append([dcts[i][16], dcts[i][17], dcts[j][16], dcts[j]
                                     [17], dcts[i][16]-dcts[j][16], dcts[i][17]-dcts[j][17]])
        else:
            for j in range(i+1, block_counter):
                pixelsim = np.linalg.norm(dcts[i][:16]-dcts[j][:16])
                pointdis = np.linalg.norm(dcts[i][-2:]-dcts[j][-2:])
                if pixelsim <= tsimilarity and pointdis >= tdistance:
                    sim_array.append([dcts[i][16], dcts[i][17], dcts[j][16], dcts[j]
                                     [17], dcts[i][16]-dcts[j][16], dcts[i][17]-dcts[j][17]])

    print("euclidean operations over!")

    # ----------------------------------------------------------------------------------------

    print("elimination starting...")

    sim_array = np.array(sim_array)
    delete_vec = []
    vector_counter = 0
    for i in range(0, sim_array.shape[0]):
        for j in range(1, sim_array.shape[0]):
            if sim_array[i][4] == sim_array[j][4] and sim_array[i][5] == sim_array[j][5]:
                vector_counter += 1
        if vector_counter < vector_limit:
            delete_vec.append(sim_array[i])
        vector_counter = 0

    delete_vec = np.array(delete_vec)
    delete_vec = delete_vec[~np.all(delete_vec == 0, axis=1)]
    delete_vec = delete_vec[np.lexsort(np.rot90(delete_vec))]

    for item in delete_vec:
        indexes = np.where(sim_array == item)
        unique, counts = np.unique(indexes[0], return_counts=True)
        for i in range(0, unique.shape[0]):
            if counts[i] == 6:
                sim_array = np.delete(sim_array, unique[i], axis=0)

    print("elimination over!")

    # ----------------------------------------------------------------------------------------

    print("painting starting...")

    for i in range(0, sim_array.shape[0]):
        index1 = int(sim_array[i][0])
        index2 = int(sim_array[i][1])
        index3 = int(sim_array[i][2])
        index4 = int(sim_array[i][3])
        for j in range(0, 7):
            for k in range(0, 7):
                prediction_mask[index1+j][index2+k] = 255
                prediction_mask[index3+j][index4+k] = 255

    print("painting over!")

    count = 0
    for i in range(0, prediction_mask.shape[0]):
        for j in range(0, prediction_mask.shape[1]):
            if prediction_mask[i][j] == 255.0:
                count = count + 1

    cv2.imwrite("static/output.png", prediction_mask)
    print(prediction_mask)

    if count >= 2000:
        return True
    else:
        return False



