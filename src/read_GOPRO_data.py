import cv2
import os
import numpy as np
import easyocr
import csv
from tqdm import tqdm 


# Point to the installed tesseract in your system
reader = easyocr.Reader(['en'])
print(reader.device)


def extract_text(image, verbose = 0):
    # Show the original image
    if verbose:
        cv2.imshow('Original Image', image)
        cv2.waitKey(0)  # Wait until any key is pressed

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range for yellow color
    lower_yellow = np.array([20, 85, 85])
    upper_yellow = np.array([35, 225, 225])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=mask)

    if verbose:
        cv2.imshow('Filtered Image', res)
        cv2.waitKey(0)

    # Convert the image to gray scale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # Show the grayscale image
    if verbose:
        cv2.imshow('Grayscale Image', gray)
        cv2.waitKey(0)

    # Crop the image (you will need to adjust these values)
    cropped = gray[600:750, 850:1250]

    # Show the cropped image
    if verbose:
        cv2.imshow('Cropped Image', cropped)
        cv2.waitKey(0)

    # Apply thresholding
    _, thresh = cv2.threshold(cropped, 70, 85, cv2.THRESH_BINARY)

    # Invert the colors (white text on black background)
    inverted = cv2.bitwise_not(thresh)

    # Threshold the inverted image to get black text on white background
    _, final = cv2.threshold(inverted, 220, 255, cv2.THRESH_BINARY_INV)

    # Resize the image to increase resolution
    enlarged = cv2.resize(final, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Show the processed image
    if verbose:
        cv2.imshow('Processed Image', enlarged)
        cv2.waitKey(0)

    # Use EasyOCR to do OCR on the processed image
    results = reader.readtext(enlarged)

    # Extract the text from the results
    text = ' '.join([result[1] for result in results])

    if verbose:
        print(f"Text in image: {text}")
    
    # Find all numbers in the text
    # Note: Good if you only want the numbers
    #numbers = re.findall(r'\d+', text)
    
    return text

def image_metadata(filename, image):
    # Go Pro - Expected 1968 pixels high, 2624 pixels wide
    print(f"Filename: {filename}. Image size: {image.shape[0]} pixels high, {image.shape[1]} pixels wide")


with open('output/GOPRO_OCR.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Filename', 'Text'])

    # Directory containing your images
    directory = 'F:/Dropbox/Projects/011 - UofC Leak/Test/May 29/Station 2 - Energy Center/Go Pro/DCIM/'  # Update this path
    
    # Initialize a list to hold all image files
    all_images = []

    # Use os.walk() to find all .JPG files in all subdirectories
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".JPG"):
                all_images.append(os.path.join(dirpath, filename))

    # Loop over all images
    for image_path in tqdm(all_images):  # Wrap the loop with tqdm
        # Read the image
        image = cv2.imread(image_path)
        #image_metadata(image_path, image)  # Pass the full path to the metadata function

        # Extract and print text
        text = extract_text(image, verbose=0)  # Set verbose=1 to display images

        # Write the filename and text to the CSV file
        writer.writerow([image_path, text])  # Write the full path to the CSV