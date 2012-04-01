####################################################################################################
# 
# DiffViewer - Diff Viewer 
# Copyright (C) Salvaire Fabrice 2012 
# 
####################################################################################################

####################################################################################################

from fnmatch import fnmatch
import os

####################################################################################################

class RstFactory(object):

    init_file_name = '__init__.py'

    end_marker = """
.. End
"""

    ##############################################

    def __init__(self, module_path, rst_directory):

        self._rst_directory = rst_directory
        self._root_module_path = module_path
        self._root_module_name = os.path.basename(module_path)
        print "Root Module Path:", self._root_module_path
        print "Root Module Name:", self._root_module_name

        if not os.path.exists(self._rst_directory):
            os.mkdir(self._rst_directory)

        for module_path, sub_directories, files in os.walk(module_path):
            if self.is_python_directory_module(module_path):
                python_files = [file_name
                                for file_name in files
                                if (file_name.endswith('.py') and
                                    file_name != self.init_file_name and
                                    'flymake'not in file_name)]
                sub_modules = []
                for sub_directory in sub_directories:
                    if self.is_python_directory_module(os.path.join(module_path, sub_directory)):
                        sub_modules.append(sub_directory)
                self._process_directory_module(module_path, python_files, sub_modules)

    ##############################################

    def _process_directory_module(self, module_path, python_files, sub_modules):

        directory_module_name = os.path.basename(module_path)
        directory_module_python_path = self._root_module_name + \
            self.path_to_python_path(module_path.replace(self._root_module_path, ''))
        dst_directory = os.path.join(self._rst_directory,
                                     self.python_path_to_path(directory_module_python_path))
        print
        print "Directory Module Name:", directory_module_name
        print "Directory Module Python Path:", directory_module_python_path
        print "Dest Path:", dst_directory

        if not os.path.exists(dst_directory):
            os.mkdir(dst_directory)

        module_names = []
        for file_name in python_files:
            module_name = file_name.replace('.py', '')
            module_names.append(module_name)
            print "  Module:", module_name
            rst = self._generate_rst_module(directory_module_python_path, module_name)
            rst_file_name = os.path.join(dst_directory, module_name + '.rst')
            with open(rst_file_name, 'w') as f:
                f.write(rst)

        # Generate TOC file
        rst = self._generate_toc(directory_module_name, module_names + sub_modules)
        rst_file_name = os.path.join(os.path.dirname(dst_directory), directory_module_name + '.rst')
        with open(rst_file_name, 'w') as f:
            f.write(rst)

    ##############################################

    @staticmethod
    def is_python_directory_module(path):

        return os.path.exists(os.path.join(path, RstFactory.init_file_name))

    ##############################################

    @staticmethod
    def path_to_python_path(path):

        return path.replace(os.path.sep, '.')

    ##############################################

    @staticmethod
    def python_path_to_path(python_path):

        return python_path.replace('.', os.path.sep)

    ##############################################

    def _generate_title(self, module_name):

        mod_rst = ' :mod:`'

        template = """
%(header_line)s
%(mod)s%(module_name)s`
%(header_line)s
"""
        
        rst = template.lstrip() % dict(
            module_name=module_name,
            mod=mod_rst,
            header_line='*'*(len(module_name) + len(mod_rst) +2),
            )

        return rst

    ##############################################

    def _generate_toc(self, directory_module_name, module_names):

        template = """
 %(title)s

.. toctree::
"""
    
        rst = template.lstrip() % dict(
            title=self._generate_title(directory_module_name),
            )

        for module_name in module_names:
            rst += ' '*2 + os.path.join(directory_module_name, module_name) + '\n'

        rst += """
.. End
"""

        return rst

    ##############################################

    def _generate_rst_module(self, module_path, module_name):

        template = """
%(title)s

.. automodule:: %(module_path)s.%(module_name)s
   :members:
   :show-inheritance:

.. End
"""
        
        rst = template.lstrip() % dict(
            title=self._generate_title(module_name),
            module_name=module_name,
            module_path=module_path,
            )

        return rst

####################################################################################################
#
# End
#
####################################################################################################
