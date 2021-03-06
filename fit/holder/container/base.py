#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2013 Anton Vorobyov
#
# This file is part of Eos.
#
# Eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Eos. If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


class HolderContainerBase:
    """
    Base class for any containers which are intended
    to ease management of holders. Hides fit-specific
    logic under its hood, letting real containers (which
    should inherit it) implement just container type-
    specific logic.

    Positional arguments:
    fit -- fit, to which container is attached
    """

    __slots__ = ('__fit')

    def __init__(self, fit):
        self.__fit = fit

    def _handleAdd(self, holder):
        """Shortcut for registration of holder in fit."""
        self.__fit._addHolder(holder)

    def _handleRemove(self, holder):
        """Shortcut for unregistration of holder in fit."""
        self.__fit._removeHolder(holder)
