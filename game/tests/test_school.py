from django.test import TestCase
from game.factories import SchoolFactory
from game.models import School, Gladiator, Challenge
from game.tests.matchers import change
from expects import *


class SchoolTestCase(TestCase):
  def test_advance_period(self):
    school = SchoolFactory.create(
      period=School.PERIODS[0]
    )

    # Step a day through its phases. Once the last phase has completed,
    # expect advance to start a new day
    def cycle_periods():
      for period in School.PERIODS:
        expect(school.period).to(equal(period))
        school.advance_period()

    expect(
      cycle_periods
    ).to(
      change(lambda: school.day).by(1)
    )

  def test_generate_candidates(self):
    school = SchoolFactory.create(day=1)
    expect(Gladiator.candidates.filter(school=school).count()).to(be(0))

    candidates = school.generate_candidates(3)
    expect(Gladiator.candidates.filter(school=school).count()).to(be(3))

    candidate0_id = candidates[0].id
    candidate1_id = candidates[1].id
    candidate2_id = candidates[2].id

    candidates[0].reserved_on = school.day
    candidates[0].save()

    candidates[1].reserved_on = school.day - 1
    candidates[1].save()

    school.day += 1
    school.save()

    candidates = school.generate_candidates()
    id_list = [c.id for c in candidates]
    expect(candidate0_id in id_list).to(be(True))
    expect(candidate1_id in id_list).to(be(False))
    expect(candidate2_id in id_list).to(be(False))

  def test_generate_challenges(self):
    school = SchoolFactory.create(day=1)
    expect(Challenge.issued.filter(school=school).count()).to(be(0))

    challenge_set_one = school.generate_challenges(3)
    expect(Challenge.issued.filter(school=school).count()).to(be(3))

    challenge_set_two = school.generate_challenges(3)
    expect(Challenge.issued.filter(school=school).count()).to(be(3))
    intersection = set(challenge_set_one).intersection(challenge_set_two)

    expect(bool(intersection)).to(be(False))
