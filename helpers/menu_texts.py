INFO_TEXT = """<pre>✅ Чтобы начать генерацию, просто отправьте боту сообщение, что вы хотите увидеть на сгенерированном изображении\n\n▪️Бот рисует в нейросети StableDiffusion\n\n\n✅Как считаются генерации?\n\n▪️Каждое отправленное боту сообщение = 1 генерация:\n▪️Новый запрос, повторный запрос = 4 изображения в ответ\n\n▪️1000 генераций = 4000 изображений\n\n▪️Генерации приобретаются на месяц и сгорают через 30 дней\n\n\nКак генерировать изображения?\n\n▪️1. Боту можно писать на русском и английском языке\n\n▪️2. Порядок построения сообщения(prompt): Стиль, КТО или ЧТО, что делает, где, в какой одежде, какой фон, его цвет, другие важные детали\n\n▪️ 3. Чем более полным будет описание, тем легче нейросети рисовать\n\n▪️ 4. Самое главное по смыслу слово всегда ставьте ближе к началу запроса\n\n▪️ 5. Можно усилить значение какого-то слова, заключив в скобки\nНапример, (красное платье) или даже (((красное платье)))\n\n▪️ 6. Чтобы исключить элементы из изображения, допишите в конце промпта:  « —no» или по-русски: « —нет» и слова через запятую, которые нужно исключить\n\n▪️ 7. Выберите в меню стиль изображения\n\n▪️ 8. Выберите в меню формат изображения\n\n▪️9. После генерации вам придёт 4 изображения \n\n▪️ 10. После генерации изображения имеют размер:
1:1    1024 х 1024 px
3:2    1024 х 672 px
16:9   1024 x 576 px
3:1    1024 x 352 px\n\nОценивайте качество правильно! 1024 х 1024 px - изображение меньше экрана вашего телефона, если его растянуть на большой экран компьютера, оно может казаться некачественным \n\n▪️ 11. Промпт созданного изображения можно отправить повторно для новой генерации, нажав на кнопку под изображением(🔄), изображение создастся в последнем выбранном стиле\n\n▪️ 12. Чтобы генерить слова или буквы на изображении, добавьте в prompt: letters “тут нужное слово"\n\n▪️ 13. Перед загрузкой на фотобанки для продажи изображения нужно увеличить до размера больше 4Мр \nНапример: 2000 х 2000 px (это 4Мр) или 3000 х 2000 px (это 6Мр), рекомендуем использовать для увеличения программу Topaz Gigapixel \n\n▪️ 14. Созданные изображения из бота не пропадают, сохранить на устройство вы сможете в любое время.\n\n▪️Работы над ботом продолжаются! Скоро будут новые функции!\n\n⌛️ Время генерации от 1 до 15 минут\n\n\nНа сайте: \n\n✅34 урока, как продавать изображения через интернет на фотобанках(как, что, почему и зачем создавать в нейросети, чтобы были стабильные и частые продажи)\n\n ✅10 уроков бесплатные! \n\n</pre>
"""

PRESET_INFO_TEXT = """<pre>▪️По умолчанию изображения создаются квадратными 1:1 \n\n▪️Ваши изображения будут создаваться в выбранном формате до тех пор, пока вы не выберете другой, либо не удалите выбранный.\n\n▪️Создание в других форматах не предусмотрено</pre>"""

STYLE_INFO_TEXT = """<pre>▪️По умолчанию изображения создаются без определенного стиля, чаще всего, похожими на фотографии\n\n▪️После выбора стиля ваши изображения будут создаваться в выбранном стиле до тех пор, пока вы не выберете другой, либо не удалите выбранный\n\n▪️Выбранный стиль не гарантирует создание 100% изображений в этом стиле, это нейросеть, она может ошибаться. Добавляйте уточняющие слова, меняйте промпты, чтобы получить лучший результат\n\n▪️Можно добавлять негативный промпт, чтобы исключить элементы другого стиля, например, чтобы бот не рисовал фото, напишите в конце промпта:  « --no photo, photography, photorealism» (или по-русски: « --нет фото, фотография» и тп)\n\n▪️Чтобы создавать изображения в любом другом  стиле, нужно удалить предыдущий и дописать в начале запроса стиль, в котором вы хотите получить изображение, например, «lego style», и в конце запроса уточняющие слова, подходящие под этот стиль. Собственный стиль не сохраняется, добавлять к запросу каждый раз\n\nПримеры стилей: graffiti style, street art, aerial shot, pop art, mosaic style и др\n\n▪️Экспериментируйте!</pre>
"""

MENU_INFORMATION_TEXT = """<pre>▪️Бот рисует в нейросети StableDiffusion\n\n✅ 10 подарочных генераций каждый месяц 1 числа. Подарки не суммируются и сгорают в конце месяца.\n\n▪️Полученные изображения можно загружать на фотобанки для продажи. AdobeStock, FreePik, 123rf, Dreamstime.\n\n▪️Авторские права и право на коммерческое использование созданных изображений передаются вам в момент создания изображения и полностью принадлежат вам\n\n</pre>"""

SUPPORT_TEXT = """<pre>❌Техподдержка не помогает продавать работы на фотобанках, для этого переходите в Меню - Уроки\n\n✅По всем техническим вопросам пишите:</pre>"""

PASSWORD_TEXT = """<pre>▪️Чтобы смотреть купленные уроки или купить курс, нужно авторизоваться на сайте\n\n▪️Логин - это ваш ник/имя пользователя/username в ТГ без «@» \n\n▪️Если забыли пароль, отправьте боту сообщение: \n\n/password и ваш новый пароль\n\nНапример, /password 12345</pre>"""

PAYMENT_TEXT = """<pre>✅Для оплаты генераций или покупки курса, нужно авторизоваться на сайте\n\n Чтобы сайт знал, кому добавлять генерации и курс😉 \n\n▪️Логин - это ваш ник/имя пользователя/username в ТГ без «@» \n\n▪️Пароль вы придумывали при регистрации в боте\n\n▪️Если забыли пароль, создайте новый простой какой-нибудь, например, 12345 \n\nДля этого отправьте боту сообщение: \n\n/password 12345</pre>"""