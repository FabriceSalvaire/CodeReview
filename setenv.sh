# -*- sh -*-

####################################################################################################

source /opt/python-virtual-env/py36/bin/activate

append_to_ld_library_path_if_not /usr/local/lib
append_to_python_path_if_not ${PWD}
