####################################################################################################
#
# CodeReview - A Python/Qt Git GUI
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If
# not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################
#
#                                              Audit
#
# - 21/08/2014 simplify ?
#
# - 13/02/2013 Fabrice
#   - add dict interface ?
#   - property
#
####################################################################################################

####################################################################################################

import os
import platform
import sys

from PyQt5 import QtCore, QtWidgets

####################################################################################################

from CodeReview.Tools.EnumFactory import EnumFactory
from CodeReview.Math.Functions import rint

####################################################################################################

platform_enum = EnumFactory('PlatformEnum', ('linux', 'windows', 'macosx'))

####################################################################################################

class Platform(object):

    ##############################################

    def __init__(self):

        self.python_version = platform.python_version()
        self.qt_version = QtCore.QT_VERSION_STR
        self.pyqt_version = QtCore.PYQT_VERSION_STR

        self.os = self._get_os()
        self.node = platform.node()
        self.distribution = ' '.join(platform.dist())
        self.machine = platform.machine()
        self.architecture = platform.architecture()[0]

        # CPU
        self.cpu = self._get_cpu()
        self.number_of_cores = self._get_number_of_cores()
        self.cpu_khz = self._get_cpu_khz()
        self.cpu_mhz = rint(self._get_cpu_khz()/float(1000))
        
        # RAM
        self.memory_size_kb = self._get_memory_size_kb()
        self.memory_size_mb = rint(self.memory_size_kb/float(1024))
        
        # Screen
        try:
            application = QtWidgets.QApplication.instance()
            self.desktop = application.desktop()
            self.number_of_screens = self.desktop.screenCount() 
        except:
            self.desktop = None
            self.number_of_screens = 0
        self.screens = []
        for i in range(self.number_of_screens):
            self.screens.append(Screen(self, i))

    ##############################################

    def _get_os(self):

        if os.name in 'nt':
            return platform_enum.windows
        elif sys.platform in 'linux2':
            return platform_enum.linux
        else:
            raise RuntimeError('unknown platform')

    ##############################################

    def _get_cpu(self):

        if self.os == platform_enum.linux:
            with open('/proc/cpuinfo', 'rt') as cpuinfo:
                for line in cpuinfo:
                    if 'model name' in line:
                        s = line.split(':')[1]
                        return s.strip().rstrip()

        elif self.os == platform_enum.windows:
            raise NotImplementedError

    ##############################################

    def _get_number_of_cores(self):

        if self.os == platform_enum.linux:
            number_of_cores = 0
            with open('/proc/cpuinfo', 'rt') as cpuinfo:
                for line in cpuinfo:
                    if 'processor' in line:
                        number_of_cores += 1
            return number_of_cores

        elif self.os == platform_enum.windows:

            return int(os.getenv('NUMBER_OF_PROCESSORS'))

    ##############################################

    def _get_cpu_khz(self):

        if self.os == platform_enum.linux:
            with open('/proc/cpuinfo', 'rt') as cpuinfo:
                for line in cpuinfo:
                    if 'cpu MHz' in line:
                        s = line.split(':')[1]
                        return int(1000 * float(s))

        if self.os == platform_enum.windows:
            raise NotImplementedError

    ##############################################

    def _get_memory_size_kb(self):

        if self.os == platform_enum.linux:
            with open('/proc/meminfo', 'rt') as cpuinfo:
                for line in cpuinfo:
                    if 'MemTotal' in line:
                        s = line.split(':')[1][:-3]
                        return int(s)

        if self.os == platform_enum.windows:
            raise NotImplementedError

    ##############################################

    def __str__(self):
      
        message_template = '''
Platform %(node)s
  Hardware:
    Machine: %(machine)s
    Architecture: %(architecture)s
    CPU: %(cpu)s
      Number of Cores: %(number_of_cores)u
      CPU Frequence: %(cpu_mhz)u MHz
    Memory: %(memory_size_mb)u MB
   Number of Screens: %(number_of_screens)u
'''
        message = message_template % self.__dict__

        for screen in self.screens:
            message += str(screen)
        
        message_template = '''
  Software Versions:
    OS: %(os)s
    Distribution: %(distribution)s
    Python: %(python_version)s
    Qt: %(qt_version)s
    PyQt: %(pyqt_version)s
'''
        message += message_template % self.__dict__
        
        return message

####################################################################################################

class Screen(object):

    ##############################################

    def __init__(self, platform_obj, screen_id):

        self.screen_id = screen_id

        qt_screen_geometry = platform_obj.desktop.screenGeometry(screen_id)
        self.screen_width, self.screen_height = qt_screen_geometry.width(), qt_screen_geometry.height()

        widget = platform_obj.desktop.screen(screen_id)
        self.dpi =  widget.physicalDpiX(), widget.physicalDpiY() 

        # qt_available_geometry = self.desktop.availableGeometry(screen_id)

    ##############################################

    def __str__(self):

        message_template = """
    Screen %(screen_id)u
     geometry   %(screen_width)ux%(screen_height)u px
     resolution %(dpi)s dpi
"""
        
        return message_template % self.__dict__

####################################################################################################
#
# End
#
####################################################################################################
