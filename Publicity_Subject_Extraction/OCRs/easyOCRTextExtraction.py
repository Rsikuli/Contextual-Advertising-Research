import cv2
import easyocr #type : ignore

reader = easyocr.Reader(['fr', 'en'])

def easyOCR_extract(IMAGE_PATH, ):

    #Image Threshold
    img_bgr = cv2.imread(IMAGE_PATH)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # Text Extraction
    result = reader.readtext(img_rgb, detail = 0, paragraph=True)
    result = " ".join(result)
    return result
 