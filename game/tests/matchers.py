from expects.matchers import Matcher

class change(Matcher):
  def __init__(self, variable_thunk, *args):
    self.variable_thunk = variable_thunk
    self.expected_initial = None
    self.expected_result = None
    self.args = args

  def by(self, amount):
    self.expected_result = self.variable_thunk() + amount
    return self

  def to_value(self, value):
    self.expected_result = value
    return self

  def from_value(self, value):
    self.expected_initial = value
    return self

  def _match(self, action_thunk, *args):
    initial = self.variable_thunk()
    action_thunk(*args)
    result = self.variable_thunk()

    if self.expected_initial is None and self.expected_result is None:
      passed = initial != final

    else:
      passed = True
      if self.expected_initial:
        passed = passed and initial == self.expected_initial

      if self.expected_result:
        passed = passed and result == self.expected_result

    return (True, ["Changed"]) if passed else (False, ["Not Changed"])
