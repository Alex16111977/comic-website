import json
from pathlib import Path

new_vocab = {
    "throne": [
        {
            "german": "die Lüge",
            "russian_hint": "намеренный обман",
            "sentence_parts": [
                "Die grausame Goneril",
                "flüstert kalt",
                "die Lüge",
                "vor Lears Thron im Saal."
            ],
            "sentence_translation": "Жестокая Гонериль холодно шепчет ложь перед троном Лира в зале.",
            "synonyms": ["обман", "неправда", "враньё"]
        },
        {
            "german": "schwören",
            "russian_hint": "торжественно обещать",
            "sentence_parts": [
                "Die grausame Goneril",
                "schwört laut",
                "auf ihre Liebe",
                "vor Lears Thron heute."
            ],
            "sentence_translation": "Жестокая Гонериль громко клянётся в своей любви перед троном Лира сегодня.",
            "synonyms": ["присягать", "обещать", "заклясться"]
        },
        {
            "german": "das Erbe",
            "russian_hint": "доля наследства",
            "sentence_parts": [
                "Die grausame Goneril",
                "beansprucht gierig",
                "das Erbe",
                "im prunkvollen Saal heute."
            ],
            "sentence_translation": "Жестокая Гонериль жадно требует наследство в роскошном зале сегодня.",
            "synonyms": ["наследство", "достояние", "имущество"]
        },
        {
            "german": "heucheln",
            "russian_hint": "притворно чувствовать",
            "sentence_parts": [
                "Die grausame Goneril",
                "heuchelt süß",
                "dem Vater",
                "vor Lears Thron im Saal."
            ],
            "sentence_translation": "Жестокая Гонериль сладко лицемерит отцу перед троном Лира в зале.",
            "synonyms": ["притворяться", "лицемерить", "двуличничать"]
        },
        {
            "german": "die Gier",
            "russian_hint": "страстное стяжание",
            "sentence_parts": [
                "Die grausame Goneril",
                "zeigt offen",
                "die Gier",
                "unter Lears Kronleuchter heute."
            ],
            "sentence_translation": "Жестокая Гонериль открыто показывает жадность под люстрой Лира сегодня.",
            "synonyms": ["алчность", "жажда", "корысть"]
        },
        {
            "german": "täuschen",
            "russian_hint": "умышленно обманывать",
            "sentence_parts": [
                "Die grausame Goneril",
                "täuscht listig",
                "den müden König",
                "im Thronsaal vor Zeugen."
            ],
            "sentence_translation": "Жестокая Гонериль хитро обманывает уставшего короля в тронном зале перед свидетелями.",
            "synonyms": ["обманывать", "одурачивать", "морочить"]
        },
        {
            "german": "schmeicheln",
            "russian_hint": "лестно говорить",
            "sentence_parts": [
                "Die grausame Goneril",
                "schmeichelt kunstvoll",
                "dem Vater",
                "vor Lears Thron sehr laut."
            ],
            "sentence_translation": "Жестокая Гонериль искусно льстит отцу перед троном Лира очень громко.",
            "synonyms": ["льстить", "угождать", "заискивать"]
        },
        {
            "german": "das Vermögen",
            "russian_hint": "богатое состояние",
            "sentence_parts": [
                "Die grausame Goneril",
                "berechnet kühl",
                "das Vermögen",
                "im geteilten Königreich heute."
            ],
            "sentence_translation": "Жестокая Гонериль хладно подсчитывает состояние в разделённом королевстве сегодня.",
            "synonyms": ["имущество", "капитал", "богатство"]
        }
    ],
    "goneril": [
        {
            "german": "die Macht",
            "russian_hint": "полная власть",
            "sentence_parts": [
                "Die grausame Goneril",
                "fordert hart",
                "die Macht",
                "über Hälfte des Reiches."
            ],
            "sentence_translation": "Жестокая Гонериль жёстко требует власть над половиной королевства.",
            "synonyms": ["власть", "могущество", "господство"]
        },
        {
            "german": "herrschen",
            "russian_hint": "управлять страной",
            "sentence_parts": [
                "Die grausame Goneril",
                "will herrschen",
                "über alte Diener",
                "im neuen Palast kühl."
            ],
            "sentence_translation": "Жестокая Гонериль хочет править над старыми слугами в новом дворце холодно.",
            "synonyms": ["властвовать", "царствовать", "управлять"]
        },
        {
            "german": "befehlen",
            "russian_hint": "давать приказ",
            "sentence_parts": [
                "Die grausame Goneril",
                "befiehlt herrisch",
                "dem Gefolge",
                "im großen Saal sofort."
            ],
            "sentence_translation": "Жестокая Гонериль властно приказывает свите в большом зале немедленно.",
            "synonyms": ["приказывать", "велеть", "распоряжаться"]
        },
        {
            "german": "der Thron",
            "russian_hint": "царское сиденье",
            "sentence_parts": [
                "Die grausame Goneril",
                "begehrt gierig",
                "den Thron",
                "des greisen Vaters heute."
            ],
            "sentence_translation": "Жестокая Гонериль жадно желает трон дряхлого отца сегодня.",
            "synonyms": ["престол", "царское кресло", "владычье место"]
        },
        {
            "german": "erobern",
            "russian_hint": "силой захватывать",
            "sentence_parts": [
                "Die grausame Goneril",
                "plant heimlich",
                "zu erobern",
                "das Herz des Reiches."
            ],
            "sentence_translation": "Жестокая Гонериль тайно планирует завоевать сердце королевства.",
            "synonyms": ["завоёвывать", "покорять", "захватывать"]
        },
        {
            "german": "die Herrschaft",
            "russian_hint": "полное господство",
            "sentence_parts": [
                "Die grausame Goneril",
                "festigt kalt",
                "die Herrschaft",
                "über Haus und Land."
            ],
            "sentence_translation": "Жестокая Гонериль холодно укрепляет господство над домом и землёй.",
            "synonyms": ["господство", "владычество", "доминирование"]
        },
        {
            "german": "regieren",
            "russian_hint": "направлять власть",
            "sentence_parts": [
                "Die grausame Goneril",
                "regiert streng",
                "die Diener",
                "in der großen Halle."
            ],
            "sentence_translation": "Жестокая Гонериль строго управляет слугами в большом зале.",
            "synonyms": ["управлять", "править", "властвовать"]
        },
        {
            "german": "unterwerfen",
            "russian_hint": "принуждать к покорности",
            "sentence_parts": [
                "Die grausame Goneril",
                "unterwirft eisig",
                "jede Stimme",
                "in ihrem Machtbereich."
            ],
            "sentence_translation": "Жестокая Гонериль ледяно подчиняет каждый голос в своей власти.",
            "synonyms": ["подчинять", "покорять", "угнетать"]
        }
    ],
    "regan": [
        {
            "german": "demütigen",
            "russian_hint": "заставлять унижаться",
            "sentence_parts": [
                "Die grausame Goneril",
                "demütigt offen",
                "den alternden Vater",
                "vor Regans kaltem Blick."
            ],
            "sentence_translation": "Жестокая Гонериль открыто унижает стареющего отца перед холодным взглядом Реганы.",
            "synonyms": ["унижать", "оскорблять", "принижать"]
        },
        {
            "german": "grausam",
            "russian_hint": "полностью жестокий",
            "sentence_parts": [
                "Die grausame Goneril",
                "handelt grausam",
                "gegen Lear",
                "im Bündnis mit Regan."
            ],
            "sentence_translation": "Жестокая Гонериль действует жестоко против Лира в союзе с Реганой.",
            "synonyms": ["жестокий", "безжалостный", "свирепый"]
        },
        {
            "german": "die Rache",
            "russian_hint": "возмездие зла",
            "sentence_parts": [
                "Die grausame Goneril",
                "schmiedet heimlich",
                "die Rache",
                "mit Regan bei Nacht."
            ],
            "sentence_translation": "Жестокая Гонериль тайно куёт месть с Реганой ночью.",
            "synonyms": ["месть", "воздаяние", "расплата"]
        },
        {
            "german": "vertreiben",
            "russian_hint": "гнать прочь",
            "sentence_parts": [
                "Die grausame Goneril",
                "vertreibt hart",
                "den Vater",
                "aus dem eigenen Schloss."
            ],
            "sentence_translation": "Жестокая Гонериль сурово изгоняет отца из собственного замка.",
            "synonyms": ["изгонять", "прогонять", "выдворять"]
        },
        {
            "german": "verachten",
            "russian_hint": "глубоко презирать",
            "sentence_parts": [
                "Die grausame Goneril",
                "verachtet offen",
                "den sanften Albany",
                "vor Regans kalten Augen."
            ],
            "sentence_translation": "Жестокая Гонериль открыто презирает мягкого Олбани перед холодными глазами Реганы.",
            "synonyms": ["презирать", "гнушаться", "пренебрегать"]
        },
        {
            "german": "verweigern",
            "russian_hint": "упрямо отказывать",
            "sentence_parts": [
                "Die grausame Goneril",
                "verweigert hart",
                "dem König",
                "jede Unterkunft in Nacht."
            ],
            "sentence_translation": "Жестокая Гонериль жёстко отказывает королю в любом приюте ночью.",
            "synonyms": ["отказывать", "лишать", "запрещать"]
        },
        {
            "german": "quälen",
            "russian_hint": "причинять мучения",
            "sentence_parts": [
                "Die grausame Goneril",
                "quält gnadenlos",
                "die alten Ritter",
                "neben Regans Blicken."
            ],
            "sentence_translation": "Жестокая Гонериль безжалостно мучает старых рыцарей рядом с взглядами Реганы.",
            "synonyms": ["мучить", "терзать", "истязать"]
        },
        {
            "german": "beschränken",
            "russian_hint": "строго ограничивать",
            "sentence_parts": [
                "Die grausame Goneril",
                "beschränkt streng",
                "die Gefolgschaft",
                "auf wenige kniende Diener."
            ],
            "sentence_translation": "Жестокая Гонериль строго ограничивает свиту до нескольких коленопреклонённых слуг.",
            "synonyms": ["ограничивать", "уменьшать", "сдерживать"]
        }
    ],
    "storm": [
        {
            "german": "verstoßen",
            "russian_hint": "из семьи выгонять",
            "sentence_parts": [
                "Die grausame Goneril",
                "verstößt hart",
                "den Vater",
                "in die stürmische Nacht."
            ],
            "sentence_translation": "Жестокая Гонериль сурово изгоняет отца в бурную ночь.",
            "synonyms": ["изгонять", "отвергать", "отрекаться"]
        },
        {
            "german": "der Sturm",
            "russian_hint": "яростная буря",
            "sentence_parts": [
                "Der tobende Sturm",
                "peitscht wild",
                "über Lear",
                "nach Gonerils hartem Befehl."
            ],
            "sentence_translation": "Бушующая буря яростно хлещет Лира после жёсткого приказа Гонериль.",
            "synonyms": ["буря", "ураган", "шторм"]
        },
        {
            "german": "gnadenlos",
            "russian_hint": "без капли жалости",
            "sentence_parts": [
                "Die grausame Goneril",
                "bleibt gnadenlos",
                "gegen Lear",
                "trotz Regens und Donner."
            ],
            "sentence_translation": "Жестокая Гонериль остаётся безжалостной к Лиру несмотря на дождь и гром.",
            "synonyms": ["беспощадный", "безжалостный", "неумолимый"]
        },
        {
            "german": "verschließen",
            "russian_hint": "плотно закрывать",
            "sentence_parts": [
                "Die grausame Goneril",
                "verschließt trotzig",
                "die Türen",
                "vor dem klagenden König."
            ],
            "sentence_translation": "Жестокая Гонериль упрямо запирает двери перед жалобным королём.",
            "synonyms": ["запирать", "закрывать", "затворять"]
        },
        {
            "german": "die Kälte",
            "russian_hint": "ледяная стужа",
            "sentence_parts": [
                "Die grausame Goneril",
                "schickt bitter",
                "die Kälte",
                "über Lear hinaus heute."
            ],
            "sentence_translation": "Жестокая Гонериль посылает горький холод на Лира сегодня.",
            "synonyms": ["холод", "стужа", "озноб"]
        },
        {
            "german": "erbarmungslos",
            "russian_hint": "совершенно без жалости",
            "sentence_parts": [
                "Die grausame Goneril",
                "bleibt erbarmungslos",
                "gegen Bitten",
                "im tosenden Nachtsturm."
            ],
            "sentence_translation": "Жестокая Гонериль остаётся совершенно безжалостной к просьбам в ревущую ночную бурю.",
            "synonyms": ["неумолимый", "жестокий", "безжалостный"]
        },
        {
            "german": "verhärten",
            "russian_hint": "делаться черствым",
            "sentence_parts": [
                "Die grausame Goneril",
                "verhärtet völlig",
                "ihr Herz",
                "im Donner der Nacht."
            ],
            "sentence_translation": "Жестокая Гонериль полностью ожесточает сердце в гром ночи.",
            "synonyms": ["ожесточаться", "черстветь", "каменеть"]
        }
    ],
    "hut": [
        {
            "german": "streiten",
            "russian_hint": "резко ругаться",
            "sentence_parts": [
                "Die grausame Goneril",
                "streitet laut",
                "mit Albany",
                "im dunklen Lagerhaus."
            ],
            "sentence_translation": "Жестокая Гонериль громко ссорится с Олбани в тёмном складе.",
            "synonyms": ["ссориться", "ругаться", "препираться"]
        },
        {
            "german": "verraten",
            "russian_hint": "изменой выдавать",
            "sentence_parts": [
                "Die grausame Goneril",
                "verrät kalt",
                "den Vater",
                "in der Nachtbesprechung."
            ],
            "sentence_translation": "Жестокая Гонериль холодно предаёт отца на ночном совещании.",
            "synonyms": ["предавать", "выдавать", "изменять"]
        },
        {
            "german": "die Zwietracht",
            "russian_hint": "семена раздора",
            "sentence_parts": [
                "Die grausame Goneril",
                "säht ständig",
                "die Zwietracht",
                "zwischen Hof und Volk."
            ],
            "sentence_translation": "Жестокая Гонериль постоянно сеет раздор между двором и народом.",
            "synonyms": ["раздор", "вражда", "распря"]
        },
        {
            "german": "hassen",
            "russian_hint": "глубоко ненавидеть",
            "sentence_parts": [
                "Die grausame Goneril",
                "hasst heftig",
                "die ehrliche Cordelia",
                "im heimlichen Lager."
            ],
            "sentence_translation": "Жестокая Гонериль яростно ненавидит честную Корделию в тайном лагере.",
            "synonyms": ["ненавидеть", "презирать", "возненавидеть"]
        },
        {
            "german": "betrügen",
            "russian_hint": "изменять тайно",
            "sentence_parts": [
                "Die grausame Goneril",
                "betrügt offen",
                "den Ehemann",
                "mit Edmund im Zelt."
            ],
            "sentence_translation": "Жестокая Гонериль открыто изменяет мужу с Эдмундом в шатре.",
            "synonyms": ["изменять", "обманывать", "жульничать"]
        },
        {
            "german": "die Verachtung",
            "russian_hint": "глубокое презрение",
            "sentence_parts": [
                "Die grausame Goneril",
                "zeigt offen",
                "die Verachtung",
                "für Albanys weiche Worte."
            ],
            "sentence_translation": "Жестокая Гонериль открыто показывает презрение к мягким словам Олбани.",
            "synonyms": ["презрение", "пренебрежение", "гордыня"]
        },
        {
            "german": "zerstören",
            "russian_hint": "полностью разрушать",
            "sentence_parts": [
                "Die grausame Goneril",
                "zerstört kalt",
                "den Frieden",
                "im Lager der Rebellen."
            ],
            "sentence_translation": "Жестокая Гонериль холодно разрушает мир в лагере мятежников.",
            "synonyms": ["разрушать", "ломать", "уничтожать"]
        },
        {
            "german": "die Leidenschaft",
            "russian_hint": "жгучая страсть",
            "sentence_parts": [
                "Die grausame Goneril",
                "entfacht verbotene",
                "Leidenschaft",
                "mit Edmund hinter Vorhängen."
            ],
            "sentence_translation": "Жестокая Гонериль разжигает запретную страсть с Эдмундом за занавесями.",
            "synonyms": ["страсть", "пыл", "вожделение"]
        }
    ],
    "dover": [
        {
            "german": "die Eifersucht",
            "russian_hint": "мучительная ревность",
            "sentence_parts": [
                "Die grausame Goneril",
                "schürt fiebernd",
                "die Eifersucht",
                "auf Regans Nähe zu Edmund."
            ],
            "sentence_translation": "Жестокая Гонериль лихорадочно разжигает ревность к близости Реганы с Эдмундом.",
            "synonyms": ["ревность", "зависть", "подозрение"]
        },
        {
            "german": "rivalisieren",
            "russian_hint": "бороться соперничая",
            "sentence_parts": [
                "Die grausame Goneril",
                "rivalisiert offen",
                "mit Regan",
                "am Feldlager bei Dover."
            ],
            "sentence_translation": "Жестокая Гонериль открыто соперничает с Реганой у полевого лагеря под Дувром.",
            "synonyms": ["соперничать", "конкурировать", "бороться"]
        },
        {
            "german": "kämpfen",
            "russian_hint": "вести бой",
            "sentence_parts": [
                "Die grausame Goneril",
                "kämpft eifrig",
                "um Edmund",
                "auf dem düsteren Feld."
            ],
            "sentence_translation": "Жестокая Гонериль усердно борется за Эдмунда на мрачном поле.",
            "synonyms": ["бороться", "сражаться", "драться"]
        },
        {
            "german": "begehren",
            "russian_hint": "страстно желать",
            "sentence_parts": [
                "Die grausame Goneril",
                "begehrt gierig",
                "den Verräter",
                "trotz Regans fordernder Nähe."
            ],
            "sentence_translation": "Жестокая Гонериль жадно желает предателя несмотря на настойчивую близость Реганы.",
            "synonyms": ["желать", "вожделеть", "домогаться"]
        },
        {
            "german": "beseitigen",
            "russian_hint": "устранять угрозу",
            "sentence_parts": [
                "Die grausame Goneril",
                "plant heimlich",
                "zu beseitigen",
                "die Schwester im Feldlager."
            ],
            "sentence_translation": "Жестокая Гонериль тайно планирует устранить сестру в полевом лагере.",
            "synonyms": ["устранять", "ликвидировать", "избавлять"]
        },
        {
            "german": "das Gift",
            "russian_hint": "смертельный яд",
            "sentence_parts": [
                "Die grausame Goneril",
                "verbirgt listig",
                "das Gift",
                "für Regan im Zelt."
            ],
            "sentence_translation": "Жестокая Гонериль хитро прячет яд для Реганы в шатре.",
            "synonyms": ["яд", "отрава", "токсин"]
        },
        {
            "german": "die Intrige",
            "russian_hint": "подлая затея",
            "sentence_parts": [
                "Die grausame Goneril",
                "spinnt täglich",
                "die Intrige",
                "um Edmunds dunkles Herz."
            ],
            "sentence_translation": "Жестокая Гонериль ежедневно плетёт интригу вокруг тёмного сердца Эдмунда.",
            "synonyms": ["интрига", "заговор", "махинация"]
        },
        {
            "german": "morden",
            "russian_hint": "хладнокровно убивать",
            "sentence_parts": [
                "Die grausame Goneril",
                "droht heimlich",
                "zu morden",
                "um Edmund allein zu besitzen."
            ],
            "sentence_translation": "Жестокая Гонериль тайно грозит убивать, чтобы владеть Эдмундом одной.",
            "synonyms": ["убивать", "умертвлять", "казнить"]
        }
    ],
    "prison": [
        {
            "german": "vergiften",
            "russian_hint": "тайно травить",
            "sentence_parts": [
                "Die grausame Goneril",
                "vergiftet heimlich",
                "die Schwester",
                "im düsteren Quartier."
            ],
            "sentence_translation": "Жестокая Гонериль тайно отравляет сестру в мрачных покоях.",
            "synonyms": ["отравлять", "травить", "поражать"]
        },
        {
            "german": "die Verzweiflung",
            "russian_hint": "крайнее отчаяние",
            "sentence_parts": [
                "Die grausame Goneril",
                "verhüllt kalt",
                "die Verzweiflung",
                "nach Edmunds tödlicher Wunde."
            ],
            "sentence_translation": "Жестокая Гонериль холодно скрывает отчаяние после смертельной раны Эдмунда.",
            "synonyms": ["отчаяние", "безысходность", "уныние"]
        },
        {
            "german": "sterben",
            "russian_hint": "утратить жизнь",
            "sentence_parts": [
                "Die grausame Goneril",
                "sieht schweigend",
                "ihn sterben",
                "im stickigen Kerkerraum."
            ],
            "sentence_translation": "Жестокая Гонериль молча видит его умирающим в душной тюремной комнате.",
            "synonyms": ["умирать", "скончаться", "гибнуть"]
        },
        {
            "german": "die Schuld",
            "russian_hint": "тяжёлое преступление",
            "sentence_parts": [
                "Die grausame Goneril",
                "spürt plötzlich",
                "die Schuld",
                "im engen Kerkerlicht."
            ],
            "sentence_translation": "Жестокая Гонериль внезапно чувствует вину в узком тюремном свете.",
            "synonyms": ["вина", "провина", "грех"]
        },
        {
            "german": "vernichten",
            "russian_hint": "полностью уничтожать",
            "sentence_parts": [
                "Die grausame Goneril",
                "vernichtet alles",
                "Vertrauen",
                "mit einem letzten Befehl."
            ],
            "sentence_translation": "Жестокая Гонериль уничтожает всё доверие последним приказом.",
            "synonyms": ["уничтожать", "истреблять", "разрушать"]
        },
        {
            "german": "das Verderben",
            "russian_hint": "неизбежная погибель",
            "sentence_parts": [
                "Die grausame Goneril",
                "spürt nah",
                "das Verderben",
                "zwischen Kerkertüren heute."
            ],
            "sentence_translation": "Жестокая Гонериль ощущает близкую погибель между тюремными дверями сегодня.",
            "synonyms": ["погибель", "гибель", "крах"]
        },
        {
            "german": "bereuen",
            "russian_hint": "горько сожалеть",
            "sentence_parts": [
                "Die grausame Goneril",
                "bereut leise",
                "ihr Gift",
                "im Schatten der Zelle."
            ],
            "sentence_translation": "Жестокая Гонериль тихо сожалеет о своём яде в тени камеры.",
            "synonyms": ["сожалеть", "каяться", "раскаиваться"]
        },
        {
            "german": "die Hölle",
            "russian_hint": "мучительный ад",
            "sentence_parts": [
                "Die grausame Goneril",
                "fühlt nah",
                "die Hölle",
                "hinter Kerkerwänden heute."
            ],
            "sentence_translation": "Жестокая Гонериль чувствует близкий ад за тюремными стенами сегодня.",
            "synonyms": ["ад", "мука", "геенна"]
        }
    ]
}

TRANSLATIONS = {
    "die Lüge": "ложь",
    "schwören": "клясться",
    "das Erbe": "наследство",
    "heucheln": "лицемерить",
    "die Gier": "жадность",
    "täuschen": "обманывать",
    "schmeicheln": "льстить",
    "das Vermögen": "состояние",
    "die Macht": "власть",
    "herrschen": "править",
    "befehlen": "приказывать",
    "der Thron": "трон",
    "erobern": "завоёвывать",
    "die Herrschaft": "господство",
    "regieren": "управлять",
    "unterwerfen": "подчинять",
    "demütigen": "унижать",
    "grausam": "жестокий",
    "die Rache": "месть",
    "vertreiben": "изгонять",
    "verachten": "презирать",
    "verweigern": "отказывать",
    "quälen": "мучить",
    "beschränken": "ограничивать",
    "verstoßen": "отвергать",
    "der Sturm": "буря",
    "gnadenlos": "безжалостный",
    "verschließen": "запирать",
    "die Kälte": "холод",
    "erbarmungslos": "беспощадный",
    "verhärten": "ожесточаться",
    "streiten": "ссориться",
    "verraten": "предавать",
    "die Zwietracht": "раздор",
    "hassen": "ненавидеть",
    "betrügen": "изменять",
    "die Verachtung": "презрение",
    "zerstören": "разрушать",
    "die Leidenschaft": "страсть",
    "die Eifersucht": "ревность",
    "rivalisieren": "соперничать",
    "kämpfen": "бороться",
    "begehren": "желать",
    "beseitigen": "устранять",
    "das Gift": "яд",
    "die Intrige": "интрига",
    "morden": "убивать",
    "vergiften": "отравлять",
    "die Verzweiflung": "отчаяние",
    "sterben": "умирать",
    "die Schuld": "вина",
    "vernichten": "уничтожать",
    "das Verderben": "погибель",
    "bereuen": "сожалеть",
    "die Hölle": "ад"
}

TRANSCRIPTIONS = {}

with Path('data/characters/goneril.json').open(encoding='utf-8') as f:
    data = json.load(f)

for phase in data['journey_phases']:
    pid = phase['id']
    vocab_list = []
    for item in new_vocab[pid]:
        german = item['german']
        original = next(v for v in phase['vocabulary'] if v['german'] == german)
        sentence = f"{item['sentence_parts'][0]} {item['sentence_parts'][1]} {item['sentence_parts'][2]} {item['sentence_parts'][3]}"
        vocab_list.append({
            "german": german,
            "russian": TRANSLATIONS[german],
            "russian_hint": item['russian_hint'],
            "transcription": original['transcription'],
            "sentence": sentence,
            "sentence_translation": item['sentence_translation'],
            "sentence_parts": item['sentence_parts'],
            "synonyms": item['synonyms']
        })
    phase['vocabulary'] = vocab_list

with Path('data/characters/goneril.json').open('w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
