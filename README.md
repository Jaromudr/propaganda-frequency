Цей набір скриптів створений для аналізу частоти використання російською пропагандою певних наративів в залежності від зовнішніх обставин

## Setup

Ми використовуємо `python3` і `pip3` і маємо встановити наступні бібліотеки:

```
pip3 install sqlalchemy
pip3 install pandas
pip3 install matplotlib
pip3 install tqdm
pip3 install configparser
```

Також перейменуйте файл `config/config.ini.template` в `config/config.ini` і заповніть кодами доступу до API телеграму, які ви можете знайти за посиланням https://my.telegram.org/ > `Api development tools`

<img width="498" alt="Знімок екрана 2022-11-27 о 20 20 09" src="https://user-images.githubusercontent.com/244409/204152813-cec0ee77-c364-437e-8af8-918022f2a9d5.png">

## Вступ
Даний пакет має три основні скрипти, що допомагають проаналізувати частоту використання наративів

`parser.py` - збирає інформацію з заданих каналів та зберігає її до бази даних
`build_graph.py` - аналізує пости на належність певному наративу пропоганди і маркує їх, враховуючи час їхнього створення
 `plotter.py` - дозволяє візуалізувати частоту використання того чи іншого наративу

## Парсинг каналів

Приклад використання:

`python3 parser.py --telegram-channel strelkovii --min-date 2022-01-01`

<img width="803" alt="Знімок екрана 2022-11-27 о 20 35 56" src="https://user-images.githubusercontent.com/244409/204153378-b7b4f660-a3c3-4546-a44c-48712b14ea03.png">

За допомогою бібліотеки `telethon` і Telegram API ми викачуємо всі повідомлення з заданого каналу і зберігаємо їх в базі данних. Ми використовуємо `sqlite` та бібліотеку `sqlalchemy` для зручності роботи з даними.

Схема:

![my_erd](https://user-images.githubusercontent.com/244409/204156258-55cb6392-15b1-42d7-a8f2-2f537af2baee.png)


## Аналіз наративів

`python3 build_graph.py`

<img width="942" alt="Знімок екрана 2022-11-27 о 21 11 23" src="https://user-images.githubusercontent.com/244409/204155002-48a83dd2-4d83-41b3-8c85-f3e5a3a0f3d7.png">


Дана версія програми дозволяє відслідкувати наративи двох типів:

*Дискредитація української влади(D)*

```python
def is_discrediting_the_authorities(text):
    return bool(re.search(r'киев.*(режим|хунта|неонац|наркоман|клоун)|(шаровар|укро|свино|неонац).*(рейх|вермахт)|наркоман.*киев|(наркоман|клоун|упорот|марионетка).*(зеленск|зеля)|государственный переворот', text, flags=re.I))
```

*Приниження за національною ознакою та демонізація українців(H)*

```python
def is_humiliation_of_culture_narrative(text):
    return bool(re.search(r'укроп|чубат|хохол|хохля|укры|салоед|кастрюл.*голов|кукраин|бандеров|укронацист|укровояк', text, flags=re.I))
```

Ці дві категорії наративів зручно розпізнати, використовуючи пошук за допомогою регулярних виразів, так як пропагандисти `створили` набір слів та фраз по яких їх зручно ідентифікувати.

Звісно такий метод не дає повної точності, але проглядаються певні тенденції.

Ідеально було б використати Machine Learning для розпізнавання наративів. Для цього можна було б використати бібліотеку TensorFlow(https://www.tensorflow.org/) або pythorh та скористатись превивченими наборами для класифікації текстів з сайту https://huggingface.co/ > Text Classification datasets.

Це б додало точності у визначені двох вже описаних наративів, а також для автоматичного маркування посту відповідносі певному наративу.

Проте така реалізація потребує збору і підготовки текстів, та їх ручної обробки з маркуванням відповідності до певного наративу в обсязі достатньому для потрібної точності автоматичного визначення після проведення machine learning.

## Аналіз частоти використання

Приклади:

Аналіз по наративу `Дискредитація влади` по всіх телеграм каналах з 1 січня 2022 року по 1 листопада 2022 року:

`python3 plotter.py --from 2022-01-01 --to 2022-11-01 --narrative D`
<img width="1486" alt="Знімок екрана 2022-11-27 о 21 15 40" src="https://user-images.githubusercontent.com/244409/204155155-98cc5962-deb2-4c89-824b-9d0b742c0d38.png">


Аналіз по наративу `Приниження та демонізація українців` каналом `SolovievLive` з 1 січня 2022 року по 1 листопада 2022 року:
`python3 plotter.py --telegram-channel SolovievLive --from 2022-01-01 --to 2022-11-01 --narrative H`
<img width="1470" alt="Знімок екрана 2022-11-27 о 21 16 49" src="https://user-images.githubusercontent.com/244409/204155200-b2accddb-9699-4562-a699-2f40d012c08b.png">


Приклади роботи та співпадіння з подіями на фронті:

Перше що кидається в очі, це збільшення використання обидвох наративів в період з 15 лютого 2022 року, що відповідає періоду перед повномасштабним вторгненням на територію України 24 лютого. Цікаво, що активність розпочинається за 10 днів до повномасштабного вторгнення і тримається на такому ж рівні до кінця березня:

<img width="1354" alt="Знімок екрана 2022-11-27 о 21 19 48" src="https://user-images.githubusercontent.com/244409/204155335-2ea1842f-d4d2-4378-aa2c-92b9eb4c1b5a.png">

Два інших яскравих піки у збільшені використання наративу `Дискредитацій української влади` співпадає з успіхами української армії на Харківському напрямку, що відбувався на початку вересня:

<img width="1045" alt="Знімок екрана 2022-11-27 о 21 25 40" src="https://user-images.githubusercontent.com/244409/204155585-e6d5daf5-93fd-48e8-8004-b166cf9c0d39.png">


а також періодом успіхів на Лиманському напрямку та його звільненням:

<img width="1500" alt="Знімок екрана 2022-11-27 о 21 33 06" src="https://user-images.githubusercontent.com/244409/204155867-a07a26be-59e0-4e78-bc70-5021b25b773d.png">

Разом з тим слід зауважити, що кількості даних і частоти виявлення наративів на конкретну дату вбачається недосатньою для гарної інтерполяцій та пошуку закономірностей.

Адже видно неозброєним оком тільки ці три піки. Тому для реального використання програма потребує доопрацювання в плані точності віднесення тексту до певного наративу aбо збільшення телеграм каналів і постів в базі данних.




