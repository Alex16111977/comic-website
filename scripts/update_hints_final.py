import json
import os
from pathlib import Path

# ПОЛНЫЙ СЛОВАРЬ ЛИНГВИСТИЧЕСКИХ ПОДСКАЗОК
ALL_HINTS = {
    # === СУЩЕСТВИТЕЛЬНЫЕ - ВЛАСТЬ И ГОСУДАРСТВО ===
    "der Thron": "символ королевской власти",
    "das Königreich": "государство короля",
    "die Macht": "абстрактная власть",
    "die Herrschaft": "конкретное правление",
    "die Krone": "знак монаршей власти",
    "die Zeremonie": "торжественный ритуал",
    "der Palast": "резиденция монарха",
    "das Schloss": "замок властителя",
    "der Hof": "королевский двор",
    "der König": "правитель государства",
    "die Königin": "супруга короля",
    "der Herrscher": "тот, кто правит",
    "das Reich": "держава, империя",
    "der Adel": "знатное сословие",
    "die Autorität": "моральный авторитет",
    
    # === СЕМЬЯ И ОТНОШЕНИЯ ===
    "der Vater": "глава семьи",
    "die Tochter": "дочь отца",
    "die Liebe": "чувство привязанности",
    "die Treue": "верность до конца",
    "der Verrat": "предательство доверия",
    "die Pflicht": "долг чести",
    "die Familie": "кровные узы",
    "der Hass": "противоположность любви",
    "die Ehe": "брачный союз",
    "der Sohn": "наследник отца",
    "der Bruder": "брат по крови",
    "die Schwester": "сестра по крови",
    "der Erbe": "наследник имущества",
    
    # === ЭМОЦИИ И СОСТОЯНИЯ ===
    "der Zorn": "благородный гнев",
    "die Wut": "слепая ярость",
    "der Ärger": "легкое раздражение",
    "die Verzweiflung": "полная безнадежность",
    "die Undankbarkeit": "черная неблагодарность",
    "die Grausamkeit": "безжалостная жестокость",
    "die Kränkung": "обида души",
    "der Fluch": "злое проклятие",
    "die Wahrheit": "объективная истина",
    "die Einsamkeit": "одиночество души",
    "der Wahnsinn": "потеря разума",
    "die Träne": "капля скорби",
    "das Herz": "средоточие чувств",
    "die Hoffnung": "вера в лучшее",
    "die Angst": "чувство страха",
    "der Mut": "храбрость духа",
    "die Freude": "радостное чувство",
    "die Trauer": "глубокая печаль",
    "der Schmerz": "душевная боль",
    "die Qual": "мучительное страдание",
    "das Leid": "тяжкое горе",
    "die Vernunft": "здравый смысл",
    "die Klarheit": "ясность ума",
    
    # === ПРИРОДА И СТИХИИ ===
    "der Sturm": "буйство стихии",
    "der Donner": "громовой раскат",
    "der Blitz": "молния в небе",
    "das Chaos": "полный беспорядок",
    "der Regen": "дождевой поток",
    "der Wind": "движение воздуха",
    "die Natur": "мир природы",
    "die Wildnis": "дикая местность",
    "die Heide": "пустошь без крова",
    "die Finsternis": "полная темнота",
    "die Ordnung": "установленный порядок",
    
    # === МЕСТА И СОСТОЯНИЯ ===
    "die Hütte": "бедное жилище",
    "das Elend": "крайняя нищета",
    "die Not": "острая нужда",
    "der Bettler": "просящий милостыню",
    "der Narr": "придворный шут",
    "der Kerker": "место заточения",
    "das Gefängnis": "тюремное узилище",
    "die Verbannung": "изгнание из страны",
    "das Exil": "вынужденное изгнание",
    "die Heimat": "родная земля",
    "die Fremde": "чужая сторона",
    "der Reichtum": "большое богатство",
    "die Armut": "материальная бедность",
    
    # === ЖИЗНЬ И СМЕРТЬ ===
    "der Tod": "конец жизни",
    "das Ende": "финал всего",
    "der Abschied": "последнее прощание",
    "die Reue": "раскаяние в содеянном",
    "die Weisheit": "мудрость опыта",
    "die Einsicht": "внезапное прозрение",
    "die Erkenntnis": "познание истины",
    "das Leben": "бытие человека",
    "das Sterben": "процесс умирания",
    "der Anfang": "начало пути",
    "das Schicksal": "неизбежная судьба",
    "das Grab": "последний приют",
    
    # === ГЛАГОЛЫ - ВЛАСТЬ И УПРАВЛЕНИЕ ===
    "herrschen": "править государством",
    "verkünden": "объявлять официально",
    "gehorchen": "подчиняться приказам",
    "regieren": "управлять страной",
    "befehlen": "отдавать приказы",
    "gebieten": "повелевать властно",
    "dienen": "служить господину",
    "unterwerfen": "подчинять силой",
    
    # === ГЛАГОЛЫ - ОТВЕРЖЕНИЕ ===
    "verstoßen": "отвергать из семьи",
    "vertreiben": "изгонять силой",
    "verlassen": "покидать по воле",
    "verbannen": "ссылать официально",
    "hinauswerfen": "выкидывать грубо",
    "fortjagen": "прогонять прочь",
    
    # === ГЛАГОЛЫ - ЭМОЦИИ ===
    "demütigen": "унижать достоинство",
    "verfluchen": "предавать проклятию",
    "lieben": "испытывать любовь",
    "verraten": "предавать доверие",
    "verzeihen": "прощать обиды",
    "leiden": "терпеть страдания",
    "weinen": "проливать слезы",
    "sterben": "прекращать жить",
    "betteln": "просить униженно",
    "toben": "буйствовать яростно",
    "schreien": "кричать громко",
    "frieren": "мерзнуть от холода",
    "erkennen": "узнавать знакомое",
    "verstehen": "понимать смысл",
    "bereuen": "сожалеть о содеянном",
    "hassen": "питать ненависть",
    "vergeben": "отпускать вину",
    "vertrauen": "доверять полностью",
    "misstrauen": "не доверять",
    "täuschen": "вводить в обман",
    "lügen": "говорить неправду",
    "betrügen": "обманывать намеренно",
    "dulden": "сносить молча",
    "ertragen": "выносить тяжесть",
    "klagen": "жаловаться на судьбу",
    "trauern": "скорбеть о потере",
    "verzweifeln": "впадать в отчаяние",
    "hoffen": "надеяться на лучшее",
    "fürchten": "бояться худшего",
    "sprechen": "говорить словами",
    "schweigen": "хранить молчание",
    "flüstern": "шептать тихо",
    "fluchen": "проклинать гневно",
    "segnen": "благословлять добром",
    "beten": "молиться богу",
    "schwören": "клясться торжественно",
    
    # === ПРИЛАГАТЕЛЬНЫЕ - ХАРАКТЕРИСТИКИ ===
    "prächtig": "роскошный, пышный",
    "feierlich": "торжественно важный",
    "treu": "верный до конца",
    "grausam": "безжалостно жестокий",
    "wahnsinnig": "потерявший разум",
    "verzweifelt": "впавший в отчаяние",
    "einsam": "одинокий душой",
    "arm": "бедный материально",
    "nackt": "лишенный одежд",
    "schuldig": "несущий вину",
    "ewig": "бесконечный во времени",
    "majestätisch": "величественный вид",
    "königlich": "достойный короля",
    "edel": "благородного рода",
    "erhaben": "возвышенный духом",
    "würdig": "достойный уважения",
    "heilig": "священный для всех",
    "böse": "злой по натуре",
    "falsch": "лживый, неискренний",
    "hinterlistig": "коварно хитрый",
    "heimtückisch": "предательски скрытный",
    "gierig": "жадный до власти",
    "neidisch": "завистливый к другим",
    "loyal": "преданный долгу",
    "ehrlich": "честный всегда",
    "aufrichtig": "искренний душой",
    "gerecht": "справедливый ко всем",
    "gütig": "добрый сердцем",
    "barmherzig": "милосердный к слабым",
    "weise": "мудрый опытом",
    "verrückt": "сдвинувшийся умом",
    "irre": "заблудший рассудком",
    "verlassen": "всеми покинутый",
    "reich": "богатый имуществом",
    "blind": "лишенный зрения",
    "alt": "проживший годы",
    "jung": "малый годами",
    "stark": "сильный телом",
    "schwach": "слабый силами",
    
    # === ДОПОЛНИТЕЛЬНЫЕ СУЩЕСТВИТЕЛЬНЫЕ ===
    "der Bastard": "незаконнорожденный",
    "der Herzog": "высший титул",
    "der Graf": "знатный титул",
    "das Gut": "имение, поместье",
    "die Gnade": "милость свыше",
    "die Rache": "месть за обиду",
    "die Schande": "позор и стыд",
    "die Schuld": "вина за поступок",
    "die Seele": "душа человека",
    "die Tugend": "добродетель",
    "das Unglück": "несчастье судьбы",
    "das Urteil": "приговор суда",
    "das Verbrechen": "злое преступление",
    "das Vermögen": "богатое имущество",
    "die Verschwörung": "тайный заговор",
    "der Verstand": "здравый рассудок",
    "der Wille": "воля к действию",
    "die Wunde": "рана тела",
    "der Zweifel": "сомнение в правде",
    "der Diener": "слуга господина",
    "die Dienerin": "служанка в доме",
    "der Feind": "враг заклятый",
    "der Freund": "друг верный",
    "der Geist": "дух человека",
    "das Gesetz": "закон страны",
    "das Gewissen": "голос совести",
    "der Grund": "причина действий",
    "die Gunst": "благосклонность",
    "das Haus": "дом семьи",
    "der Himmel": "небеса над нами",
    "die Hölle": "ад под нами",
    "die Hoffnungslosigkeit": "без надежды",
    "die Intrige": "хитрый план",
    "der Kampf": "борьба за жизнь",
    "die Klage": "жалоба на судьбу",
    "die Kraft": "сила духа",
    "der Krieg": "война народов",
    "die Kunst": "искусство жизни",
    "die Last": "тяжкое бремя",
    "das Laster": "порок души",
    "das Recht": "право по закону",
    "die Rettung": "спасение от беды",
    "der Richter": "судья народа",
    "der Ruhm": "слава героя",
    "die Sünde": "грех перед богом",
    "der Trost": "утешение в беде",
    "das Übel": "зло в мире",
    "das Unrecht": "несправедливость",
    "die Verantwortung": "ответственность",
    "das Verderben": "погибель души",
    "das Verhängnis": "роковая судьба",
    "der Verlust": "потеря важного",
    "die Vernichtung": "полное уничтожение",
    "die Versöhnung": "примирение сторон",
    "der Vorwurf": "упрек в вине",
    "die Wahl": "выбор пути",
    "der Wandel": "перемена судьбы",
    "die Warnung": "предупреждение",
    "das Wesen": "суть вещей",
    "der Wunsch": "желание сердца",
    "die Würde": "достоинство",
    "der Zeuge": "свидетель дела",
    "das Ziel": "цель стремлений",
    "die Zukunft": "будущее время",
    "die Zuneigung": "теплая симпатия"
}

def update_all_characters():
    """Обновляем подсказки для всех персонажей"""
    
    characters_dir = Path(r"F:\AiKlientBank\KingLearComic\data\characters")
    characters = [
        "king_lear", "cordelia", "goneril", "regan",
        "gloucester", "edgar", "edmund", "kent",
        "fool", "albany", "cornwall", "oswald"
    ]
    
    print("[ФИНАЛЬНОЕ ОБНОВЛЕНИЕ RUSSIAN_HINT]")
    print("=" * 60)
    
    total_updated = 0
    
    for char in characters:
        file_path = characters_dir / f"{char}.json"
        
        try:
            # Читаем файл
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            char_updated = 0
            
            # Обновляем подсказки
            for phase in data.get("journey_phases", []):
                for vocab in phase.get("vocabulary", []):
                    german = vocab.get("german", "")
                    
                    # Применяем подсказку из словаря
                    if german in ALL_HINTS:
                        old_hint = vocab.get("russian_hint", "")
                        vocab["russian_hint"] = ALL_HINTS[german]
                        char_updated += 1
                    elif vocab.get("russian_hint"):
                        # Убираем скобки из существующих подсказок
                        old_hint = vocab["russian_hint"]
                        if "(" in old_hint:
                            # Берем только часть до скобки
                            new_hint = old_hint.split("(")[0].strip()
                            vocab["russian_hint"] = new_hint
                            char_updated += 1
            
            # Сохраняем обновленный файл
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"  [OK] {char:12} - Обновлено {char_updated} подсказок")
            total_updated += char_updated
            
        except Exception as e:
            print(f"  [ERROR] {char}: {e}")
    
    print("-" * 60)
    print(f"ИТОГО обновлено: {total_updated} подсказок")
    return total_updated

if __name__ == "__main__":
    result = update_all_characters()
    print(f"\n[УСПЕХ] Обновление завершено!")
