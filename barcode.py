from PIL import Image
import zbarlight
import requests

# Get product barcode from image using zbarlight
def get_barcode(image):

    barcode = zbarlight.scan_codes(['ean13'], image)
    while True:
        try:
            code =  str(barcode[0])[2:-1]
            return(code)
        except:
            #print("Can't find this barcode")
            break

# Get product name using the barcode
def product_from_barcode(barcode):
    url = "https://api.upcitemdb.com/prod/trial/lookup?upc=" + barcode
    r = requests.get(url)
    print("Request status: " +  str(r.status_code))
    item = r.json()

    while True:
        try:
            title = r.json()["items"][0]["title"]
            return(title)
        except:
            print("Cannot find item")
            break

def main():

    formatted_barcode = get_barcode(image)

    product_name = product_from_barcode(formatted_barcode)

    print(product_name)

if __name__ == '__main__':
    main()
