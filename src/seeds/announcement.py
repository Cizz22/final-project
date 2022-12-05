from repositories import AnnouncementRepository

def announcementSeeder():
    brand = ["A", "B", "C", "D"]
    content = "This is announcement"

    for b in brand:
        AnnouncementRepository.create(b, content)
