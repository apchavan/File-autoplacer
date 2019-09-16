"""
Collection of directory names for respective file format.
"""

# Specify directory names for each type of files being downloaded.
_document_dirname = "Document downloads"            # Directory for all type of documents.
_image_dirname = "Image downloads"                  # Directory for all type of images.
_audio_dirname = "Audio downloads"                  # Directory for all type of audios.
_video_dirname = "Video downloads"                  # Directory for all type of videos.
_other_dirname = "Other downloads"                  # Directory for other files.


def autoplacer_directories():
    ''' Return names of all autoplacer created directories as a tuple. '''
    return (_document_dirname, _image_dirname, _audio_dirname, _video_dirname, _other_dirname)


def document_directory():
    ''' Return name of directory as "Document downloads". '''
    return _document_dirname


def image_directory():
    ''' Return name of directory as "Image downloads". '''
    return _image_dirname


def audio_directory():
    ''' Return name of directory as "Audio downloads". '''
    return _audio_dirname


def video_directory():
    ''' Return name of directory as "Video downloads". '''
    return _video_dirname


def other_directory():
    ''' Return name of directory as "Other downloads". '''
    return _other_dirname
