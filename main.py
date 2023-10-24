import numpy as np
from PIL import Image
import cv2


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

    return magnitude


def largest_object_box(image_array):

    # Set the threshold for the image
    _, threshold = cv2.threshold(image_array, 115, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area in descending order
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Check if there is at least 1 contour to check the image is actually displaying something
    if len(sorted_contours) < 1:
        raise ValueError("There are fewer than 1 object in the image.")

    # Get the largest contour as this is likely to contain the box
    largest_contour = sorted_contours[0]

    # Get the bounding box
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Draw the bounding box on a copy of the image and display it
    boxed_image = image_array.copy()
    cv2.rectangle(boxed_image, (x, y), (x + w, y + h), (255,), 2)
    cv2.imshow('Largest Object Bounding Box', boxed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return x, y, w, h


edge_detected_image = sobel_edge_detection("Images/img.png")
# Parse the image generated in the edge_detected_image function through to identify the box
boundary_box = largest_object_box(edge_detected_image)
print(f"Bounding Box: {boundary_box}")

