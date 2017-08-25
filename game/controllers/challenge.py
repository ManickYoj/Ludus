# from game.factories import MatchFactory
# from game.models import Challenge


# def challenge(challenger, recipient):
#   match = MatchFactory(entry=True)

#   challenger_challenge = Challenge(
#     status=Challenge.ACCEPTED,
#     day=challenger.day,
#     school=challenger,
#     match=match,
#   )

#   recipient_challenge = Challenge(
#     status=Challenge.ISSUED,
#     day=recipient.day,
#     school=recipient,
#     match=match,
#   )

#   challenger_challenge.save()
#   recipient_challenge.save()

#   return recipient_challenge
