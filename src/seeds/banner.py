from repositories import BannerRepository


def bannerSeeder():
    for i in range(4):
        BannerRepository.create(
            title=f"Banner {i}",
            image="https://picsum.photos/1920/1080",
        )
