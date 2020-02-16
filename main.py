"""
Creates GUI, system-tray icon, begins application execution.
"""

import os
import sys
import threading
import time

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel, QMenu,
                             QMessageBox, QPushButton, QSystemTrayIcon,
                             QWidget)

import app_data
import excluded_formats
import monitor_downloads


class FileAutoplacer(QWidget):
    ''' Class that handles the execution of "File autoplacer" application. '''
    _lockfile = None            # Stores the object of lockfile to be created.
    _monitor_thread = None      # Stores thread object that do monitoring.
    _systemtray = None          # Stores object of systemtray.
    _start_button = None        # Stores object of 'Start' button (used to disable button when needed).

    def __init__(self, width: int, height: int):
        super().__init__()
        self._init_ui(width, height)

    def _init_ui(self, width: int, height: int):
        ''' Creates GUI window with required controls. '''
        self.setFixedSize(width, height)
        self.setWindowTitle(app_data.app_name())
        self.setWindowIcon(QIcon(app_data.app_logo_path()))
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)           # Only enable titlebar minimize button.
        self._set_controls(width, height)                                 # Add & create controls on window.
        if self._check_systemtray():
            self._create_systemtray()                                     # Create systemtray icon with menu options.
        self._create_lockfile()                                           # Create lockfile to avoid multiple launching of application.
        self.show()

    def _set_controls(self, window_width: int, window_height: int):
        ''' Adds other required controls on window. '''
        if self._start_button:
            return

        animation_label = QLabel(parent=self)
        animation_movie = QMovie(app_data.animation_logo_path())
        animation_movie.setScaledSize(QtCore.QSize(window_width // 1.5, window_height))
        animation_label.setMovie(animation_movie)
        animation_movie.start()
        animation_label.resize(window_width // 1.5, window_height)
        animation_label.move(0, 0)

        start_button = QPushButton(QIcon(app_data.yes_logo_path()), "Start", self, default=True, autoDefault=True)
        start_button.setToolTip("Start to monitor '<B>Downloads</B>' directory on system.")
        start_button.resize(start_button.sizeHint())
        start_button.move(window_width // 1.4, window_height // 10)
        start_button.clicked.connect(self._start_clicked)
        self._start_button = start_button

        about_button = QPushButton(QIcon(app_data.about_logo_path()), "About", self, autoDefault=True)
        about_button.setToolTip("About application & developer.")
        about_button.resize(about_button.sizeHint())
        about_button.move(window_width // 1.4, window_height // 3.35)
        about_button.clicked.connect(self._about_clicked)

        exclusions_button = QPushButton(QIcon(app_data.exclusions_logo_path()), "Exclusions", self, autoDefault=True)
        exclusions_button.setToolTip("Add file/directory to be <B>ignored by app</B>.")
        exclusions_button.resize(exclusions_button.sizeHint())
        exclusions_button.move(window_width // 1.4, window_height // 2)
        exclusions_button.clicked.connect(self._exclusions_clicked)

        quit_button = QPushButton(QIcon(app_data.quit_logo_path()), "Quit", self, autoDefault=True)
        quit_button.setToolTip("'<B>Quit</B>' the application.")
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(window_width // 1.4, window_height // 1.42)
        quit_button.clicked.connect(self._quit_clicked)

    def _start_clicked(self):
        ''' Confirmation box for 'Start' button. '''
        if self._monitor_thread:    # Return if monitoring already.
            return
        confirmation = QMessageBox(self)
        confirmation.setIcon(QMessageBox.Question)
        confirmation.setWindowTitle("Start confirmation")
        confirmation.setText("Start monitoring '<B>Downloads</B>' directory?")
        confirmation.setInformativeText("After starting, <BR />application will be hidden to <B>systemtray</B> " +
                                        "if available, otherwise minimized as usual." +
                                        "<BR /><BR /> " +
                                        "<B>NOTE:</B>" +
                                        "<ul>"
                                        "<li>Consider <B>Exclusions</B> button option " +
                                        "(on main app screen or in systemtray menu) " +
                                        "if you do not want to move some of existing files or directories.</li>" +
                                        "<li>You have to add your exclusions again if the app is re-launched.</li>"
                                        "<ul/>")
        confirmation.setStandardButtons(QMessageBox.Abort | QMessageBox.Yes)
        confirmation.setDefaultButton(QMessageBox.Abort)
        result = confirmation.exec_()
        if result == QMessageBox.Yes:
            self._start_button.setDisabled(True)
            if self._check_systemtray():
                self.hide()
                self._systemtray.showMessage(app_data.app_name(), "Minimized to systemtray.\nRight click app icon for options.",\
                                            QSystemTrayIcon.Information, 2000)
            else:
                self.showMinimized()
            self._monitor_thread = \
                threading.Thread(target=monitor_downloads.monitor_downloads_directory,\
                                name="Monitor thread")
            self._monitor_thread.start()
        else:    # Otherwise if 'Abort' button is clicked or dialog is closed.
            confirmation.done(1)

    def _about_clicked(self):
        ''' Information box for 'About' button. '''
        license_link = QLabel("<BR /> License: <a href='https://github.com/apchavan/File-autoplacer/blob/master/LICENSE'><B>MIT</B></a>", self)
        license_link.setOpenExternalLinks(True)
        repo_link = QLabel("Source: <a href='https://github.com/apchavan/File-autoplacer'><B>Repository</B></a>")
        repo_link.setOpenExternalLinks(True)
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Information)
        info.setWindowTitle("About application & developer")
        info.setText("<B>File autoplacer</B> keep '<B>Downloads</B>' directory on your system clean & managed automatically.")
        info.setInformativeText("Developer: <B>Amey Chavan</B>" + license_link.text() + ", " + repo_link.text())
        info.setStandardButtons(QMessageBox.Ok)
        # info.setDefaultButton(QMessageBox.Ok)
        result = info.exec_()
        # if result == QMessageBox.Ok:
        info.done(1)

    def _exclusions_clicked(self):
        ''' Show dialog to choose exclusion between 'File' or 'Directory'. '''
        exclusion = QMessageBox(self)
        exclusion.setIcon(QMessageBox.Question)
        exclusion.setWindowTitle("Exclusion options")
        exclusion.setText("Select which one to exclude, '<B>File</B> or '<B>Directory</B>' ?")

        file_button = QPushButton(QIcon(app_data.file_logo_path()), "File", self)
        directory_button = QPushButton(QIcon(app_data.directory_logo_path()), "Directory", self)
        close_button = QPushButton(QIcon(app_data.quit_logo_path()), "Close", self)
        exclusion.addButton(file_button, QMessageBox.AcceptRole)
        exclusion.addButton(directory_button, QMessageBox.YesRole)
        exclusion.addButton(close_button, QMessageBox.RejectRole)
        exclusion.setDefaultButton(close_button)

        result = exclusion.exec_()
        if result == 0:             # 'QMessageBox.AcceptRole' return the result 0.
            self._add_file_exclusion()
        elif result == 1:           # 'QMessageBox.YesRole' return the result 1.
            self._add_directory_exclusion()
        elif result == 2:           # 'QMessageBox.RejectRole' return the result 2.
            exclusion.done(1)

    def _quit_clicked(self):
        ''' Confirmation box for 'Quit' button. '''
        confirmation = QMessageBox(self)
        confirmation.setIcon(QMessageBox.Question)
        confirmation.setWindowTitle("Quit confirmation")
        confirmation.setText("<B>Quit</B> 'File autoplacer' ?")
        confirmation.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        confirmation.setDefaultButton(QMessageBox.No)
        result = confirmation.exec_()
        if result == QMessageBox.Yes:
            if self._systemtray:              # Clear systemtray icon if added.
                self._systemtray.hide()
                self._systemtray = None
            self._remove_lockfile()           # Remove lockfile.
            QApplication.instance().quit()    # Quit application.
            del self                          # Remove application instance (can also done with class destructor).
        else:
            confirmation.done(1)

    def _add_file_exclusion(self):
        ''' Add the file to exclusion list. '''
        file_exclude_path = QFileDialog(self)
        file_exclude_path.setFileMode(QFileDialog.AnyFile)
        file_exclude_path.setWindowTitle("Select a FILE for exclusion")

        _ = file_exclude_path.exec_()
        file_path = file_exclude_path.selectedFiles()
        if file_path:
            file_name = file_path[0][(file_path[0].rfind("/") + 1) :]
            excluded_formats.add_new_format(new_format=file_name)
            success_message = QMessageBox(self)
            success_message.setIcon(QMessageBox.Information)
            success_message.setWindowTitle("FILE exclusion")
            success_message.setText(f"'<B>{file_name.strip()}</B>' file is added to exclusion list !")
            success_message.setStandardButtons(QMessageBox.Ok)
            success_message.exec_()

    def _add_directory_exclusion(self):
        ''' Add the directory to exclusion list. '''
        dir_path = QFileDialog.getExistingDirectory(self, "Select a DIRECTORY for exclusion",
                                                        os.path.expanduser("~/Downloads/"),
                                                        QFileDialog.ShowDirsOnly)
        if dir_path:
            dir_name = dir_path[(dir_path.rfind("/") + 1) :]
            excluded_formats.add_new_format(new_format=dir_name)
            success_message = QMessageBox(self)
            success_message.setIcon(QMessageBox.Information)
            success_message.setWindowTitle("DIRECTORY exclusion")
            success_message.setText(f"'<B>{dir_name.strip()}</B>' directory is added to exclusion list !")
            success_message.setStandardButtons(QMessageBox.Ok)
            success_message.exec_()

    def _create_systemtray(self):
        ''' Create & add systemtray icon with controls. '''
        if self._systemtray:
            return
        systemtray = QSystemTrayIcon(self)
        systemtray.setToolTip(app_data.app_name())
        systemtray.setIcon(QIcon(app_data.app_logo_path()))
        systemtray.setVisible(True)

        menu = QMenu(self)
        about_action = menu.addAction(QIcon(app_data.about_logo_path()), "About")
        about_action.triggered.connect(self._about_clicked)
        exclusions_action = menu.addAction(QIcon(app_data.exclusions_logo_path()), "Exclusions")
        exclusions_action.triggered.connect(self._exclusions_clicked)
        quit_action = menu.addAction(QIcon(app_data.quit_logo_path()), "Quit")
        quit_action.triggered.connect(self._quit_clicked)
        systemtray.setContextMenu(menu)
        self._systemtray = systemtray

    def _check_systemtray(self):
        ''' Check and return if systemtray is available for the operating system. '''
        if QSystemTrayIcon.isSystemTrayAvailable():
            return True
        self._show_systemtray_unavailable()
        return False

    def _show_systemtray_unavailable(self):
        ''' Shows message box to user if systemtray for operating system is not available. '''
        unavailable_msg = QMessageBox(self)
        unavailable_msg.setIcon(QMessageBox.Warning)
        unavailable_msg.setWindowTitle("Systemtray info")
        unavailable_msg.setText("Systemtray for your OS is <B>NOT</B> available, so app can't minimized to systemtray.\n Instead app window will minimized as usual.")
        unavailable_msg.setStandardButtons(QMessageBox.Ok)
        # unavailable_msg.setDefaultButton(QMessageBox.Ok)
        result = unavailable_msg.exec_()
        if result == QMessageBox.Ok:
            unavailable_msg.done(1)

    def _create_lockfile(self):
        ''' Creates a lockfile at beginning to avoid more than one instances of application to be launched. '''
        if self._lockfile:
            return
        with open(app_data.lockfile_name(), "w+") as self._lockfile:
            self._lockfile.write(app_data.writable_lockfile_content())
        self._lockfile = open(app_data.lockfile_name(), "r")

    def _remove_lockfile(self):
        ''' Removes lock and created lockfile when application is exited. '''
        if not self._lockfile:
            return
        self._lockfile.close()
        os.remove(app_data.lockfile_name())


def app_already_running():
    info = QMessageBox()
    info.setIcon(QMessageBox.Warning)
    info.setWindowIcon(QIcon(app_data.app_logo_path()))
    info.setWindowTitle(app_data.app_name())
    info.setText("Hey! I'm <B>already running</B>! 😊")
    info.setInformativeText("I might be <B>minimized</B> or in your <B>systemtray</B>. 🙄" +
                            "<BR /><BR />If still not found, <BR />try to delete '<B>" + app_data.lockfile_name() +
                            "</B>' lockfile in app directory and run again. 🙂")
    info.setStandardButtons(QMessageBox.Ok)
    result = info.exec_()
    if result == QMessageBox.Ok:
        QApplication.instance().quit()


def main():
    ''' First method to begin execution of 'File autoplacer'. '''
    app = QApplication(sys.argv)

    # First check for lockfile, to avoid more than one app launches.
    try:
        lockfile = open(app_data.lockfile_name(), mode="r")
    except FileNotFoundError:
        pass
    else:
        file_content = lockfile.read()
        if app_data.is_valid_content(file_content):
            app_already_running()
            return
        else:
            lockfile.close()
            try:
                os.remove(app_data.lockfile_name())
            except PermissionError:
                app_already_running()
                return

    app.setQuitOnLastWindowClosed(False)

    # Screen size link: https://stackoverflow.com/questions/35887237/current-screen-size-in-python3-with-pyqt5
    screen = app.primaryScreen()                      # Return 'QScreen' object.
    # full_size = screen.size()                         # Return exact size of screen.

    available_size = screen.availableGeometry()       # Return available size of screen (excluding panels, bars etc)
    app_window = FileAutoplacer(width=(available_size.width() // 5),
                                height=(available_size.height() // 4.5))
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
