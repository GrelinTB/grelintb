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
import sqlite3


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
        

class Startup(QScrollArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setWidget(QWidget(parent = self))
        self.widget().setLayout(QGridLayout(self.widget()))
        
        self.temps_worked = False
        self.temps_labels = {}
        self.temps_number = 0
        self.fans_worked = False
        self.fans_labels = {}
        self.fans_number = 0
        self.batt_worked = False
        self.batt_labels = {}
        
        self.welcome_label = QLabel(parent = self.widget(), alignment = align_center, 
                                    text = f"{_('Hello')} {username}!")
        self.weather_label = QLabel(parent = self.widget(), alignment = align_center, 
                                    text = f"{_('Weather forecast')}: {_('Getting')}")
        self.system_label = QLabel(parent = self.widget(), alignment = align_center, 
                                   text = _('System'))
        self.hostname_label = QLabel(parent = self.widget(), alignment = align_center, 
                                     text = f"{_('Hostname')}: {socket.gethostname()}")
        self.distro_label = QLabel(parent = self.widget(), alignment = align_center, 
                                   text = f"{_('Distrubiton')}: {distro.name(pretty = True)}")
        self.kernel_label = QLabel(parent = self.widget(), alignment = align_center, 
                                   text = f"{_('Kernel')}: {platform.platform()}")
        self.packages_label = QLabel(parent = self.widget(), alignment = align_center, 
                                     text = f"{_('Number of packages')}: ")
        self.uptime_label = QLabel(parent = self.widget(), alignment = align_center, 
                                   text = f"{_('Uptime')}: "
                                   + str(datetime.timedelta(seconds = float(os.popen('cat /proc/uptime').read().split()[0]))))
        self.boot_time_label = QLabel(parent = self.widget(), alignment = align_center, 
                                      text = f"{_('Boot time')}: "
                                      + datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%d.%m.%Y %H:%M:%S'))
        self.usages_label = QLabel(parent = self.widget(), alignment = align_center, 
                                   text = _('Usages'))
        self.cpu_label = QLabel(parent = self.widget(), alignment = align_center, 
                                text = f"CPU: {_('Getting')}")
        self.disk_label = QLabel(parent = self.widget(), alignment = align_center, 
                                 text = f"Disk: %{str(psutil.disk_usage('/')[3])}")
        self.ram_label = QLabel(parent = self.widget(), alignment = align_center, 
                                text = f"RAM: %{str(psutil.virtual_memory().percent)}")
        self.swap_label = QLabel(parent = self.widget(), alignment = align_center, 
                                 text = f"{_('Swap')}: %{str(psutil.swap_memory().percent)}")
        
        self.welcome_label.setStyleSheet("QLabel{font-size: 14pt;}")
        self.system_label.setStyleSheet("QLabel{font-size: 14pt; margin-top: 14px;}")
        self.usages_label.setStyleSheet("QLabel{font-size: 14pt; margin-top: 14px;}")
        
        self.widget().layout().addWidget(self.welcome_label, 0, 0, 1, 4)
        self.widget().layout().addWidget(self.weather_label, 1, 0, 1, 4)
        self.widget().layout().addWidget(self.system_label, 2, 0, 1, 4)
        self.widget().layout().addWidget(self.hostname_label, 3, 0, 1, 4)
        self.widget().layout().addWidget(self.distro_label, 4, 0, 1, 4)
        self.widget().layout().addWidget(self.kernel_label, 5, 0, 1, 4)
        self.widget().layout().addWidget(self.packages_label, 6, 0, 1, 4)
        self.widget().layout().addWidget(self.uptime_label, 7, 0, 1, 4)
        self.widget().layout().addWidget(self.boot_time_label, 8, 0, 1, 4)
        self.widget().layout().addWidget(self.usages_label, 9, 0, 1, 4)
        self.widget().layout().addWidget(self.cpu_label, 10, 0)
        self.widget().layout().addWidget(self.disk_label, 10, 1)
        self.widget().layout().addWidget(self.ram_label, 10, 2)
        self.widget().layout().addWidget(self.swap_label, 10, 3)
        
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
            self.temps_labels[self.temps_number] = QLabel(parent = self.widget(), alignment = align_center, 
                                                          text = _('Temparatures'))
            self.temps_labels[self.temps_number].setStyleSheet("QLabel{font-size: 14pt; margin-top: 14px;}")
            self.widget().layout().addWidget(self.temps_labels[self.temps_number], self.temps_grid, 0, 1, 4)
            for self.temps_hardware, self.temps_hardwares in self.get_temps.items():
                self.temps_grid += 1
                self.temps_number += 1
                self.temps_labels[self.temps_number] = QLabel(parent = self.widget(), alignment = align_center, 
                                  text = f"{_('Hardware')}: {self.temps_hardware}")
                if self.temps_number == 1:
                    self.temps_labels[self.temps_number].setStyleSheet("QLabel{font-size: 12pt;}")
                else:
                    self.temps_labels[self.temps_number].setStyleSheet("QLabel{font-size: 12pt; margin-top: 12px;}")
                self.widget().layout().addWidget(self.temps_labels[self.temps_number], self.temps_grid, 0, 1, 4)
                for self.temps in self.temps_hardwares:
                    self.temps_grid  += 1
                    self.temps_number += 1
                    self.temps_labels[self.temps_number] = QLabel(parent = self.widget(), alignment = align_center, 
                                                                  text = f"{self.temps.label or self.temps_hardware}: {_('Current')} = {self.temps.current} °C, " 
                                                                  + f"{_('high')} = {self.temps.high} °C, {_('critical')} = {self.temps.critical} °C")
                    self.widget().layout().addWidget(self.temps_labels[self.temps_number], self.temps_grid, 0, 1, 4)
        
        if hasattr (psutil, "sensors_fans") and psutil.sensors_fans():
            self.fans_worked = True
            if self.temps_worked == True:
                self.fans_grid = self.temps_grid + 1
            else:
                self.fans_grid = 11
            self.get_fans = psutil.sensors_fans()
            self.fans_labels[self.fans_number] = QLabel(parent = self.widget(), alignment = align_center, 
                                                        text = _('Fans'))
            self.fans_labels[self.fans_number].setStyleSheet("QLabel{font-size: 14pt; margin-top: 14px;}")
            self.widget().layout().addWidget(self.fans_labels[self.fans_number], self.fans_grid, 0, 1, 4)
            for self.fans_hardware, self.fans_hardwares in self.get_fans.items():
                self.fans_grid += 1
                self.fans_number += 1
                self.fans_labels[self.fans_number] = QLabel(parent = self.widget(), alignment = align_center, 
                                                            text = f"{_('hardware')}: {self.fans_hardware}")
                if self.fans_number == 1:
                    self.fans_labels[self.fans_number].setStyleSheet("QLabel{font-size: 12pt;}")
                else:
                    self.fans_labels[self.fans_number].setStyleSheet("QLabel{font-size: 12pt; margin-top: 12px;}")
                self.widget().layout().addWidget(self.fans_labels[self.fans_number], self.fans_grid, 0, 1, 4)
                for self.fans in self.fans_hardwares:
                    self.fans_grid += 1
                    self.fans_number += 1
                    self.fans_labels[self.fans_number] = QLabel(parent = self.widget(), alignment = align_center, 
                                                                text = f"{self.fans.label or self.fans_hardware}: {self.fans.current} RPM")
                    self.widget().layout().addWidget(self.fans_labels[self.fans_number], self.fans_grid, 0, 1, 4)
        
        if hasattr (psutil, "sensors_battery") and psutil.sensors_battery():
            self.batt_worked = True
            if self.fans_worked == True:
                self.batt_grid = self.fans_grid + 1
            elif self.temps_worked == True:
                self.batt_grid = self.temps_grid + 1
            else:
                self.batt_grid = 10
            self.get_batt = psutil.sensors_battery()
            self.batt_labels[1] = QLabel(parent = self.widget(), alignment = align_center, 
                                                        text = _('Battery'))
            self.batt_labels[1].setStyleSheet("QLabel{font-size: 14pt; margin-top: 14px;}")
            self.batt_labels[2] = QLabel(parent = self.widget(), alignment = align_center, 
                                                            text = f"{_('Charge')}: {str(round(self.get_batt.percent, 2))}")
            if self.get_batt.power_plugged:
                self.batt_labels[3] = QLabel(parent = self.widget(), alignment = align_center,
                                             text = f"{_('Remaining')}: {str(datetime.timedelta(seconds = self.get_batt.secsleft))}")
                self.batt_labels[4] = QLabel(parent = self.widget(), alignment = align_center,
                                             text = f"{_('Status')}: "
                                             + str(_('Charging') if self.get_batt.percent < 100 else _('Charged')))
                self.batt_labels[5] = QLabel(parent = self.widget(), alignment = align_center,
                                             text = _('Plugged-in: Yes'))
            else:
                self.batt_labels[3] = QLabel(parent = self.widget(), alignment = align_center,
                                             text = f"{_('Remaining')}: {str(datetime.timedelta(seconds = self.get_batt.secsleft))}")
                self.batt_labels[4] = QLabel(parent = self.widget(), alignment = align_center,
                                             text = f"{_('Status')}: {_('Discharging')}")
                self.batt_labels[5] = QLabel(parent = self.widget(), alignment = align_center,
                                             text = _('Plugged-in: No'))
            self.widget().layout().addWidget(self.batt_labels[1], self.batt_grid, 0, 1, 4)
            self.widget().layout().addWidget(self.batt_labels[2], self.batt_grid + 1, 0, 1, 4)
            self.widget().layout().addWidget(self.batt_labels[3], self.batt_grid + 2, 0, 1, 4)
            self.widget().layout().addWidget(self.batt_labels[4], self.batt_grid + 3, 0, 1, 4)
            self.widget().layout().addWidget(self.batt_labels[5], self.batt_grid + 4, 0, 1, 4)
        
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.go_refresh)
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

    def go_refresh(self):
        self.refresh_thread = threading.Thread(target = self.refresh, daemon = True)
        self.refresh_thread.start()
            

class Notes(QTabWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.setStatusTip(_('Tip: For a new note, just type a name below.'))
        
        with sqlite3.connect("notes.db") as self.notes_db_init:
            self.sql_init = """
            CREATE TABLE IF NOT EXISTS notes (
                name TEXT NOT NULL PRIMARY KEY,
                content TEXT,
                backup TEXT, 
                created TEXT NOT NULL,
                edited TEXT
            );"""
            self.notes_cur_init = self.notes_db_init.cursor()
            self.notes_cur_init.execute(self.sql_init)
            self.notes_db_init.commit()
        
        self.widgets = {}
        self.textedits = {}
        self.contents = {}
        self.outputs = {}
        self.buttons = {}
        self.are_news = {}
        
        self.home = QWidget(self)
        self.home.setLayout(QGridLayout(self.home))
        
        self.main = QWidget(self.home)
        self.main.setLayout(QVBoxLayout(self.main))
        
        self.details = QWidget(self.home)
        self.details.setLayout(QHBoxLayout(self.details))
        self.detail1 = QLabel(parent = self.details, alignment = align_center, 
                                    text = _('Backed up: '))
        self.detail2 = QLabel(parent = self.details, alignment = align_center, 
                                    text = _('Created: '))
        self.detail3 = QLabel(parent = self.details, alignment = align_center, 
                                    text = _('Modefied: '))
        
        self.list_view = QListView(self.main)
        self.list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.list_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.list_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        
        self.model = QStringListModel()
        self.list_view.setModel(self.model)

        self.list_view.selectionModel().selectionChanged.connect(
                                                                 lambda: self.insert(self.list_view.model().itemData(self.list_view.currentIndex())))

        self.side = QWidget(self.home)
        self.side.setFixedWidth(144)
        self.side.setLayout(QVBoxLayout(self.side))
        
        self.entry = QLineEdit(parent = self)
        self.entry.setPlaceholderText(_('Type a note name.'))
        
        self.opener = QPushButton(parent = self.side, text = _('Open note'))
        self.opener.clicked.connect(lambda: self.open(self.entry.text()))
        
        self.renamer = QPushButton(parent = self.side, text = _('Rename note'))
        self.renamer.clicked.connect(self.rename)
        
        self.deleter = QPushButton(parent = self.side, text = _('Delete content'))
        self.deleter.clicked.connect(self.delete)

        self.backup_shower = QPushButton(parent = self.side, text = _('Show backup'))
        self.backup_shower.clicked.connect(self.show_backup)

        self.backup_loader = QPushButton(parent = self.side, text = _('Load backup'))
        self.backup_loader.clicked.connect(self.load_backup)
        
        self.backup_deleter = QPushButton(parent = self.side, text = _('Delete backup'))
        self.backup_deleter.clicked.connect(self.delete_backup)
        
        self.details.layout().addWidget(self.detail1)
        self.details.layout().addWidget(self.detail2)
        self.details.layout().addWidget(self.detail3)
        self.main.layout().addWidget(self.details)
        self.main.layout().addWidget(self.list_view)
        self.side.layout().addWidget(self.entry)
        self.side.layout().addWidget(self.opener)
        self.side.layout().addWidget(self.renamer)
        self.side.layout().addWidget(self.deleter)
        self.side.layout().addWidget(self.backup_shower)
        self.side.layout().addWidget(self.backup_loader)
        self.side.layout().addWidget(self.backup_deleter)
        self.home.layout().addWidget(self.main, 0, 0)
        self.home.layout().addWidget(self.side, 0, 1)
        
        self.addTab(self.home, _('Home'))
        self.setTabsClosable(True)
        self.setMovable(True)
        
        self.refresh()
        
        self.tabCloseRequested.connect(self.close)
         
    def close(self, index):
        if index != self.indexOf(self.home):
            self.removeTab(index)
         
    def insert(self, name):
        with sqlite3.connect("notes.db") as self.notes_db_insert:
            self.notes_cur_insert = self.notes_db_insert.cursor()
            self.notes_cur_insert.execute(f"select * from notes where name = '{name[0]}'")
            self.fetch_insert = self.notes_cur_insert.fetchone()
        self.entry.setText(self.fetch_insert[0])
        if self.fetch_insert[2] != "":
            self.detail1.setText(f"{_('Backed up')}: Yes")
        else:
            self.detail1.setText(f"{_('Backed up')}: No")
        self.detail2.setText(f"{_('Created')}: {self.fetch_insert[3]}")
        self.detail3.setText(f"{_('Edited')}: {self.fetch_insert[4]}")
    
    def refresh(self):
        self.list = []
        
        with sqlite3.connect("notes.db") as self.notes_db_refresh:
            self.notes_cur_refresh = self.notes_db_refresh.cursor()
            self.notes_cur_refresh.execute("select name from notes")
            self.fetch_refresh = self.notes_cur_refresh.fetchall()
        
        for i in range(0, len(self.fetch_refresh)):
            self.list.append(self.fetch_refresh[i][0])

        self.model.setStringList(self.list)
        
    def control(self, name):
        try:
            with sqlite3.connect("notes.db") as self.notes_db_control:
                self.notes_cur_control = self.notes_db_control.cursor()
                self.notes_cur_control.execute(f"select * from notes where name = '{name}'")
                self.fetch_control = self.notes_cur_control.fetchone()[0]
            return True
        except TypeError as e:
            QMessageBox.critical(self, _('Error'), _(f'There is note note called {name}.'))
            return False
            
    def save(self, name, content, date):
        if self.control(name) == False:
            return
        
        try:
            with sqlite3.connect("notes.db") as self.notes_db_save1:
                self.notes_cur_save1 = self.notes_db_save1.cursor()
                self.notes_cur_save1.execute(f"select content from notes where name = '{name}'")
                self.fetch_save1 = self.notes_cur_save1.fetchone()[0]
            
            with sqlite3.connect("notes.db") as self.notes_db_save2:
                self.sql_save2 = f"""update notes set content = '{content}', backup = '{self.fetch_save1}',
                edited = '{date}' where name = '{name}'"""
                self.notes_cur_save2 = self.notes_db_save2.cursor()
                self.notes_cur_save2.execute(self.sql_save2)
                self.notes_db_save2.commit()

        except TypeError:
            with sqlite3.connect("notes.db") as self.notes_db_save3:
                self.sql_save3 = f"""insert into notes (name, content, backup, created, edited) 
                values ('{name}', '{content}', '', '{date}', '{date}')"""
                self.notes_cur_save3 = self.notes_db_save3.cursor()
                self.notes_cur_save3.execute(self.sql_save3)
                self.notes_db_save3.commit()
    
        with sqlite3.connect("notes.db") as self.notes_db_save4:
            self.notes_cur_save4 = self.notes_db_save4.cursor()
            self.notes_cur_save4.execute(f"select content from notes where name = '{name}'")
            self.fetch_save4 = self.notes_cur_save4.fetchone()[0]

        if self.fetch_save4 == content:
            QMessageBox.information(self, _('Successful'), _(f'Note {name} saved.'))
            self.refresh()

        else:
            QMessageBox.critical(self, _('Error'), _(f'Failed to save note {name}.'))
    
    def open(self, name):
        if name == "" or name == None:
            QMessageBox.critical(self, _('Error'), _(f'Note name can not be blank.'))
            return
            
        with sqlite3.connect("notes.db") as self.notes_db_open:
            self.notes_cur_open = self.notes_db_open.cursor()
            self.notes_cur_open.execute(f"select content from notes where name = '{name}'")
            
            self.widgets[name] = QWidget(self)
            self.widgets[name].setLayout(QVBoxLayout(self.widgets[name]))
            self.textedits[name] = QWidget(self.widgets[name])
            self.textedits[name].setLayout(QHBoxLayout(self.textedits[name]))
            
            self.contents[name] = QTextEdit(parent = self.textedits[name])
            self.outputs[name] = QTextEdit(parent = self.textedits[name], readOnly = True)
            self.contents[name].textChanged.connect(
                lambda name = name: self.outputs[name].setMarkdown(self.contents[name].toPlainText()))
            
            self.buttons[name] = QPushButton(parent = self.widgets[name], text = _('Save'))
            self.buttons[name].clicked.connect(lambda: self.save(name,
                                                                 self.contents[name].toPlainText(),
                                                                 datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            
            self.textedits[name].layout().addWidget(self.contents[name])
            self.textedits[name].layout().addWidget(self.outputs[name])
            self.widgets[name].layout().addWidget(self.textedits[name])
            self.widgets[name].layout().addWidget(self.buttons[name])
            
            try:
                self.fetch_open = self.notes_cur_open.fetchone()[0]
                self.contents[name].setPlainText(self.fetch_open)
                self.outputs[name].setMarkdown(self.fetch_open)
            except TypeError:
                self.are_news[name] = True

            self.addTab(self.widgets[name], name)
            self.setCurrentWidget(self.widgets[name])
    
    def rename(self):
        self.old_name = self.entry.text()
        
        if self.control(self.old_name) == False:
            return
        
        self.new_name, self.completed = QInputDialog.getText(self, f"Rename {self.old_name} Note", f"Please enter a new name for {self.old_name} below.")
        if self.new_name != "" and self.new_name != None and self.completed == True:
            with sqlite3.connect("notes.db") as self.notes_db_rename1:
                self.sql_rename1 = f"update notes set name = '{self.new_name}' where name = '{self.old_name}'"
                self.notes_cur_rename1 = self.notes_db_rename1.cursor()
                self.notes_cur_rename1.execute(self.sql_rename1)
                self.notes_db_rename1.commit()

            try:
                with sqlite3.connect("notes.db") as self.notes_db_rename2:
                    self.notes_cur_rename2 = self.notes_db_rename2.cursor()
                    self.notes_cur_rename2.execute(f"select * from notes where name = '{self.new_name}'")
                    self.notes_db_rename2.commit()
                
                QMessageBox.information(self, _('Successful'), _(f'Note {self.old_name} renamed as {self.new_name}.'))
                self.refresh()
            except TypeError:
                QMessageBox.critical(self, _('Error'), _(f'Failed to rename note {self.old_name}.'))
        else:
            QMessageBox.critical(self, _('Error'), _(f'Failed to rename note {self.old_name}.'))
    
    def delete(self):
        self.delete_name = self.entry.text()
        
        if self.control(self.delete_name) == False:
            return
        
        with sqlite3.connect("notes.db") as self.notes_db_delete1:
            self.notes_cur_delete1 = self.notes_db_delete1.cursor()
            self.notes_cur_delete1.execute(f"select content from notes where name = '{self.delete_name}'")
            self.fetch_delete1 = self.notes_cur_delete1.fetchone()[0]
        
        with sqlite3.connect("notes.db") as self.notes_db_delete2:
            self.notes_cur_delete2 = self.notes_db_delete2.cursor()
            self.notes_cur_delete2.execute(f"update notes set content = '', backup = '{self.fetch_delete1}' where name = '{self.delete_name}'")
            self.notes_db_delete2.commit()
        
        with sqlite3.connect("notes.db") as self.notes_db_delete3:
            self.notes_cur_delete3 = self.notes_db_delete3.cursor()
            self.notes_cur_delete3.execute(f"select content from notes where name = '{self.delete_name}'")
            self.fetch_delete3 = self.notes_cur_delete3.fetchone()[0]
    
        if self.fetch_delete3 != None:
            QMessageBox.information(self, _('Successful'), _(f'Content of note {self.delete_name} deleted.'))
            self.refresh()
        else:
            QMessageBox.critical(self, _('Error'), _(f'Failed to delete content of {self.delete_name} note.'))
    
    def show_backup(self):
        pass
    
    def load_backup(self):
        pass
    
    def delete_backup(self):
        pass
        
class Store(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
class Tools(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

            
class MainWindow(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout(self.widget))

        self.tabview = QTabWidget(self.widget)
        self.tabview.addTab(Startup(parent = self),
                            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon)), _("Startup"))
        
        self.tabview.addTab(Notes(parent = self), 
                            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)), _("Notes"))
        
        self.tabview.addTab(Store(parent = self), 
                            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)), _("Store"))
        
        self.tabview.addTab(Tools(parent = self), 
                            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DriveCDIcon)), _("Tools"))

        self.dock = QDockWidget(self)
        self.dock.setFixedWidth(144)
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.dock.setWidget(Sidebar(parent = self))
        
        self.statusbar = QStatusBar(self)
        self.setStatusTip(_('Copyright (C) 2024 MuKonqi (Muhammed S.), licensed under GPL v3 or later'))
        
        self.file = self.menuBar().addMenu(_('File'))
        self.file.addAction(_('Quit'), QKeySequence("Ctrl+Q"), lambda: sys.exit(0))
        self.file.addAction(_('New'), QKeySequence("Ctrl+N"), lambda: subprocess.Popen(__file__))
        
        self.sidebar = self.menuBar().addMenu(_('Sidebar'))
        self.sidebar.addAction(_('Show Sidebar'), lambda: self.restoreDockWidget(self.dock))
        self.sidebar.addAction(_('Close Sidebar'), lambda: self.removeDockWidget(self.dock))
        self.sidebar.addAction(_('Changelogs'), lambda: Sidebar().changelogs(self))
        self.sidebar.addAction(_('License'), lambda: Sidebar().license(self))
        self.sidebar.addAction(_('Upgrade'), lambda: Sidebar().go_update(self))
        self.sidebar.addAction(_('Reset'), lambda: Sidebar().reset(self))
        self.sidebar.addAction(_('Remove'), lambda: Sidebar().remove(self))
        
        self.startup = self.menuBar().addMenu(_('Startup'))
        self.startup.addAction(_('Startup'))
        
        self.notes = self.menuBar().addMenu(_('Notes'))
        self.notes.addAction(_('Notes'))
        
        self.store = self.menuBar().addMenu(_('Store'))
        self.store.addAction(_('Packages'))
        self.store.addAction(_('Desktop Environments, Window Managers and Compotisors'))
        self.store.addAction(_('Scripts'))
        self.store.addAction(_('Systemd Services'))
        
        self.tools = self.menuBar().addMenu(_('Tools'))
        self.tools.addAction(_('About Some Distributions'))
        self.tools.addAction(_('Configure .bashrc and .zshrc'))
        self.tools.addAction(_('Calculator'))
        
        self.setWindowTitle(f"GrelinTB")
        self.setGeometry(0, 0, 960, 540)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.setCentralWidget(self.widget)
        self.setStatusBar(self.statusbar)
        self.widget.layout().addWidget(self.tabview)


if __name__ == "__main__":
    application = QApplication(sys.argv)
    application.setWindowIcon(QIcon("/home/mukonqi/works/grelintb/app/icon.png"))

    window = MainWindow()
    window.show()

    application.exec()