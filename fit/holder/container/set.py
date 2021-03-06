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


from eos.fit.exception import HolderAddError
from .base import HolderContainerBase


class HolderSet(HolderContainerBase):
    """
    Unordered container for holders.

    Positional arguments:
    fit -- fit, to which container is attached
    """

    __slots__ = ('__set')

    def __init__(self, fit):
        self.__set = set()
        HolderContainerBase.__init__(self, fit)

    def add(self, holder):
        """
        Add holder to container.

        Possible exceptions:
        ValueError -- raised when holder cannot be
        added to container (e.g. already belongs to some fit)
        """
        self.__set.add(holder)
        try:
            self._handleAdd(holder)
        except HolderAddError as e:
            self.__set.remove(holder)
            raise ValueError(holder) from e

    def remove(self, holder):
        """
        Remove holder from container.

        Possible exceptions:
        KeyError -- raised when holder cannot be removed
        from container (e.g. it doesn't belong to it)
        """
        if holder not in self.__set:
            raise KeyError(holder)
        self._handleRemove(holder)
        self.__set.remove(holder)

    def clear(self):
        """Remove everything from container."""
        for holder in self.__set:
            self._handleRemove(holder)
        self.__set.clear()

    def __iter__(self):
        return self.__set.__iter__()

    def __contains__(self, holder):
        return self.__set.__contains__(holder)

    def __len__(self):
        return self.__set.__len__()
