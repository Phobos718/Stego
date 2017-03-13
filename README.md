# Stego
Steganography tool concealing a payload file (txt) into an image (lossless formats). It does this by manipulating the RGB channel vaules to represent binary bits. The original image is used as a key to extract data. 
Work in progress

Concealment:
- Converting payload text file into binary (each ascii character is an octet)
- Iterating over the image pixel by pixel and incrementing RGB values by 1 if the corresponding bit in the text file is a 1. (3 bits stored   per pixel)
- After the last bits, it increments by 3 to mark the end of the data.

Extraction:
- Iterates over the original image (which in this case is used as a key) and the image containing data.
- Subtracts RGB values of original image from the one containing data.
- Converts binary back to ascii text and saves it to result.txt
