from flask_restful import Resource
from flask_restful.reqparse import Argument
from utils import parse_params, response, admin_required
from repositories import AnnouncementRepository


class AnnouncementsResource(Resource):
    """ Brands Resource """

    def get(self):
        """ Get all brands """

        announcements = AnnouncementRepository.get_all()

        data = [
            {
                "id": announcement.id,
                "title": announcement.title,
                "content": announcement.content
            } for announcement in announcements
        ]

        res = {
            "data": data
        }

        return response(res, 200)

    @parse_params(
        Argument("title", location="json", required=True, help="Titiel is required"),
        Argument("content", location="json", required=True, help="Content is required")
    )
    @admin_required
    def post(self, title, content, user_id):
        """ Create announcement """

        announcement = AnnouncementRepository.get_by(title=title).one_or_none()

        if announcement is not None:
            return response({
                "error": "Announcement is already exists"
            }, 400)

        AnnouncementRepository.create(title=title, content=content)

        res = {
            "message": "Announcement added"
        }

        return response(res, 201)

    @parse_params(
        Argument("id", location="json", required=True, help="Id is required"),
        Argument("title", location="json", required=True, help="Titiel is required"),
        Argument("content", location="json", required=True, help="Content is required")
    )
    @admin_required
    def put(self, id, title, content, user_id):
        """ Update announcement """

        announcement = AnnouncementRepository.get_by(id=id).one_or_none()

        if announcement is None:
            return response({
                "error": "Announcement not found"
            }, 404)

        AnnouncementRepository.update(id=id, title=title, content=content)

        res = {
            "message": "Announcement updated"
        }


class AnnouncementResource(Resource):

    def delete(self, id):
        """ Delete announcement """

        announcement = AnnouncementRepository.get_by(id=id).one_or_none()

        if announcement is None:
            return response({
                "error": "Announcement not found"
            }, 404)

        AnnouncementRepository.delete(id=id)

        res = {
            "message": "Announcement deleted"
        }

        return response(res, 200)
