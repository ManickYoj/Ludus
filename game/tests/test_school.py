from django.test import TestCase
from game.factories import SchoolFactory
from game.models import School
from game.tests.matchers import change
from expects import *


class SchoolTestCase(TestCase):
  def test_advance(self):
    school = SchoolFactory.create(
      period=School.PERIODS[0]
    )

    # Step a day through its phases. Once the last phase has completed,
    # expect advance to start a new day
    def cycleThroughPeriods():
      for period in School.PERIODS:
        expect(school.period).to(equal(period))
        school.advancePeriod()

    expect(
      cycleThroughPeriods
    ).to(
      change(lambda: school.day).by(1)
    )
