from api import PetFriends
from proba import *
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_post_pitomec_bez_photo(name='Василий', animal_type='крокодил', age='100'):
    """Проверка на добавление сущности через ПОСТ запросс без фото
    и сравнение результатов в данных"""

    auth_key = get_api_key("https://petfriends.skillfactory.ru/")
    print(auth_key)
    result = post_bez_foto(name, animal_type, age)
    """Возвращаем полный ответ о новой сущности POST без photo"""
    print(result)
    assert result == 200


def test_put_obnovlenie_suchnosti_bez_photo():
    """Проверка замены сущности с помощью запроса API PUT"""
    auth_key = get_api_key("https://petfriends.skillfactory.ru/")
    print(auth_key)# получаем токкен для запроса

    """Вызываем список my_pets с помощью функции """
    my_pets = moi_pets(auth_key)
    print(my_pets)

    """Получаем ID сущности"""
    pet_id = my_pets['pets'][0]['id']
    print(pet_id)

    """Отправляем put запрос"""
    put_zapross = put_inform(auth_key, pet_id, 'МОНСТРЮКА', '56', 'вепрь')
    print(put_zapross)

    """Проверяем список my_pets"""
    my_pets = moi_pets(auth_key)
    print(my_pets)

    assert put_zapross != my_pets


def test_post_zapross_dobavlenie_photo():

    """Отправляем ПОСТ запрос c  корректными даными фото
      к существующему питомцу и получаем статус код 200 """
    auth_key = get_api_key("https://petfriends.skillfactory.ru/")
    print(auth_key)  # получаем токкен для запроса

    """Вызываем список my_pets с помощью функции  и смотрим в ответ что питомцы без фото"""
    my_pets = moi_pets(auth_key)
    print(my_pets)

    """Получаем ID сущности"""
    pet_id = my_pets['pets'][0]['id']
    print(pet_id)

    """Отправляем ПОСТ запрос на добавление фото с помощью метода и получаем статус код 200"""

    photo = photo_pitomca(auth_key, pet_id, pet_photo='images/DRUNIA2.jpg')
    print(photo)

    """Вызываем список my_pets с помощью функции  и смотрим в ответ что питомец с фото"""
    my_pets = moi_pets(auth_key)
    print(my_pets)
    assert photo == 200


def test_post_zapross_dobavlenie_photo_status_cod_400():

    """Отправляем ПОСТ запрос c не корректными даными фото
      к существующему питомцу и получаем статус код 400 """
    auth_key = get_api_key("https://petfriends.skillfactory.ru/")
    print(auth_key)  # получаем токкен для запроса

    """Вызываем список my_pets с помощью функции  и смотрим в ответ что питомцы без фото"""
    my_pets = moi_pets(auth_key)
    print(my_pets)

    """Получаем ID сущности"""
    pet_id = my_pets['pets'][0]['id']
    print(pet_id)

    """Отправляем ПОСТ запрос на добавление фото (другим форматом) с помощью метода 
    и получаем статус код 400"""

    photo = photo_pitomca_ne_formant(auth_key, pet_id, pet_photo='images/P1040103.jpg')
    print(photo)

    assert photo == 400

def test_post_pitomec_bez_photo_ochibka_403(name='Василий', animal_type='крокодил', age='100'):
    """Проверка на добавление сущности через ПОСТ запросс без фото
    c недостоверным auth_key и вызов ошибки 403"""

    auth_key = {'key': '87e4bc24c77bf6029047a3aa8950efa6cb8fdf14328f2901'}
    """Обращаемся к методу и вызываем ПОСТ запросс с фальшивым KEY"""
    result = post_bez_foto_ochibka_key_403(auth_key, name, animal_type, age)
    """Возвращаем  ответ статус код ошибка 403"""
    print(result)
    assert result == 403




