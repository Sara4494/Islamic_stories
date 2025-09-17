import os
import dropbox
from django.conf import settings

def upload_to_dropbox(file_obj, filename):
    dbx = dropbox.Dropbox(settings.DROPBOX_ACCESS_TOKEN)

    dropbox_path = os.path.join(settings.DROPBOX_BASE_PATH, filename)

    # رفع الملف (overwrite)
    dbx.files_upload(file_obj.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))

    # الأول نبحث لو فيه لينك موجود
    links = dbx.sharing_list_shared_links(path=dropbox_path, direct_only=True).links
    if links:
        url = links[0].url
    else:
        # لو مفيش لينك نعمل واحد جديد
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        url = shared_link_metadata.url

    # نحوله لداونلود مباشر
    return url.replace("?dl=0", "?dl=1")
