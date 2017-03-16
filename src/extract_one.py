from bs4 import BeautifulSoup
#import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import string
import os


#Define the MongoDB database and collection
db_cilent = MongoClient()
db = db_cilent['WBLS']
collection = db.biz

class extract(object):
    """Creates object which holds extracted values using BeautifulSoup
    """
    def __init__(self):
        self.soup = None
        self.business_name = None
        self.address_one = None
        self.address_one = None
        self.address_mailing = None
        self.ubi = None
        self.city = 'Seattle'
        self.zip_code = None

    def create_soup(self, page_source):
        self.soup = BeautifulSoup()
        self.soup = self.sou(page_source, 'html.parser')

    def get_buisiness_name(self):
        self.business_name = self.soup.find(id='caption2_c-e')
        if self.business_name is not None:
            self.business_name = self.business_name.contents[0].encode('utf-8').strip()
        else:
            self.business_name=""

    def get_address_one(self):
        self.address_one = self.soup.find(id='caption2_c-u')
        if self.address_one is not None:
            if len(self.address_one.contents) != 0:
                self.address_one = self.address_one.contents[0].encode('utf-8').strip()
            else:
                self.address_one=""
        else:
            self.address_one=""

    def get_zip_code(self):
        self.zip_code = self.soup.find(id='caption2_c-v')
        if self.zip_code is not None:
            if len(self.zip_code.contents) != 0:
                zipfield = self.zip_code.contents[0].encode('utf-8').strip()
                self.zip_code = zipfield[-5:]
            else:
                self.zip_code=""
        else:
            self.zip_code=""

    def get_address_mailing(self):
        self.address_mailing = self.soup.find(id='caption2_c-01')
        if self.address_mailing is not None:
            if len(self.address_mailing.contents) != 0:
                self.address_mailing = self.address_mailing.contents[0].encode('utf-8').strip()
            else:
                self.address_mailing=""
        else:
            self.address_mailing=""

    def get_ubi(self):
        self.ubi = self.soup.find(id='caption2_c-i')
        if self.ubi is not None:
            self.ubi = self.ubi.contents[0].encode('utf-8').strip()
        else:
            self.ubi=""

    def build(self, filename):
        """Calls subfunction which create values for the parameters
        arg: filename is html file to be extracted
        """
        self.create_soup(filename)
        self.get_buisiness_name()
        self.get_address_one()
        self.get_address_mailing()
        self.get_ubi()
        self.get_zip_code()

    def db_add(self, collection):
        collection.insert_one({
                "Bus Name" : self.business_name,
                "Address" : self.address_one,
                "Addr_mail" : self.address_mailing,
                "UBI" : self.ubi,
                "City" : self.city,
                "Zip" : self.zip_code
            })
"""
if __name__ == '__main__':
    code processes all html files in data folder and
    saves fields to records in mongoDB.
    collection name is defined at the top of the code.

    print "DB and collection is:" , collection.full_name
    print "Initial record count:" , collection.count()
    for file in os.listdir('../data/'):
        if '.html' in file:
            extracted = extract()
            extracted.build(file)
            extracted.db_add(collection)
    print "Final record count:" , collection.count()
"""