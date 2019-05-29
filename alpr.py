from openalpr import Alpr
from argparse import ArgumentParser
import locale
locale.setlocale(locale.LC_ALL, 'C')
import cv2
"""
parser = ArgumentParser(description='OpenALPR Python Test Program')
parser.add_argument("-c", "--country", dest="country", action="store", default=b"us",
                  help="License plate Country" )
parser.add_argument("--config", dest="config", action="store", default=b"/etc/openalpr/openalpr.conf",
                  help="Path to openalpr.conf config file" )
parser.add_argument("--runtime_data", dest="runtime_data", action="store", default=b"/usr/share/openalpr/runtime_data",
                  help="Path to OpenALPR runtime_data directory" )
parser.add_argument('plate_image', help='License plate image file')
options = parser.parse_args()
"""


def getPlate(img):
    alpr = None
    plates = []
    try:
        country = b"us"
        config = b"/etc/openalpr/openalpr.conf"
        runtime_data =b"/usr/share/openalpr/runtime_data"
        alpr = Alpr(country, config,runtime_data)
        #print("trying alpr")
        if not alpr.is_loaded():
            print("Error loading OpenALPR")
        else:
            #print("Using OpenALPR " + alpr.get_version())

            alpr.set_top_n(7)
            alpr.set_default_region("wa")
            alpr.set_detect_region(False)
            success, encoded_image = cv2.imencode('.jpg', img)
            jpeg_bytes = encoded_image.tobytes()#open(options.plate_image, "rb").read()
            #print("jpeg bytes",jpeg_bytes)
            results = alpr.recognize_array(jpeg_bytes)

            # Uncomment to see the full results structure
            #import pprint
            #pprint.pprint(results)

            #print("Image size: %dx%d" %(results['img_width'], results['img_height']))
            #print("Processing Time: %f" % results['processing_time_ms'])
            #print("Results",results)
            i = 0
            for plate in results['results']:
                i += 1
                plates.append(plate)
                #print("Plate #%d" % i)
                #print("   %12s %12s" % ("Plate", "Confidence"))
                for candidate in plate['candidates']:
                    prefix = "-"
                    if candidate['matches_template']:
                        prefix = "*"

                    #print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))



    finally:
        if alpr:
            alpr.unload()
    return plates