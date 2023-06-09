from django.db import models
from django.utils.translation import gettext_lazy as _


class RoomType(models.TextChoices):
    FOCUS = "focus", _("Focus")
    TEAM = "team", _("Team")
    CONFERENCE = "conference", _("Conference")
