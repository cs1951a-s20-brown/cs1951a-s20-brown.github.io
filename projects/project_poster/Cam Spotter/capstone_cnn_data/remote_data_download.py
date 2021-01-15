import os
import json
import requests
import shutil
import sys
import pickle

def get_labelbox_data(labelbox_json_filepath):
    data = None
    os.mkdir('project_data')
    with open(labelbox_json_filepath) as json_file:
        data = json.load(json_file)

    successful_downloads = []
    failed_downloads = []
    for i, datarow in enumerate(data):
        image_data_url = datarow['Labeled Data']
        image_label = datarow['Label']
        filename = datarow['External ID']
        filepath = 'project_data/' + filename
        r = requests.get(image_data_url, stream = True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            # Open a local file with wb ( write binary ) permission.
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            successful_downloads.append([i, image_data_url, image_label, filename])
        else:
            failed_downloads.append([i, image_data_url, image_label, filename])

    with open('failed.txt', 'w') as outfile:
        json.dump(failed_downloads, outfile)

    with open('successful.txt', 'w') as outfile:
        json.dump(successful_downloads, outfile)

    return successful_downloads, failed_downloads

def main(labelbox_json_filepath):
    successful_downloads, failed_downloads = get_labelbox_data(labelbox_json_filepath)
    print(len(successful_downloads))
    print('===================================================')
    print(len(failed_downloads))


if __name__ == '__main__':
    path_to_label_json = './export-2020-05-05T17_23_24.761Z.json' if len(sys.argv) == 1 else sys.argv[1]
    main(path_to_label_json)
