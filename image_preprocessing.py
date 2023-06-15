
from skimage import io, color
import numpy as np

matrix = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ])

def preprocess_image(image):
    gray_image = to8BitGrayscale256(image)
    gray_image = matrix_filter(gray_image, matrix)
    return gray_image

def to8BitGrayscale256(img): 
    gray_image = color.rgb2gray(img)
    scaled_image = (gray_image * 255).astype(np.uint8)
    return scaled_image

def to1Bit(img, threshold): 
    img_array = np.array(img)   
    bin_img = np.where(img_array > threshold, 1, 0)
    return bin_img

def matrix_filter(in_image, filter, offset=1, edge='none'):
    if len(filter.shape) != 2:
        print("Filtermatrix muss eine 2D-Matrix sein")
        return False
    if filter.shape[0] != filter.shape[1]:
        print("Filtermatrix muss quadratisch sein")
        return False
    if filter.shape[0] % 2 == 0:
        print("Die Seitenlänge der Filtermatrix muss ungerade sein")
        return False
    if np.sum(filter) == 0:
        print("Filter Summe darf nicht 0 sein.")
        return False

    N, M, = in_image.shape
    s = 1.0/np.sum(filter)

    K = int(len(filter[0])/2)
    L = int(len(filter)/2)

    new_img = np.zeros((int((N-K*2)/offset+1), int((M-K*2)/offset+1)))
    u_start = K
    v_start = L
    v_range_stop = N-L
    u_range_stop = M-K
    
    if edge == "continue":
        v_start = 0
        u_start = 0
        v_range_stop = N-1
        u_range_stop = M-1

    for v in range(v_start, v_range_stop, offset):
        for u in range(u_start, u_range_stop, offset):
            sum = 0
            for j in range(-L, L+1):
                for i in range(-K, K+1):
                    if edge != 'none' and (v+j < 0 or v+j >= N or u+i < 0 or u+i >= M):
                        tmp_v = v+j
                        tmp_u = u+i
                        if (v+j < 0 or v+j >= N):
                            tmp_v = v
                        if (u+i < 0 or u+i >= M):
                            tmp_u = u
                        p = in_image[tmp_v, tmp_u]
                        if edge == 'min':
                            p = 0
                        if edge == 'max':
                            p = 255
                    else:
                        p = in_image[v+j, u+i] 
                    c = filter[j][i]
                    sum = sum + c * p
            q = int(np.round(s*sum))
            #edge
            if edge == 'min':
               q = min
            if edge == 'max':
                q = max
            new_img[int(v/offset)-1,int(u/offset)-1] = q
    return new_img
