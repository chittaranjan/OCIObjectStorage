# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

import filecmp
import oci
from oci.object_storage.models import CreateBucketDetails


config = oci.config.from_file()
compartment_id = config["tenancy"]
object_storage = oci.object_storage.ObjectStorageClient(config)

namespace = object_storage.get_namespace().data
bucket_name = "NosqlMultipart"
object_name = "fm1915dev4iot_exported_20190304074251.zip"


# Retrieve the file, streaming it into another file in 1 MiB chunks
print('Retrieving file from object storage')
get_obj = object_storage.get_object(namespace, bucket_name, object_name)
with open('test.zip', 'wb') as f:
    for chunk in get_obj.data.raw.stream(1024 * 1024, decode_content=False):
        f.write(chunk)

print('Uploaded and downloaded files are the same: {}'.format(filecmp.cmp(object_name, 'test.zip')))
