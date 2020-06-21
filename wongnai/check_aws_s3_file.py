import os
import boto3
import fnmatch
import sys
from constants import *
import requests


# AWS S3 Bucket for storage the files
def uploadToAWS(image_dir_path, new_image_name):
    for _ in range(1, 3):
        try:
            # AWS S3 Bucket session
            SESSION = boto3.Session(profile_name=AWS_PROFILE_NAME)
            S3 = SESSION.client('s3')
            S3.upload_file(image_dir_path + new_image_name, AWS_S3_BUCKET_NAME, AWS_S3_FOLDER_NAME + '/{}'.format(new_image_name))
            print("File have been updated to S3", new_image_name)
            return SUCCESS
        except Exception as e:
            print("Error in uploadToAws: ", e)
            continue
    return FAILED


# function for delete the files after upload to S3
def aws_main(image_url, new_image_name, image_dir_path):
    """
    :param image_url: web image url
    :param new_image_name: it is image name including .jpg
    :param image_dir_path: it should contains '/' in the last
    :return:
    """
    try:
        status = get_image_using_url(image_url, new_image_name, image_dir_path)

        if status != SUCCESS:
            raise ValueError("ERROR IN GET IMAGE USING URL")

        upload_status = uploadToAWS(image_dir_path, new_image_name)

        if upload_status == SUCCESS:
            os.remove(image_dir_path + new_image_name)

        return SUCCESS
    except Exception as e:
        print("Error in the main - {}".format(e))
        return CODE_ERROR


def get_image_using_url(image_url, new_image_path, image_dir_path):
    try:
        print(image_url)
        print(new_image_path)
        print(image_dir_path)
        import time
        time.sleep(60)
        img_data = requests.get(image_url).content
        with open(image_dir_path + new_image_path, 'wb') as handler:
            handler.write(img_data)
        return SUCCESS
    except Exception as err:
        print("ERROR IN GET IMAGE USING URL {}".format(err))
        return CODE_ERROR