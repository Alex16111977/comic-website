import hashlib
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CHAR_DIR = BASE_DIR / "data" / "characters"

RU_NAMES = {
    "king_lear": "Лир",
    "cordelia": "Корделия",
    "goneril": "Гонерилья",
    "regan": "Регана",
    "gloucester": "Глостер",
    "edgar": "Эдгар",
    "edmund": "Эдмунд",
    "kent": "Кент",
    "fool": "Шут",
    "albany": "Олбани",
    "cornwall": "Корнуолл",
    "oswald": "Освальд",
}

CLAUSE_TEMPLATES = [
    {
        "de": "Ich halte das Wort {word_quote} wie eine Fackel vor meinem Herzen.",
        "ru": "Я держу слово {word_ru_quote} как факел у сердца.",
    },
    {
        "de": "Mit fester Stimme schwöre ich mir: Das Wort {word_quote} wird heute nicht verraten.",
        "ru": "Твёрдым голосом я клянусь себе: слово {word_ru_quote} сегодня не будет предано.",
    },
    {
        "de": "Das Echo des Wortes {word_quote} übertönt das Flüstern der Höflinge.",
        "ru": "Эхо слова {word_ru_quote} заглушает шёпот придворных.",
    },
    {
        "de": "Ich presse das Wort {word_quote} zwischen die Zähne, damit kein Zweifel entweicht.",
        "ru": "Я стискиваю слово {word_ru_quote} зубами, чтобы не вырвалось сомнение.",
    },
    {
        "de": "Wie ein stilles Gebet legt sich das Wort {word_quote} auf meine Lippen.",
        "ru": "Как тихая молитва слово {word_ru_quote} ложится на мои губы.",
    },
    {
        "de": "Ich zeichne das Wort {word_quote} in Gedanken über die Linien des Schicksals.",
        "ru": "Я черчу слово {word_ru_quote} в мыслях поверх линий судьбы.",
    },
    {
        "de": "Mit jeder Faser meines Körpers verspreche ich: Das Wort {word_quote} bleibt lebendig.",
        "ru": "Каждой клеткой тела я обещаю: слово {word_ru_quote} останется живым.",
    },
    {
        "de": "Das kalte Licht lässt das Wort {word_quote} wie geschmolzenes Gold erscheinen.",
        "ru": "Холодный свет заставляет слово {word_ru_quote} сиять словно расплавленное золото.",
    },
    {
        "de": "Ich flüstere den Wächtern des Schicksals zu: Das Wort {word_quote} darf nicht vergehen.",
        "ru": "Я шепчу стражам судьбы: слово {word_ru_quote} не должно исчезнуть.",
    },
    {
        "de": "Mein Atem zeichnet das Wort {word_quote} in die kalte Luft zwischen uns.",
        "ru": "Моё дыхание рисует слово {word_ru_quote} в холодном воздухе между нами.",
    },
    {
        "de": "Ich umarme das Wort {word_quote}, als wäre es mein einziger Verbündeter.",
        "ru": "Я обнимаю слово {word_ru_quote}, будто это единственный союзник.",
    },
    {
        "de": "Selbst wenn die Welt zerfällt, bleibt das Wort {word_quote} mein Nordstern.",
        "ru": "Даже если мир распадается, слово {word_ru_quote} остаётся моим северным светом.",
    },
    {
        "de": "Ich zeichne das Wort {word_quote} mit unsichtbarer Tinte auf meine Handfläche.",
        "ru": "Я вывожу слово {word_ru_quote} невидимыми чернилами на ладони.",
    },
    {
        "de": "Der Sturm vor den Fenstern verstärkt den Schwur: Das Wort {word_quote} gehört mir.",
        "ru": "Буря за окнами усиливает клятву: слово {word_ru_quote} принадлежит мне.",
    },
    {
        "de": "Ich atme tief ein und lasse nur das Wort {word_quote} wieder hinaus.",
        "ru": "Я глубоко вдыхаю и выпускаю только слово {word_ru_quote}.",
    },
]

EXAMPLE_CONTEXTS = [
    {
        "de": "Im Sturm auf der Heide ruft der Erzähler aus Lears Gefolge.",
        "ru": "В буре на пустоши говорит рассказчик из свиты Лира.",
    },
    {
        "de": "Im Thronsaal, wo Banner knistern, flüstert die jüngste Tochter.",
        "ru": "В тронном зале, где потрескивают штандарты, шепчет младшая дочь.",
    },
    {
        "de": "Vor den Toren von Gloucester berichtet ein müder Bote.",
        "ru": "У ворот Глостера докладывает усталый гонец.",
    },
    {
        "de": "Unter den Klippen von Dover singt der Wind den Soldaten zu.",
        "ru": "Под скалами Дувра ветер напевает солдатам.",
    },
    {
        "de": "Im Lager der Franzosen zeichnet Cordelia einen Plan in den Sand.",
        "ru": "В лагере французов Корделия рисует план на песке.",
    },
    {
        "de": "Auf den Stufen des Palastes warnt der Narr mit ernster Miene.",
        "ru": "На ступенях дворца шут с серьёзным лицом предупреждает.",
    },
    {
        "de": "Im Kerker von Lear hallt die Stimme eines treuen Freundes.",
        "ru": "В темнице Лира звучит голос верного друга.",
    },
    {
        "de": "Neben dem brennenden Kamin von Regan erzählt ein verschreckter Diener.",
        "ru": "У пылающего камина Реганы рассказывает перепуганный слуга.",
    },
    {
        "de": "Im Schatten der Kapelle betet Albany für ein gerechtes Urteil.",
        "ru": "В тени капеллы Олбани молится о справедливом решении.",
    },
    {
        "de": "Auf dem Markt von London verbreitet ein Barde neue Gerüchte.",
        "ru": "На рынке Лондона бард распространяет новые слухи.",
    },
    {
        "de": "Im geheimen Zelt von Edmund tuscheln Spione über das nächste Manöver.",
        "ru": "В тайном шатре Эдмунда шепчутся шпионы о следующем манёвре.",
    },
    {
        "de": "Am Morgen über den Mooren wacht ein Scout der königlichen Garde.",
        "ru": "На рассвете над болотами дежурит разведчик королевской стражи.",
    },
    {
        "de": "Auf den alten Mauern von Cornwall stößt eine Wache auf unruhige Zeichen.",
        "ru": "На старых стенах Корнуолла страж замечает тревожные знаки.",
    },
    {
        "de": "Im Hof von Goneril zählt ein Schreiber die verschwundenen Gäste.",
        "ru": "Во дворе Гонерильи писец пересчитывает исчезнувших гостей.",
    },
    {
        "de": "Unter den Sternen des Heereslagers schwört Kent auf die Morgendämmerung.",
        "ru": "Под звёздами лагеря Кент клянётся дождаться рассвета.",
    },
    {
        "de": "In der Burgkapelle von Gloucester erklingt ein einsames Gebet.",
        "ru": "В замковой часовне Глостера звучит одинокая молитва.",
    },
]

PHASE_DETAILS = {
    "throne": [
        {
            "de": "{name} steht unter dem glühenden Kronleuchter des Thronsaals.",
            "ru": "{name_ru} стоит под пылающей люстрой тронного зала.",
        },
        {
            "de": "Neben der ausgerollten Reichskarte beugt sich {name} über Lears schweren Tisch.",
            "ru": "У развернутой карты королевства {name_ru} склоняется над тяжёлым столом Лира.",
        },
        {
            "de": "Vor den steinernen Ahnenstatuen verschränkt {name} die Hände hinter dem Rücken.",
            "ru": "Перед каменными статуями предков {name_ru} сцепляет руки за спиной.",
        },
        {
            "de": "Zwischen flüsternden Höflingen gleitet {name} über den kalten Marmorboden.",
            "ru": "Между шепчущимися придворными {name_ru} скользит по холодному мраморному полу.",
        },
        {
            "de": "Am Rand des purpurnen Teppichs wartet {name} auf ein Zeichen des Königs.",
            "ru": "На краю пурпурного ковра {name_ru} ждёт знака от короля.",
        },
        {
            "de": "Unter wehenden Standarten der Schwestern senkt {name} kurz den Blick.",
            "ru": "Под развевающимися штандартами сестёр {name_ru} на миг опускает взгляд.",
        },
        {
            "de": "Hinter der vergoldeten Balustrade beobachtet {name} das gespannte Antlitz des Hofes.",
            "ru": "За позолоченной балюстрадой {name_ru} наблюдает за напряжёнными лицами двора.",
        },
        {
            "de": "Im Schein der offenen Feuerbecken erhebt {name} langsam die Stimme.",
            "ru": "В отблесках открытых жаровен {name_ru} медленно поднимает голос.",
        },
    ],
    "goneril": [
        {
            "de": "Im hallenden Torbogen von Gonerils Burg verharrt {name} zwischen gepackten Kisten.",
            "ru": "В гулком проёме ворот замка Гонерильи {name_ru} замирает среди нагруженных ящиков.",
        },
        {
            "de": "Auf der windigen Freitreppe blickt {name} zum schweigenden Hof hinunter.",
            "ru": "На продуваемой ветром лестнице {name_ru} смотрит вниз на молчаливый двор.",
        },
        {
            "de": "Zwischen zurückgelassenen Dienern schließt {name} den Reisemantel enger.",
            "ru": "Среди оставленных слуг {name_ru} плотнее запахивает дорожный плащ.",
        },
        {
            "de": "Am dunklen Pferdestall streicht {name} einem nervösen Tier über die Mähne.",
            "ru": "У тёмного конюшенного ряда {name_ru} гладит гриву нервного коня.",
        },
        {
            "de": "Vor dem knarrenden Fallgatter tastet {name} ein letztes Mal nach dem Haustor.",
            "ru": "Перед скрипящим подъёмным мостом {name_ru} в последний раз касается родной двери.",
        },
        {
            "de": "Zwischen verstreuten Schriftrollen dreht {name} den Ring an der Hand.",
            "ru": "Среди разбросанных свитков {name_ru} вертит кольцо на пальце.",
        },
        {
            "de": "Am leeren Bankettisch zählt {name} die verlöschenden Kerzen.",
            "ru": "У пустого банкетного стола {name_ru} пересчитывает гаснущие свечи.",
        },
        {
            "de": "Zwischen schweigenden Wachen geht {name} auf den kalten Hof hinaus.",
            "ru": "Между молчаливыми стражниками {name_ru} выходит на холодный двор.",
        },
    ],
    "regan": [
        {
            "de": "Im zugigen Seitenflügel lauscht {name} dem Heulen der Küstenwinde.",
            "ru": "В продуваемом ветром боковом крыле {name_ru} слушает вой прибрежного ветра.",
        },
        {
            "de": "Vor dem rauchigen Kamin der Burg faltet {name} einen zerknitterten Brief.",
            "ru": "Перед дымным камином замка {name_ru} складывает измятый лист.",
        },
        {
            "de": "Unter farblosen Wandteppichen schreitet {name} rastlos auf und ab.",
            "ru": "Под выцветшими гобеленами {name_ru} беспокойно меряет шагами зал.",
        },
        {
            "de": "An der schmalen Fensterluke zählt {name} die Fackeln auf dem Hof.",
            "ru": "У узкой бойницы {name_ru} считает факелы на дворе.",
        },
        {
            "de": "Zwischen Reisekoffern der Gesandten sucht {name} nach frischen Botschaften.",
            "ru": "Среди дорожных сундуков послов {name_ru} ищет свежие вести.",
        },
        {
            "de": "Im stillen Kapellenraum kniet {name} vor der kalten Steinfigur.",
            "ru": "В тихой капелле {name_ru} преклоняет колени перед холодной каменной фигурой.",
        },
        {
            "de": "Auf dem Balkon, den das Meer besprüht, hält {name} die Laterne fest.",
            "ru": "На балконе, омываемом морскими брызгами, {name_ru} крепко держит фонарь.",
        },
        {
            "de": "Im Schatten der hohen Burgmauern schreibt {name} eine fiebrige Antwort.",
            "ru": "В тени высоких стен {name_ru} пишет лихорадочный ответ.",
        },
    ],
    "storm": [
        {
            "de": "Mitten auf der vom Regen gepeitschten Heide stemmt sich {name} gegen den Wind.",
            "ru": "Посреди хлещущей дождём пустоши {name_ru} упирается в ветер.",
        },
        {
            "de": "Unter einem zerrissenen Banner schützt {name} die Augen vor den Blitzen.",
            "ru": "Под разорванным знаменем {name_ru} прикрывает глаза от молний.",
        },
        {
            "de": "Am Rand eines umgestürzten Baumes sucht {name} Deckung vor dem Donner.",
            "ru": "У поваленного дерева {name_ru} ищет укрытия от грома.",
        },
        {
            "de": "Zwischen schäumenden Wassergräben stolpert {name} durch den Schlamm.",
            "ru": "Между пенящимися лужами {name_ru} пробирается через грязь.",
        },
        {
            "de": "Vor einem zuckenden Himmel hebt {name} die Arme trotzig an.",
            "ru": "На фоне вспыхивающего неба {name_ru} упрямо поднимает руки.",
        },
        {
            "de": "Unter dem durchtränkten Umhang presst {name} den Atem gegen die Kälte.",
            "ru": "Под промокшим плащом {name_ru} прижимает дыхание к груди, спасаясь от холода.",
        },
        {
            "de": "Am kläglichen Feuerrest wärmt {name} zitternde Finger.",
            "ru": "У жалких огненных углей {name_ru} греет дрожащие пальцы.",
        },
        {
            "de": "Zwischen heulenden Hunden ruft {name} gegen den tosenden Sturm an.",
            "ru": "Среди воющих псов {name_ru} перекрикивает беснующуюся бурю.",
        },
    ],
    "hut": [
        {
            "de": "Im dunklen Zelt der Feldärzte sitzt {name} bei der flackernden Kerze.",
            "ru": "В тёмном шатре полевых лекарей {name_ru} сидит у мерцающей свечи.",
        },
        {
            "de": "Zwischen zerbeulten Rüstungen streicht {name} über ein altes Wappen.",
            "ru": "Среди помятых доспехов {name_ru} гладит старый герб.",
        },
        {
            "de": "Am niedrigen Dachbalken der Hütte stößt {name} fast den Kopf.",
            "ru": "О низкую балку хижины {name_ru} едва не ударяется головой.",
        },
        {
            "de": "Neben der schlafenden Wache flüstert {name} in die schwere Nacht.",
            "ru": "Рядом со спящим стражем {name_ru} шепчет в тяжёлую ночь.",
        },
        {
            "de": "Vor dem einfachen Feldbett betrachtet {name} die Narben vergangener Schlachten.",
            "ru": "Перед грубой походной койкой {name_ru} разглядывает шрамы прошлых битв.",
        },
        {
            "de": "Im Geruch von feuchtem Stroh legt {name} den Mantel zur Seite.",
            "ru": "В запахе влажной соломы {name_ru} откладывает плащ в сторону.",
        },
        {
            "de": "Auf dem wackligen Holztisch ordnet {name} zerlesene Briefe.",
            "ru": "На шатком деревянном столе {name_ru} раскладывает зачитанные письма.",
        },
        {
            "de": "Am Eingang der Hütte späht {name} nach einem vertrauten Schatten.",
            "ru": "У входа в хижину {name_ru} высматривает знакомую тень.",
        },
    ],
    "dover": [
        {
            "de": "Auf den weißen Klippen von Dover blickt {name} in den aufgewühlten Kanal.",
            "ru": "На белых скалах Дувра {name_ru} смотрит в вздыбленный пролив.",
        },
        {
            "de": "Zwischen flatternden Feldzeichen richtet {name} den Helm.",
            "ru": "Среди хлопающих штандартов {name_ru} поправляет шлем.",
        },
        {
            "de": "Am Lagerfeuer der Franzosen zeichnet {name} Marschrouten in den Sand.",
            "ru": "У французского костра {name_ru} рисует в песке путь марша.",
        },
        {
            "de": "Neben verschnürten Versorgungskisten kontrolliert {name} das Siegel.",
            "ru": "У перевязанных провиантных ящиков {name_ru} проверяет печати.",
        },
        {
            "de": "Vor dem Seidenzelt der Heerführer lauscht {name} dem dumpfen Meer.",
            "ru": "Перед шёлковым шатром полководцев {name_ru} слушает глухой шум моря.",
        },
        {
            "de": "Auf dem sandigen Trainingsplatz übt {name} das Ziehen des Schwerts.",
            "ru": "На песчаном плацу {name_ru} отрабатывает выхват меча.",
        },
        {
            "de": "Zwischen pochenden Trommeln hebt {name} das Banner der Hoffnung.",
            "ru": "Под гул барабанов {name_ru} поднимает знамя надежды.",
        },
        {
            "de": "Am Morgennebel der Küste legt {name} die Hand auf das pochende Herz.",
            "ru": "В утреннем тумане побережья {name_ru} кладёт ладонь на бьющееся сердце.",
        },
    ],
    "prison": [
        {
            "de": "Im feuchten Kerker stützt {name} sich an den tropfenden Stein.",
            "ru": "В сыром подземелье {name_ru} опирается на сочащийся камень.",
        },
        {
            "de": "Unter der trüben Laterne zählt {name} die eisernen Ringe der Kette.",
            "ru": "Под мутным фонарём {name_ru} пересчитывает железные кольца цепи.",
        },
        {
            "de": "Neben der schweren Holztür horcht {name} auf entferntes Schluchzen.",
            "ru": "У тяжёлой двери {name_ru} прислушивается к далёким рыданиям.",
        },
        {
            "de": "Auf der kalten Steinbank zieht {name} den Mantel enger um die Schultern.",
            "ru": "На холодной каменной скамье {name_ru} плотнее кутается в плащ.",
        },
        {
            "de": "Zwischen Schatten der Gitterstäbe hebt {name} das Gesicht zum Licht.",
            "ru": "Между тенями решёток {name_ru} поднимает лицо к свету.",
        },
        {
            "de": "Am rostigen Wassereimer spiegelt {name} kurz die eigenen Augen.",
            "ru": "У ржавого ведра с водой {name_ru} на мгновение видит отражение глаз.",
        },
        {
            "de": "Im dumpfen Hall der Schritte zählt {name} den Rhythmus der Wachen.",
            "ru": "В глухом эхе шагов {name_ru} отсчитывает ритм часовых.",
        },
        {
            "de": "Vor dem verriegelten Fenster zeichnet {name} Kreise in den Staub.",
            "ru": "Перед заколоченным окном {name_ru} чертит круги в пыли.",
        },
    ],
    "loyalty": [
        {
            "de": "Mitten im Tumult der Thronfeier tritt {name} vor den Königsthron.",
            "ru": "Посреди суматохи тронной церемонии {name_ru} выходит к королевскому трону.",
        },
        {
            "de": "Zwischen scharfgezogenen Schwertern stellt sich {name} vor die jüngste Tochter.",
            "ru": "Между обнажёнными мечами {name_ru} встаёт перед младшей дочерью.",
        },
        {
            "de": "Vor der erstaunten Ritterschar reißt {name} sein Wappen vom Brustpanzer.",
            "ru": "Перед изумлёнными рыцарями {name_ru} срывает герб с нагрудника.",
        },
        {
            "de": "Unter den strengen Blicken des Hofes schlägt {name} die Faust auf das Geländer.",
            "ru": "Под строгими взглядами двора {name_ru} бьёт кулаком по перилам.",
        },
        {
            "de": "Neben Lears Stab kniet {name} und hebt unbeirrbar den Kopf.",
            "ru": "У посоха Лира {name_ru} встаёт на колено и упрямо поднимает голову.",
        },
        {
            "de": "Auf den Stufen zur Thronrampe breitet {name} schützend die Arme aus.",
            "ru": "На ступенях ведущих к трону {name_ru} защитно разводит руки.",
        },
        {
            "de": "Zwischen höfischen Fanfaren ruft {name} seine Warnung gegen das Hofgeflüster.",
            "ru": "Среди придворных фанфар {name_ru} выкрикивает предупреждение против шёпота двора.",
        },
        {
            "de": "Im Schatten des Königsbanners legt {name} die Hand auf das Herz.",
            "ru": "В тени королевского знамени {name_ru} кладёт руку на сердце.",
        },
    ],
    "banishment": [
        {
            "de": "Auf den kalten Stufen des Hofes hört {name} das Urteil der Verbannung.",
            "ru": "На холодных ступенях двора {name_ru} слышит приговор об изгнании.",
        },
        {
            "de": "Zwischen abziehenden Soldaten hält {name} nur den Reisestock in der Hand.",
            "ru": "Среди расходящихся солдат {name_ru} сжимает в руке лишь дорожный посох.",
        },
        {
            "de": "Vor dem geschlossenen Burgtor wirft {name} den Blick noch einmal zurück.",
            "ru": "У закрытых ворот замка {name_ru} бросает последний взгляд назад.",
        },
        {
            "de": "Auf dem Regenpflaster bleibt {name} stehen, während die Trommeln schweigen.",
            "ru": "На мокрой мостовой {name_ru} замирает, пока барабаны смолкают.",
        },
        {
            "de": "Zwischen verstreuten Reisebündeln befestigt {name} das Schwert am Gürtel.",
            "ru": "Среди разбросанных узлов {name_ru} затягивает меч на поясе.",
        },
        {
            "de": "Unter dem grauen Himmel zieht {name} den Mantelkragen hoch.",
            "ru": "Под серым небом {name_ru} поднимает ворот плаща.",
        },
        {
            "de": "Vor der trostlosen Landstraße richtet {name} den Blick entschlossen nach vorn.",
            "ru": "Перед пустынной дорогой {name_ru} решительно смотрит вперёд.",
        },
    ],
    "disguise": [
        {
            "de": "In der verqualmten Herberge streift {name} das grobe Knechtsgewand über.",
            "ru": "В задымлённой харчевне {name_ru} натягивает грубое платье слуги.",
        },
        {
            "de": "Vor einem beschlagenen Spiegel übt {name} die raue Stimme des Kays.",
            "ru": "Перед запотевшим зеркалом {name_ru} тренирует хриплый голос Кая.",
        },
        {
            "de": "Unter einem zerknitterten Hut verbirgt {name} die königliche Haltung.",
            "ru": "Под мятой шляпой {name_ru} скрывает королевскую осанку.",
        },
        {
            "de": "Zwischen neugierigen Fuhrknechten studiert {name} die Dienstbefehle.",
            "ru": "Среди любопытных возниц {name_ru} изучает служебные приказы.",
        },
        {
            "de": "Am Ufer des Hafens wäscht {name} die Spuren des alten Lebens ab.",
            "ru": "На пристани {name_ru} смывает следы прежней жизни.",
        },
        {
            "de": "Auf dem staubigen Markt prüft {name} die Tragriemen des Gepäcks.",
            "ru": "На пыльном рынке {name_ru} проверяет ремни поклажи.",
        },
        {
            "de": "Im Schatten einer Gasse versteckt {name} den einst glänzenden Siegelring.",
            "ru": "В тени переулка {name_ru} прячет некогда блестящий перстень.",
        },
        {
            "de": "Unter einem Wagenrad kauert {name}, bis der Ruf nach Dienern erschallt.",
            "ru": "Под колесом телеги {name_ru} затаивается, пока не прозвучит зов для слуг.",
        },
    ],
    "service": [
        {
            "de": "Im nächtlichen Wachraum poliert {name} schweigend die Rüstung des Königs.",
            "ru": "В ночной караульной {name_ru} молча полирует королевские доспехи.",
        },
        {
            "de": "Neben dem Lager des erschöpften Herrschers hält {name} unbeweglich Wache.",
            "ru": "У ложа измождённого правителя {name_ru} неподвижно несёт стражу.",
        },
        {
            "de": "Unter Regenmänteln der Wachen verbirgt {name} seine Narben.",
            "ru": "Под дождевыми плащами стражей {name_ru} скрывает свои шрамы.",
        },
        {
            "de": "Am Stalltor sattelt {name} in der Dunkelheit ein trotziges Pferd.",
            "ru": "У дверей конюшни {name_ru} в темноте осёдлывает упрямого коня.",
        },
        {
            "de": "In der Küche der Dienerschaft füllt {name} den dampfenden Becher.",
            "ru": "В кухне прислуги {name_ru} наполняет дымящийся кубок.",
        },
        {
            "de": "Vor der Schlafstatt des Königs ordnet {name} die verstreuten Decken.",
            "ru": "Перед ложем короля {name_ru} раскладывает разбросанные покрывала.",
        },
        {
            "de": "Auf dem Hof prüft {name} das Zaumzeug, bevor der Morgen graut.",
            "ru": "Во дворе {name_ru} проверяет уздечку, пока не рассвело.",
        },
    ],
    "stocks": [
        {
            "de": "Im Regen der Burgmauer sitzt {name} mit gefesselten Füßen in den harten Hölzern.",
            "ru": "Под дождём у крепостной стены {name_ru} сидит с закреплёнными ногами в жёстких колодках.",
        },
        {
            "de": "Neben den Spottliedern der Wachen hält {name} den Kopf stolz erhoben.",
            "ru": "Под насмешливые песни стражи {name_ru} гордо держит голову.",
        },
        {
            "de": "Vor dem trüben Mondlicht reibt {name} den schmerzenden Nacken.",
            "ru": "В тусклом лунном свете {name_ru} растирает затёкшую шею.",
        },
        {
            "de": "Zwischen den Pfützen der Nacht starren {name}s Schuhe in den Himmel.",
            "ru": "Среди ночных луж сапоги {name_ru} устремлены в небо.",
        },
        {
            "de": "Am Morgenfrost haucht {name} Eisblumen auf das Holz.",
            "ru": "В утренний мороз {name_ru} выдыхает ледяные узоры на дерево.",
        },
        {
            "de": "Neben einem verirrten Bauernkind lächelt {name} trotz der Demütigung.",
            "ru": "Рядом с заблудившимся крестьянином {name_ru} улыбается несмотря на унижение.",
        },
        {
            "de": "Unter dem grauen Himmel zählt {name} geduldig die Tropfen auf dem Gesicht.",
            "ru": "Под серым небом {name_ru} терпеливо считает капли на лице.",
        },
        {
            "de": "Auf dem verlassenen Hof lauscht {name} dem fern rollenden Donner.",
            "ru": "На пустынном дворе {name_ru} прислушивается к далёкому грохоту грома.",
        },
    ],
    "storm_companion": [
        {
            "de": "Mit der Laterne in der Faust sucht {name} nach dem Schatten des Königs.",
            "ru": "С фонарём в кулаке {name_ru} ищет тень короля.",
        },
        {
            "de": "Neben dem tobenden Monarchen breitet {name} den Mantel wie ein Schild.",
            "ru": "Рядом с бушующим монархом {name_ru} раскрывает плащ как щит.",
        },
        {
            "de": "Auf dem überfluteten Pfad hält {name} das Pferd am Zügel.",
            "ru": "На затопленной тропе {name_ru} держит коня за повод.",
        },
        {
            "de": "Zwischen klatschenden Ästen ruft {name} beruhigende Worte.",
            "ru": "Среди хлещущих веток {name_ru} говорит успокаивающие слова.",
        },
        {
            "de": "Vor der klappernden Hütte hebt {name} die Fackel, um den Weg zu zeigen.",
            "ru": "Перед дрожащей хижиной {name_ru} поднимает факел, освещая путь.",
        },
        {
            "de": "Am Rand des Moorfelds stützt {name} den taumelnden Herrscher.",
            "ru": "На краю болотного поля {name_ru} поддерживает качающегося правителя.",
        },
        {
            "de": "Unter dem peitschenden Regen spricht {name} ein leises Trostlied.",
            "ru": "Под хлещущим дождём {name_ru} тихо напевает утешительную песнь.",
        },
    ],
    "final_loyalty": [
        {
            "de": "Im stillen Sterbezimmer wacht {name} an Lears letztem Lager.",
            "ru": "В тихой опочивальне смерти {name_ru} стоит у последнего ложа Лира.",
        },
        {
            "de": "Neben der verlöschenden Kerze streicht {name} über den zerrissenen Umhang.",
            "ru": "У догорающей свечи {name_ru} гладит разорванный плащ.",
        },
        {
            "de": "Vor den starren Wachen flüstert {name} ein letztes Versprechen.",
            "ru": "Перед оцепеневшими стражами {name_ru} шепчет последнее обещание.",
        },
        {
            "de": "Auf dem leeren Thronstuhl legt {name} den eigenen Stab nieder.",
            "ru": "На пустом троне {name_ru} кладёт свой посох.",
        },
        {
            "de": "Zwischen verblassenden Wandmalereien schließt {name} kurz die Augen.",
            "ru": "Среди блекнущих настенных росписей {name_ru} на мгновение закрывает глаза.",
        },
        {
            "de": "Am offenen Fenster lässt {name} den kalten Morgen herein.",
            "ru": "У распахнутого окна {name_ru} впускает холодное утро.",
        },
        {
            "de": "Im Schatten der Trauernden hält {name} Lears Hand bis zum letzten Schlag.",
            "ru": "В тени скорбящих {name_ru} держит руку Лира до последнего удара.",
        },
        {
            "de": "Vor der stillen Hofkapelle beugt {name} das Knie für ein stummes Gebet.",
            "ru": "Перед молчаливой придворной часовней {name_ru} преклоняет колено в безмолвной молитве.",
        },
    ],
    "ambitious_duke": [
        {
            "de": "In der Waffenkammer betrachtet {name} gierig die ausgestellten Kronjuwelen.",
            "ru": "В оружейной {name_ru} жадно рассматривает выставленные коронные драгоценности.",
        },
        {
            "de": "Vor der Karte Englands fährt {name} mit dem Dolch über neue Grenzen.",
            "ru": "Перед картой Англии {name_ru} проводит кинжалом новые границы.",
        },
        {
            "de": "Zwischen knienden Vasallen lässt {name} die Finger über den Thronsessel gleiten.",
            "ru": "Среди преклонивших колено вассалов {name_ru} проводит пальцами по тронному креслу.",
        },
        {
            "de": "Am hohen Fenster misst {name} den Abstand zur Hauptstadt.",
            "ru": "У высокого окна {name_ru} вымеряет расстояние до столицы.",
        },
        {
            "de": "Neben dem schwelenden Kamin testet {name} das Gewicht eines Schwertes.",
            "ru": "У тлеющего камина {name_ru} взвешивает на руке меч.",
        },
        {
            "de": "Auf dem Turnierplatz lässt {name} seine Reiter zu später Stunde antreten.",
            "ru": "На турнирной площадке {name_ru} строит всадников поздним вечером.",
        },
        {
            "de": "Zwischen Pergamentrollen überdenkt {name} geheime Bündnisse.",
            "ru": "Среди свитков пергамента {name_ru} обдумывает тайные союзы.",
        },
        {
            "de": "Im Spiegel der Audienzhalle probt {name} das Lächeln eines Herrschers.",
            "ru": "В зеркале аудиенц-зала {name_ru} репетирует улыбку правителя.",
        },
    ],
    "cruel_husband": [
        {
            "de": "Neben Regans vergiftetem Lächeln hebt {name} den Kelch zum Spott.",
            "ru": "Рядом с ядовитой улыбкой Реганы {name_ru} поднимает кубок насмешки.",
        },
        {
            "de": "Auf der Galerie des Schlosses applaudiert {name} den Demütigungen des Königs.",
            "ru": "На галерее замка {name_ru} аплодирует унижениям короля.",
        },
        {
            "de": "Zwischen eingeschüchterten Dienern greift {name} nach der Peitsche.",
            "ru": "Среди запуганных слуг {name_ru} тянется к плётке.",
        },
        {
            "de": "Am hohen Lehnsessel sitzt {name} mit kalter Zufriedenheit.",
            "ru": "В высоком кресле-ленном {name_ru} сидит с холодным довольством.",
        },
        {
            "de": "Vor dem Bannerschrank zerreißt {name} einen höflichen Bittbrief.",
            "ru": "Перед шкафом со штандартами {name_ru} разрывает вежливое прошение.",
        },
        {
            "de": "Unter stürmischen Trommeln befiehlt {name} den Wachen näherzukommen.",
            "ru": "Под грохот барабанов {name_ru} приказывает стражам подойти ближе.",
        },
        {
            "de": "Im Schatten der Folterkammer tauscht {name} mit Regan heimliche Blicke.",
            "ru": "В тени пыточной {name_ru} обменивается с Реганой тайными взглядами.",
        },
    ],
    "tyrant": [
        {
            "de": "Auf dem Burghof verteilt {name} neue, erbarmungslose Dekrete.",
            "ru": "На замковом дворе {name_ru} раздаёт новые беспощадные указы.",
        },
        {
            "de": "Vor gefesselten Gefangenen lässt {name} die Streitkolben prüfen.",
            "ru": "Перед связанными пленниками {name_ru} приказывает проверить боевые булавы.",
        },
        {
            "de": "Zwischen klirrenden Ketten schreitet {name} mit schwerem Schritt.",
            "ru": "Среди звенящих цепей {name_ru} идёт тяжёлым шагом.",
        },
        {
            "de": "Am schwarzen Banner der Macht schwört {name} sich ewige Herrschaft.",
            "ru": "У чёрного знамени власти {name_ru} клянётся вечным господством.",
        },
        {
            "de": "Auf dem Gerichtspodest stützt {name} sich auf den Stab aus Eisen.",
            "ru": "На судейском помосте {name_ru} опирается на железный посох.",
        },
        {
            "de": "Unter den Blicken eingeschüchterter Edelleute reißt {name} das Urteil an sich.",
            "ru": "Под взглядами запуганных дворян {name_ru} присваивает себе право суда.",
        },
        {
            "de": "An der Treppe zum Kerker verteilt {name} grausame Befehle.",
            "ru": "У лестницы в темницу {name_ru} раздаёт жестокие приказы.",
        },
        {
            "de": "Im düsteren Thronsaal schlägt {name} mit der Faust auf die Armlehne.",
            "ru": "В мрачном тронном зале {name_ru} бьёт кулаком по подлокотнику.",
        },
    ],
    "punishment": [
        {
            "de": "Vor den geschockten Höflingen deutet {name} auf die leeren Holzkolben.",
            "ru": "Перед потрясёнными придворными {name_ru} указывает на пустые колодки.",
        },
        {
            "de": "Auf dem nassen Hof befiehlt {name} die Fesselung des Widerspenstigen.",
            "ru": "На мокром дворе {name_ru} приказывает заковать непокорного.",
        },
        {
            "de": "Neben Regans spöttischem Blick wirft {name} das Urteil in die Luft.",
            "ru": "Рядом с насмешливым взглядом Реганы {name_ru} бросает приговор в воздух.",
        },
        {
            "de": "Am Werkzeugtisch der Garde prüft {name} die scharfen Nägel.",
            "ru": "У верстака стражи {name_ru} проверяет острые гвозди.",
        },
        {
            "de": "Vor den verschreckten Dienern lächelt {name} über das Flehen um Gnade.",
            "ru": "Перед перепуганными слугами {name_ru} улыбается мольбам о пощаде.",
        },
        {
            "de": "Unter Donnerhall befiehlt {name} das Opfer in den Regen zu stellen.",
            "ru": "Под раскаты грома {name_ru} приказывает поставить жертву под дождь.",
        },
        {
            "de": "Auf dem Steinboden hinterlässt {name} Spuren von Blut und Wasser.",
            "ru": "На каменном полу {name_ru} оставляет следы крови и воды.",
        },
    ],
    "torturer": [
        {
            "de": "Im düsteren Saal bindet {name} den Grafen an den eichenen Stuhl.",
            "ru": "В мрачном зале {name_ru} приковывает графа к дубовому креслу.",
        },
        {
            "de": "Neben knirschenden Seilen entfachen Regans Diener das Feuer, während {name} zuschaut.",
            "ru": "Под скрип канатов слуги Реганы раздувают огонь, пока {name_ru} наблюдает.",
        },
        {
            "de": "Vor der versammelten Ritterschaft lässt {name} die Dolche bereitlegen.",
            "ru": "Перед собравшимся рыцарством {name_ru} велит приготовить кинжалы.",
        },
        {
            "de": "Am blutbefleckten Boden tritt {name} das Geständnis aus dem Gefangenen.",
            "ru": "На забрызганном кровью полу {name_ru} выбивает признание из пленника.",
        },
        {
            "de": "Zwischen aufschreienden Dienern bleibt {name} eiskalt und unbewegt.",
            "ru": "Среди вскрикивающих слуг {name_ru} остаётся ледяным и неподвижным.",
        },
        {
            "de": "Unter Regans Jubel reißt {name} das grausame Werk zu Ende.",
            "ru": "Под ликование Реганы {name_ru} довершает жестокую работу.",
        },
        {
            "de": "Vor den entsetzten Augen des Hofes wischt {name} das Blut vom Stiefel.",
            "ru": "Перед ужаснувшимися придворными {name_ru} стирает кровь с сапога.",
        },
        {
            "de": "Im Nachhall der Schreie richtet {name} den Mantel und wendet sich zur Tür.",
            "ru": "В отзвуках криков {name_ru} поправляет плащ и разворачивается к двери.",
        },
    ],
    "wounded": [
        {
            "de": "Im dunklen Korridor presst {name} die Hand gegen die frische Wunde.",
            "ru": "В тёмном коридоре {name_ru} прижимает руку к свежей ране.",
        },
        {
            "de": "Auf der Treppe taumelt {name}, während das Blut den Stein färbt.",
            "ru": "На лестнице {name_ru} пошатывается, окрашивая камень кровью.",
        },
        {
            "de": "Neben Regans erschrockener Stimme sucht {name} Halt am Geländer.",
            "ru": "Рядом с испуганным голосом Реганы {name_ru} ищет опоры в перилах.",
        },
        {
            "de": "Im Stall greift {name} nach einem Sattel, doch die Kräfte schwinden.",
            "ru": "В конюшне {name_ru} тянется к седлу, но силы уходят.",
        },
        {
            "de": "Vor dem Tor der Burg hinterlässt {name} eine Spur aus rotem Staub.",
            "ru": "Перед воротами замка {name_ru} оставляет след из красной пыли.",
        },
        {
            "de": "Auf dem Hof sinkt {name} zwischen erschrockenen Wachen zusammen.",
            "ru": "На дворе {name_ru} падает среди испуганных стражников.",
        },
        {
            "de": "Unter dem bleiernen Himmel schwört {name} Rache mit letzter Kraft.",
            "ru": "Под свинцовым небом {name_ru} клянётся в мести из последних сил.",
        },
    ],
    "death": [
        {
            "de": "Im Treppenhaus der Burg bricht {name} auf das kalte Steinpodest.",
            "ru": "На лестнице замка {name_ru} рушится на холодную площадку.",
        },
        {
            "de": "Zwischen zerbrochenen Waffen liegt {name} und ringt nach Atem.",
            "ru": "Среди разбитого оружия {name_ru} лежит, хватая воздух.",
        },
        {
            "de": "Vor Regans entsetztem Blick verliert {name} den Griff um das eigene Blut.",
            "ru": "Перед ужаснувшимся взглядом Реганы {name_ru} теряет хватку на собственной ране.",
        },
        {
            "de": "Am Fuß der Treppe murmelt {name} die letzten Befehle.",
            "ru": "У подножия лестницы {name_ru} бормочет последние приказы.",
        },
        {
            "de": "Auf der kalten Flaggenkiste sinkt {name} schwer zusammen.",
            "ru": "На холодном сундуке со знамёнами {name_ru} тяжело оседает.",
        },
        {
            "de": "Neben zerborstenen Fenstern haucht {name} den letzten Fluch aus.",
            "ru": "У разбитых окон {name_ru} выдыхает последний проклятый звук.",
        },
        {
            "de": "Unter dem prasselnden Regen verglimmt {name}s Leben rasch.",
            "ru": "Под проливным дождём жизнь {name_ru} быстро гаснет.",
        },
        {
            "de": "Im Staub des Hofes starrt {name} zum grauen Himmel, bevor die Augen erlöschen.",
            "ru": "В пыли двора {name_ru} смотрит в серое небо, прежде чем глаза угасают.",
        },
    ],
    "jester": [
        {
            "de": "Im grellen Licht des Thronsaals schlägt {name} die Laute an.",
            "ru": "В ярком свете тронного зала {name_ru} ударяет по струнам лютни.",
        },
        {
            "de": "Neben Lears Krone balanciert {name} auf einem Fuß.",
            "ru": "Рядом с короной Лира {name_ru} балансирует на одной ноге.",
        },
        {
            "de": "Zwischen Hofdamen und Rittern wirbelt {name} mit flatterndem Schellenkleid.",
            "ru": "Между дамами двора и рыцарями {name_ru} кружится в звенящем костюме.",
        },
        {
            "de": "Vor dem königlichen Podest verzieht {name} die Maske zum Spott.",
            "ru": "Перед королевским помостом {name_ru} кривит маску насмешки.",
        },
        {
            "de": "Am Bankettisch jongliert {name} mit goldenen Pokalen.",
            "ru": "У банкетного стола {name_ru} жонглирует золотыми кубками.",
        },
        {
            "de": "Zwischen Lachern und Seufzern zeichnet {name} Grimassen in die Luft.",
            "ru": "Среди смеха и вздохов {name_ru} рисует в воздухе гримасы.",
        },
        {
            "de": "Im Schatten der Säulen lauscht {name} den leisen Worten Cordelias.",
            "ru": "В тени колонн {name_ru} прислушивается к тихим словам Корделии.",
        },
        {
            "de": "Auf der Marmorstufe lässt {name} ein Glöckchen über den Boden tanzen.",
            "ru": "На мраморной ступени {name_ru} пускает колокольчик плясать по полу.",
        },
    ],
    "bitter_truths": [
        {
            "de": "Vor Lears Ohr flüstert {name} mit funkelndem Blick die spöttische Wahrheit.",
            "ru": "У самого уха Лира {name_ru} с блеском в глазах шепчет язвительную правду.",
        },
        {
            "de": "Auf dem Hofbalkon zeigt {name} mit der Laute auf die heuchlerischen Schwestern.",
            "ru": "На дворцовом балконе {name_ru} указывает лютней на лицемерных сестёр.",
        },
        {
            "de": "Zwischen umgestoßenen Bechern sammelt {name} die Lügen wie Perlen auf.",
            "ru": "Среди опрокинутых кубков {name_ru} собирает ложь словно жемчуг.",
        },
        {
            "de": "An Lears Seite zeichnet {name} mit Kreide eine Krone auf den Boden.",
            "ru": "Рядом с Лиром {name_ru} мелом рисует корону на полу.",
        },
        {
            "de": "Im Gedränge der Höflinge spielt {name} eine schrille Warnmelodie.",
            "ru": "В толчее придворных {name_ru} играет пронзительную мелодию предупреждения.",
        },
        {
            "de": "Auf den Stufen zum Thron zieht {name} die Stirn in tiefe Falten.",
            "ru": "На ступенях, ведущих к трону, {name_ru} морщит лоб глубокими складками.",
        },
        {
            "de": "Neben dem Tränenstrom des Königs wischt {name} die Schminke vom Gesicht.",
            "ru": "Рядом с потоками слёз короля {name_ru} стирает грим с лица.",
        },
    ],
    "prophecies": [
        {
            "de": "Unter dem Sternenzelt deutet {name} mit dem Stab die funkelnden Zeichen.",
            "ru": "Под звёздным шатром {name_ru} посохом указывает на мерцающие знаки.",
        },
        {
            "de": "Auf den Mauern des Schlosses rezitiert {name} Verse von kommenden Stürmen.",
            "ru": "На стенах замка {name_ru} декламирует стихи о грядущих бурях.",
        },
        {
            "de": "Zwischen Rauch und Kerzenduft schleudert {name} rätselhafte Reime.",
            "ru": "Среди дыма и аромата свечей {name_ru} бросает загадочные рифмы.",
        },
        {
            "de": "Am Brunnen des Hofes wirft {name} Kiesel, um die Zukunft zu spiegeln.",
            "ru": "У дворцового фонтана {name_ru} бросает гальку, чтобы отразить будущее.",
        },
        {
            "de": "Vor erstaunten Dienern zeichnet {name} Kreise in den Staub.",
            "ru": "Перед поражёнными слугами {name_ru} чертит круги в пыли.",
        },
        {
            "de": "Auf der Markttreppe singt {name} von Königen, die zu Bettlern werden.",
            "ru": "На рыночной лестнице {name_ru} поёт о королях, становящихся нищими.",
        },
        {
            "de": "Neben einem reisenden Pilger deutet {name} in den flammenden Himmel.",
            "ru": "Рядом со странствующим пилигримом {name_ru} указывает на пылающее небо.",
        },
        {
            "de": "Im Gewitterlicht zählt {name} die Schläge, die die Zukunft ankündigen.",
            "ru": "В свете грозы {name_ru} отсчитывает удары, возвещающие будущее.",
        },
    ],
    "mad_companion": [
        {
            "de": "In der sturmgepeitschten Heide drückt {name} Lear die klammen Hände.",
            "ru": "На залитой бурей пустоши {name_ru} сжимает озябшие руки Лира.",
        },
        {
            "de": "Zwischen zerrissenen Zelten singt {name} ein trostloses Wiegenlied.",
            "ru": "Среди разорванных шатров {name_ru} поёт безутешную колыбельную.",
        },
        {
            "de": "Am umgestürzten Wagen schirmt {name} den König vor der Peitsche des Regens.",
            "ru": "У перевёрнутой повозки {name_ru} заслоняет короля от кнута дождя.",
        },
        {
            "de": "Unter dem knarzenden Dach der Hütte sitzt {name} dicht an Lear gedrängt.",
            "ru": "Под скрипучей крышей хижины {name_ru} сидит вплотную к Лиру.",
        },
        {
            "de": "Vor der tobenden Nacht schreit {name} seine Possen gegen den Wind.",
            "ru": "Перед бушующей ночью {name_ru} выкрикивает свои шутки наперекор ветру.",
        },
        {
            "de": "Am aufgeweichten Boden zeichnet {name} mit Stock und Witz ein Schutzschild.",
            "ru": "На размокшей земле {name_ru} рисует палкой и шутками защитный круг.",
        },
        {
            "de": "In der Finsternis des Waldes zündet {name} einen letzten Funken Mut an.",
            "ru": "В темноте леса {name_ru} зажигает последний огонёк мужества.",
        },
    ],
    "songs": [
        {
            "de": "Im warmen Schein der Hütte summt {name} eine Melodie über verlorene Kronen.",
            "ru": "В тёплом свете хижины {name_ru} напевает мелодию о потерянных коронах.",
        },
        {
            "de": "Neben Lear legt {name} den Kopf auf die Knie und schaukelt im Takt.",
            "ru": "Рядом с Лиром {name_ru} кладёт голову на колени и покачивается в такт.",
        },
        {
            "de": "Vor der knisternden Feuerstelle klatscht {name} den Rhythmus in die Hände.",
            "ru": "Перед потрескивающим огнём {name_ru} отбивает ритм ладонями.",
        },
        {
            "de": "Auf dem Holzbalken sitzt {name} und schwingt die Beine zur Melodie.",
            "ru": "На деревянной балке {name_ru} сидит и качает ногами в такт песне.",
        },
        {
            "de": "Zwischen Schlafenden senkt {name} die Stimme zu einem flüsternden Refrain.",
            "ru": "Среди спящих {name_ru} понижает голос до шёпотного припева.",
        },
        {
            "de": "Am offenen Feld singt {name} gegen das Heulen der Nacht.",
            "ru": "На открытом поле {name_ru} поёт наперекор вою ночи.",
        },
        {
            "de": "In der Morgendämmerung stimmt {name} ein hoffnungsvolles Lied an.",
            "ru": "На рассвете {name_ru} заводит песню надежды.",
        },
        {
            "de": "Über Lear gebeugt beendet {name} das Lied mit einem sanften Kuss auf die Stirn.",
            "ru": "Наклонившись над Лиром, {name_ru} завершает песню мягким поцелуем в лоб.",
        },
    ],
    "wisdom": [
        {
            "de": "Im verlassenen Hof sitzt {name} auf einem leeren Fass und denkt laut nach.",
            "ru": "На пустынном дворе {name_ru} сидит на пустой бочке и размышляет вслух.",
        },
        {
            "de": "Unter einer nackten Eiche zählt {name} die Fehler der Mächtigen.",
            "ru": "Под обнажённым дубом {name_ru} пересчитывает ошибки власть имущих.",
        },
        {
            "de": "Am stillen Bachlauf wirft {name} Steine, um die Zeit zu messen.",
            "ru": "У тихого ручья {name_ru} бросает камни, чтобы измерить время.",
        },
        {
            "de": "Neben einer verlassenen Bühne probt {name} Zeilen über Narrheit und Macht.",
            "ru": "У заброшенной сцены {name_ru} репетирует строки о глупости и власти.",
        },
        {
            "de": "Auf dem Dachboden der Burg sortiert {name} Erinnerungen wie alte Kostüme.",
            "ru": "На чердаке замка {name_ru} раскладывает воспоминания как старые костюмы.",
        },
        {
            "de": "Vor einem Spiegel ohne Glas betrachtet {name} das eigene müde Gesicht.",
            "ru": "Перед зеркалом без стекла {name_ru} разглядывает собственное усталое лицо.",
        },
        {
            "de": "Im ersten Morgenlicht schreibt {name} letzte Sprüche auf Pergament.",
            "ru": "В первом утреннем свете {name_ru} записывает последние остроты на пергамент.",
        },
    ],
    "vanishing": [
        {
            "de": "Im Nebel des Morgens löst sich {name} zwischen den Zelten der Armee auf.",
            "ru": "В утреннем тумане {name_ru} растворяется между шатрами армии.",
        },
        {
            "de": "Auf dem verlassenen Pfad lässt {name} nur ein Glöckchen zurück.",
            "ru": "На пустой тропе {name_ru} оставляет лишь один колокольчик.",
        },
        {
            "de": "Zwischen verstreuten Karten verschwindet {name} hinter einem Wandteppich.",
            "ru": "Среди разбросанных карт {name_ru} исчезает за гобеленом.",
        },
        {
            "de": "Am Rand des Schlachtfelds weht {name}s bunter Schal davon.",
            "ru": "На краю поля битвы уносит пёстрый шарф {name_ru}.",
        },
        {
            "de": "Unter den Blicken der Soldaten verbeugt sich {name} und geht ohne Abschied.",
            "ru": "Под взглядами солдат {name_ru} кланяется и уходит без прощания.",
        },
        {
            "de": "Auf der Treppe der Burg bleibt {name}s Schellenstab einsam liegen.",
            "ru": "На лестнице замка одиноко остаётся жезл с бубенчиками {name_ru}.",
        },
        {
            "de": "Im Rauschen des Meeres verliert sich {name}s Stimme wie ein ferner Traum.",
            "ru": "В шуме моря голос {name_ru} растворяется как далёкий сон.",
        },
        {
            "de": "Vor der aufgehenden Sonne wirft {name} einen letzten Schatten und verblasst.",
            "ru": "Перед восходящим солнцем {name_ru} бросает последнюю тень и растворяется.",
        },
    ],
    "steward": [
        {
            "de": "Im Saal der Herrin richtet {name} die silbernen Teller entlang der langen Tafel aus.",
            "ru": "В зале госпожи {name_ru} выравнивает серебряные блюда вдоль длинного стола.",
        },
        {
            "de": "Vor dem Spiegel prüft {name} den makellosen Sitz des Dienerkleids.",
            "ru": "Перед зеркалом {name_ru} проверяет безупречную посадку дворецкого наряда.",
        },
        {
            "de": "Zwischen Rechnungsbüchern notiert {name} jedes Fass Wein.",
            "ru": "Среди бухгалтерских книг {name_ru} записывает каждую бочку вина.",
        },
        {
            "de": "Am Hofeingang begrüßt {name} mit steifem Nicken die ankommenden Lords.",
            "ru": "У входа во двор {name_ru} сдержанно кивает прибывающим лордам.",
        },
        {
            "de": "Unter den wachsamen Augen Gonerils verteilt {name} die Tagesbefehle.",
            "ru": "Под внимательным взглядом Гонерильи {name_ru} раздаёт дневные распоряжения.",
        },
        {
            "de": "Auf der Küchenrampe kontrolliert {name} die frischen Vorräte.",
            "ru": "На кухонном пандусе {name_ru} проверяет свежие припасы.",
        },
        {
            "de": "Neben der Ahnengalerie wischt {name} letzte Staubkörner fort.",
            "ru": "Рядом с галереей предков {name_ru} смахивает последние пылинки.",
        },
        {
            "de": "Im Kontor versiegelt {name} sorgsam die königliche Korrespondenz.",
            "ru": "В конторе {name_ru} тщательно запечатывает королевскую корреспонденцию.",
        },
    ],
    "messenger": [
        {
            "de": "Auf staubigen Straßen peitscht {name} das Pferd zu größerer Eile.",
            "ru": "На пыльных дорогах {name_ru} подгоняет коня к большей скорости.",
        },
        {
            "de": "Vor verschlossenen Toren zeigt {name} das mit Wachs versiegelte Schreiben.",
            "ru": "Перед закрытыми воротами {name_ru} предъявляет письмо, запечатанное воском.",
        },
        {
            "de": "In der Nacht rast {name} mit einer Laterne als einzigem Stern.",
            "ru": "Ночью {name_ru} мчится, освещаемый одной лишь латерной.",
        },
        {
            "de": "Am Grenzposten überreicht {name} den Befehl mit überheblichem Lächeln.",
            "ru": "На пограничной заставе {name_ru} вручает приказ с высокомерной улыбкой.",
        },
        {
            "de": "Zwischen zerrissenen Bannern schützt {name} die Nachricht vor dem Regen.",
            "ru": "Среди порванных знамён {name_ru} прикрывает письмо от дождя.",
        },
        {
            "de": "Auf dem Hofe Lear erhebt {name} die Stimme über den Tumult.",
            "ru": "На дворе Лира {name_ru} возвышает голос над шумом.",
        },
        {
            "de": "Im Schatten der Stallungen tauscht {name} heimlich versiegelte Rollen.",
            "ru": "В тени конюшен {name_ru} тайно меняет запечатанные свитки.",
        },
    ],
    "insult": [
        {
            "de": "Vor dem gealterten König verneigt sich {name} nur einen Hauch zu wenig.",
            "ru": "Перед постаревшим королём {name_ru} кланяется лишь на долю меньше.",
        },
        {
            "de": "Am Torbogen blockiert {name} den Weg mit erhobenem Stab.",
            "ru": "В проёме ворот {name_ru} преграждает путь поднятым жезлом.",
        },
        {
            "de": "Zwischen entrüsteten Rittern rollt {name} mit den Augen.",
            "ru": "Среди возмущённых рыцарей {name_ru} закатывает глаза.",
        },
        {
            "de": "Auf der Treppe wischt {name} imaginären Staub von Lears Mantel.",
            "ru": "На лестнице {name_ru} стряхивает воображаемую пыль с плаща Лира.",
        },
        {
            "de": "Neben Gonerils kühlen Blick flüstert {name} eine spitze Bemerkung.",
            "ru": "Рядом с холодным взглядом Гонерильи {name_ru} шепчет едкое замечание.",
        },
        {
            "de": "Auf dem Hof setzt {name} sich mit verschränkten Armen gegen jede Bitte zur Wehr.",
            "ru": "На дворе {name_ru} скрестив руки сопротивляется любой просьбе.",
        },
        {
            "de": "Im Flur stößt {name} den alten König absichtlich zur Seite.",
            "ru": "В коридоре {name_ru} нарочно отталкивает старого короля в сторону.",
        },
        {
            "de": "Auf dem Balkon lacht {name} laut über Lears Hilflosigkeit.",
            "ru": "На балконе {name_ru} громко смеётся над беспомощностью Лира.",
        },
    ],
    "spy": [
        {
            "de": "Im Dunkel des Treppenhauses hält {name} den Atem an, um Gespräche zu belauschen.",
            "ru": "В темноте лестницы {name_ru} задерживает дыхание, подслушивая разговоры.",
        },
        {
            "de": "Hinter schweren Vorhängen notiert {name} jedes geflüsterte Wort.",
            "ru": "За тяжёлыми портьерами {name_ru} записывает каждое прошептанное слово.",
        },
        {
            "de": "Auf den Mauern späht {name} nach Reitern am Horizont.",
            "ru": "На стенах {name_ru} высматривает всадников на горизонте.",
        },
        {
            "de": "Zwischen Küchenmägden tauscht {name} Gerüchte gegen Kupferstücke.",
            "ru": "Среди кухонных служанок {name_ru} обменивает слухи на медяки.",
        },
        {
            "de": "Im Kerzenlicht zeichnet {name} geheime Wege auf Pergament.",
            "ru": "При свете свечи {name_ru} вычерчивает тайные пути на пергаменте.",
        },
        {
            "de": "Unter dem Fenster von Regan beugt {name} sich tief in die Nacht hinaus.",
            "ru": "Под окном Реганы {name_ru} глубоко склоняется в ночную тьму.",
        },
        {
            "de": "Vor Gonerils Gemach übergibt {name} flüsternd die gesammelten Nachrichten.",
            "ru": "Перед покоями Гонерильи {name_ru} шёпотом передаёт собранные вести.",
        },
    ],
    "schemer": [
        {
            "de": "In der Schreibstube entwirft {name} ein Netz aus widersprüchlichen Botschaften.",
            "ru": "В писчей комнате {name_ru} плетёт сеть противоречивых посланий.",
        },
        {
            "de": "Neben Gonerils Lager zeichnet {name} heimlich zwei Namen auf ein Pergament.",
            "ru": "Рядом с ложем Гонерильи {name_ru} тайком выводит два имени на пергаменте.",
        },
        {
            "de": "Auf der Gartenterrasse verbrennt {name} Beweise im bronzezeitigen Becken.",
            "ru": "На садовой террасе {name_ru} сжигает улики в бронзовой чаше.",
        },
        {
            "de": "Im Stall flüstert {name} falsche Befehle in die Ohren der Reiter.",
            "ru": "В конюшне {name_ru} шепчет ложные приказы в уши всадников.",
        },
        {
            "de": "Vor Regans Dienern versteckt {name} die Briefe im Futter der Pferde.",
            "ru": "Перед слугами Реганы {name_ru} прячет письма в корме лошадей.",
        },
        {
            "de": "Unter der Laube formt {name} aus Wachs ein neues Siegel.",
            "ru": "Под беседкой {name_ru} отливает из воска новую печать.",
        },
        {
            "de": "In der Mitternachtspause verteilt {name} verschlüsselte Notizen.",
            "ru": "В полночный перерыв {name_ru} раздаёт зашифрованные записки.",
        },
        {
            "de": "Auf dem Kartentisch verschiebt {name} Figuren, als wären es echte Menschen.",
            "ru": "На столе с картами {name_ru} переставляет фигурки, будто это живые люди.",
        },
    ],
    "pursuer": [
        {
            "de": "Mit gespannter Armbrust durchstreift {name} die nächtlichen Felder.",
            "ru": "С натянутым арбалетом {name_ru} прочёсывает ночные поля.",
        },
        {
            "de": "Auf dem Küstenpfad späht {name} nach Spuren des fliehenden Grafen.",
            "ru": "На прибрежной тропе {name_ru} высматривает следы бегущего графа.",
        },
        {
            "de": "Zwischen Dornenhecken zückt {name} das versteckte Messer.",
            "ru": "Среди колючих кустов {name_ru} выхватывает спрятанный нож.",
        },
        {
            "de": "Am Moorloch testet {name} die Tiefe mit der Spitze der Lanze.",
            "ru": "У болотной ямы {name_ru} проверяет глубину наконечником копья.",
        },
        {
            "de": "Vor einem verlassenen Hof horcht {name} auf das Schnaufen der Pferde.",
            "ru": "У заброшенного двора {name_ru} прислушивается к сопению коней.",
        },
        {
            "de": "Unter Regans Banner motiviert {name} die Soldaten zu schnellerer Jagd.",
            "ru": "Под знаменем Реганы {name_ru} подгоняет солдат к более быстрой охоте.",
        },
        {
            "de": "Auf den Klippen über Dover späht {name} in die graue Ferne.",
            "ru": "На скалах над Дувром {name_ru} вглядывается в серую даль.",
        },
    ],
    "coward_death": [
        {
            "de": "Im dunstigen Wald stürzt {name} vor Edgars Klinge rückwärts.",
            "ru": "В туманном лесу {name_ru} падает навзничь перед клинком Эдгара.",
        },
        {
            "de": "Neben einem morschen Baum bittet {name} mit erhobenen Händen um Gnade.",
            "ru": "У трухлявого дерева {name_ru} вздымает руки, умоляя о пощаде.",
        },
        {
            "de": "Am Boden liegend tastet {name} vergeblich nach dem verlorenen Schwert.",
            "ru": "Лежа на земле, {name_ru} тщетно ищет потерянный меч.",
        },
        {
            "de": "Vor Edgars ernster Miene rutscht {name} im nassen Laub aus.",
            "ru": "Перед суровым взглядом Эдгара {name_ru} скользит на мокрой листве.",
        },
        {
            "de": "Unter einem kalten Regen stammelt {name} letzte Ausflüchte.",
            "ru": "Под холодным дождём {name_ru} лепечет последние оправдания.",
        },
        {
            "de": "Im Schatten der Bäume erkennt {name} zu spät die gerechte Vergeltung.",
            "ru": "В тени деревьев {name_ru} слишком поздно осознаёт справедливое возмездие.",
        },
        {
            "de": "Auf dem Waldboden erlischt {name}s Atem ohne Ehrenwache.",
            "ru": "На лесной земле дыхание {name_ru} гаснет без почётного караула.",
        },
        {
            "de": "Neben dem fallengelassenen Brief liegt {name} reglos im Schlamm.",
            "ru": "Рядом с оброненным письмом {name_ru} неподвижно лежит в грязи.",
        },
    ],
    "passive_duke": [
        {
            "de": "Im goldenen Saal sitzt {name} schweigend neben Gonerils Thron.",
            "ru": "В золотом зале {name_ru} молча сидит рядом с троном Гонерильи.",
        },
        {
            "de": "Vor den streitenden Schwestern faltet {name} die Hände hinter dem Rücken.",
            "ru": "Перед ссорящимися сёстрами {name_ru} складывает руки за спиной.",
        },
        {
            "de": "Am Fenster der Audienzhalle betrachtet {name} die vorbeiziehenden Wolken.",
            "ru": "У окна зала приёмов {name_ru} наблюдает за плывущими облаками.",
        },
        {
            "de": "Zwischen zerstreuten Ratsmitgliedern nickt {name} zu allem bereitwillig.",
            "ru": "Среди рассеянных советников {name_ru} покорно кивает всему.",
        },
        {
            "de": "Am Ende der Tafel legt {name} das Besteck ordentlich beiseite.",
            "ru": "В конце стола {name_ru} аккуратно откладывает приборы.",
        },
        {
            "de": "Neben Gonerils triumphierendem Lächeln bleibt {name} reglos.",
            "ru": "Рядом с торжествующей улыбкой Гонерильи {name_ru} остаётся неподвижным.",
        },
        {
            "de": "Auf dem Balkon lauscht {name} stumm den Beschwerden der Diener.",
            "ru": "На балконе {name_ru} безмолвно слушает жалобы слуг.",
        },
        {
            "de": "Im Schatten der Säulen lässt {name} den Streit an sich vorbeiziehen.",
            "ru": "В тени колонн {name_ru} позволяет спору пройти мимо себя.",
        },
    ],
    "first_doubts": [
        {
            "de": "In der nächtlichen Galerie betrachtet {name} das verblassende Familienwappen.",
            "ru": "В ночной галерее {name_ru} рассматривает тускнеющий семейный герб.",
        },
        {
            "de": "Vor dem Spiegel entdeckt {name} zum ersten Mal den Schatten des Zweifels.",
            "ru": "Перед зеркалом {name_ru} впервые замечает тень сомнения.",
        },
        {
            "de": "Neben gestapelten Tributschriften blättert {name} nervös.",
            "ru": "Рядом с кипами податных свитков {name_ru} нервно перелистывает страницы.",
        },
        {
            "de": "Am dunklen Hof beobachtet {name} heimlich die Grausamkeit der Wachen.",
            "ru": "Во тёмном дворе {name_ru} украдкой наблюдает жестокость стражи.",
        },
        {
            "de": "Zwischen verlassenen Banketttischen greift {name} nach einem halb vollen Kelch.",
            "ru": "Среди пустых банкетных столов {name_ru} тянется к наполовину полному кубку.",
        },
        {
            "de": "Auf dem Flur belauscht {name} ein Gespräch über Lear.",
            "ru": "В коридоре {name_ru} подслушивает разговор о Лире.",
        },
        {
            "de": "Im Schlafgemach rollt {name} die Karten des Reiches unruhig zusammen.",
            "ru": "В опочивальне {name_ru} беспокойно скручивает карты королевства.",
        },
    ],
    "awakening": [
        {
            "de": "Vor einem zerschlagenen Spiegel erkennt {name} die eigene Ohnmacht.",
            "ru": "Перед разбитым зеркалом {name_ru} понимает собственное бессилие.",
        },
        {
            "de": "Auf dem staubigen Kampfplatz zieht {name} zum ersten Mal das Schwert.",
            "ru": "На пыльном плацу {name_ru} впервые обнажает меч.",
        },
        {
            "de": "Zwischen aufgebrachten Dienern erhebt {name} die Stimme gegen Goneril.",
            "ru": "Среди взбунтовавшихся слуг {name_ru} поднимает голос против Гонерильи.",
        },
        {
            "de": "Am Fenster beobachtet {name} Lear, der in den Sturm getrieben wird.",
            "ru": "У окна {name_ru} видит, как Лира гонят в бурю.",
        },
        {
            "de": "Auf dem Hof stoppt {name} eine grausame Strafe mit ausgestreckter Hand.",
            "ru": "На дворе {name_ru} протянутой рукой останавливает жестокую казнь.",
        },
        {
            "de": "Im Kriegssaal zerreißt {name} einen falschen Befehl.",
            "ru": "В военном зале {name_ru} разрывает ложный приказ.",
        },
        {
            "de": "Neben Kent tauscht {name} einen verständnisvollen Blick.",
            "ru": "Рядом с Кентом {name_ru} обменивается понимающим взглядом.",
        },
        {
            "de": "An der Grenze des Herzogtums schwört {name} dem Unrecht ab.",
            "ru": "На границе герцогства {name_ru} отрекается от несправедливости.",
        },
    ],
    "confrontation": [
        {
            "de": "Im Kriegslager stellt sich {name} Goneril mitten zwischen die Zelte.",
            "ru": "В военном лагере {name_ru} становится перед Гонерильей среди шатров.",
        },
        {
            "de": "Vor den versammelten Offizieren wirft {name} den Handschuh auf den Tisch.",
            "ru": "Перед собравшимися офицерами {name_ru} бросает перчатку на стол.",
        },
        {
            "de": "Am Wagen voller Waffen blockiert {name} den Weg der Flüchtenden.",
            "ru": "У повозки с оружием {name_ru} преграждает путь беглянке.",
        },
        {
            "de": "Zwischen wehenden Bannern nennt {name} laut den Verrat.",
            "ru": "Под развевающимися знамёнами {name_ru} громко называет предательство.",
        },
        {
            "de": "Auf dem Felsen bei Dover fordert {name} Edmund heraus.",
            "ru": "На скале у Дувра {name_ru} вызывает Эдмунда.",
        },
        {
            "de": "Vor der Armee verliest {name} Gonerils geheime Briefe.",
            "ru": "Перед войском {name_ru} зачитывает тайные письма Гонерильи.",
        },
        {
            "de": "Im hellen Tageslicht zeigt {name} auf die Verräter, ohne zu zittern.",
            "ru": "При ярком дневном свете {name_ru} указывает на предателей без дрожи.",
        },
    ],
    "moral_stand": [
        {
            "de": "Im Feldzelt der Verbündeten zeichnet {name} eine Linie in den Sand.",
            "ru": "В шатре союзников {name_ru} проводит линию на песке.",
        },
        {
            "de": "Zwischen verletzten Soldaten spricht {name} von Gnade.",
            "ru": "Среди раненых солдат {name_ru} говорит о милосердии.",
        },
        {
            "de": "Am Schlachtplan stellt {name} die Figuren der Gerechten nach vorn.",
            "ru": "Над картой сражения {name_ru} выдвигает вперёд фигуры праведников.",
        },
        {
            "de": "Im Rat der Feldherren widerspricht {name} einer grausamen Idee.",
            "ru": "На совете полководцев {name_ru} возражает жестокой задумке.",
        },
        {
            "de": "Vor dem Banner der Wahrheit hebt {name} die Stimme zu einem Eid.",
            "ru": "Перед знаменем правды {name_ru} поднимает голос для клятвы.",
        },
        {
            "de": "Auf dem Hügel über dem Schlachtfeld hält {name} ein feierliches Gebet.",
            "ru": "На холме над полем битвы {name_ru} произносит торжественную молитву.",
        },
        {
            "de": "In der Morgensonne wäscht {name} das Blut vom Schwert und schwört Frieden.",
            "ru": "В утреннем солнце {name_ru} смывает кровь с меча и клянётся миром.",
        },
        {
            "de": "Bei den Feldärzten verspricht {name} Schutz den Verwundeten.",
            "ru": "У полевых лекарей {name_ru} обещает защиту раненым.",
        },
    ],
    "justice_seeker": [
        {
            "de": "Auf dem Tribunal errichtet {name} einen einfachen Holzstuhl als Richterstuhl.",
            "ru": "На трибунале {name_ru} ставит простой деревянный стул как судейский.",
        },
        {
            "de": "Vor den überlebenden Soldaten verliest {name} die Namen der Schuldigen.",
            "ru": "Перед уцелевшими солдатами {name_ru} читает имена виновных.",
        },
        {
            "de": "In der Kapelle legt {name} die Hand auf die Bibel, bevor er urteilt.",
            "ru": "В капелле {name_ru} кладёт руку на Библию, прежде чем судить.",
        },
        {
            "de": "Am Tor von Dover begrüßt {name} die Rückkehrer mit offenen Armen.",
            "ru": "У ворот Дувра {name_ru} встречает возвращающихся с распахнутыми руками.",
        },
        {
            "de": "Auf dem Feldlager sammelt {name} Zeugnisse der Überlebenden.",
            "ru": "В походном лагере {name_ru} собирает свидетельства выживших.",
        },
        {
            "de": "Zwischen verstummten Trommeln verliest {name} den Befehl zur Gerechtigkeit.",
            "ru": "Среди смолкших барабанов {name_ru} зачитывает приказ о справедливости.",
        },
        {
            "de": "Im Schatten des zerstörten Schlosses schwört {name} das Reich zu erneuern.",
            "ru": "В тени разрушенного замка {name_ru} клянётся обновить королевство.",
        },
    ],
    "new_ruler": [
        {
            "de": "Im Saal voller Verwundeter verteilt {name} sanfte Worte und Befehle zugleich.",
            "ru": "В зале, полном раненых, {name_ru} раздаёт мягкие слова и приказы одновременно.",
        },
        {
            "de": "Auf dem behelfsmäßigen Thron richtet {name} das Reich wieder auf.",
            "ru": "На временном троне {name_ru} вновь поднимает королевство.",
        },
        {
            "de": "Zwischen vertrockneten Kränzen trägt {name} die neue Krone ohne Triumph.",
            "ru": "Среди засохших венков {name_ru} носит новую корону без торжества.",
        },
        {
            "de": "Vor dem Volk verspricht {name} Heilung für das verwundete Land.",
            "ru": "Перед народом {name_ru} обещает исцеление раненой земле.",
        },
        {
            "de": "Auf den Stufen des Tempels hebt {name} die Gefallenen in Ehren hervor.",
            "ru": "На ступенях храма {name_ru} чтит павших.",
        },
        {
            "de": "Unter wehenden Flaggen lässt {name} die Glocken der Hoffnung schlagen.",
            "ru": "Под развевающимися флагами {name_ru} велит бить колоколам надежды.",
        },
        {
            "de": "Im Rat der Überlebenden hört {name} jedem zu, bevor er entscheidet.",
            "ru": "На совете выживших {name_ru} выслушивает каждого, прежде чем решать.",
        },
        {
            "de": "An der Küste von Dover lässt {name} neue Schiffe zum Schutz auslaufen.",
            "ru": "У берега Дувра {name_ru} отправляет в море новые корабли для защиты.",
        },
    ],
}


def _hash_index(*values, modulo):
    key = "|".join(values)
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(digest, 16) % modulo


def _hash_index(*values, modulo):
    key = "|".join(values)
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(digest, 16) % modulo


def build_clause(character_id, phase_id, german, russian):
    index = _hash_index(character_id, phase_id, german, modulo=len(CLAUSE_TEMPLATES))
    template = CLAUSE_TEMPLATES[index]
    word_quote = f"„{german}“"
    word_ru_quote = f"«{russian}»"
    clause_de = template["de"].format(word_quote=word_quote)
    clause_ru = template["ru"].format(word_ru_quote=word_ru_quote)
    return clause_de, clause_ru


def update_sentences():
    for path in sorted(CHAR_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        char_id = data.get("id")
        ru_name = RU_NAMES.get(char_id, data.get("name", char_id))

        changed = False
        for phase in data.get("journey_phases", []):
            phase_id = phase.get("id")
            details = PHASE_DETAILS.get(phase_id)
            if not details:
                continue

            vocabulary = phase.get("vocabulary") or []
            if not vocabulary:
                continue

            for idx, vocab in enumerate(vocabulary):
                detail = details[idx % len(details)]
                clause_de, clause_ru = build_clause(char_id, phase_id, vocab.get("german", ""), vocab.get("russian", ""))

                detail_de = detail["de"].format(name=data.get("name", char_id))
                detail_ru = detail["ru"].format(name_ru=ru_name)

                vocab["sentence"] = f"{detail_de} {clause_de}"
                vocab["sentence_translation"] = f"{detail_ru} {clause_ru}"
                changed = True

        if changed:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[UPDATED] {path.name}")


def update_vocabulary_examples():
    vocab_path = BASE_DIR / "data" / "vocabulary" / "vocabulary.json"
    if not vocab_path.exists():
        return

    data = json.loads(vocab_path.read_text(encoding="utf-8"))
    vocabulary = data.get("vocabulary")
    if not isinstance(vocabulary, list):
        return

    changed = False
    for entry in vocabulary:
        if not isinstance(entry, dict):
            continue

        german = entry.get("german") or entry.get("german_stressed")
        russian = entry.get("translation")
        if not german or not russian:
            continue

        base_key = str(entry.get("id") or german)
        context_index = _hash_index(base_key, "context", modulo=len(EXAMPLE_CONTEXTS))
        context = EXAMPLE_CONTEXTS[context_index]

        clause_index = str(_hash_index(base_key, "clause", modulo=97))
        clause_de, clause_ru = build_clause("vocab", clause_index, german, str(russian))

        example = {
            "de": f"{context['de']} {clause_de}",
            "ru": f"{context['ru']} {clause_ru}",
        }

        entry["example_sentences"] = [example]
        changed = True

    if changed:
        vocab_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print("[UPDATED] vocabulary.json")


if __name__ == "__main__":
    update_sentences()
    update_vocabulary_examples()
