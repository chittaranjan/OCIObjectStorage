# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

import filecmp
import oci
from oci.object_storage.models import CreateBucketDetails
from time import sleep
import sys
import pprint




def progress_callback(bytes_uploaded):
    print("{} additional bytes uploaded".format(bytes_uploaded))

config = oci.config.from_file()
compartment_id = config["tenancy"]
object_storage = oci.object_storage.ObjectStorageClient(config)

namespace = object_storage.get_namespace().data
bucket_name = "NosqlMultipart"
object_name = "fm1915dev4iot_exported_20190304074251.zip"


# Retrieve the file, streaming it into another file in 1 MiB chunks
head_obj = object_storage.head_object(namespace, bucket_name, object_name)
total_length = head_obj.headers["Content-Length"]
get_obj = object_storage.get_object(namespace, bucket_name, object_name)
with open('test.zip', 'wb') as f:
    if total_length is None:  # no content length header
        f.write(get_obj)
    else:
        dl = 0
        total_length = int(total_length)
        print('Downloading file form object storage')
        for data in get_obj.data.raw.stream(1024 * 1024, decode_content=False):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r[%s%s] %s%%" % ('=' * done, ' ' * (50 - done), int((dl / total_length) * 100)))
            sys.stdout.flush()

#print('Uploaded and downloaded files are the same: {}'.format(filecmp.cmp(object_name, 'test.zip')))
