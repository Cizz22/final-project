"""
Defines the blueprint for the announcement
"""
from flask import Blueprint
from flask_restful import Api

from resources import AnnouncementsResource, AnnouncementResource

ANNOUNCEMENT_BLUEPRINT = Blueprint("announcement", __name__)

Api(ANNOUNCEMENT_BLUEPRINT).add_resource(
    AnnouncementsResource, "/announcements"
)

Api(ANNOUNCEMENT_BLUEPRINT).add_resource(
    AnnouncementResource, "/announcements/<string:id>"
)
