from repositories import CategoryRepository

def categorySeeder():
    category = ["T-shirt",
                "Trouser",
                "Pullover",
                "Dress",
                "Coat",
                "Sandal",
                "Shirt",
                "Sneaker",
                "Bag",
                "Ankle boot",
                "Hat"]

    for c in category:
        CategoryRepository.create(c)
