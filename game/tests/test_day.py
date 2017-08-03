from django.test import TestCase
from game.models import Day
from game.factories import SchoolFactory
from expects import *


class DayTestCase(TestCase):
  def test_tomorrow(self):
    school = SchoolFactory.create()

    expect(school.day.number).to(equal(0))

    school.day.tomorrow()

    expect(school.day.number).to(equal(1))

  def test_advance(self):
    school = SchoolFactory.create()

    expect(school.day.number).to(equal(0))

    # Step a day through its phases. Once the last phase has completed,
    # expect advance to start a new day
    for phase in Day.PHASES:
      expect(school.day.phase).to(equal(phase))
      school.day.advance()

    expect(school.day.phase).to(equal(Day.PHASES[0]))
    expect(school.day.number).to(equal(1))
