#!/usr/bin/env python

"""
Basic helper functions.

Copyright (C) Sarah Mount, 2011.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

def uniq(lst):
    """Remove duplicates from a sequence, preserving order.

    By Raymond Hettinger http://code.activestate.com/recipes/52560/
    """
    myset = {}
    return [myset.setdefault(e,e) for e in lst if e not in myset]

