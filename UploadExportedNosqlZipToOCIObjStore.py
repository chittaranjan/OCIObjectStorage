# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

from __future__ import print_function
import os
import oci
from oci.object_storage import UploadManager
from oci.object_storage.models import CreateBucketDetails
from oci.object_storage.transfer.constants import MEBIBYTE


def progress_callback(bytes_uploaded):
    print("{} additional bytes uploaded".format(bytes_uploaded))


config = oci.config.from_file()
compute = oci.core.ComputeClient(config)

compute.base_client.session.proxies = {'https': 'www-proxy-us.oracle.com:80'}

compartment_id = "ocid1.compartment.oc1..aaaaaaaaztutmzjbatyykud7b5yzvmj466hcjo6jgzf5dd5zpqxgx5tvplcq"
object_storage = oci.object_storage.ObjectStorageClient(config)

namespace = object_storage.get_namespace().data
bucket_name = "NosqlMultipart"
object_name = "NosqlMultipart"

print("Creating a new bucket {!r} in compartment {!r}".format(bucket_name, compartment_id))
request = CreateBucketDetails()
request.compartment_id = compartment_id
request.name = bucket_name
bucket = object_storage.create_bucket(namespace, request)

print("Uploading new object {!r}".format(object_name))

# upload manager will automatically use multipart uploads if the part size is less than the file size
compressedFile="./fm_metrics_1.txt"
part_size = 10 * MEBIBYTE  # part size (in bytes)
upload_manager = UploadManager(object_storage, allow_parallel_uploads=True, parallel_process_count=3)
response = upload_manager.upload_file(
    namespace, bucket_name, object_name, compressedFile, part_size=part_size, progress_callback=progress_callback)
