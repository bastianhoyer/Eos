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

from eos.const import State, Location, Context, RunTime, FilterType, Operator, SourceType
from eos.eve.const import Attribute as DgmAttribute, EffectCategory
from eos.fit.fit import Fit
from eos.fit.items.drone import Drone
from eos.fit.items.module import Module
from eos.fit.attributeCalculator.info.info import Info
from eos.eve.attribute import Attribute
from eos.eve.effect import Effect
from eos.eve.type import Type


class TestFilterLocationSkillrq(TestCase):
    """Test location-skill requirement filter"""

    def setUp(self):
        self.tgtAttr = tgtAttr = Attribute(1)
        srcAttr = Attribute(2)
        info = Info()
        info.state = State.offline
        info.context = Context.local
        info.runTime = RunTime.duration
        info.gang = False
        info.location = Location.ship
        info.filterType = FilterType.skill
        info.filterValue = 56
        info.operator = Operator.postPercent
        info.targetAttributeId = tgtAttr.id
        info.sourceType = SourceType.attribute
        info.sourceValue = srcAttr.id
        effect = Effect(1, EffectCategory.passive)
        effect._Effect__infos = {info}
        influenceSource = Module(Type(1, effects={effect}, attributes={srcAttr.id: 20}))
        self.fit = Fit(lambda attrId: {tgtAttr.id: tgtAttr, srcAttr.id: srcAttr}[attrId])
        self.fit._addHolder(influenceSource)

    def testMatch(self):
        influenceTarget = Module(Type(2, attributes={self.tgtAttr.id: 100, DgmAttribute.skillRq1: 56}))
        self.fit._addHolder(influenceTarget)
        notExpValue = 100
        self.assertNotAlmostEqual(influenceTarget.attributes[self.tgtAttr.id], notExpValue, msg="value must be modified")

    def testOtherLocation(self):
        influenceTarget = Drone(Type(2, attributes={self.tgtAttr.id: 100, DgmAttribute.skillRq1: 56}))
        self.fit._addHolder(influenceTarget)
        expValue = 100
        self.assertAlmostEqual(influenceTarget.attributes[self.tgtAttr.id], expValue, msg="value must stay unmodified")

    def testOtherSkill(self):
        influenceTarget = Module(Type(2, attributes={self.tgtAttr.id: 100, DgmAttribute.skillRq1: 87}))
        self.fit._addHolder(influenceTarget)
        expValue = 100
        self.assertAlmostEqual(influenceTarget.attributes[self.tgtAttr.id], expValue, msg="value must stay unmodified")
