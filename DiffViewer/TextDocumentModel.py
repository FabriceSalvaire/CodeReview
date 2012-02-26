####################################################################################################

####################################################################################################

class TextBlock(list):

    ##############################################
    
    def __init__(self, line_slice, frame_type=None):

        super(TextBlock, self).__init__()

        self.line_slice = line_slice
        self.frame_type = frame_type

    ##############################################
    
    def __repr__(self):

        return 'Text Block ' + str(self.frame_type) + ' ' + repr(self.line_slice)
        
####################################################################################################

class TextFragment(object):

    ##############################################

    def __init__(self, text, frame_type=None, token_type=None):

        self.text = text
        self.frame_type = frame_type
        self.token_type = token_type

    ##############################################

    def __unicode__(self):

        return self.text

    ##############################################
    
    def __repr__(self):

        return 'Text Fragment  ' + str(self.frame_type) + ' ' + str(self.token_type) \
            + ' ' + repr(self.text)
    
####################################################################################################

class TextDocumentModel(list):
    pass

####################################################################################################
#
# End
#
####################################################################################################
