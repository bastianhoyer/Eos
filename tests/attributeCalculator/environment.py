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


from eos.const.eos import State, Location
from eos.fit.attributeCalculator import LinkTracker, MutableAttributeMap
from eos.tests.environment import Logger


class HolderContainer:

    def __init__(self, fit):
        self.__fit = fit
        self.__set = set()

    def add(self, holder):
        self.__set.add(holder)
        self.__fit._addHolder(holder)

    def remove(self, holder):
        self.__fit._removeHolder(holder)
        self.__set.remove(holder)

    def __len__(self):
        return len(self.__set)

    def __iter__(self):
        return iter(self.__set)


class Eos:

    def __init__(self, cacheHandler):
        self._logger = Logger()
        self._cacheHandler = cacheHandler


class Fit:

    def __init__(self, cacheHandler):
        self.eos = Eos(cacheHandler)
        self._linkTracker = LinkTracker(self)
        self.__ship = None
        self.__character = None
        self.items = HolderContainer(self)

    @property
    def ship(self):
        return self.__ship

    @ship.setter
    def ship(self, ship):
        if self.__ship is not None:
            self._removeHolder(self.__ship)
        self.__ship = ship
        if ship is not None:
            self._addHolder(self.__ship)

    @property
    def character(self):
        return self.__character

    @character.setter
    def character(self, character):
        if self.__character is not None:
            self._removeHolder(self.__character)
        self.__character = character
        if character is not None:
            self._addHolder(self.__character)

    def _addHolder(self, holder):
        if holder._fit is not None:
            raise Exception
        holder._fit = self
        self._linkTracker.addHolder(holder)
        enabledStates = set(filter(lambda s: s <= holder.state, State))
        self._linkTracker.enableStates(holder, enabledStates)

    def _removeHolder(self, holder):
        if holder._fit is not self:
            raise Exception
        disabledStates = set(filter(lambda s: s <= holder.state, State))
        self._linkTracker.disableStates(holder, disabledStates)
        self._linkTracker.removeHolder(holder)
        holder._fit = None

    def _holderStateSwitch(self, holder, newState):
        enabledStates = set(filter(lambda s: s > holder.state and s <= newState, State))
        disabledStates = set(filter(lambda s: s > newState and s <= holder.state, State))
        self._linkTracker.enableStates(holder, enabledStates)
        self._linkTracker.disableStates(holder, disabledStates)

class Holder:

    __slots__ = ('__fit', 'item', 'attributes', '__state')

    def __init__(self, type_):
        self.__fit = None
        self.item = type_
        self.attributes = MutableAttributeMap(self)
        self.__state = State.offline

    @property
    def _fit(self):
        return self.__fit

    @_fit.setter
    def _fit(self, newFit):
        self.attributes.clear()
        self.__fit = newFit

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, newState):
        oldState = self.state
        if newState == oldState:
            return
        if self._fit is not None:
            self._fit._holderStateSwitch(self, newState)
        self.__state = newState


class IndependentItem(Holder):

    __slots__ = ()

    def __init__(self, type_):
        Holder.__init__(self, type_)

    @property
    def _location(self):
        return None


class CharacterItem(Holder):

    __slots__ = ()

    def __init__(self, type_):
        Holder.__init__(self, type_)

    @property
    def _location(self):
        return Location.character


class ShipItem(Holder):

    __slots__ = ()

    def __init__(self, type_):
        Holder.__init__(self, type_)

    @property
    def _location(self):
        return Location.ship


class SpaceItem(Holder):

    __slots__ = ()

    def __init__(self, type_):
        Holder.__init__(self, type_)

    @property
    def _location(self):
        return Location.space


class Skill(IndependentItem):

    __slots__ = ('level',)

    def __init__(self, type_):
        CharacterItem.__init__(self, type_)
        self.level = 0


class ItemWithOther(IndependentItem):

    __slots__ = ('_other',)

    def __init__(self, type_):
        CharacterItem.__init__(self, type_)
        self._other = None

    def makeOtherLink(self, other):
        if self._other is not None or other._other is not None:
            raise Exception
        self._other = other
        other._other = self

    def breakOtherLink(self, other):
        if self._other is not other or other._other is not self:
            raise Exception
        self._other = None
        other._other = None
