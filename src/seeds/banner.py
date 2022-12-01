from repositories import BannerRepository


def bannerSeeder():
    for i in range(4):
        BannerRepository.create(
            title=f"Banner {i}",
            image=f"image/banner{i+1}.jpg",
        )
