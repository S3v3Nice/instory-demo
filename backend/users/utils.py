from django.contrib.auth.tokens import PasswordResetTokenGenerator

from users.models import User


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp):
        return str(user.pk) + str(timestamp) + str(user.email) + str(user.date_verified_email)
