"""
Collection of document file formats.
"""


# Specify document filename extensions.
_document_file_formats = {
    ".html",
    ".htm",
    ".pdf",
    ".xml",
    ".txt",
    ".csv",
    ######################### MS Office formats #########################
    ".doc",
    ".docm",
    ".docx",
    ".dot",
    ".dotm",
    ".dotx",
    ".mht",
    ".mhtml",
    ".rtf",
    ".wps",        # <== This format also used by WPS Office for writer document.
    ".xps",
    ".dbf",
    ".dif",
    ".prn",
    ".slk",
    ".xla",
    ".xlam",
    ".xls",
    ".xlsb",
    ".xlsm",
    ".xlsx",
    ".xlt",
    ".xltm",
    ".xltx",
    ".xlw",
    ".emf",
    ".pot",
    ".potm",
    ".potx",
    ".ppa",
    ".ppam",
    ".pps",
    ".ppsm",
    ".ppsx",
    ".ppt",
    ".pptm",
    ".pptx",
    ".thmx",
    ".wmf",
    ######################### LibreOffice formats #########################
    ".ods",      # Spreadsheet.
    ".odt",      # Document.
    ".ott",      # Text template.
    ".odm",      # Master document.
    ".oth",      # HTML document template.
    ".ots",      # Spreadsheet template.
    ".odg",      # Drawing.
    ".otg",      # Drawing template.
    ".odp",      # Presentation.
    ".otp",      # Presentation template.
    ".odf",      # Formula.
    ".odb",      # Database.
    ".oxt",      # Extension.
    ######################### WPS Office formats #########################
    ".dps",
    ".dpt",
    ".et",
    ".ett",
    ".kuip",
    ".wpt",
    ".dsc",
    ".str",
    ######################### FreeOffice formats #########################
    ".tmdx",
    ".pmd",
    ".pmdx",
    ".pmv",
    ".pmvx",
    ".prd",
    ".prdx",
    ".prv",
    ".prvx",
    ".psw",
    ".pwd"
    ".pwt",
    ".tmd",
    ".tmv",
    ".tmvx"
}


def document_file_formats():
    return _document_file_formats
