# utils/dropbox_utils.py
import dropbox
from django.conf import settings
import os

def upload_to_dropbox(file_obj, filename):
    dbx = dropbox.Dropbox(settings.DROPBOX_ACCESS_TOKEN)

    # تحديد المسار في Dropbox
    dropbox_path = os.path.join(settings.DROPBOX_BASE_PATH, filename)

    # رفع الملف
    dbx.files_upload(file_obj.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))

    # عمل share link
    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
    return shared_link_metadata.url.replace("?dl=0", "?dl=1")  # نخليها لينك تحميل مباشر
