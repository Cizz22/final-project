""" Defines the User repository """

from models import User


class UserRepository:
    """ The repository for the user model """

    @staticmethod
    def get_by_email(email):
        """ Query a user by email """
        return User.query.filter_by(email=email).one_or_none()

    @staticmethod
    def create(name, email, phone_number, password, type):
        """ Create a new user """
        user = User(name, email, phone_number, type=type)
        user.set_password(password)
        return user.save()
    
        
