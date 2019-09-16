"""
Functions to monitor 'Downloads' directory.
"""

import distutils.errors as distutils_errors
import os
import random
import time
from distutils.dir_util import copy_tree, remove_tree
from distutils.file_util import copy_file
from platform import system

import app_data
import audio_formats
import directory_names
import document_formats
import excluded_formats
import image_formats
import video_formats


def _get_download_dir_details():
    ''' Return path of 'Downloads' directory depending on OS and whether OS is 'Windows' (True) or not (False). '''
    user_os = system().lower()
    current_username = os.getlogin()
    if user_os == "windows":
        return ("C:\\Users\\" + current_username + "\\Downloads\\"), True
    else:
        return ("~/Downloads/"), False


def _is_hidden(file_folder: str="", _is_windows=False):
    ''' Check for "file_folder" is hidden or not, return bool value 'True' if hidden else return 'False' for regular ones. '''
    if not file_folder.strip():
        return
    if _is_windows:
        import win32api, win32con
        ff_attribute = win32api.GetFileAttributes(file_folder)
        return ff_attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return file_folder.strip().startswith(".")


def _move_document(doc_name: str, download_path: str):
    ''' Move downloaded document to document directory specified below. '''
    if not doc_name.strip() or not download_path.strip():
        return
    doc_dir = download_path + directory_names.document_directory()
    if not os.path.isdir(doc_dir):
        os.mkdir(doc_dir)

    source_path = os.path.join(download_path, doc_name)
    destination_path = os.path.join(doc_dir, doc_name)
    try:
        copy_file(src=source_path, dst=destination_path)
        os.remove(path=source_path)
    except (PermissionError, distutils_errors.DistutilsFileError) as Error:
        return


def _move_image(image_name: str, download_path: str):
    ''' Move downloaded image to image directory specified below. '''
    if not image_name.strip() or not download_path.strip():
        return
    img_dir = download_path + directory_names.image_directory()
    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)

    source_path = os.path.join(download_path, image_name)
    destination_path = os.path.join(img_dir, image_name)
    try:
        copy_file(src=source_path, dst=destination_path)
        os.remove(path=source_path)
    except (PermissionError, distutils_errors.DistutilsFileError) as Error:
        return


def _move_audio(audio_name: str="", download_path: str=""):
    ''' Move downloaded audio to audio directory specified below. '''
    if not audio_name.strip() or not download_path.strip():
        return
    aud_dir = download_path + directory_names.audio_directory()
    if not os.path.isdir(aud_dir):
        os.mkdir(aud_dir)

    source_path = os.path.join(download_path, audio_name)
    destination_path = os.path.join(aud_dir, audio_name)
    try:
        copy_file(src=source_path, dst=destination_path)
        os.remove(path=source_path)
    except (PermissionError, distutils_errors.DistutilsFileError) as Error:
        return


def _move_video(video_name: str="", download_path: str=""):
    ''' Move downloaded video to video directory specified below. '''
    if not video_name.strip() or not download_path.strip():
        return
    vid_dir = download_path + directory_names.video_directory()
    if not os.path.isdir(vid_dir):
        os.mkdir(vid_dir)

    source_path = os.path.join(download_path, video_name)
    destination_path = os.path.join(vid_dir, video_name)
    try:
        copy_file(src=source_path, dst=destination_path)
        os.remove(path=source_path)
    except (PermissionError, distutils_errors.DistutilsFileError) as Error:
        return


def _move_other(file_dir_name: str="", download_path: str=""):
    ''' Move downloaded other file/folder to other directory specified below. '''
    if not file_dir_name.strip() or not download_path.strip():
        return
    other_dir = download_path + directory_names.other_directory()
    if not os.path.isdir(other_dir):
        os.mkdir(other_dir)

    source_path = os.path.join(download_path, file_dir_name)
    destination_path = os.path.join(other_dir, file_dir_name)
    if os.path.isdir(source_path):
        try:
            copy_tree(src=source_path, dst=destination_path)
            remove_tree(directory=source_path)
        except (PermissionError, distutils_errors.DistutilsFileError) as Error:
            return
    elif os.path.isfile(source_path):
        try:
            copy_file(src=source_path, dst=destination_path)
            os.remove(path=source_path)
        except (PermissionError, distutils_errors.DistutilsFileError) as Error:
            return


def _is_autoplacer_dirs(dir_name: str=""):
    ''' Return whether 'dir_name' is created by autoplacer application or not. '''
    if not dir_name.strip():
        return False
    autoplacer_dirs = directory_names.autoplacer_directories()
    if dir_name.strip() in autoplacer_dirs:
        return True
    return False


def _is_dir_downloading(dir_path: str=""):
    ''' Return whether directory contents still being downloaded (True) or not (False). '''
    if not dir_path.strip():
        return False
    excluded_file_formats = excluded_formats.excluded_formats()
    for root, directories, files in os.walk(dir_path):
        for file in files:
            file_extension = file[file.rfind(".") :]
            if file_extension.upper() in excluded_file_formats:
                return True
    return False


def monitor_downloads_directory():
    ''' Monitors 'Downloads' directory on system. '''
    _download_path, _is_windows = _get_download_dir_details()
    excluded_file_formats = excluded_formats.excluded_formats()

    while os.path.isfile(app_data.lockfile_name()):
        time.sleep(random.randint(5, 10))
        with os.scandir(path=_download_path) as scanner:
            for entry in scanner:
                if not os.path.isfile(app_data.lockfile_name()):
                    return
                elif _is_hidden(file_folder=(_download_path + entry.name), _is_windows=_is_windows)\
                  or _is_autoplacer_dirs(dir_name=entry.name):
                    continue
                elif entry.is_file():
                    file_extension = entry.name[entry.name.rfind(".") :]
                    if file_extension.upper() in excluded_file_formats:
                        continue
                    elif file_extension.lower() in video_formats.video_file_formats():
                        _move_video(video_name=entry.name, download_path=_download_path)
                    elif file_extension.lower() in audio_formats.audio_file_formats():
                        _move_audio(audio_name=entry.name, download_path=_download_path)
                    elif file_extension.lower() in document_formats.document_file_formats():
                        _move_document(doc_name=entry.name, download_path=_download_path)
                    elif file_extension.lower() in image_formats.image_file_formats():
                        _move_image(image_name=entry.name, download_path=_download_path)
                    else:
                        _move_other(file_dir_name=entry.name, download_path=_download_path)

                elif entry.is_dir() and \
                not _is_dir_downloading(dir_path=(_download_path + entry.name)) and \
                entry.name not in excluded_formats.excluded_formats():
                    _move_other(file_dir_name=entry.name, download_path=_download_path)
