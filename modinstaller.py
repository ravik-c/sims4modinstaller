import glob
import zipfile
import shutil
import os
import patoolib

temp_extract_folder = ""
mod_files_location= ""
mod_after_install_location= ""
mod_folder= ""
tray_folder= ""
misc_file_folder= ""
file_count= 0

def move(destination, depth=''): 
    current_depth = os.path.join(destination, depth) 
    for file_or_dir in os.listdir(current_depth): 
        file_or_dir = os.path.join(current_depth, file_or_dir) 
        if os.path.isfile(file_or_dir): 
            if depth:
                shutil.move(os.path.join(destination, file_or_dir), os.path.join(temp_extract_folder, file_or_dir) )
        else: 
            move(destination, os.path.join(depth, file_or_dir)) 

folder = os.fsencode(mod_files_location)
if not os.path.exists(temp_extract_folder):
    os.mkdir(temp_extract_folder)

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.zip') ): 
        my_zip = mod_files_location + "\\" + filename
        with zipfile.ZipFile(my_zip) as zip:
            for zip_info in zip.infolist():
                if zip_info.filename[-1] == '/':
                    continue
                zip_info.filename = os.path.basename(zip_info.filename)
                zip.extract(zip_info, temp_extract_folder)
        
        shutil.move(my_zip, mod_after_install_location)
        print("Processed zip file:" + my_zip)
        file_count = file_count + 1

    elif filename.endswith( ('.package') ):
        my_package_file = mod_files_location + "\\" + filename
        shutil.copy(my_package_file, temp_extract_folder)
        os.remove(my_package_file)
        print("Processed package file:" + my_package_file)
        file_count = file_count + 1
    elif filename.endswith( ('.rar') ): 
        my_rar = mod_files_location + "\\" + filename
        patoolib.extract_archive(my_rar, outdir=temp_extract_folder)
        shutil.move(my_rar, mod_after_install_location)
        print("processed rar file:" + my_rar)
        file_count = file_count + 1

move(temp_extract_folder)
extract_folder = os.fsencode(temp_extract_folder)

for file in os.listdir(extract_folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.hhi', '.sgi', '.trayitem', '.householdbinary', '.bpi', '.blueprint') ): # whatever file types you're using...
        my_tray_files = temp_extract_folder + "\\" + filename
        shutil.copy(my_tray_files, tray_folder)
    elif filename.endswith( ('.package', '.ts4script') ):
        my_package_file = temp_extract_folder + "\\" + filename
        shutil.copy(my_package_file, mod_folder)
    elif not os.path.isfile(file):
        pass
    else:
        my_package_file = temp_extract_folder + "\\" + filename
        shutil.copy(my_package_file, misc_file_folder)

shutil.rmtree(temp_extract_folder)
print("End of Program. Total processed files: " + str(file_count))
