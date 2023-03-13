Inhousead_test
==============

### Входные данные: 
1) 2 ссылки на wikipedia (можно из файла можно из консоли вводить)
2) ссылки за пределами wikipedia путем не считаются
3) вручную от одной страницы до второй можно дойти за 3 клика (см прмиер)
4) необходимо показать полный путь как пройти от ссылки 1 до ссылки 2. 
5) отображение пути должно для каждого шага должно содержать текст (полное предложение в котором эта ссылка найдена) и ссылку на следующую страницу
6) отображать это можно как в консоли так и в web
7) дополнительно можно вести лог файл со всеми страницами что были посещены при поиске
 

### Пример работы:

* исходная ссылка: https://ru.wikipedia.org/wiki/Xbox_360_S
* конечная - https://ru.wikipedia.org/wiki/Nintendo_3DS
 

Ожидаемый вывод:
> * 1 ------------------------
И 15 июня 2010 года Microsoft подтвердили их на выставке E³, объявив о прекращении производства старых версий Xbox 360 и скором старте продаж усовершенствованной версии консоли.
https://ru.wikipedia.org/wiki/Electronic_Entertainment_Expo
> * 2-------------------------
Это совпало с появлением нового поколения консолей, в частности с выпуском Sega Saturn, и анонсами предстоящих релизов PlayStation, Virtual Boy и Neo Geo CD.
https://ru.wikipedia.org/wiki/Virtual_Boy
> * 3-------------------------
Стереоскопическая технология в игровых приставках вновь появилась в более поздние годы и имела больший успех, включая портативную игровую приставку Nintendo 3DS
https://ru.wikipedia.org/wiki/Nintendo_3DS
результат работы:
github + readme файл с описание логики
либо файл скрипта + readme файл с описание логики

## Основные технологии
* Python 3.11.1

## Запуск

* Переходим в корень проекта
```
cd Inhousead_test
```

* Создаем виртуальное окружение

```
python3 -m venv venv
```

* Активируем виртуальное окружение

```
source venv/bin/activate
```

* Устанавливаем зависимости

```
pip install -r requirements.txt
```

* Запускаем скрипт

```
python3 main.py
```
