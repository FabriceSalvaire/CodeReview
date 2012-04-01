/*
 *  Bazaar -- distributed version control
 *
 * Copyright (C) 2008 by Canonical Ltd
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

/* Provide the typedefs that pyrex does automatically in newer versions, to
 * allow older versions  to build our extensions.
 */

#ifndef _BZR_PYTHON_COMPAT_H
#define _BZR_PYTHON_COMPAT_H

/* http://www.python.org/dev/peps/pep-0353/ */
#if PY_VERSION_HEX < 0x02050000 && !defined(PY_SSIZE_T_MIN)
    typedef int Py_ssize_t;
    typedef Py_ssize_t (*lenfunc)(PyObject *);
    typedef PyObject * (*ssizeargfunc)(PyObject *, Py_ssize_t);
    typedef PyObject * (*ssizessizeargfunc)(PyObject *, Py_ssize_t, Py_ssize_t);
    #define PY_SSIZE_T_MAX INT_MAX
    #define PY_SSIZE_T_MIN INT_MIN
    #define PyInt_FromSsize_t(z) PyInt_FromLong(z)
    #define PyInt_AsSsize_t(o) PyInt_AsLong(o)
#endif

#if defined(_WIN32) || defined(WIN32)
    /* Defining WIN32_LEAN_AND_MEAN makes including windows quite a bit
     * lighter weight.
     */
    #define WIN32_LEAN_AND_MEAN
    #include <windows.h>

    /* Needed for htonl */
    #include "Winsock2.h"

    /* sys/stat.h doesn't have any of these macro definitions for MSVC, so
     * we'll define whatever is missing that we actually use.
     */
    #if !defined(S_ISDIR)
        #define S_ISDIR(m) (((m) & 0170000) == 0040000)
    #endif
    #if !defined(S_ISREG)
        #define S_ISREG(m) (((m) & 0170000) == 0100000)
    #endif
    #if !defined(S_IXUSR)
        #define S_IXUSR 0000100/* execute/search permission, owner */
    #endif
    /* sys/stat.h doesn't have S_ISLNK on win32, so we fake it by just always
     * returning False
     */
    #if !defined(S_ISLNK)
        #define S_ISLNK(mode) (0)
    #endif
#else /* Not win32 */
    /* For htonl */
    #include "arpa/inet.h"
#endif

#include <stdio.h>

#ifdef _MSC_VER
#define  snprintf  _snprintf
/* gcc (mingw32) has strtoll, while the MSVC compiler uses _strtoi64 */
#define strtoll _strtoi64
#define strtoull _strtoui64
#endif

/* Introduced in Python 2.6 */
#ifndef Py_TYPE
#  define Py_TYPE(o) ((o)->ob_type)
#endif
#ifndef Py_REFCNT
#  define Py_REFCNT(o) ((o)->ob_refcnt)
#endif

#endif /* _BZR_PYTHON_COMPAT_H */
