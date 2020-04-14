import cv2
import encode
import decode
import numpy as np
from collections import Counter

img_path = input("Enter image path: ")
img = cv2.imread(img_path)
block_size = int(input("Enter block size: "))
float_type = input("Enter float type (e.g. 'float16'): ")
n = img.shape[0]
m = img.shape[1]
print("shape of the image: (i.e. ex1.jpeg)")
print(img.shape)
# jsut to be sure that is the image is a grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pixels = np.array(gray.flatten())
# append zeros to be divisible by the block_size
additional_pixels = 0
while pixels.shape[0] % block_size != 0:
    pixels = np.append(pixels, 0)
    additional_pixels += 1

length = pixels.shape[0]
freq = Counter(pixels)
probs = {}
for key in freq.keys():
    probs[key] = freq[key]/length

start = 0
probs_limits = {}
for key in probs.keys():
    probs_limits[key] = start, start+probs[key]
    start += probs[key]

np.save("probabilities.npy", probs_limits)
print("Processing input and calculating probabilities: Done!")
encode.encode_image(pixels, block_size, probs_limits, float_type)
# additonal pixels is zeros to make the array divisible by block_size so I need to handle it in decoding also
decode.decode_image("encoded_array", n, m, block_size,
                    probs_limits, additional_pixels)
