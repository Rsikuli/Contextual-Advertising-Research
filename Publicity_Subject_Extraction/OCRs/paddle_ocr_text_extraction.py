from paddleocr import PaddleOCR  #type: ignore
import cv2  #type: ignore

# Initialize PaddleOCR
ocr_model = PaddleOCR(lang='fr', use_dilation=True)  # 'lang=fr' for French

def paddleOCR_extract(IMAGE_PATH):
    """
    Extracts text from an image using the PaddleOCR model.
    Args:
        IMAGE_PATH (str): The file path to the image from which text is to be extracted.
    Returns:
        str: The extracted text from the image.
    Raises:
        FileNotFoundError: If the image at the specified path cannot be loaded.
    """
    # Image Threshold
    img_bgr = cv2.imread(IMAGE_PATH)
    
    # Check if the image was loaded successfully
    if img_bgr is None:
        raise FileNotFoundError(f"Error: Unable to load image at {IMAGE_PATH}")
    
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # Text Extraction
    result = ocr_model.ocr(img_rgb, cls=False)  # cls=False skips text orientation classification
    text = " ".join([line[1][0] for line in result[0]])
    return text
