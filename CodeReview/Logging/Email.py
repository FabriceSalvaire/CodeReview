####################################################################################################
#
# CodeReview - A Python/Qt Git GUI
# Copyright (C) 2015 Fabrice Salvaire
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

import re
import smtplib

from email.mime.text import MIMEText

####################################################################################################

class Email(object):

    ##############################################

    def __init__(self,
                 from_address='',
                 subject='',
                 recipients=[],
                 message='',
                 ):

        self.check_email_is_valid(from_address)

        self._from_address = from_address
        self._subject = subject
        self.message = message

        self._recipients = []
        self.add_recipients(recipients)

    ##############################################

    def check_email_is_valid(self, email):

        return re.match('^[\w\.\-]+@[\w\.\-]+$', email) is not None

    ##############################################

    def add_recipients(self, recipients):

        for email in recipients:
            if not self.check_email_is_valid(email):
                raise ValueError("Email '%s' is not valid" % (email))
            self._recipients.append(email)

    ##############################################

    def add_recipients_from_string(self, recipients):

        self.add_recipients([x.strip() for x in recipients.split(',')])

    ##############################################

    def send(self):

        if not self._recipients:
            raise ValueError("Recipients is empty")

        message = MIMEText(self.message)
        message['Subject'] = self._subject
        message['From'] = self._from_address
        message['To'] = ', '.join([x + ' <' + x + '>' for x in self._recipients])

        smtp = smtplib.SMTP()
        smtp.connect()
        smtp.sendmail(self._from_address,
                      self._recipients,
                      message.as_string())
        smtp.quit()

####################################################################################################
#
# End
#
####################################################################################################
