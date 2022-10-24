####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2020 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from pathlib import Path
import getpass
import logging

from github import Github # http://pygithub.readthedocs.io/en/latest/
import github3 # https://github.com/sigmavirus24/github3.py

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Account:

    _logger = _module_logger.getChild('Account')

    ##############################################

    def __init__(self):
        self._github = None

    ##############################################

    @property
    def credentials_path(self):
        return Path.home().joinpath('.github-token') # Fixme: Windows / OSX ???

    ##############################################

    @classmethod
    def two_factor_callback():
        otp = ''
        while not otp:
            # The user could accidentally press Enter before being ready,
            # let's protect them from doing that.
            otp = getpass.getpass(prompt='OTP: ', stream=None)
        return otp

    ##############################################

    def make_token_file(self, user, password, note_url='', two_factor_callback=None):

        note = 'github-api'
        scopes = ['user', 'repo']

        authorisation = github3.authorize(
            user, password,
            scopes,
            note, note_url,
            two_factor_callback=two_factor_callback,
        )

        with open(self.credentials_path, 'w') as fd:
            # fd.write(authorisation.token + '\n')
            # fd.write(str(authorisation.id))
            fd.write(authorisation.token)

    ##############################################

    def login(self):

        if self._github is None:
            with open(self.credentials_path, 'r') as fd:
                token = fd.readline().strip()
                # token_id = fd.readline().strip()

            self._github = Github(login_or_token=token)
            # gh = github3.login(token=token)

    ##############################################

    @property
    def github(self):
        return self._github
