from setting import valid_email, valid_password

from requests_toolbelt.multipart.encoder import MultipartEncoder

import requests

"""Свои методы с запросами"""

base_url = "https://petfriends.skillfactory.ru/"

#pet_photo = (open('venv/images/DRUNIA2.jpg', 'rb'), 'images/jpeg')

"""Метод выдает auth_key"""
def get_api_key(URL):
    base_url = URL

    headers = {
                'email': valid_email,
                'password': valid_password,
            }
    res = requests.get(base_url + 'api/key', headers=headers)

    return res.json()


auth_key = get_api_key(base_url)
# print(auth_key)


"""Получаем всех питомцев"""
def spisok_pets(auth_key):
    auth_key = auth_key
    headers = {'auth_key': auth_key['key']}

    filter = {'filter': ""}# Пустой фильтр на всех питомцев
    res = requests.get(base_url + 'api/pets', headers=headers, params=filter)
    result = res.json()
    status = res.status_code
    return result

# vse_pitomci = spisok_pets(auth_key)

#print(vse_pitomci)

def moi_pets(auth_key):
    auth_key = auth_key
    headers = {'auth_key': auth_key['key']}

    filter = {'filter': 'my_pets'}# Фильтр на своих питомцев my pets
    res = requests.get(base_url + 'api/pets', headers=headers, params=filter)
    result = res.json()
    status = res.status_code
    return result

my_pets = moi_pets(auth_key)
# print(my_pets)

"""Полный ПОСТ запрос"""

def polnuy_post(name='', animal_type='', age='', pet_photo=''):

    data = MultipartEncoder(
        fields={
            'name': name,
            'animal_type': animal_type,
            'age': age,
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/jpeg')
        })
    headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

    res = requests.post(base_url + 'api/pets', headers=headers, data=data)

    return res.status_code



#status = polnuy_post(name='Бруня', animal_type='кошка', age='8', pet_photo= 'venv/images/DRUNIA2.jpg')


#print(status)


"""Метод ПОСТ на добавление питомца без фото"""

def post_bez_foto(name='', animal_type='', age=''):


    data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })
    headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

    res = requests.post(base_url + '/api/create_pet_simple', headers=headers, data=data)

    return res.status_code


# result = post_bez_foto(name = 'Бoруня',animal_type = 'кошка',age = '17')
#
# print(result)

#pet_id = my_pets['pets'][0]['id']


"""Метод PUT добавляем информацию в последнюю созданую сущность"""

def put_inform(auth_key, pet_id, name: str, age: str, animal_type: str ):

    headers = {'auth_key': auth_key['key']}
    data = {
        'name': name,
        'age': age,
        'animal_type': animal_type
    }

    res = requests.put(base_url + 'api/pets/' + pet_id, headers=headers, data=data)

    return res.json()

# put_zapross = put_inform(auth_key, pet_id, 'козяка', '56', 'бизон')
#
# print(put_zapross)


"""Метод ДЕЛИТ автоматически удаляет питомцев с 0 ID"""
def delete_my_pets(auth_key, pet_id):

    headers = {'auth_key': auth_key['key']}

    res = requests.delete(base_url + 'api/pets/' + pet_id, headers=headers)

    return res.status_code

#otvet_delete = delete_my_pets(auth_key, pet_id)

#print(otvet_delete)

"""Метод ПОСТ на добавление фото питомца"""

def photo_pitomca(auth_key, pet_id, pet_photo=''):

    data = MultipartEncoder(
        fields={
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/jpeg')
        })
    headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
    res = requests.post(base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)

    return res.status_code

#photo = photo_pitomca(auth_key, pet_id, pet_photo='DRUNIA2.jpg')

#print(photo)

"""Метод ПОСТ на добавление фото с некорректными данными фото"""

def photo_pitomca_ne_formant(auth_key, pet_id, pet_photo=''):


    data = MultipartEncoder(
        fields={
            'pet_photo': (pet_photo)
        })
    headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
    res = requests.post(base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)

    return res.status_code


def post_bez_foto_ochibka_key_403(auth_key, name='', animal_type='', age=''):


    data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })
    headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

    res = requests.post(base_url + '/api/create_pet_simple', headers=headers, data=data)

    return res.status_code