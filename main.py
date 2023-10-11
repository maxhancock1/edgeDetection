import numpy as np
from PIL import Image


def sobel_edge_detection(image_path):
    # Load the image and convert to grayscale and then converts the image into an array ready for convolution
    image = Image.open(image_path).convert('L')
    image = np.array(image)

    # Define Sobel filters, np used for matrix maths
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])

    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]])
    # Calculate image dimensions for reference
    width, height = image.shape

    # Initialise matrices for gradients
    gx = np.zeros((width, height))
    gy = np.zeros((width, height))
    magnitude = np.zeros((width, height))

    # Apply convolution, multiplying each vertical and horizontal kernel until the image has been filled
    for i in range(1, width-1):
        for j in range(1, height-1):
            gx[i, j] = np.sum(sobel_x * image[i-1:i+2, j-1:j+2])
            gy[i, j] = np.sum(sobel_y * image[i-1:i+2, j-1:j+2])
            magnitude[i, j] = np.sqrt(gx[i, j]**2 + gy[i, j]**2)

    # Normalise the magnitude values to fit the range [0, 255] as 255 is the max in 8-bit images
    magnitude = (magnitude / np.max(magnitude) * 255).astype(np.uint8)

    # Return the edge image
    return Image.fromarray(magnitude)


# Test the function
output_image = sobel_edge_detection("cartoon.png")
output_image.show()

