###################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2019 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

__all__ = ['QmlApplication', 'Application']

####################################################################################################

from pathlib import Path
import argparse
import logging
import sys
import traceback

# Fixme:
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    Qt, QTimer, QUrl
)
from QtShim.QtGui import QGuiApplication, QIcon
from QtShim.QtQml import qmlRegisterType, QQmlApplicationEngine
# Fixme: PYSIDE-574 qmlRegisterSingletonType and qmlRegisterUncreatableType missing in QtQml
from QtShim.QtQml import qmlRegisterUncreatableType
from QtShim.QtQuick import QQuickPaintedItem, QQuickView
# from QtShim.QtQuickControls2 import QQuickStyle

from CodeReview.Common.ArgparseAction import PathAction
from CodeReview.Common.Platform2 import QtPlatform
from .ApplicationMetadata import ApplicationMetadata
from .ApplicationSettings import ApplicationSettings, Shortcut
from .KeySequenceEditor import KeySequenceEditor

from .rcc import CodeReviewRessource

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlApplication(QObject):

    """Class to implement a Qt QML Application."""

    show_message = Signal(str) # message
    show_error = Signal(str, str) # message backtrace

    _logger = _module_logger.getChild('QmlApplication')

    ##############################################

    def __init__(self, application):

        super().__init__()

        self._application = application

    ##############################################

    def notify_message(self ,message):
        self.show_message.emit(str(message))

    def notify_error(self, message):
        backtrace_str = traceback.format_exc()
        self.show_error.emit(str(message), backtrace_str)

    ##############################################

    @Property(str, constant=True)
    def application_name(self):
        return ApplicationMetadata.name

    @Property(str, constant=True)
    def application_url(self):
        return ApplicationMetadata.url

    @Property(str, constant=True)
    def about_message(self):
        return ApplicationMetadata.about_message()

####################################################################################################

# Fixme: why not derive from QGuiApplication ???
class Application(QObject):

    """Class to implement a Qt Application."""

    instance = None

    QmlApplication_CLS = QmlApplication

    _logger = _module_logger.getChild('Application')

    ##############################################

    # Fixme: Singleton

    @classmethod
    def create(cls, *args, **kwargs):

        if cls.instance is not None:
            raise NameError('Instance exists')

        cls.instance = cls(*args, **kwargs)
        return cls.instance

    ##############################################

    def __init__(self):

        self._logger.info('Ctor')

        super().__init__()

        QtCore.qInstallMessageHandler(self._message_handler)

        self._parse_arguments()

        # For Qt Labs Platform native widgets
        # self._application = QGuiApplication(sys.argv)
        # use QCoreApplication::instance() to get instance
        self._application = QApplication(sys.argv)
        self._application.main = self
        self._init_application()

        self._engine = QQmlApplicationEngine()
        self._qml_application = self.QmlApplication_CLS(self)
        self._application.qml_main = self._qml_application

        self._platform = QtPlatform()
        # self._logger.info('\n' + str(self._platform))

        #! self._load_translation()
        self.register_qml_types()
        self._set_context_properties()
        self._load_qml_main()

        # self._run_before_event_loop()

        self._application.aboutToQuit.connect(self.aboutToQuit)

        QTimer.singleShot(0, self.post_init)

    ##############################################

    @property
    def parser(self):
        return self._parser

    @property
    def args(self):
        return self._args

    @property
    def platform(self):
        return self._platform

    @property
    def settings(self):
        return self._settings

    @property
    def qml_application(self):
        return self._qml_application

    ##############################################

    def _print_critical_message(self, message):
        # print('\nCritical Error on {}'.format(datetime.datetime.now()))
        # print('-'*80)
        # print(message)
        self._logger.critical(message)

    ##############################################

    def _message_handler(self, msg_type, context, msg):

        if msg_type == QtCore.QtDebugMsg:
            method = self._logger.debug
        elif msg_type == QtCore.QtInfoMsg:
            method = self._logger.info
        elif msg_type == QtCore.QtWarningMsg:
            method = self._logger.warning
        elif msg_type in (QtCore.QtCriticalMsg, QtCore.QtFatalMsg):
            method = self._logger.critical
            # method = None

        # local_msg = msg.toLocal8Bit()
        # localMsg.constData()
        context_file = context.file
        if context_file is not None:
            file_path = Path(context_file).name
        else:
            file_path = ''
        message = '{1} {3} — {0}'.format(msg, file_path, context.line, context.function)
        if method is not None:
            method(message)
        else:
            self._print_critical_message(message)

    ##############################################

    def _on_critical_exception(self, exception):
        message = str(exception) + '\n' + traceback.format_exc()
        self._print_critical_message(message)
        self._qml_application.notify_error(exception)
        # sys.exit(1)

    ##############################################

    def _init_application(self):

        self._application.setOrganizationName(ApplicationMetadata.organisation_name)
        self._application.setOrganizationDomain(ApplicationMetadata.organisation_domain)

        self._application.setApplicationName(ApplicationMetadata.name)
        self._application.setApplicationDisplayName(ApplicationMetadata.display_name)
        self._application.setApplicationVersion(ApplicationMetadata.version)

        logo_path = ':/icons/logo/logo-256.png'
        self._application.setWindowIcon(QIcon(logo_path))

        QIcon.setThemeName('material')

        self._settings = ApplicationSettings()

    ##############################################

    @classmethod
    def setup_gui_application(self):

        QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        # QQuickStyle.setStyle('Material')

    ##############################################

    def _parse_arguments(self):

        self._parser = argparse.ArgumentParser(
            description='CodeReview',
        )

        self.parse_arguments()

        self._args = self._parser.parse_args()

    ##############################################

    def parse_arguments(self):

        # self.parser.add_argument(
        #     '--version',
        #     action='store_true', default=False,
        #     help="show version and exit",
        # )

        self.parser.add_argument(
            '--dont-translate',
            action='store_true',
            default=False,
            help="Don't translate application",
        )

        self.parser.add_argument(
            '--user-script',
            action=PathAction,
            default=None,
            help='user script to execute',
        )

        self.parser.add_argument(
            '--user-script-args',
            default='',
            help="user script args (don't forget to quote)",
        )

    ##############################################

    def _load_translation(self):

        if self._args.dont_translate:
            return

        # Fixme: ConfigInstall
        # directory = ':/translations'
        directory = str(Path(__file__).parent.joinpath('rcc', 'translations'))

        locale = QtCore.QLocale()
        self._translator = QtCore.QTranslator()
        if self._translator.load(locale, 'code-review', '.', directory, '.qm'):
            self._application.installTranslator(self._translator)
        else:
            raise NameError('No translator for locale {}'.format(locale.name()))

    ##############################################

    def register_qml_types(self):

        qmlRegisterType(KeySequenceEditor, 'CodeReview', 1, 0, 'KeySequenceEditor')

        qmlRegisterUncreatableType(Shortcut, 'CodeReview', 1, 0, 'Shortcut', 'Cannot create Shortcut')
        qmlRegisterUncreatableType(ApplicationSettings, 'CodeReview', 1, 0, 'ApplicationSettings', 'Cannot create ApplicationSettings')
        qmlRegisterUncreatableType(self.QmlApplication_CLS, 'CodeReview', 1, 0, 'QmlApplication', 'Cannot create QmlApplication')

    ##############################################

    def _set_context_properties(self):
        context = self._engine.rootContext()
        context.setContextProperty('application', self._qml_application)
        context.setContextProperty('application_settings', self._settings)

    ##############################################

    def _load_qml_main(self):

        self._logger.info('Load QML...')

        qml_path = Path(__file__).parent.joinpath('qml')
        # qml_path = 'qrc:///qml'
        self._engine.addImportPath(str(qml_path))

        main_qml_path = qml_path.joinpath('main.qml')
        self._qml_url = QUrl.fromLocalFile(str(main_qml_path))
        # QUrl('qrc:/qml/main.qml')
        self._engine.objectCreated.connect(self._check_qml_is_loaded)
        self._engine.load(self._qml_url)

        self._logger.info('QML loaded')

    ##############################################

    def _check_qml_is_loaded(self, obj, url):
        # See https://bugreports.qt.io/browse/QTBUG-39469
        if (obj is None and url == self._qml_url):
            sys.exit(-1)

    ##############################################

    def exec_(self):
        self._logger.info('Start event loop')
        rc = self._application.exec_()
        self._logger.info('Event loop done {}'.format(rc))
        del self._engine # solve quit issue ?
        sys.exit(rc)

    ##############################################

    def aboutToQuit(self):
        self._logger.info('')

    ##############################################

    def post_init(self):

        # Fixme: ui refresh ???

        self._logger.info('post Init...')

        if self._args.user_script is not None:
            self.execute_user_script(self._args.user_script)

        self._logger.info('Post Init Done')

    ##############################################

    def execute_user_script(self, script_path):

        """Execute an user script provided by file *script_path* in a context where is defined a
        variable *application* that is a reference to the application instance.

        """

        script_path = Path(script_path).absolute()
        self._logger.info('Execute user script:\n  {}'.format(script_path))
        try:
            source = open(script_path).read()
        except FileNotFoundError:
            self._logger.info('File {} not found'.format(script_path))
            sys.exit(1)
        try:
            bytecode = compile(source, script_path, 'exec')
        except SyntaxError as exception:
            self._on_critical_exception(exception)
        try:
            exec(bytecode, {'application':self})
        except Exception as exception:
            self._on_critical_exception(exception)
        self._logger.info('User script done')
