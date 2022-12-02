from repositories import BrandRepository

def brandSeeder():
    brand = ["A", "B", "C", "D"]

    for b in brand:
        BrandRepository.create(b)
