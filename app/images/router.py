import shutil
from fastapi import APIRouter, UploadFile
from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Загрузка изображений"]
)


@router.post("/hotels/{hotel_id}")
async def add_hotel_images(hotel_id: int, file1: UploadFile,
                           file2: UploadFile, file3: UploadFile):
    """Загрузка изображений для отеля"""

    # сделать всё адекватно в цикле
    # + добавить возможность добавлять меньше 3 изображений

    im_path_1 = f"app/static/images/hotels/{hotel_id}_1.webp"
    im_path_2 = f"app/static/images/hotels/{hotel_id}_2.webp"
    im_path_3 = f"app/static/images/hotels/{hotel_id}_3.webp"
    with open(im_path_1, "wb+") as file_object:
        shutil.copyfileobj(file1.file, file_object)
    process_pic.delay(im_path_1)
    with open(im_path_2, "wb+") as file_object:
        shutil.copyfileobj(file2.file, file_object)
    process_pic.delay(im_path_2)
    with open(im_path_3, "wb+") as file_object:
        shutil.copyfileobj(file3.file, file_object)
    process_pic.delay(im_path_3)

    return {"details": f"Все изображения успешно загружены для отеля с id {hotel_id}"}


@router.post("/rooms/{room_id}")
async def add_rooms_images(room_id: int, file1: UploadFile,
                           file2: UploadFile, file3: UploadFile):
    """Загрузка изображений для комнаты"""

    # сделать всё адекватно в цикле
    # + добавить возможность добавлять меньше 3 изображений

    im_path_1 = f"app/static/images/rooms/{room_id}_1.webp"
    im_path_2 = f"app/static/images/rooms/{room_id}_2.webp"
    im_path_3 = f"app/static/images/rooms/{room_id}_3.webp"
    with open(im_path_1, "wb+") as file_object:
        shutil.copyfileobj(file1.file, file_object)
    process_pic.delay(im_path_1)
    with open(im_path_2, "wb+") as file_object:
        shutil.copyfileobj(file2.file, file_object)
    process_pic.delay(im_path_2)
    with open(im_path_3, "wb+") as file_object:
        shutil.copyfileobj(file3.file, file_object)
    process_pic.delay(im_path_3)

    return {"details": f"Все изображения успешно загружены для комнаты с id {room_id}"}
