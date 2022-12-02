from repositories import BannerRepository


def bannerSeeder():
    for i in range(3):
        BannerRepository.create(
            title=f"Banner {i}",
            image=f"image/banner1.jpg",
        )
