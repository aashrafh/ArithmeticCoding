import numpy as np


def encode_image(pixels, block_size, probs_limits, float_type='float64'):
    i = 0
    block = []
    blocks = []
    for pixel in pixels:
        i += 1
        block.append(pixel)
        if i % block_size == 0:
            blocks.append(block)
            block = []

    encoded_array = []
    encoded_array_limit = {}
    encoded_number = 0
    start = 0
    end = 0
    t_start = 0
    t_end = 0
    for i in range(len(blocks)):
        start = t_start = probs_limits[blocks[i][0]][0]
        end = t_end = probs_limits[blocks[i][0]][1]
        for pixel in blocks[i]:
            t_start = start + (end-start)*probs_limits[pixel][0]
            t_end = start + (end-start)*probs_limits[pixel][1]
            start = t_start
            end = t_end
        avg = (start+end)/2
        bins = ""
        for j in range(32):
            avg *= 2
            if int(avg) == 1:
                bins += "1"
            else:
                bins += "0"
            avg -= int(avg)

        encoded_array.append(bins[::-1])
        encoded_array_limit[bins] = start, end

    # I do not need to use float type (e.g. .astype(float_type)) because I am saving the encoded "binary" not the float number itself
    encoded_array = np.array(encoded_array)
    np.save("encoded_array.npy", encoded_array)
    print("Encoding: Done!")
