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


from eos.tests.attributeCalculator.attrCalcTestCase import AttrCalcTestCase
from eos.tests.attributeCalculator.environment import IndependentItem
from eos.tests.environment import Logger


class TestNonExistent(AttrCalcTestCase):
    """Test return value when requesting attribute which isn't set"""

    def testAttributeDataError(self):
        # Check case when attribute value is available, but
        # cache handler doesn't know about such attribute
        holder = IndependentItem(self.ch.type_(typeId=57, attributes={105: 20}))
        self.fit.items.add(holder)
        self.assertRaises(KeyError, holder.attributes.__getitem__, 105)
        self.assertEqual(len(self.log), 1)
        logRecord = self.log[0]
        self.assertEqual(logRecord.name, 'eos_test.attributeCalculator')
        self.assertEqual(logRecord.levelno, Logger.ERROR)
        self.assertEqual(logRecord.msg, 'unable to fetch metadata for attribute 105, requested for item 57')
        self.fit.items.remove(holder)
        self.assertBuffersEmpty(self.fit)

    def testAbsentBaseValueError(self):
        # Check case when default value of attribute cannot be
        # determined. and item itself doesn't define any value
        # either
        attr = self.ch.attribute(attributeId=89)
        holder = IndependentItem(self.ch.type_(typeId=649))
        self.fit.items.add(holder)
        self.assertRaises(KeyError, holder.attributes.__getitem__, attr.id)
        self.assertEqual(len(self.log), 1)
        logRecord = self.log[0]
        self.assertEqual(logRecord.name, 'eos_test.attributeCalculator')
        self.assertEqual(logRecord.levelno, Logger.WARNING)
        self.assertEqual(logRecord.msg, 'unable to find base value for attribute 89 on item 649')
        self.fit.items.remove(holder)
        self.assertBuffersEmpty(self.fit)

    def testAbsentDefaultValue(self):
        # Default value should be used if attribute
        # value is not available on item
        attr = self.ch.attribute(attributeId=1, defaultValue=5.6)
        holder = IndependentItem(self.ch.type_(typeId=1))
        self.fit.items.add(holder)
        self.assertAlmostEqual(holder.attributes[attr.id], 5.6)
        self.fit.items.remove(holder)
        self.assertEqual(len(self.log), 0)
        self.assertBuffersEmpty(self.fit)
