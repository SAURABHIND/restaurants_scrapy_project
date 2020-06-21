import os, sys
from datetime import datetime

SUCCESS = 100
FAILED = 200
CODE_ERROR = 300

curr_date = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
json_file_name = 'restaurant_' + str(curr_date) + '.json'

RESTAURANT_SCRAPY_CMD = 'scrapy crawl restaurant -o {}'.format(json_file_name)
SPIDER_PATH = 'wongnai/wongnai/spiders'

AWS_PROFILE_NAME = ''
AWS_S3_BUCKET_NAME = ''
AWS_S3_FOLDER_NAME = ''