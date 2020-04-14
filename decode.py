import cv2
import numpy as np


def decode_image(encoded_array_name, n, m, block_size, probs_limits, additional_pixels):
    encoded_array = np.load(encoded_array_name+".npy")
    decoded_array = []
    length = encoded_array.shape[0]
    for i in range(length):
        start = t_start = 0
        end = t_end = 1
        encoded_number = encoded_array[i]
        block = 0
        for j in range(32):
            if encoded_number[31-j] == "1":
                block += pow(2, -(j+1))
        for j in range(block_size):
            t_key = block
            if t_start != t_end:
                t_key = (block-t_start)/(t_end-t_start)

            # t_key = round(t_key, )

            prob = 0
            for key in probs_limits.keys():
                # print("K          E             YS")
                # print(t_key)
                # print(probs_limits[key][0])
                # print(probs_limits[key][1])
                if (t_key >= probs_limits[key][0]) and (t_key < probs_limits[key][1]):
                    # print("new key")
                    # print(key)
                    prob = key
                    break
            # print(prob)
            decoded_array.append(prob)
            t_start = start + (end-start)*probs_limits[prob][0]
            t_end = start + (end-start)*probs_limits[prob][1]
            start = t_start
            end = t_end
    while additional_pixels != 0:
        decoded_array.remove(0)
        additional_pixels -= 1

    res = np.array(decoded_array).reshape(n, m)
    cv2.imwrite('result.jpg', res)
    print("Decoding: Done!")
    cv2.imshow('result.jpg', res)
    cv2.waitKey(0)  # waits until a key is pressed
    cv2.destroyAllWindows()  # destroys the window showing image
