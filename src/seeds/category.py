from repositories import CategoryRepository

def categorySeeder():
    category = ["T-shirt/top",
                "Trouser",
                "Pullover",
                "Dress",
                "Coat",
                "Sandal",
                "Shirt",
                "Sneaker",
                "Bag",
                "Ankle boot"]

    for c in category:
        CategoryRepository.create(c)
