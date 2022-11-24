from flask_seeder import Faker, generator
from repositories import UserRepository
from models import User

def userSeeder():
    faker = Faker(
        cls=User,
        init={
            "name": generator.Name(),
            "email": generator.Email(),
            "phone_number": generator.String(pattern=r"08[0-9]{8,9}"),
            "type": "buyer",
        },
    )

    for user in faker.create(10):
        UserRepository.create(
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            password="password",
            type=user.type,
        )

    UserRepository.create("admin", "admin@admin", "08123456789", "password", "seller")


