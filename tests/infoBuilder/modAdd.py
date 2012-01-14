#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2012 Anton Vorobyov
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

from unittest import TestCase

from eos import const
from eos.data.expression import Expression
from eos.data.effect.builder import InfoBuilder

class TestPreModAddAttr(TestCase):
    """Test parsing of trees describing increment by attribute in the beginning of the cycle"""

    def testBuildSuccess(self):
        eTgt = Expression(1, 24, value="Ship")
        eTgtAttr = Expression(2, 22, attributeId=264)
        eSrcAttr = Expression(3, 22, attributeId=68)
        eTgtSpec = Expression(4, 12, arg1=eTgt, arg2=eTgtAttr)
        ePreAdd = Expression(5, 42, arg1=eTgtSpec, arg2=eSrcAttr)
        ePostStub = Expression(6, 27, value="1")
        infos, status = InfoBuilder().build(ePreAdd, ePostStub)
        expStatus = const.effectInfoOkFull
        self.assertEqual(status, expStatus, msg="expressions must be successfully parsed (ID {})".format(expStatus))
        self.assertEqual(len(infos), 1, msg="one info must be generated")
        info = infos.pop()
        expType = const.infoPre
        self.assertEqual(info.type, expType, msg="info type must be instant pre-modifier (ID {})".format(expType))
        expGang = False
        self.assertIs(info.gang, expGang, msg="info gang flag must be {}".format(expGang))
        expLocation = const.locShip
        self.assertEqual(info.location, expLocation, msg="info target location must be ship (ID {})".format(expLocation))
        self.assertIsNone(info.filterType, msg="info target filter type must be None")
        self.assertIsNone(info.filterValue, msg="info target filter value must be None")
        expOperation = const.optrIncr
        self.assertEqual(info.operation, expOperation, msg="info operation must be Increment (ID {})".format(expOperation))
        expTgtAttr = 264
        self.assertEqual(info.targetAttributeId, expTgtAttr, msg="info target attribute ID must be {}".format(expTgtAttr))
        expSrcType = const.srcAttr
        self.assertEqual(info.sourceType, expSrcType, msg="info source type must be attribute (ID {})".format(expSrcType))
        expSrcVal = 68
        self.assertEqual(info.sourceValue, expSrcVal, msg="info source value must be {}".format(expSrcVal))
        self.assertIsNone(info.conditions, msg="info conditions must be None")


class TestPreModAddVal(TestCase):
    """Test parsing of trees describing increment by value in the beginning of the cycle"""

    def testBuildSuccess(self):
        eTgt = Expression(1, 24, value="Ship")
        eTgtAttr = Expression(2, 22, attributeId=264)
        eSrcVal = Expression(3, 27, value="200")
        eTgtSpec = Expression(4, 12, arg1=eTgt, arg2=eTgtAttr)
        ePreAdd = Expression(5, 42, arg1=eTgtSpec, arg2=eSrcVal)
        ePostStub = Expression(6, 27, value="1")
        infos, status = InfoBuilder().build(ePreAdd, ePostStub)
        expStatus = const.effectInfoOkFull
        self.assertEqual(status, expStatus, msg="expressions must be successfully parsed (ID {})".format(expStatus))
        self.assertEqual(len(infos), 1, msg="one info must be generated")
        info = infos.pop()
        expType = const.infoPre
        self.assertEqual(info.type, expType, msg="info type must be instant pre-modifier (ID {})".format(expType))
        expGang = False
        self.assertIs(info.gang, expGang, msg="info gang flag must be {}".format(expGang))
        expLocation = const.locShip
        self.assertEqual(info.location, expLocation, msg="info target location must be ship (ID {})".format(expLocation))
        self.assertIsNone(info.filterType, msg="info target filter type must be None")
        self.assertIsNone(info.filterValue, msg="info target filter value must be None")
        expOperation = const.optrIncr
        self.assertEqual(info.operation, expOperation, msg="info operation must be Increment (ID {})".format(expOperation))
        expTgtAttr = 264
        self.assertEqual(info.targetAttributeId, expTgtAttr, msg="info target attribute ID must be {}".format(expTgtAttr))
        expSrcType = const.srcVal
        self.assertEqual(info.sourceType, expSrcType, msg="info source type must be value (ID {})".format(expSrcType))
        expSrcVal = 200
        self.assertEqual(info.sourceValue, expSrcVal, msg="info source value must be {}".format(expSrcVal))
        self.assertIsNone(info.conditions, msg="info conditions must be None")


class TestPostModAddAttr(TestCase):
    """Test parsing of trees describing increment by attribute in the end of the cycle"""

    def testBuildSuccess(self):
        ePreStub = Expression(1, 27, value="1")
        eTgt = Expression(2, 24, value="Ship")
        eTgtAttr = Expression(3, 22, attributeId=264)
        eSrcAttr = Expression(4, 22, attributeId=68)
        eTgtSpec = Expression(5, 12, arg1=eTgt, arg2=eTgtAttr)
        ePostAdd = Expression(6, 42, arg1=eTgtSpec, arg2=eSrcAttr)
        infos, status = InfoBuilder().build(ePreStub, ePostAdd)
        expStatus = const.effectInfoOkFull
        self.assertEqual(status, expStatus, msg="expressions must be successfully parsed (ID {})".format(expStatus))
        self.assertEqual(len(infos), 1, msg="one info must be generated")
        info = infos.pop()
        expType = const.infoPost
        self.assertEqual(info.type, expType, msg="info type must be instant post-modifier (ID {})".format(expType))
        expGang = False
        self.assertIs(info.gang, expGang, msg="info gang flag must be {}".format(expGang))
        expLocation = const.locShip
        self.assertEqual(info.location, expLocation, msg="info target location must be ship (ID {})".format(expLocation))
        self.assertIsNone(info.filterType, msg="info target filter type must be None")
        self.assertIsNone(info.filterValue, msg="info target filter value must be None")
        expOperation = const.optrIncr
        self.assertEqual(info.operation, expOperation, msg="info operation must be Increment (ID {})".format(expOperation))
        expTgtAttr = 264
        self.assertEqual(info.targetAttributeId, expTgtAttr, msg="info target attribute ID must be {}".format(expTgtAttr))
        expSrcType = const.srcAttr
        self.assertEqual(info.sourceType, expSrcType, msg="info source type must be attribute (ID {})".format(expSrcType))
        expSrcVal = 68
        self.assertEqual(info.sourceValue, expSrcVal, msg="info source value must be {}".format(expSrcVal))
        self.assertIsNone(info.conditions, msg="info conditions must be None")


class TestPostModAddVal(TestCase):
    """Test parsing of trees describing increment by value in the end of the cycle"""

    def testBuildSuccess(self):
        ePreStub = Expression(1, 27, value="1")
        eTgt = Expression(2, 24, value="Ship")
        eTgtAttr = Expression(3, 22, attributeId=264)
        eSrcVal = Expression(4, 27, value="3")
        eTgtSpec = Expression(5, 12, arg1=eTgt, arg2=eTgtAttr)
        ePostAdd = Expression(6, 42, arg1=eTgtSpec, arg2=eSrcVal)
        infos, status = InfoBuilder().build(ePreStub, ePostAdd)
        expStatus = const.effectInfoOkFull
        self.assertEqual(status, expStatus, msg="expressions must be successfully parsed (ID {})".format(expStatus))
        self.assertEqual(len(infos), 1, msg="one info must be generated")
        info = infos.pop()
        expType = const.infoPost
        self.assertEqual(info.type, expType, msg="info type must be instant post-modifier (ID {})".format(expType))
        expGang = False
        self.assertIs(info.gang, expGang, msg="info gang flag must be {}".format(expGang))
        expLocation = const.locShip
        self.assertEqual(info.location, expLocation, msg="info target location must be ship (ID {})".format(expLocation))
        self.assertIsNone(info.filterType, msg="info target filter type must be None")
        self.assertIsNone(info.filterValue, msg="info target filter value must be None")
        expOperation = const.optrIncr
        self.assertEqual(info.operation, expOperation, msg="info operation must be Increment (ID {})".format(expOperation))
        expTgtAttr = 264
        self.assertEqual(info.targetAttributeId, expTgtAttr, msg="info target attribute ID must be {}".format(expTgtAttr))
        expSrcType = const.srcVal
        self.assertEqual(info.sourceType, expSrcType, msg="info source type must be value (ID {})".format(expSrcType))
        expSrcVal = 3
        self.assertEqual(info.sourceValue, expSrcVal, msg="info source value must be {}".format(expSrcVal))
        self.assertIsNone(info.conditions, msg="info conditions must be None")