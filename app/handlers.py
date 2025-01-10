
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests

import app.keyboards as kb
import app.db as db

URL = "http://79.174.91.102:5000"

router = Router()

# class Register(StatesGroup):
#     name = State()
#     age = State()
#     number = State()

class UserStates(StatesGroup):
    user_code = State()
    name = State()
    add_userId = State()
    delete_userId = State()
    add_self_subject = State()
    delete_self_subject = State()
    show_test = State()
    show_result = State()
    active_attempt = State()
    test_results = State()
    create_subject = State()
    update_subject = State()
    delete_subject = State()
    create_test = State()
    update_test = State()
    delete_test = State()
    info_test = State()
    create_question = State()
    update_question = State()
    delete_question = State()
    info_question = State()
    get_questions = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    session_token = str(message.from_user.id)
    response = requests.get(URL+"/user/get_data", headers={"session_token": session_token})
    if response.ok:
        role = "Не определено"
        if response.json()["role"] == 0:
            role = "Студент"
        elif response.json()["role"] == 1:
            role = "Преподаватель"
        await message.answer(f"userId: {response.json()["userId"]}\n Фамилия: {response.json()["lastName"]}\n Имя: {response.json()["firstName"]}\n Отчество: {response.json()["patronymic"]}\n Роль: {role}")
    else:
        await message.answer("Вы не зарегистрированы")
    # await message.answer('Выберите способ регистрации', reply_markup=kb.catalog)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("""Перечень команд бота\n
/start - запуск бота\n 
/help - поддержка\n 
/login - вход в аккаунт\n 
/logout - выход из аккаунта\n 
/change_name - изменить данные о пользователе(ФИО)\n 
/get_code - получить код, для входа с другого устройства\n 
/submit_role - подтверждение роли\n 
/get_subjects - получение предметов, на которые пользователь записан\n 
/get_all_subjects - получение предметов, находящихся в системе\n 
/get_data - получение личных данных\n
/add_user_to_subject - добавить студента на предмет(ПРЕПОДАВАТЕЛЬ)\n
/delete_user_from_subject - удалить студента с предмета(ПРЕПОДАВАТЕЛЬ)\n
/add_to_subject - добавиться на предмет(СТУДЕНТ)\n
/delete_from_subject - покинуть предмет(СТУДЕНТ)\n
/show_test - показывает информацию о тесте студенту\n
/get_attempt - получить информацию о попытке(сколько баллов получил, завершена или нет)(ПОДРОБНЫЙ ОТВЕТ\n)
/get_attempts - получить все свои попытки(КОРОТКАЯ ИНФОРМАЦИЯ)\n
/create_subject - создать предмет(ПРЕПОДАВАТЕЛЬ)\n
/update_subject - обновить предмет(ПРЕПОДАВАТЕЛЬ)\n
/delete_subject - удалить предмет(ПРЕПОДАВАТЕЛЬ)\n
/create_test - создать тест(ПРЕПОДАВАТЕЛЬ)\n
/update_test - обновить тест(ПРЕПОДАВАТЕЛЬ)\n
/delete_test - удалить тест(ПРЕПОДАВАТЕЛЬ)\n
/info_test - показывает более подробную информацию о тесте(ПРЕПОДАВАТЕЛЬ)\n
/create_question - создать вопрос(ПРЕПОДАВАТЕЛЬ)\n
/update_question - обновить вопрос(ПРЕПОДАВАТЕЛЬ)\n
/delete_question - удалить вопрос(ПРЕПОДАВАТЕЛЬ)\n
/info_question - показывает более подробную информацию о вопросе(ПРЕПОДАВАТЕЛЬ)\n
/get_questions -  показывает все вопросы в предмете(ПРЕПОДАВАТЕЛЬ)""")





async def cmd_login(message: Message):
    session_token = str(message.from_user.id)
    response = requests.get(URL+"/user/get_data", headers={"session_token": session_token})
    if response.ok:
        await message.answer("Вы уже зарегистрированы")
    else:
        data = {
        'access_token': 'none',
        'refresh_token': 'none',
        'session_token': session_token
        }
        response_token = requests.put(URL+"/token/link_token", json=data)
        print(response_token.json())
        await message.answer('После перехода по ссылке, если вы не регистрировались ренее или \
                             ваш аккаунт не активирован, то выберите роль по команде /submit_role')
        await message.answer('Выберите способ регистрации', reply_markup=kb.catalog)


@router.message(Command("logout"))
async def cmd_logout(message: Message):
    session_token = str(message.from_user.id)
    data = {
        "session_token": session_token
    }
    response = requests.post(URL+"/user/logout", json=data)
    if response.ok:
        await message.answer("Вы успешно вышли из аккаунта")
    else:
        await message.answer("Произошла ошибка")


@router.message(Command("change_name"))
async def cmd_change_name(message: Message, state: FSMContext):
    await state.set_state(UserStates.name)
    await message.answer('Введите свое новое ФИО через пробел')

@router.message(UserStates.name)
async def changed_name(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    arr = message.text.split(" ")
    if len(arr) != 3:
        await message.answer("Введен неправильный формат данных")
        return
    
    data = {
        "session_token": session_token,
        "firstName": arr[1],
        "lastName": arr[0],
        "patronymic": arr[2]
    }
    response = requests.post(URL+"/user/update_data", json=data)
    if response.ok:
        await message.answer("Данные успешно обновлены")
    else:
        await message.answer("Данные обновить не удалось")
    
    await state.clear()

@router.callback_query(F.data == 'yandex')
async def yandex(callback: CallbackQuery):
    await callback.answer(' ')
    session_token = str(callback.from_user.id)
    params = {"session_token": session_token, "type": "yandex"}
    response_ya = requests.get(URL+"/user/link_registration_tg", params=params)
    await callback.message.answer(response_ya.json()["link"])



@router.callback_query(F.data == 'git')
async def git(callback: CallbackQuery):
    await callback.answer(' ')
    session_token = str(callback.from_user.id)
    params = {"session_token": session_token, "type": "github"}
    response_git = requests.get(URL+"/user/link_registration_tg", params=params)
    await callback.message.answer(response_git.json()["link"])


@router.callback_query(F.data == 'code')
async def code(callback: CallbackQuery, state: FSMContext):
    await callback.answer(' ')
    await state.set_state(UserStates.user_code)
    await callback.message.answer('Введите код')


@router.message(UserStates.user_code)
async def state_code(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    data = {
        "session_token": session_token,
        "code": message.text
    }
    response = requests.post(URL+"/user/submit_code", json=data)
    if response.ok:
        await message.answer("Вы успешно ввели код")
    else:
        await message.answer("Код неверный")
    await state.clear()
    
@router.message(Command('get_code'))
async def get_code(message: Message):
    session_token = str(message.from_user.id)
    response = requests.get(URL+"/user/get_code", headers={"session_token": session_token})
    if response.ok:
        await message.answer(f"Код: {response.json()["code"]}")
    else:
        await message.answer(f"Получение кода невозможно {response.status_code}")

@router.message(Command('submit_role'))
async def sub_role(message: Message):
    await message.answer("Выберите роль", reply_markup=kb.roles)
    # response = requests.get(URL+"/user/get_data", headers={})


@router.callback_query(F.data =='student')
async def student(callback: CallbackQuery):
    await callback.answer(' ')
    session_token = str(callback.from_user.id)
    data = {
        "session_token": session_token,
        "role": "student"
    }
    response = requests.post(URL+"/user/submit_role", json=data)
    if response.ok:
        await callback.message.answer("Роль установлена")
    else:
        await callback.message.answer("Роль не установлена. Возможно она у вас уже есть.")


@router.callback_query(F.data =='teacher')
async def teacher(callback: CallbackQuery):
    await callback.answer(' ')
    session_token = str(callback.from_user.id)
    data = {
        "session_token": session_token,
        "role": "teacher"
    }
    response = requests.post(URL+"/user/submit_role", json=data)
    if response.ok:
        await callback.message.answer("Роль установлена")
    else:
        await callback.message.answer("Роль не установлена. Возможно она у вас уже есть.")


@router.message(Command('get_subjects'))
async def get_subj(message: Message):
    session_token = str(message.from_user.id)
    response = requests.post(URL+"/subject/get_data", headers={"session_token": session_token})
    if response.ok:
        text_response = "Ваши предметы\n\n"
        for item in response.json():
            text_response += f"Название: {item["title"]}\n Описание: {item["description"]}\n Автор: {item["userId"][0]}\n Тесты: {", ".join(map(str, item["testsId"]))}\n subjectId: {item["id"]}\n{ ("Пользователи: " +(", ".join(map(str, item["usersId"]))) + "\n") if "usersId" in item else " " } \n"
        await message.answer(text_response)
    else:
        await message.answer('Данные получить не удалось')



@router.message(Command('get_data'))
async def cmd_start(message: Message):
    session_token = str(message.from_user.id)
    response = requests.get(URL+"/user/get_data", headers={"session_token": session_token})
    if response.ok:
        role = "Не определено"
        if response.json()["role"] == 0:
            role = "Студент"
        elif response.json()["role"] == 1:
            role = "Преподаватель"
        await message.answer(f"userId: {response.json()["userId"]}\n Фамилия: {response.json()["lastName"]}\n Имя: {response.json()["firstName"]}\n Отчество: {response.json()["patronymic"]}\n Роль: {role}")
    else:
        await message.answer("Вы не зарегистрированы")



@router.message(Command('get_all_subjects'))
async def get_all_subjs(message: Message):
    session_token = str(message.from_user.id)
    response = requests.post(URL+"/subject/get_all", headers={"session_token": session_token})
    if response.ok:
        text_response = "Ваши предметы\n\n"
        for item in response.json():
            text_response += f"Название: {item["title"]}\n Описание: {item["description"]}\n Автор: {item["userId"][0]} \n subjectId: {item["id"]}\n\n"
        await message.answer(text_response)
    else:
        await message.answer('Данные получить не удалось')




@router.message(Command('add_user_to_subject'))
async def add_user_to_sub(message: Message, state: FSMContext):
    await state.set_state(UserStates.add_userId)
    await message.answer('Введите subjectId и userId которого хотите добавить (доступно только преподавателю)')

@router.message(UserStates.add_userId)
async def changed_name(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    arr = message.text.split(" ")
    if len(arr) != 2:
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    data = {
        "session_token": session_token,
        "userId": arr[1],
        "subjectId": int(arr[0]),
    }
    response = requests.post(URL+"/subject/add_user", json=data)
    if response.ok:
        await message.answer("Пользователь успешно добавлен")
    else:
        await message.answer("Добавить пользователя не удалось")

    await state.clear()



@router.message(Command('delete_user_from_subject'))
async def add_user_to_sub(message: Message, state: FSMContext):
    await state.set_state(UserStates.delete_userId)
    await message.answer('Введите subjectId и userId которого хотите удалить (доступно только преподавателю)')

@router.message(UserStates.delete_userId)
async def changed_name(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    arr = message.text.split(" ")
    if len(arr) != 2:
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    data = {
        "session_token": session_token,
        "userId": arr[1],
        "subjectId": int(arr[0]),
    }
    response = requests.post(URL+"/subject/delete_user", json=data)
    if response.ok:
        await message.answer("Пользователь успешно удален")
    else:
        await message.answer("Удалить пользователя не удалось")

    await state.clear()



@router.message(Command('add_to_subject'))
async def add_user_to_sub(message: Message, state: FSMContext):
    await state.set_state(UserStates.add_self_subject)
    await message.answer('Введите subjectId куда хотите добавиться')

@router.message(UserStates.add_self_subject)
async def changed_name(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
   
    if (not(message.text.isdigit()) ) :
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    data = {
        "session_token": session_token,
        "subjectId": int(message.text),
    }
    response = requests.post(URL+"/subject/add_user_self", json=data)
    if response.ok:
        await message.answer("Вы успешно добавлены")
    else:
        await message.answer("Добавить не удалось")

    await state.clear()




@router.message(Command('delete_from_subject'))
async def add_user_to_sub(message: Message, state: FSMContext):
    await state.set_state(UserStates.delete_self_subject)
    await message.answer('Введите subjectId которе хотите покинуть')

@router.message(UserStates.delete_self_subject)
async def changed_name(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
   
    if (not (message.text.isdigit())):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    data = {
        "session_token": session_token,
        "subjectId": int(message.text),
    }

    response = requests.post(URL+"/subject/delete_user_self", json=data)
    if response.ok:
        await message.answer("Вы успешно удалены")
    else:
        await message.answer("Удалить не удалось")

    await state.clear()



@router.message(Command('show_test'))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.show_test)
    await message.answer('Введите subjectId и testId которого хотите увидеть (доступно только студенту)')


@router.message(UserStates.show_test)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    arr = message.text.split(" ")
    if len(arr) != 2:
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    if (not (arr[0].isdigit() or arr[1].isdigit())):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    data = {
        "session_token": session_token,
        "testId": int(arr[1]),
        "subjectId":  int(arr[0]),
    }
    response = requests.post(URL+"/test/get_data", json=data)
    if response.ok:
        await message.answer(f"Название: {response.json()["name"]} \n Описание: {response.json()["description"]} \n Автор: {response.json()["userId"]}",reply_markup=kb.start_test)
    else:
        await message.answer("Получить данные не удалось")

    await state.clear()



@router.callback_query(F.data == "start_test")
async def start_test(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.active_attempt)
    await state.update_data(active_attempt = -1)
    tt = await state.get_data()
    print(tt)
    await callback.message.answer('Введите subjectId и testId которое хотите начать проходить (доступно только студенту)')

@router.message(UserStates.active_attempt)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    cur_attemptId = (await state.get_data())["active_attempt"]
    if message.text == "stop":
        data = {
            "session_token": session_token,
            "attemptId": int(cur_attemptId)
        }
        response = requests.post(URL+"/test/stop_attempt", json=data)
        if not response.ok:
            await message.answer("Закончить тест не удалось")
            return
        else:
            await message.answer("Попытка завершена")
            await state.clear()
            return  

    if cur_attemptId == -1:
        arr = message.text.split(" ")
        if len(arr) != 2:
            await message.answer("Введен неправильный формат данных")
            await state.clear()
            return
        
        if (not (arr[0].isdigit() or arr[1].isdigit())):
            await message.answer("Введен неправильный формат данных")
            await state.clear()
            return  
        data = {
            "session_token": session_token,
            "testId": int(arr[1]),
            "subjectId":  int(arr[0]),
        }
        response = requests.post(URL+"/test/start_test", json=data)
        if not response.ok:
            response = requests.post(URL+"/test/get_active_attempt", json=data)
            if not response.ok:
                await message.answer("Начать не получилось. Возможно что то пошло не так.")
                return
            await message.answer("Вы были перенаправленны на текущую попытку")
        
        attemptId = response.json()["attemptId"]
        await state.update_data(active_attempt = attemptId)
        data1 = {
            "session_token": session_token,
            "attemptId": response.json()["attemptId"]
        }
        response1 = requests.post(URL+"/test/get_question_attempt", json=data1)
        if not response1:
            await message.answer("Не удалось получить данные")
            return
        test = "+ Значит, что вы ранее выбирали этот вариант ответа.\nВведите ответы в формате:(вариант ответа для 1 вопроса) (вариант ответа для 2 вопроса) ...\nЕсли не хотите выбирать выбрать вариант ответа, то напишите -1\nЕсли хотите остановить ввод ответов, то пропишите:stop\n"
        response1_json = response1.json()
        for i in range(0,len(response1_json["questions"])):
            variants = ""
            for j in range(0,len(response1_json["questions"][i]["options"])):
                variants += f"  {"+" if response1_json["attempt"]["data"][i] == j else "-"} {str(j+1)}) {response1_json["questions"][i]["options"][j]["text"]}\n"
            test += f"{str(i+1)}) Вопрос: {response1_json["questions"][i]["question"]}\nВарианты ответов:\n{variants}\n"
        await message.answer(test)
    else:
        arr = message.text.split(" ")
        answer = []
        for i in range(len(arr)):
            if(not arr[i].isdigit()):
                await message.answer("Введен неправильный формат данных")
                return
            answer.append(int(arr[i])-1)
        data1 = {
            "session_token": session_token,
            "attemptId": cur_attemptId,
            "answers": answer
        }
        response = requests.post(URL+"/test/save_answers", json=data1)
        if not response:
            await message.answer("Не удалось сохранить ответы")
            return
        else:
            await message.answer("Ответы сохранены")
            return




@router.callback_query(F.data == "get_all_attempts")
async def start_test(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.test_results)
    await callback.message.answer('Введите testId')

@router.message(UserStates.test_results)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)

    if (not (message.text.isdigit()) ):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    data = {
        "session_token": session_token,
        "testId": int(message.text)
    }
    response = requests.post(URL+"/test/get_attempts", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        return
    
    text = ""
    response_json = response.json()
    for i in range(0,len(response_json)):
        text += f"id: {str(response_json[i]["id"])}\n"
        text += f"статус: {"закончен" if response_json[i]["finished"] else "не закончен"}\n"
        text += f"результат: {str(response_json[i]["result"])}\n\n"
        
    await message.answer(text)
    await state.clear()

    # data1 = await state.get_data()
    # print(data1)


@router.message(Command("get_attempt"))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.show_result)
    await message.answer('Введите attemptId')

@router.message(UserStates.show_result)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)

    if (not (message.text.isdigit()) ):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    data = {
        "session_token": session_token,
        "attemptId": int(message.text)
    }
    response = requests.post(URL+"/test/get_question_attempt_result", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        return
    
    text = "+ Значит, выбран этот вариант ответа.\n"
    response_json = response.json()
    for i in range(0,len(response_json["questions"])):
        variants = ""
        for j in range(0,len(response_json["questions"][i]["options"])):
            variants += f"  {"+" if response_json["attempt"]["data"][i] == j else "-"} {str(j+1)}) {response_json["questions"][i]["options"][j]["text"]}\n"
        text += f"{str(i+1)}) Вопрос: {response_json["questions"][i]["question"]}\nВарианты ответов:\n{variants}\n"
    await message.answer(text)

    await state.clear()



@router.message(Command("create_subject"))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.create_subject)
    await message.answer('(доступно только преподавателю)\nВведите название и описание через переход на новою строку  в одном сообщении:\n(название)\n(описание)')

@router.message(UserStates.create_subject)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    arr = message.text.split("\n")
    if len(arr) != 2:
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    data = {
        "session_token": session_token,
        "data": {
            "title":arr[0],
            "description":arr[1],
            "testsId":[],
            "usersId":[]
        }
    }
    
    response = requests.post(URL+"/subject/add_subject", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        await state.clear()
        return
    else:
        await message.answer("Предмет создан")
        await state.clear()
        return



@router.message(Command("update_subject"))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.update_subject)
    await message.answer('(доступно только преподавателю)\nВведите subjectId и новые название и описание через переход на новою строку в одном сообщении:\n(subjectId)\n(название)\n(описание)')

@router.message(UserStates.update_subject)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    arr = message.text.split("\n")
    if len(arr) != 3 or (not arr[0].isdigit()):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return

    data = {
        "session_token": session_token,
        "title":arr[1],
        "description":arr[2],
        "subjectId":int(arr[0])
    }
    
    response = requests.post(URL+"/subject/update_data", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        await state.clear()
        return
    else:
        await message.answer("Предмет изменен")
        await state.clear()
        return



@router.message(Command("delete_subject"))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.delete_subject)
    await message.answer('Введите subjectId которое хотите удалить (доступно только преподавателю)')

@router.message(UserStates.delete_subject)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    if not message.text.isdigit():
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return

    data = {
        "session_token": session_token,
        "subjectId":int(message.text)
    }
    
    response = requests.post(URL+"/subject/delete_data", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        await state.clear()
        return
    else:
        await message.answer("Предмет удален")
        await state.clear()
        return




@router.message(Command("create_test"))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.create_test)
    await message.answer('(доступно только преподавателю)\nВведите (статус (активирован или нет)), (название), (описание), (id вопросов) и (subjectId) через переход на новою строку в одном сообщении:\n("+" или "-")\n(название)\n(описание)\n(id вопросов через пробел, например:1 4 6 7 3)\n(subjectId)')

@router.message(UserStates.create_test)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    arr = message.text.split("\n")
    if (len(arr) != 5) or (not arr[4].isdigit()):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    id_q = arr[3].split(" ")
    id_q_int = []
    for i in range(len(id_q)):
        if not id_q[i].isdigit():
            await message.answer("Введен неправильный формат данных")
            await state.clear()
            return
        else:
             id_q_int.append(int(id_q[i]))
    hh={
        "name":arr[1],
        "description":arr[2],
        "questionsId":id_q_int,
        "activate": True if arr[0] == "+" else False,
        "attempts":[],
        "subjectId":int(arr[4]),
    }
    data = {
        "session_token": session_token,
        "data":hh
    }
    
    response = requests.post(URL+"/test/add_test", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        await state.clear()
        return
    else:
        await message.answer("Тест создан")
        await state.clear()
        return



@router.message(Command("update_test"))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.update_test)
    await message.answer('(доступно только преподавателю)\nВведите новые (статус (активирован или нет)), (название), (описание), (id вопросов) и (testId) через переход на новою строку в одном сообщении:\n("+" или "-")\n(название)\n(описание)\n(id вопросов через пробел, например:1 4 6 7 3)\n(testId)')

@router.message(UserStates.update_test)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    arr = message.text.split("\n")
    print(arr)
    if (len(arr) != 5) or (not arr[4].isdigit()):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    id_q = arr[3].split(" ")
    id_q_int = []
    for i in range(len(id_q)):
        if not id_q[i].isdigit():
            await message.answer("Введен неправильный формат данных")
            await state.clear()
            return
        else:
             id_q_int.append(int(id_q[i]))
    hh={
        "name":arr[1],
        "description":arr[2],
        "questionsId":id_q_int,
        "activate": True if arr[0] == "+" else False,
        "attempts":[]
    }
    data = {
        "session_token": session_token,
        "data":hh,
        "testId":int(arr[4]),
    }
    
    response = requests.post(URL+"/test/update_data", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        await state.clear()
        return
    else:
        await message.answer("Тест изменен")
        await state.clear()
        return



@router.message(Command("delete_test"))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.delete_test)
    await message.answer('Введите testId которое хотите удалить (доступно только преподавателю)')

@router.message(UserStates.delete_test)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    if not message.text.isdigit():
        await message.answer("Введен неправильный формат данных")
        return

    data = {
        "session_token": session_token,
        "testId":int(message.text)
    }
    
    response = requests.post(URL+"/test/delete_data", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        await state.clear()
        return
    else:
        await message.answer("Тест удален")
        await state.clear()
        return


@router.message(Command('info_test'))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.info_test)
    await message.answer('Введите testId которого хотите увидеть (доступно только преподавателю)')


@router.message(UserStates.info_test)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    
    if not (message.text.isdigit()):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    data = {
        "session_token": session_token,
        "testId": int(message.text)
    }
    response = requests.post(URL+"/test/get_full_data", json=data)
    if response.ok:
        text_attempts = "Для более подробной информации пропишите /get_attempt\n"
        for i in range(len(response.json()["attempts"])):
            text_attempts += f"{"закончен" if response.json()["attempts"][i]["finished"] == True else "не закончен"}\nattemptId:{str(response.json()["attempts"][i]["id"])}\nПользователь:{response.json()["attempts"][i]["userId"]}\nРезультат:{str(response.json()["attempts"][i]["result"])}\n\n"
        await message.answer(f"Активен: {"+" if response.json()["data"]["activate"] == True else "-" }\nНазвание: {response.json()["data"]["name"]} \n Описание: {response.json()["data"]["description"]} \n Автор: {response.json()["data"]["userId"]}\n Вопросы: {", ".join(map(str, response.json()["data"]["questionsId"])) } ")
        await message.answer(text_attempts)
    else:
        await message.answer("Получить данные не удалось")

    await state.clear()
    


@router.message(Command("create_question"))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.create_question)
    await message.answer('(доступно только преподавателю)\nВведите ((subjectId) (название), (вопрос), (номер правильного варианта) и (вопросы) через переход на новою строку в одном сообщении:\n(subjectId)\n(название)\n(вопрос)\n(номер правильного варианта)\n(вопрос №1)\n(вопрос №2)\n(вопрос №3)\n...')

@router.message(UserStates.create_question)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    arr = message.text.split("\n")

    if (len(arr) < 5) or (not arr[0].isdigit()) or (not arr[3].isdigit()):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    if not (len(arr) - 4) >= int(arr[3]):
        await message.answer("Номер правильного варианта ответа больше чем количество вариантов ответов")
        await state.clear()
        return
    if not (0 < int(arr[3])):
        await message.answer("Номер правильного варианта ответа меньше или равен 0")
        await state.clear()
        return
    arr_questions = []
    for i in range(4,len(arr)):
        arr_questions.append({"text":arr[i]})
    

    hh= {
        "var":[
            {
            "name":arr[1],
            "question":arr[2],
            "answer": int(arr[3])-1,
            "options":arr_questions
            }
        ]
    }
    data = {
        "session_token": session_token,
        "data":hh,
        "subjectId":int(arr[0])
    }
    
    response = requests.post(URL+"/test/add_question", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        await state.clear()
        return
    else:
        await message.answer("Вопрос создан")
        await state.clear()
        return

@router.message(Command("update_question"))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.update_question)
    await message.answer('(доступно только преподавателю)\nВведите новые (questionId), (название), (вопрос), (номер правильного варианта) и (вопросы) через переход на новою строку в одном сообщении:\n(questionId)\n(название)\n(вопрос)\n(номер правильного варианта)\n(вопрос №1)\n(вопрос №2)\n(вопрос №3)\n...')

@router.message(UserStates.update_question)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    arr = message.text.split("\n")

    if (len(arr) < 5) or (not arr[0].isdigit()) or (not arr[3].isdigit()):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    if not (len(arr) - 4) >= int(arr[3]):
        await message.answer("Номер правильного варианта ответа больше чем количество вариантов ответов")
        await state.clear()
        return
    if not (0 < int(arr[3])):
        await message.answer("Номер правильного варианта ответа меньше или равен 0")
        await state.clear()
        return
    arr_questions = []
    for i in range(4,len(arr)):
        arr_questions.append({"text":arr[i]})
    

    hh = {
        "name":arr[1],
        "question":arr[2],
        "answer": int(arr[3])-1,
        "options":arr_questions
    }
        
    
    data = {
        "session_token": session_token,
        "data":hh,
        "questionId":int(arr[0])
    }
    
    response = requests.post(URL+"/test/update_question", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        await state.clear()
        return
    else:
        await message.answer("Вопрос изменен")
        await state.clear()
        return


@router.message(Command("delete_question"))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.delete_question)
    await message.answer('Введите questionId которое хотите удалить (доступно только преподавателю)')

@router.message(UserStates.delete_question)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    if not message.text.isdigit():
        await message.answer("Введен неправильный формат данных")
        return

    data = {
        "session_token": session_token,
        "questionId":int(message.text)
    }
    
    response = requests.post(URL+"/test/delete_question", json=data)
    if not response.ok:
        await message.answer("Ошибка. Возможно что то пошло не так.")
        await state.clear()
        return
    else:
        await message.answer("Вопрос удален")
        await state.clear()
        return


@router.message(Command('info_question'))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.info_question)
    await message.answer('Введите questionId которого хотите увидеть (доступно только преподавателю)')


@router.message(UserStates.info_question)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    
    if not (message.text.isdigit()):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    data = {
        "session_token": session_token,
        "questionId": int(message.text)
    }
    response = requests.post(URL+"/test/get_questions", json=data)
    if response.ok:
        text = ""
        response_json = response.json()
        last_var = len(response_json["var"]) - 1
        text += f"questionId: {response_json["id"]}\n"
        text += f"Название: {response_json["var"][last_var]["name"]}\n"
        text += f"Вопрос: {response_json["var"][last_var]["question"]}\n"
        text += f"Правильный ответ: {response_json["var"][last_var]["answer"]}\n"
        text += f"Вопросы:\n"
        for i in range(len(response_json["var"][last_var]["options"])):
            text += f"  {str(i+1)}) {response_json["var"][last_var]["options"][i]["text"]}\n"
        await message.answer(text)
    else:
        await message.answer("Получить данные не удалось")

    await state.clear()
    
@router.message(Command('get_questions'))
async def show_test(message: Message, state: FSMContext):
    await state.set_state(UserStates.get_questions)
    await message.answer('Введите subjectId вопросы которого хотите увидеть (доступно только преподавателю)')


@router.message(UserStates.get_questions)
async def test_info(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    session_token = str(message.from_user.id)
    
    if not (message.text.isdigit()):
        await message.answer("Введен неправильный формат данных")
        await state.clear()
        return
    
    data = {
        "session_token": session_token,
        "subjectId": int(message.text)
    }
    response = requests.post(URL+"/test/get_questions", json=data)
    if response.ok:
        text = ""
        for h in range(len(response.json())):
            response_json = response.json()[h]
            last_var = len(response_json["var"]) - 1
            text += f"questionId: {response_json["id"]}\n"
            text += f"Название: {response_json["var"][last_var]["name"]}\n"
            text += "\n"
        await message.answer(text)
    else:
        await message.answer("Получить данные не удалось")
    await state.clear()