"""
Collection of document file formats or directories to be excluded while moving.
"""


# From: https://fileinfo.com/filetypes/misc
# https://fileinfo.com/filetypes/misc-all
# https://www.webopedia.com/quick_ref/fileextensionsfull.asp
# Specify excluded file formats/directories.
_excluded_formats = {
    ######################### Common partially downloaded file extensions #########################
    ".!BT",
    ".!QB",
    ".!SYNC"
    ".!UT",
    ".ADADOWNLOAD",
    ".APPDOWNLOAD",
    ".AZ!",
    ".BC",
    ".BC!",
    ".BT!",
    ".CRDOWNLOAD",
    ".DAP",
    ".DCTMP",
    ".DE"
    ".DOWNLOADING",
    ".DSTUDIO",
    ".DTAPART",
    ".E3P"
    ".FB!",
    ".JC",
    ".JC!",
    ".OB!",
    ".OPDOWNLOAD",
    ".PART",
    ".PARTIAL",
    ".TD",
    ".TMP",
    ".XLX",
    ######################### Common directory formats #########################
    "Telegram Desktop"
}


def excluded_formats():
    return _excluded_formats


def add_new_format(new_format: str=""):
    ''' Add the specified 'new_format' to above exclusion set. '''
    if not new_format.strip():
        return
    global _excluded_formats
    _excluded_formats.add(new_format)
