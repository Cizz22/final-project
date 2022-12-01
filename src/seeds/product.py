from repositories import CategoryRepository, ProductRepository


def productSeeder():
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

    for c in category, 1:
        category = CategoryRepository.get_by(category_name=c).first()
        for i in range(5):
            product = ProductRepository.create(title=f"{c}_{i}" , price=10000 , category_id=category.id,
                                               condition="New", product_detail=f"This is {c} detail")
            ProductRepository.create_image(["image/dummy.jpg"], product_id=product.id)
