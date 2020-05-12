####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2020 Fabrice Salvaire
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

__all__ = ['Review']

####################################################################################################

from pathlib import Path

import json

####################################################################################################

class ReviewNote:

    ##############################################

    def __init__(self, sha, text=''):

        self._sha = str(sha)
        self._text = str(text)

    ##############################################

    @property
    def sha(self):
        return self._sha

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)

    ##############################################

    def to_json(self):
        return {key:getattr(self, key) for key in ('text',)}

####################################################################################################

class Review:

    ##############################################

    def __init__(self, path):

        self._path = Path(path)

        self._notes = {}
        if self._path.exists():
            with open(self._path) as fh:
                data = json.load(fh)
                for sha, review in data.items():
                    self.add(ReviewNote(sha, **review))

    ##############################################

    def save(self):
        with open(self._path, 'w') as fh:
            data = {note.sha:note.to_json() for note in self._notes.values()}
            json.dump(data, fh, indent=4, sort_keys=True, ensure_ascii=False)

    ##############################################

    def __getitem__(self, sha):
        return self._notes.get(sha, None)

    ##############################################

    def add(self, review_note):
        self._notes[review_note.sha] = review_note
