from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

''''Тест 1'''
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''Проверяем что код статуса запроса 200 и в переменной result
        содержится слово key'''
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

''''Тест 2'''
def test_get_all_pets_with_valid_key(filter=""):
    '''Проверяем что код статуса запроса 200 и список всех питомцев не пустой
        Для этого при помощи метода get_app_key() получаем ключ, сохраняем его в переменной
        api_key, затем применяем метод get_list_of_pets() и проверяем статус ответа и то
        что список питомцев не пустой'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0

''''Тест 3'''
def test_add_pets_with_valid_data(name='Kotia', animal_type='cat', age='2', pet_photo='images/Kotia.jpg'):
    '''Проверяем что код статуса запроса 200 и что список с добавленными данными не пустой для этого
       в переменную pet_photo сохраняем путь к файлу фотографии питомца, сохраняем ключ в переменную api_key,
       проверяем статус ответа и что в ответе содержатся добавленные данные.
        '''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

'''Тест 4'''
def test_delete_pet():
    '''Проверяем возможность удаления питомца'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pets(api_key, 'Motia', 'cat', '5', 'images/Kotia.jpg')
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pets(api_key, pet_id)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

'''Тест 5'''
def test_update_pet_info(name='из', animal_type='измененный', age='5'):
    '''Проверяем возможность изменения данных питомца'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")

'''Тест 6'''
def test_add_pets_with_valid_data_without_photo(name='КотяБезФото', animal_type='кот', age='8'):
    '''Проверяем возможность добавления нового питомца без фото'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

'''Тест 7'''
def test_add_photo_at_pet(pet_photo='images/Pesia.jpg'):
    '''Проверяем возможность добавления новой фотографии питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")

'''Тест 8'''
def test_add_pet_negative_age_number(name='Kotik', animal_type='dog', age='-3', pet_photo='images/Pesia.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
       Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.
        '''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert age not in result['age'], 'Питомец добавлен на сайт с отрицательным числом в поле возраст'

'''Тест 9'''
def test_add_pet_with_four_digit_age_number(name='Kotik', animal_type='dog', age='2235', pet_photo='images/Pesia.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с числом более трех знаков в переменной age.
       Тест не будет пройден ели питомец будет добавлен на сайт с числом превышающим три знака в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    number = result['age']

    assert len(number) < 4, 'Питомец добавлен на сайт с числом привышающим 3 знака в поле возраст'

'''Тест 10'''
def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='dog', age='5', pet_photo='images/Pesia.jpg'):
    '''Проверяем возможность добавления питомца с пустым значением в переменной name
    Тест не будет пройден если питомец будет добавлен на сайт с пустым значением в поле "имя"'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != '', 'Питомец добавлен на сайт с пустым значением в имени'

'''Тест 11'''
def test_add_pet_with_a_lot_of_words_in_variable_name(animal_type='cat', age='2', pet_photo='images/Kotia.jpg'):
    '''Проверка с негативным сценарием. Добавления питомца имя которого превышает 5 слов
    Тест не будет пройден если питомец будет добавлен на сайт с именем состоящим из более 5 слов'''

    name = 'Хуан Пабло Диего Альварес Эскобар'

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    word_count = len(list_name)

    assert status == 200
    assert word_count < 5, 'Питомец добавлен с именем больше 5 слов'

'''Тест 12'''
def test_add_pet_with_special_characters_in_variable_animal_type(name='Kotia', age='3', pet_photo='images/Kotia.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с специальными символами вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен на сайт с спец.символами вместо букв в поле порода.
    '''
    animal_type = 'Cat%@'
    symbols = '#$%^&*{}|?/><=+_~@'
    symbol = []

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    for i in symbols:
        if i in result['animal_type']:
            symbol.append(i)
    assert symbol[0] not in result['animal_type'], 'Питомец добавлен с недопустимыми спец.символами'

'''Тест 13'''
def test_add_pet_with_numbers_in_variable_animal_type(name='Pesia', animal_type='52456', age='2',
                                                      pet_photo='images/Pesia.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с цифрами вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен на сайт с цифрами вместо букв в поле порода.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец добавлен на сайт с цифрами вместо букв в поле порода'

'''Тест 14'''
def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Pesia', age='3', pet_photo='images/Pesia.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца название породы которого превышает 5 слов
    Тест не будет пройден если питомец будет добавлен на сайт с названием породы состоящим из более 5 слов'''

    animal_type = 'брабансон австралийский овчаро подобный но милый'

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count < 5, 'Питомец добавлен с названием породы больше 5 слов'

'''Тест 15'''
def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_app_key(email, password)
    assert status == 403
    assert 'key' not in result

'''Тест 16'''
def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_app_key(email, password)
    assert status == 403
    assert 'key' not in result