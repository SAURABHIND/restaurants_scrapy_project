import re
import os
import logging
import json
from flask import Flask, request, jsonify, make_response
from constants import *
from check_aws_s3_file import *


app = Flask(__name__)
app.config['DEBUG'] = True  # set to False in production environment
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.secret_key = 'FEHWR3Y4T3IU437EHRE'


@app.route('/scrape_restaurant', methods=['GET'])
def check_scrape_restaurant():
    try:
        print("PROCESS START FOR SCRAPE RESTAURANT")
        #os.chdir(SPIDER_PATH)
        os_csm = os.system(RESTAURANT_SCRAPY_CMD)
        return make_response(jsonify(message="SUCCESSFUL", status='200'), 200)
    except Exception as err:
        print("ERROR IN CHECK SCRAPE RESTAURANT {}".format(err))
        return make_response(jsonify(message="CODE ERROR", status='900'), 900)


@app.route('/import_image', methods=['POST'])
def check_upload_image_aws():
    try:
        data = request.get_json(force=True)
        json_path = data['json_path']
        image_dir_path = data['image_dir_path']

        json_file_path = open(json_path, encoding="utf8")
        json_data = json.load(json_file_path)

        for file in json_data:
            if 'product_photos' in file:
                new_image_name = file['product_photos'].split('/')[-1]
                aws_main(file['product_photos'], new_image_name, image_dir_path)

            if 'product_image' in file:
                new_image_name = file['product_image'].split('/')[-1]
                aws_main(file['product_image'], new_image_name, image_dir_path)

            if 'product_recommended_by_user' in file:
                new_image_name = file['product_recommended_by_user'].split('/')[-1]
                aws_main(file['product_recommended_by_user'], new_image_name, image_dir_path)

        return make_response(jsonify(message="SUCCESS", status='200'), 200)
    except Exception as err:
        print("ERROR IN API REQUEST {}".format(err))
        return make_response(jsonify(message="CODE ERROR", status='900'), 900)


if __name__ == "__main__":
    app.run()