
from barcode import Code128
from barcode.writer import ImageWriter


def generate_barcode(data, filename):

    barcode = Code128(str(data), writer=ImageWriter())
    barcode.save(filename)
    import cv2

    image = cv2.imread(f"{filename}.png")
        # y: top → bottom
    cropped = image[100:, ]
    cv2.imwrite(f"{filename}.png",cropped)