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


from unittest.mock import call

from eos.fit.exception import HolderAddError
from eos.fit.holder.container import HolderList, SlotTakenError
from eos.tests.fit.holderContainer.containerTestCase import ContainerTestCase
from eos.tests.fit.environment import Holder


class TestContainerOrderedPlace(ContainerTestCase):

    def setUp(self):
        ContainerTestCase.setUp(self)
        self.fitMock = self._fitMockMemberCheck()
        self.container = HolderList(self.fitMock)

    def testHolderOutside(self):
        container = self.container
        fitMock = self.fitMock
        holder1 = Holder()
        holder2 = Holder()
        container.append(holder1)
        self.assertEqual(len(container), 1)
        self.assertRaises(IndexError, container.__getitem__, 3)
        self.assertEqual(len(fitMock.mock_calls), 1)
        container.place(3, holder2)
        self.assertEqual(len(fitMock.mock_calls), 2)
        self.assertEqual(fitMock.method_calls[1], call._addHolder(holder2))
        self.assertIs(container[3], holder2)
        self.assertEqual(len(container), 4)
        container.remove(holder1)
        container.remove(holder2)
        self.assertBuffersEmpty(container)

    def testHolderOntoNone(self):
        container = self.container
        fitMock = self.fitMock
        holder1 = Holder()
        holder2 = Holder()
        holder3 = Holder()
        container.append(holder1)
        container.insert(3, holder2)
        self.assertIsNone(container[1])
        self.assertEqual(len(container), 4)
        self.assertEqual(len(fitMock.mock_calls), 2)
        container.place(1, holder3)
        self.assertEqual(len(fitMock.mock_calls), 3)
        self.assertEqual(fitMock.method_calls[2], call._addHolder(holder3))
        self.assertIs(container[1], holder3)
        self.assertEqual(len(container), 4)
        container.remove(holder1)
        container.remove(holder2)
        container.remove(holder3)
        self.assertBuffersEmpty(container)

    def testHolderOntoHolder(self):
        container = self.container
        fitMock = self.fitMock
        holder1 = Holder()
        holder2 = Holder()
        container.append(holder1)
        self.assertIs(container[0], holder1)
        self.assertEqual(len(container), 1)
        self.assertEqual(len(fitMock.mock_calls), 1)
        self.assertRaises(SlotTakenError, container.place, 0, holder2)
        self.assertEqual(len(fitMock.mock_calls), 1)
        self.assertIs(container[0], holder1)
        container.remove(holder1)
        self.assertBuffersEmpty(container)

    def testHolderOutsideFailure(self):
        container = self.container
        fitMock = self.fitMock
        holder = Holder()
        fitMock._addHolder.side_effect = HolderAddError(holder)
        self.assertRaises(ValueError, container.place, 2, holder)
        self.assertEqual(len(fitMock.mock_calls), 1)
        self.assertEqual(fitMock.method_calls[0], call._addHolder(holder))
        self.assertEqual(len(container), 0)
        self.assertBuffersEmpty(container)

    def testHolderOntoNoneFailure(self):
        container = self.container
        fitMock = self.fitMock
        holder1 = Holder()
        holder2 = Holder()
        container.insert(1, holder1)
        self.assertEqual(len(container), 2)
        self.assertIsNone(container[0])
        self.assertIs(container[1], holder1)
        self.assertEqual(len(fitMock.mock_calls), 1)
        fitMock._addHolder.side_effect = HolderAddError(holder2)
        self.assertRaises(ValueError, container.place, 0, holder2)
        self.assertEqual(len(fitMock.mock_calls), 2)
        self.assertEqual(fitMock.method_calls[1], call._addHolder(holder2))
        self.assertEqual(len(container), 2)
        self.assertIsNone(container[0])
        self.assertIs(container[1], holder1)
        container.remove(holder1)
        self.assertBuffersEmpty(container)
