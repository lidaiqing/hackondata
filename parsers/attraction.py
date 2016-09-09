from pymongo import MongoClient
from time import time
from utils import mongo_safe_write
import csv
import geocoder

TS = int(time())
MONGO_URI = 'mongodb://localhost/HackOnData'
ATTRACTION_COLLECTION = 'ATTRACTION'

class AttractionParser(object):

    def __init__(self, csv_reader):
        db = MongoClient(MONGO_URI).get_default_database()
        self.collection = db[ATTRACTION_COLLECTION]
        self.csv_reader = csv_reader

    def serialize_data(self, r, id, coordinates):
        return {
            'id': id,
            'name': r[0].decode('utf-8', 'ignore'),
            'full_address': r[1].decode('utf-8', 'ignore'),
            'street_number': r[2],
            'street_name': r[3].decode('utf-8', 'ignore'),
            'suite': r[4],
            'city': r[5],
            'province': r[6],
            'postal_code': r[7].decode('utf-8', 'ignore'),
            'ward': r[8],
            'performance': r[9],
            'exhibition': r[10],
            'screen': r[11],
            'library': r[12],
            'multipurpose': r[13],
            'heritage': r[14],
            'ownership': r[15],
            "coordinates": coordinates,
            'timestamp': TS
        }

    def parse(self):
        results = []
        id = 0
        for row in self.csv_reader:
            if id == 0:
                id = id + 1
                continue
            geo_coder = geocoder.google(row[1].decode('utf-8', 'ignore'), key='AIzaSyDHocit0leJww6QZpwm_xUFX5AWmQyohDo')
            if geo_coder.status != 'OK':
                print ('fail')
                continue
            coordinates = geo_coder.latlng
            coordinates.reverse()
            result = self.serialize_data(row, id, coordinates)
            results.append(result)
            id = id + 1
            print  (id, coordinates)
        #print (self.collection.count())
        mongo_safe_write(results, self.collection)

def main():
    with open('attraction.csv', 'rb') as f:
        reader = csv.reader(f)
        parser = AttractionParser(reader)
        parser.parse()


if __name__ == '__main__':
    main()
