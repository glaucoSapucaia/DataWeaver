import zipfile


def zip_file_extractor(full_path_zip, zip_out_folder):
    with zipfile.ZipFile(full_path_zip, "r") as zip_file:
        zip_file.extractall(zip_out_folder)
