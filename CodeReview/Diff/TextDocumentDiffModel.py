####################################################################################################
#
# CodeReview - A Code Review GUI
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

"""This module provides a document model for the Diff Viewer.

A document is made of text blocks that are themselves made of text fragments.  A text block
corresponds to a chunck of lines and is decorated by a frame type corresponding to the type of
chunck.  A text fragment is a piece of text and is decorated by a frame type and a token type used
for the syntax highlighting.  The frame type is used for replace chunck type to show the inner-line
difference.

"""

####################################################################################################

from .RawTextDocumentDiff import chunk_type
from .TextDocumentModel import TextDocumentModel, TextBlock, TextFragment
from CodeReview.Tools.Slice import LineSlice

####################################################################################################

class TextBlockDiff(TextBlock):

    """This class implements a text block with a link to the other side."""

    ##############################################

    def __init__(self, line_slice, frame_type=None, other_side=None):

        """The parameter *line_slice* specifies the line slice corresponding to the text block and the
        parameter *frame_type* the type of frame.  The parameter *other_side* specifies the
        corresponding text block of the second document.

        Public Attributes:

          :attr:`other_side`

        """

        super(TextBlockDiff, self).__init__(line_slice, frame_type)

        self.other_side = other_side

    ##############################################

    def copy(self):

        """Return a copy of the instance."""

        return self.__class__(self.line_slice, self.frame_type, self.other_side)

    ##############################################

    def link_other_side(self, other_side):

        """Link to the other side."""

        self.other_side = other_side

    ##############################################

    def alignment_padding(self):

        number_of_lines1 = len(self.line_slice)
        number_of_lines2 = len(self.other_side.line_slice)
        if number_of_lines1 < number_of_lines2:
            return number_of_lines2 - number_of_lines1
        else:
            return 0

####################################################################################################

class TextDocumentDiffModelFactory:

    ###############################################

    def process(self, file_diff):

        """Build two :class:`DiffViewer.TextDocumentModel` instances from a class
        :class:`DiffViewer.RawTextDocumentDiff` instance.

        Return the 2-tuple mades of the document models.

        """

        document1 = file_diff.document1
        document2 = file_diff.document2
        document_model1 = TextDocumentModel()
        document_model2 = TextDocumentModel()
        current_line1 = 0
        current_line2 = 0

        def add_equal_contents(stop_line1, stop_line2):
            line_slice1 = LineSlice(current_line1, stop_line1)
            line_slice2 = LineSlice(current_line2, stop_line2)
            text_block1 = self._complete_one_side(document1, line_slice1, document_model1)
            text_block2 = self._complete_one_side(document2, line_slice2, document_model2)
            self._link(text_block1, text_block2)

        for group in file_diff:

            # Inter-group lines corresponds to equal contents
            if current_line1 < group.slice1.start or current_line2 < group.slice2.start:
                add_equal_contents(group.slice1.start, group.slice2.start)

            for chunk in group:
                frame_type = chunk.chunk_type
                text_block1 = TextBlockDiff(chunk.chunk1.slice, frame_type)
                text_block2 = TextBlockDiff(chunk.chunk2.slice, frame_type)
                self._link(text_block1, text_block2)

                if frame_type == chunk_type.replace:
                    self._append_sub_chunk(chunk, text_block1, text_block2)
                else:
                    text_block1.append(TextFragment(chunk.chunk1))
                    text_block2.append(TextFragment(chunk.chunk2))

                document_model1.append(text_block1)
                document_model2.append(text_block2)

            current_line1 = group.slice1.stop
            current_line2 = group.slice2.stop

        # Last group lines corresponds to equal contents
        if current_line1 < document1.line_slice.stop or current_line2 < document2.line_slice.stop:
            add_equal_contents(document1.line_slice.stop, document2.line_slice.stop)

        return document_model1, document_model2

    ###############################################

    def _link(self, text_block1, text_block2):

        """ Create the links between the two text blocks. """

        text_block1.link_other_side(text_block2)
        text_block2.link_other_side(text_block1)

    ###############################################

    def _complete_one_side(self, document, line_slice, document_model):

        """ Add to the document model an equal block. """

        text_block = TextBlockDiff(line_slice, chunk_type.equal_block)
        document_model.append(text_block)

        if bool(line_slice):
            flat_slice = document.to_flat_slice(line_slice)
            chunk = document[flat_slice]
            text_block.append(TextFragment(chunk))

        return text_block

    ###############################################

    def _append_sub_chunk(self, sub_chunks, text_block1, text_block2):

        """ Append sub-chunks to the text blocks. """

        for sub_chunk in sub_chunks:
            sub_frame_type = sub_chunk.chunk_type
            if bool(sub_chunk.chunk1):
                text_block1.append(TextFragment(sub_chunk.chunk1, sub_frame_type))
            if bool(sub_chunk.chunk2):
                text_block2.append(TextFragment(sub_chunk.chunk2, sub_frame_type))

####################################################################################################

def highlight_document(document_model, highlighted_text):

    """Merge a Diff document model and highlighted counter part.

    Return a new document model.

    """

    raw_text_document = highlighted_text.raw_text_document

    highlighted_text_iterator = iter(highlighted_text)
    highlighted_fragment = next(highlighted_text_iterator)
    highlighted_slice= highlighted_fragment.slice

    highlighted_document = TextDocumentModel(metadata=document_model.metadata)
    for text_block in document_model:
        highlighted_text_block = text_block.copy()
        highlighted_document.append(highlighted_text_block)
        text_block_iterator = iter(text_block)
        text_fragment = next(text_block_iterator)
        text_slice = text_fragment.text.flat_slice()
        while True:
            # Fixme: add func in classes ?
            if highlighted_slice.is_included_in(text_slice):
                append_intersection = True
                next_highlighted_fragment = True
                next_text_fragment = False
            elif highlighted_slice.intersect(text_slice):
                append_intersection = True
                next_highlighted_fragment = highlighted_slice.stop == text_slice.stop
                next_text_fragment = True
            else:
                # highlighted_fragment is after text_fragment
                append_intersection = False
                next_highlighted_fragment = False
                next_text_fragment = True
            if append_intersection:
                text = raw_text_document[highlighted_slice & text_slice]
                highlighted_text_fragment = TextFragment(text,
                                                         frame_type=text_fragment.frame_type,
                                                         token_type=highlighted_fragment.token)
                highlighted_text_block.append(highlighted_text_fragment)
            try:
                if next_highlighted_fragment:
                    highlighted_fragment = next(highlighted_text_iterator)
                    highlighted_slice= highlighted_fragment.slice
                if next_text_fragment:
                    text_fragment = next(text_block_iterator)
                    text_slice = text_fragment.text.flat_slice()
            except StopIteration:
                break

    return highlighted_document
