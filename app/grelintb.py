#!/usr/bin/env python3

# Copyright (C) 2024 MuKonqi (Muhammed S.)

# GrelinTB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GrelinTB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GrelinTB.  If not, see <https://www.gnu.org/licenses/>.


def return_arg(arg: str): return arg # temporary

import os
import sys
import getpass
import locale
import gettext
import threading
import subprocess
import time
import datetime
import socket
import platform


if os.path.isfile("/etc/debian_version"):
    pkg_mngr = "APT"
    pkg_type = "DEB"
elif os.path.isfile("/etc/fedora-release"):
    pkg_mngr = "DNF5"
    pkg_type = "RPM"
elif os.path.isfile("/bin/zypper") or os.path.isfile("/usr/bin/zypper"):
    pkg_mngr = "Zypper"
    pkg_type = "RPM"
elif os.path.isfile("/etc/arch-release"):
    pkg_mngr = "Pacman"
    pkg_type = "Pacman"
else:
    sys.stderr.write("The operating system you are using is not supported. (1)\n")
    sys.exit(1)
    
    
from PyQt6.QtCore import Qt, QSize, QStringListModel, QTimer
from PyQt6.QtGui import QIcon, QKeyEvent, QPixmap, QMovie, QFont, QAction, QKeySequence
from PyQt6.QtWidgets import *
import psutil
import distro


try:
    from PyQt6.QtCore import Qt, QSize, QStringListModel, QTimer
    from PyQt6.QtGui import QIcon, QPixmap, QMovie, QFont, QAction, QKeySequence
    from PyQt6.QtWidgets import *
    import psutil
    import distro
except:
    if not os.path.isfile("/bin/pip") and not os.path.isfile("/usr/bin/pip"):
        if not pkg_mngr.lower() == "zypper":
            print("Installing pip...")
        elif pkg_mngr.lower == "apt":
            os.system("pkexec apt -y install python3-pip")
        elif pkg_mngr.lower == "dnf5":
            os.system("pkexec dnf5 -y --nogpgcheck install python3-pip")
        elif pkg_mngr.lower == "zypper":
            print("Installing PyQt6, psutil, distro via Zypper for Python 3.12/3.11...")
            os.system("pkexec zypper -n install python312 python312-PyQt6 python312-psutil "
                      + "python312-distro python311 python311-PyQt6 python311-psutil python311-distro")
        elif pkg_mngr.lower == "pacman":
            os.system("pkexec pacman --noconfirm -S python-pip")
    try:
        if not pkg_mngr.lower() == "zypper":
            print("Installing other requirements...")
            os.system(f"pip install pyqt6 psutil distro")
        from PyQt6.QtCore import Qt, QSize, QStringListModel, QTimer
        from PyQt6.QtGui import QIcon, QPixmap, QMovie, QFont, QAction, QKeySequence
        from PyQt6.QtWidgets import *
        import psutil
        import distro
    except:
        if not pkg_mngr.lower() == "zypper":
            print("Installing other requirements with --break-system-packages parameter...")
            os.system(f"pip install pyqt6 psutil distro --break-system-packages")
        os.system(__file__)
        sys.exit(0)
        
username = getpass.getuser()
appdir = None # temporary
operations_number = 0
operations_list = []
operations_model = QStringListModel()
align_center = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter

# try:
#     with open(f"{appdir}version.txt") as version_file:
#         current_version = version_file.read().replace("\n", "")
# except:
#     sys.stderr.write("The version file can not found! (2)\n")
#     sys.exit(2)

try:
    if "tr" in locale.getlocale()[0][0:]:
        language = "tr"
        # translations = gettext.translation("grelintb", "locales", languages=["tr"])
    else:
        language = "en"
        # translations = gettext.translation("grelintb", "locales", languages=["en"])
    # translations.install()
    # _ = translations.gettext
    _ = return_arg
except:
    sys.stderr.write("The language can not be setted! (3)\n")
    sys.exit(3)


def add_operation(operation: str, time: str):
    operations_list.append(f"{operation}\n{_('Started at')} {time}")
    operations_model.setStringList(operations_list)

def delete_operation(operation: str, time: str):
    operations_list.remove(f"{operation}\n{_('Started at')} {time}")
    operations_model.setStringList(operations_list)
    

class Sidebar(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.changelogs_button = QPushButton(parent = self, text = _("Changelogs"))
        self.changelogs_button.clicked.connect(self.changelogs)
        self.license_button = QPushButton(parent = self, text = _("License"))
        self.license_button.clicked.connect(self.license)
        self.upgrade_button = QPushButton(parent = self, text = _("Upgrade"))
        self.upgrade_button.clicked.connect(self.update)
        self.reset_button = QPushButton(parent = self, text = _("Reset"))
        self.reset_button.clicked.connect(self.reset)
        self.remove_button = QPushButton(parent = self, text = _("Remove"))
        self.remove_button.clicked.connect(self.remove)
        
        self.list_view = QListView(self)
        self.list_view.setModel(operations_model)

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.changelogs_button, 0)
        self.layout().addWidget(self.license_button, 1)
        self.layout().addWidget(self.upgrade_button, 2)
        self.layout().addWidget(self.reset_button, 3)
        self.layout().addWidget(self.remove_button, 4)
        self.layout().addWidget(self.list_view, 5, Qt.AlignmentFlag.AlignHCenter)
        
    def changelogs(self):
        pass
    
    def license(self):
        pass
    
    def do_update(self):
        pass
    
    def go_update(self):
        pass
    
    def reset(self):
        pass
    
    def remove(self):
        pass 
        

class Startup(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.temps_worked = False
        self.temps_labels = {}
        self.temps_number = 0
        self.fans_worked = False
        self.fans_labels = {}
        self.fans_number = 0
        self.batt_worked = False
        self.batt_labels = {}
        
        self.setLayout(QGridLayout(self))
        
        self.welcome_label = QLabel(parent = self, alignment = align_center, 
                                    text = f"{_('Hello')} {username}!")
        self.weather_label = QLabel(parent = self, alignment = align_center, 
                                    text = f"{_('Weather forecast')}: {_('Getting')}")
        self.system_label = QLabel(parent = self, alignment = align_center, 
                                   text = _('System'))
        self.hostname_label = QLabel(parent = self, alignment = align_center, 
                                     text = f"{_('Hostname')}: {socket.gethostname()}")
        self.distro_label = QLabel(parent = self, alignment = align_center, 
                                   text = f"{_('Distrubiton')}: {distro.name(pretty = True)}")
        self.kernel_label = QLabel(parent = self, alignment = align_center, 
                                   text = f"{_('Kernel')}: {platform.platform()}")
        self.packages_label = QLabel(parent = self, alignment = align_center, 
                                     text = f"{_('Number of packages')}: ")
        self.uptime_label = QLabel(parent = self, alignment = align_center, 
                                   text = f"{_('Uptime')}: "
                                   + str(datetime.timedelta(seconds = float(os.popen('cat /proc/uptime').read().split()[0]))))
        self.boot_time_label = QLabel(parent = self, alignment = align_center, 
                                      text = f"{_('Boot time')}: "
                                      + datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%d.%m.%Y %H:%M:%S'))
        self.usages_label = QLabel(parent = self, alignment = align_center, 
                                   text = _('Usages'))
        self.cpu_label = QLabel(parent = self, alignment = align_center, 
                                text = f"CPU: {_('Getting')}")
        self.disk_label = QLabel(parent = self, alignment = align_center, 
                                 text = f"Disk: %{str(psutil.disk_usage('/')[3])}")
        self.ram_label = QLabel(parent = self, alignment = align_center, 
                                text = f"RAM: %{str(psutil.virtual_memory().percent)}")
        self.swap_label = QLabel(parent = self, alignment = align_center, 
                                 text = f"{_('Swap')}: %{str(psutil.swap_memory().percent)}")
        
        self.welcome_label.setStyleSheet("QLabel{font-size: 14pt;}")
        self.system_label.setStyleSheet("QLabel{font-size: 14pt; margin-top: 14px;}")
        self.usages_label.setStyleSheet("QLabel{font-size: 14pt; margin-top: 14px;}")
        
        self.layout().addWidget(self.welcome_label, 0, 0, 1, 4)
        self.layout().addWidget(self.weather_label, 1, 0, 1, 4)
        self.layout().addWidget(self.system_label, 2, 0, 1, 4)
        self.layout().addWidget(self.hostname_label, 3, 0, 1, 4)
        self.layout().addWidget(self.distro_label, 4, 0, 1, 4)
        self.layout().addWidget(self.kernel_label, 5, 0, 1, 4)
        self.layout().addWidget(self.packages_label, 6, 0, 1, 4)
        self.layout().addWidget(self.uptime_label, 7, 0, 1, 4)
        self.layout().addWidget(self.boot_time_label, 8, 0, 1, 4)
        self.layout().addWidget(self.usages_label, 9, 0, 1, 4)
        self.layout().addWidget(self.cpu_label, 10, 0)
        self.layout().addWidget(self.disk_label, 10, 1)
        self.layout().addWidget(self.ram_label, 10, 2)
        self.layout().addWidget(self.swap_label, 10, 3)
        
        self.weather_thread = threading.Thread(target = self.get_weather, daemon = True)
        self.weather_thread.start()
        
        self.packages_thread = threading.Thread(target = self.get_packages, daemon = True)
        self.packages_thread.start()
        
        self.cpu_thread = threading.Thread(target = self.get_cpu, daemon = True)
        self.cpu_thread.start()
        
        if hasattr (psutil, "sensors_temperatures") and psutil.sensors_temperatures():
            self.temps_worked = True
            self.temps_grid = 11
            self.get_temps = psutil.sensors_temperatures()
            self.temps_labels[self.temps_number] = QLabel(parent = self, alignment = align_center, 
                                                          text = _('Temparatures'))
            self.temps_labels[self.temps_number].setStyleSheet("QLabel{font-size: 14pt; margin-top: 14px;}")
            self.layout().addWidget(self.temps_labels[self.temps_number], self.temps_grid, 0, 1, 4)
            for self.temps_hardware, self.temps_hardwares in self.get_temps.items():
                self.temps_grid += 1
                self.temps_number += 1
                self.temps_labels[self.temps_number] = QLabel(parent = self, alignment = align_center, 
                                  text = f"{_('Hardware')}: {self.temps_hardware}")
                if self.temps_number == 1:
                    self.temps_labels[self.temps_number].setStyleSheet("QLabel{font-size: 12pt;}")
                else:
                    self.temps_labels[self.temps_number].setStyleSheet("QLabel{font-size: 12pt; margin-top: 12px;}")
                self.layout().addWidget(self.temps_labels[self.temps_number], self.temps_grid, 0, 1, 4)
                for self.temps in self.temps_hardwares:
                    self.temps_grid  += 1
                    self.temps_number += 1
                    self.temps_labels[self.temps_number] = QLabel(parent = self, alignment = align_center, 
                                                                  text = f"{self.temps.label or self.temps_hardware}: {_('current')} = {self.temps.current} °C " 
                                                                  + f"{_('high')} = {self.temps.high} °C, {_('critical')} = {self.temps.critical} °C")
                    self.layout().addWidget(self.temps_labels[self.temps_number], self.temps_grid, 0, 1, 4)
        
        if hasattr (psutil, "sensors_fans") and psutil.sensors_fans():
            self.fans_worked = True
            if self.temps_worked == True:
                self.fans_grid = self.temps_grid + 1
            else:
                self.fans_grid = 11
            self.get_fans = psutil.sensors_fans()
            self.fans_labels[self.fans_number] = QLabel(parent = self, alignment = align_center, 
                                                        text = _('Fans'))
            self.fans_labels[self.fans_number].setStyleSheet("QLabel{font-size: 14pt; margin-top: 14px;}")
            self.layout().addWidget(self.fans_labels[self.fans_number], self.fans_grid, 0, 1, 4)
            for self.fans_hardware, self.fans_hardwares in self.get_fans.items():
                self.fans_grid += 1
                self.fans_number += 1
                self.fans_labels[self.fans_number] = QLabel(parent = self, alignment = align_center, 
                                                            text = f"{_('hardware')}: {self.fans_hardware}")
                if self.fans_number == 1:
                    self.fans_labels[self.fans_number].setStyleSheet("QLabel{font-size: 12pt;}")
                else:
                    self.fans_labels[self.fans_number].setStyleSheet("QLabel{font-size: 12pt; margin-top: 12px;}")
                self.layout().addWidget(self.fans_labels[self.fans_number], self.fans_grid, 0, 1, 4)
                for self.fans in self.fans_hardwares:
                    self.fans_grid += 1
                    self.fans_number += 1
                    self.fans_labels[self.fans_number] = QLabel(parent = self, alignment = align_center, 
                                                                text = f"{self.fans.label or self.fans_hardware}: {self.fans.current} RPM")
                    self.layout().addWidget(self.fans_labels[self.fans_number], self.fans_grid, 0, 1, 4)
        
        if hasattr (psutil, "sensors_battery") and psutil.sensors_battery():
            self.batt_worked = True
            if self.fans_worked == True:
                self.batt_grid = self.fans_grid + 1
            elif self.temps_worked == True:
                self.batt_grid = self.temps_grid + 1
            else:
                self.batt_grid = 10
            self.get_batt = psutil.sensors_battery()
            self.batt_labels[1] = QLabel(parent = self, alignment = align_center, 
                                                        text = _('Battery'))
            self.batt_labels[1].setStyleSheet("QLabel{font-size: 14pt; margin-top: 14px;}")
            self.batt_labels[2] = QLabel(parent = self, alignment = align_center, 
                                                            text = f"{_('Charge')}: {str(round(self.get_batt.percent, 2))}")
            if self.get_batt.power_plugged:
                self.batt_labels[3] = QLabel(parent = self, alignment = align_center,
                                             text = f"{_('Remaining')}: {str(datetime.timedelta(seconds = self.get_batt.secsleft))}")
                self.batt_labels[4] = QLabel(parent = self, alignment = align_center,
                                             text = f"{_('Status')}: "
                                             + str(_('Charging') if self.get_batt.percent < 100 else _('Charged')))
                self.batt_labels[5] = QLabel(parent = self, alignment = align_center,
                                             text = _('Plugged-in: Yes'))
            else:
                self.batt_labels[3] = QLabel(parent = self, alignment = align_center,
                                             text = f"{_('Remaining')}: {str(datetime.timedelta(seconds = self.get_batt.secsleft))}")
                self.batt_labels[4] = QLabel(parent = self, alignment = align_center,
                                             text = f"{_('Status')}: {_('Discharging')}")
                self.batt_labels[5] = QLabel(parent = self, alignment = align_center,
                                             text = _('Plugged-in: No'))
            self.layout().addWidget(self.batt_labels[1], self.batt_grid, 0, 1, 4)
            self.layout().addWidget(self.batt_labels[2], self.batt_grid + 1, 0, 1, 4)
            self.layout().addWidget(self.batt_labels[3], self.batt_grid + 2, 0, 1, 4)
            self.layout().addWidget(self.batt_labels[4], self.batt_grid + 3, 0, 1, 4)
            self.layout().addWidget(self.batt_labels[5], self.batt_grid + 4, 0, 1, 4)
        
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.refresh)
        self.timer.start()        
        
    def get_weather(self):
        self.weather_label.setText(f"{_('Weather forecast')}: "
                                   + subprocess.Popen(f'curl -H "Accept-{language}" wttr.in/?format="%l:+%C+%t+%w+%h+%M"', 
                                                      shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
                                   .communicate()[0])

    def get_packages(self): 
        if pkg_mngr.lower() == "apt":
            self.traditional_packages_cmd = 'dpkg --list | grep ^i | wc -l'
        elif pkg_mngr.lower() == "dnf5":
            self.traditional_packages_cmd = 'dnf5 list --installed | wc -l'
        elif pkg_mngr.lower() == "zypper":
            self.traditional_packages_cmd = 'zypper pa -i | wc -l'
        elif pkg_mngr.lower() == "pacman":
            self.traditional_packages_cmd = 'pacman -Q | wc -l'
        self.traditional_packages_num = (subprocess.Popen(self.traditional_packages_cmd,
                                                         shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
                                         .communicate()[0])
        self.flatpak_packages_num = (subprocess.Popen("flatpak list | wc -l",
                                                         shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
                                     .communicate()[0])
        self.packages_label.setText(f"{_('Number of packages')}: {self.traditional_packages_num} ({pkg_type}), {self.flatpak_packages_num} (Flatpak)".replace("\n", ""))
        
    def get_cpu(self):
        while True:
            self.cpu_label.setText(f"CPU: %{str(psutil.cpu_percent(4))}")
        
    def refresh(self):
        self.uptime_label.setText(f"{_('Uptime')}: "
                                + str(datetime.timedelta(seconds = float(os.popen('cat /proc/uptime').read().split()[0]))))
        self.disk_label.setText(f"Disk: %{str(psutil.disk_usage('/')[3])}")
        self.ram_label.setText(f"RAM: %{str(psutil.virtual_memory().percent)}")
        self.swap_label.setText(f"{_('Swap')}: %{str(psutil.swap_memory().percent)}")
        
        if hasattr (psutil, "sensors_temperatures") and psutil.sensors_temperatures():
            self.get_temps = psutil.sensors_temperatures()
            for self.temps_hardware, self.temps_hardwares in self.get_temps.items():
                self.temps_labels[self.temps_number].setText(f"{_('Hardware')}: {self.temps_hardware}")
                for self.temps in self.temps_hardwares:
                    self.temps_labels[self.temps_number].setText(f"{self.temps.label or self.temps_hardware}: {_('current')} = {self.temps.current} °C " 
                                                                 + f"{_('high')} = {self.temps.high} °C, {_('critical')} = {self.temps.critical} °C")
        
        if hasattr (psutil, "sensors_fans") and psutil.sensors_fans():
            self.get_fans = psutil.sensors_fans()
            for self.fans_hardware, self.fans_hardwares in self.get_fans.items():
                self.fans_labels[self.fans_number].setText(f"{_('Hardware')}: {self.fans_hardware}")
                for self.fans in self.fans_hardwares:
                    self.fans_labels[self.fans_number].setText(f"{self.fans.label or self.fans_hardware}: {self.fans.current} RPM")
        
        if hasattr (psutil, "sensors_battery") and psutil.sensors_battery():
            self.get_batt = psutil.sensors_battery()
            self.batt_labels[2].setText(f"{_('Charge')}: {str(round(self.get_batt.percent, 2))}")
            if self.get_batt.power_plugged:
                self.batt_labels[3].setText(f"{_('Remaining')}: {str(datetime.timedelta(seconds = self.get_batt.secsleft))}")
                self.batt_labels[4].setText(f"{_('Status')}: "
                                            + str(_('Charging') if self.get_batt.percent < 100 else _('Charged')))
                self.batt_labels[5].setText(_('Plugged-in: Yes'))
            else:
                self.batt_labels[3].setText(f"{_('Remaining')}: {str(datetime.timedelta(seconds = self.get_batt.secsleft))}")
                self.batt_labels[4].setText(f"{_('Status')}: {_('Discharging')}")
                self.batt_labels[5].setText( _('Plugged-in: No'))
            

class NotesAndDocuments(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
class Store(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
class Tools(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

            
class MainWindow(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        global statusbar
        
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout(self.widget))
        
        self.tabview = QTabWidget(self.widget)
        
        self.startup = QScrollArea(self)
        self.startup.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.startup.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.startup.setWidgetResizable(True)
        self.startup.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.startup.setWidget(Startup(parent = self))
        self.tabview.addTab(self.startup, 
                            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon)), _("Startup"))
        
        self.tabview.addTab(NotesAndDocuments(), 
                            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)), _("Notes and Documents"))
        
        self.tabview.addTab(Store(parent = self), 
                            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), _("Store"))
        
        self.tabview.addTab(Tools(parent = self), 
                            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DriveCDIcon)), _("Tools"))

        
        self.file = self.menuBar().addMenu(_('File'))
        self.file.addAction(_('Quit'), QKeySequence("Ctrl+Q"), lambda: sys.exit(0))
        self.file.addAction(_('New'), QKeySequence("Ctrl+N"), lambda: subprocess.Popen(__file__))
        
        self.manage = self.menuBar().addMenu(_('Manage'))
        self.manage.addAction(_('Upgrade'), lambda: Sidebar().go_update(self))
        self.manage.addAction(_('Reset'), lambda: Sidebar().reset(self))
        self.manage.addAction(_('Remove'), lambda: Sidebar().remove(self))
        
        self.startup = self.menuBar().addMenu(_('Startup'))
        self.startup.addAction(_('Startup'))
        
        self.nad = self.menuBar().addMenu(_('Notes and Documents'))
        self.nad.addAction(_('Notes and Documents'))
        
        self.store = self.menuBar().addMenu(_('Store'))
        self.store.addAction(_('Packages'))
        self.store.addAction(_('Desktop Environments, Window Managers and Compotisors'))
        self.store.addAction(_('Scripts'))
        self.store.addAction(_('Systemd Services'))
        
        self.tools = self.menuBar().addMenu(_('Tools'))
        self.tools.addAction(_('About Some Distributions'))
        self.tools.addAction(_('Configure .bashrc and .zshrc'))
        self.tools.addAction(_('Calculator'))

        self.about = self.menuBar().addMenu(_('About'))
        self.about.addAction(_('Changelogs'), lambda: Sidebar().changelogs(self))
        self.about.addAction(_('License'), lambda: Sidebar().license(self))
        
        self.dock = QDockWidget(self)
        self.dock.setFixedWidth(144)
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dock.setWidget(Sidebar(parent = self))
        
        statusbar = QStatusBar(self)

        self.setWindowTitle(f"GrelinTB")
        self.setGeometry(0, 0, 960, 540)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.setCentralWidget(self.widget)
        self.setStatusBar(statusbar)
        self.widget.layout().addWidget(self.tabview)


if __name__ == "__main__":
    application = QApplication(sys.argv)
    application.setWindowIcon(QIcon("/home/mukonqi/works/grelintb/app/icon.png"))

    window = MainWindow()
    window.show()

    application.exec()