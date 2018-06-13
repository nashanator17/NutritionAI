import cv2
import sys
import pytesseract

if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		print('Usage: python ocr_simple.py image.jpg')
		sys.exit(1)

	imPath = sys.argv[1]

	config = ('-l eng --oem 1 --psm 3')

	im = cv2.imread(imPath, cv2.IMREAD_COLOR)
	text = pytesseract.image_to_string(im, config=config)
	print(text)


