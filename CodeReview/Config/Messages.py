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

about_CodeReview = """
<h2>CodeReview {version}</h2>

<p><a href="https://fabricesalvaire.github.io/CodeReview">CodeReview</a> is a GUI tool to perform
code review.</p>

<p><strong>Copyright © 2015 Fabrice Salvaire</strong></p>

<p>This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.</p>

<p>This program is distributed in the hope that it will be useful, but <strong>WITHOUT ANY
WARRANTY</strong>; without even the implied warranty of <strong>MERCHANTABILITY</strong> or <strong>FITNESS
FOR A PARTICULAR PURPOSE</strong>.  See the GNU General Public License for more details.</p>

<p>You should have received a copy of the GNU General Public License along with this program.  If
not, see <a href="http://www.gnu.org/licenses">here</a>.</p>

The source code and the Git repository of CodeReview is available on <a
href="https://github.com/FabriceSalvaire/CodeReview">GitHub</a>.
"""

####################################################################################################

system_information_message_pattern = """
<h2>CodeReview {version}</h2>
<h2>Host {node}</h2>
<h3>Hardware</h3>
<ul>
<li>Machine: {machine}</li>
<li>Architecture: {architecture}</li>
<li>CPU: {cpu}</li>
<li>Number of cores: {number_of_cores}</li>
<li>Memory Size: {memory_size_mb} MB</li>
</ul>
<h3>Software Versions</h3>
<ul>
<li>OS: {os} {distribution}</li>
<li>Python {python_version}</li>
<li>Qt {qt_version}</li>
<li>PyQt {pyqt_version}</li>
</ul>
"""

####################################################################################################
#
# End
#
####################################################################################################
