import io
import logging
import requests

import boto3
from boto3.exceptions import (
    Boto3Error,
    S3UploadFailedError,
    ResourceLoadException,
    ResourceNotExistsError,
    RetriesExceededError,
)
from botocore.client import Config
import xlsxwriter

from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from geocodio import GeocodioClient

logging.basicConfig(level=logging.DEBUG)

def getParsedLocation(location):
    client = GeocodioClient(settings.GEOCODIO_API_KEY)
    return client.geocode(location)

def get_logger(name):
    return logging.getLogger(name)

def create_export_xlsx(title, headers, data):

    def _get_attribute(obj, attr):
        if attr.find('__') > 0:
            attr_trail = attr.split('__')
            attr, trail = attr_trail[0], '__'.join(attr_trail[1:]) 
            new_obj = obj.get(attr, None)
            if not new_obj:
                return ''
            return _get_attribute(new_obj, trail)
        return obj.get(attr, '')

    output = io.BytesIO()
    
    workbook = xlsxwriter.Workbook(output,{'in_memory': True})
    worksheet = workbook.add_worksheet()
    row_num = 0
    for ci, header in enumerate(headers.keys()):
        worksheet.write(row_num, ci, header)
    for obj in data:
        row_num += 1
        for ci, accessor in enumerate(headers.values()):
            value = _get_attribute(obj, accessor)
            worksheet.write(row_num, ci, value)
    workbook.close()

    output.seek(0)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % title
    response.write(output.read())
    return response

def get_usernames_and_emails(receivers):
    usernames = []
    emails = []
    for item in receivers:
        item = item.strip()
        if item.startswith('@'):
            usernames.append(item.strip('@'))
        else:
            try:
                validate_email(item)
                emails.append(item)
            except ValidationError:
                continue
    return usernames, emails


def upload_image_to_s3(url, uid):
    try:
        session = boto3.Session(settings.AWS_ACCESS_KEY_ID,
                                settings.AWS_SECRET_ACCESS_KEY)
        s3 = session.resource('s3')
        bucket  = s3.Bucket(settings.AWS_PROPERTY_PHOTOS_BUCKET_NAME)
        r = requests.get(url, stream=True)
        content_type = r.headers['Content-Type']
        key = "%s.%s" % (uid, content_type.split('/')[1])
        bucket.upload_fileobj(r.raw, key)
        return get_s3_url_for_key(key, session=session)
    except (Boto3Error, S3UploadFailedError, RetriesExceededError):
        #TODO: logging here
        return
    
                        
def get_s3_url_for_key(key, session=None):
    try:
        if not session:
            session = boto3.Session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        s3 = session.client('s3', config=Config(region_name="us-east-2", signature_version='s3v4'))
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.AWS_PROPERTY_PHOTOS_BUCKET_NAME,
                'Key': key
            }
        )
        return {
            "key": key,
            "url": url
        }
    except (ResourceNotExistsError, ResourceLoadException, RetriesExceededError):
        #TODO: logging here
        return 
