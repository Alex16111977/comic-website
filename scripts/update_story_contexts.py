import json
import glob

def add_prefix(text: str, prefix: str) -> str:
    text = text.strip()
    if not text:
        return prefix
    if text.startswith(prefix):
        return text
    if text.lower().startswith(prefix.lower()):
        return text
    return f"{prefix}: {text}"

character_phase_contexts = {
    "albany": {
        "passive_duke": ("Im Schloss von Goneril am Hof König Lears gesteht Albany", "Во дворце Гонериль при дворе короля Лира признаётся Олбани"),
        "first_doubts": ("Nach Cordelias Verbannung flüstert Albany in den stillen Fluren seines Schlosses", "После изгнания Корделии Олбани шепчет в тихих коридорах своего замка"),
        "awakening": ("Als Gonerils Grausamkeit vor König Lear offenbart wird, erwacht Albany", "Когда жестокость Гонериль раскрывается перед королём Лиром, Олбани пробуждается"),
        "confrontation": ("Im Saal, in dem Lear gedemütigt wurde, stellt Albany seine Frau", "В зале, где унижали Лира, Олбани бросает вызов своей жене"),
        "moral_stand": ("Vor den erschütterten Höflingen Lears verkündet Albany", "Перед потрясёнными придворными Лира Олбани заявляет"),
        "justice_seeker": ("An Lears verwaistem Hof sammelt Albany die Getreuen", "При опустевшем дворе Лира Олбани собирает верных"),
        "new_ruler": ("Nach der Tragödie von Dover übernimmt Albany im Thronsaal Lears", "После трагедии в Дувре Олбани принимает власть в тронном зале Лира"),
    },
    "cordelia": {
        "throne": ("Im Thronsaal von König Lear spricht Cordelia", "В тронном зале короля Лира Корделия говорит"),
        "goneril": ("Auf dem Kai vor der Abreise nach Frankreich schwört Cordelia", "На причале перед отъездом во Францию Корделия клянётся"),
        "regan": ("Im französischen Exil erinnert sich Cordelia an Lear", "Во французском изгнании Корделия вспоминает Лира"),
        "storm": ("Mit der französischen Armee vor Dover ruft Cordelia", "Во главе французской армии у Дувра Корделия восклицает"),
        "hut": ("In der armseligen Hütte, wo Lear tobt, hält Cordelia seine Hände", "В убогой хижине, где метётся Лир, Корделия держит его руки"),
        "dover": ("Nach der Niederlage auf dem Feld von Dover spricht Cordelia als Gefangene", "После поражения на поле под Дувром Корделия говорит как пленница"),
        "prison": ("Im Kerker, den Edmund bewacht, haucht Cordelia", "В темнице, которую стерёжёт Эдмунд, Корделия шепчет"),
    },
    "cornwall": {
        "ambitious_duke": ("In Glosters Schloss plant Herzog Cornwall", "В замке Глостера герцог Корнуолл замышляет"),
        "cruel_husband": ("In Regans Gemächern zeigt Cornwall seiner Frau die Härte", "В покоях Реганы Корнуолл демонстрирует жене свою жестокость"),
        "tyrant": ("Während Lear vor der Burg um Einlass fleht, prahlt Cornwall", "Пока Лир умоляет впустить его в замок, Корнуолл хвастается"),
        "punishment": ("Vor den Mauern von Glosters Burg befiehlt Cornwall", "Перед стенами замка Глостера Корнуолл приказывает"),
        "torturer": ("Im Kerker von Gloster bereitet Cornwall die Folter", "В застенках Глостера Корнуолл готовит пытку"),
        "wounded": ("Nachdem Gloucester geblendet ist, taumelt Cornwall blutend durch den Hof", "Осле слепления Глостера Корнуолл, истекая кровью, шатается по двору"),
        "death": ("Sterbend in Regans Gemächern knurrt Cornwall", "Умирая в покоях Реганы, Корнуолл рычит"),
    },
    "edgar": {
        "throne": ("In Glosters Halle verspricht Edgar seinem Vater", "В зале Глостера Эдгар обещает отцу"),
        "goneril": ("Nach Edmunds Verrat flieht Edgar durch den Wald", "После предательства Эдмунда Эдгар бежит через лес"),
        "regan": ("Als armer Tom auf der Heide erklärt Edgar", "Под видом бедного Тома на пустоши Эдгар объясняет"),
        "storm": ("In Lears sturmgepeitschter Nacht begleitet Edgar den König", "В штормовую ночь Лира Эдгар сопровождает короля"),
        "hut": ("Vor der Hütte führt Edgar den blinden Gloucester", "Перед хижиной Эдгар ведёт слепого Глостера"),
        "dover": ("Auf den Klippen von Dover schwört Edgar", "На утёсах Дувра Эдгар клянётся"),
        "prison": ("Nach dem Sieg über Edmund vor Lears Hof erklärt Edgar", "После победы над Эдмундом перед двором Лира Эдгар объявляет"),
    },
    "edmund": {
        "throne": ("Im Schloss von Gloucester schwört Edmund heimlich", "В замке Глостера Эдмунд тайно клянётся"),
        "goneril": ("In seiner Kammer unterschreibt Edmund den falschen Brief", "В своей комнате Эдмунд подписывает фальшивое письмо"),
        "regan": ("Im Saal, den Regan hält, prahlt Edmund", "В зале, который удерживает Регана, Эдмунд хвастается"),
        "storm": ("Während die Schwestern über Lear beraten, versichert Edmund", "Пока сёстры совещаются о Лире, Эдмунд уверяет"),
        "hut": ("Vor den Toren von Gloucester verkauft Edmund seinen Vater", "Перед воротами Глостера Эдмунд продаёт отца"),
        "dover": ("Zwischen den Lagern von Goneril und Regan flüstert Edmund", "Между лагерями Гонериль и Реганы Эдмунд шепчет"),
        "prison": ("Im Feldlager von Albany vor dem Duell erkennt Edmund", "В лагере Олбани перед дуэлью Эдмунд признаёт"),
    },
    "fool": {
        "jester": ("Im Thronsaal von Lear tanzt der Narr neben Cordelia", "В тронном зале Лира шут пляшет рядом с Корделией"),
        "bitter_truths": ("Unter Gonerils kaltem Blick singt der Narr", "Под холодным взглядом Гонериль шут поёт"),
        "prophecies": ("Auf der sturmgepeitschten Heide prophezeit der Narr", "На продуваемой бурей пустоши шут пророчит"),
        "mad_companion": ("In der Hütte teilt der Narr Lears Wahnsinn", "В хижине шут разделяет безумие Лира"),
        "songs": ("Bei Cordelias Rückkehr nach Dover singt der Narr leise", "Во время возвращения Корделии в Дувр шут тихо поёт"),
        "wisdom": ("Nach dem Marsch nach Dover sinniert der Narr", "После перехода в Дувр шут размышляет"),
        "vanishing": ("Kurz vor Cordelias Gefangennahme verschwindet der Narr", "Незадолго до пленения Корделии шут исчезает"),
    },
    "gloucester": {
        "throne": ("Im Schloss von Gloucester versichert der alte Graf König Lear", "В замке Глостера старый граф уверяет короля Лира"),
        "goneril": ("Als Edmund den Brief präsentiert, vertraut Gloucester Gonerils Hof", "Когда Эдмунд показывает письмо, Глостер доверяет придворным Гонериль"),
        "regan": ("Im Hof von Regans Burg verflucht Gloucester seinen Sohn", "Во дворе замка Реганы Глостер проклинает сына"),
        "storm": ("In der Nacht auf der Heide hilft Gloucester dem wahnsinnigen Lear", "В ночи на пустоши Глостер помогает обезумевшему Лиру"),
        "hut": ("Im finsteren Kerker der Burg lassen Regan und Cornwall Gloucester leiden", "В тёмном застенке замка Реганы и Корнуолла Глостер страдает"),
        "dover": ("An den Klippen von Dover führt armer Tom den blinden Gloucester", "На утёсах Дувра бедный Том ведёт слепого Глостера"),
        "prison": ("Nach der Rettung in Dover erkennt Gloucester in Edgars Armen", "После спасения в Дувре Глостер узнаёт Эдгара в его объятиях"),
    },
    "goneril": {
        "throne": ("Im Thronsaal von König Lear haucht Goneril", "В тронном зале короля Лира Гонериль шепчет"),
        "goneril": ("In ihrem Palast in Albany prahlt Goneril", "В своём дворце в Олбани Гонериль хвастается"),
        "regan": ("Als Lear bei ihr Quartier nimmt, befiehlt Goneril", "Когда Лир квартирует у неё, Гонериль приказывает"),
        "storm": ("Vor den Toren ihres Schlosses stößt Goneril den Vater hinaus", "Перед воротами своего замка Гонериль выталкивает отца"),
        "hut": ("In Albanys Kriegslager streitet Goneril mit ihrem Mann", "В военном лагере Олбани Гонериль ссорится с мужем"),
        "dover": ("Im Feldlager vor Dover grollt Goneril gegen Regan", "В поле под Дувром Гонериль злится на Регану"),
        "prison": ("Allein in ihrem Zelt nach Regans Tod flüstert Goneril", "Одна в своём шатре после смерти Реганы Гонериль шепчет"),
    },
    "kent": {
        "loyalty": ("Im Thronsaal von Lear kniet Kent", "В тронном зале Лира Кент преклоняется"),
        "banishment": ("Vor der Hofpforte, nachdem Lear ihn verstoßen hat, ruft Kent", "У ворот дворца, после изгнания Лиром, Кент восклицает"),
        "disguise": ("Vor Gonerils Burg legt Kent seine Verkleidung an", "Перед замком Гонериль Кент надевает своё маскировочное платье"),
        "service": ("Als Diener Caius an Lears Seite schwört Kent", "В облике слуги Кая при Лире Кент клянётся"),
        "stocks": ("Im Hof von Regans Schloss sitzt Kent im Pranger", "Во дворе замка Реганы Кент сидит в колодках"),
        "storm_companion": ("Auf der Heide im Sturm stützt Kent den alten König", "На пустоши в бурю Кент поддерживает старого короля"),
        "final_loyalty": ("Vor Cordelias Leichnam in Dover verweigert Kent die Krone", "Перед телом Корделии в Дувре Кент отвергает корону"),
    },
    "king_lear": {
        "throne": ("Im prunkvollen Thronsaal ruft König Lear", "В роскошном тронном зале восклицает король Лир"),
        "goneril": ("In Gonerils Palast fühlt Lear", "Во дворце Гонериль Лир ощущает"),
        "regan": ("Auf dem Hof von Regans Burg fleht Lear", "На дворе замка Реганы Лир умоляет"),
        "storm": ("Auf der Heide unter peitschendem Regen schreit Lear", "На пустоши под хлещущим дождём Лир кричит"),
        "hut": ("In der verfallenen Hütte bei Gloucester halluziniert Lear", "В полуразвалившейся хижине у Глостера Лир бредит"),
        "dover": ("Vor den Klippen von Dover bei Cordelias Truppen erkennt Lear", "У утёсов Дувра рядом с войском Корделии Лир осознаёт"),
        "prison": ("Im Kerker, den Edmund bewacht, flüstert Lear", "В темнице, которую охраняет Эдмунд, Лир шепчет"),
    },
    "oswald": {
        "steward": ("Im Haus der Goneril herrscht Oswald als Verwalter", "В доме Гонериль Освальд распоряжается как управляющий"),
        "messenger": ("Zwischen Gonerils Palast und Regans Burg rennt Oswald", "Между дворцом Гонериль и замком Реганы Освальд бегает"),
        "insult": ("Vor König Lear am Tor von Gonerils Schloss spottet Oswald", "Перед королём Лиром у ворот замка Гонериль Освальд издевается"),
        "spy": ("In den Korridoren von Albanys Burg schleicht Oswald", "В коридорах замка Олбани Освальд крадётся"),
        "schemer": ("Bei nächtlichen Beratungen mit Goneril plant Oswald", "На ночных советах с Гонериль Освальд планирует"),
        "pursuer": ("Auf den Feldern nahe Dover jagt Oswald den blinden Gloucester", "На полях близ Дувра Освальд гонится за слепым Глостером"),
        "coward_death": ("Als Edgar ihn am Strand von Dover stellt, jammert Oswald", "Когда Эдгар настигает его на берегу Дувра, Освальд стонет"),
    },
    "regan": {
        "throne": ("Im Thronsaal von Lear wetteifert Regan mit ihrer Schwester", "В тронном зале Лира Регана соперничает с сестрой"),
        "goneril": ("Beim geheimen Pakt in Gonerils Gemächern flüstert Regan", "На тайном сговоре в покоях Гонериль Регана шепчет"),
        "regan": ("In ihrem Schloss in Gloucester demütigt Regan den König", "В своём замке в Глостере Регана унижает короля"),
        "storm": ("Während Gloucester geblendet wird, befiehlt Regan", "Во время ослепления Глостера Регана приказывает"),
        "hut": ("Als Witwe nach Cornwalls Tod verlangt Regan nach Edmund", "Став вдовой после смерти Корнуолла, Регана требует Эдмунда"),
        "dover": ("Im Lager vor Dover droht Regan ihrer Schwester", "В лагере под Дувром Регана грозит сестре"),
        "prison": ("Vergiftet von Goneril stirbt Regan in ihrem Zelt", "Отравленная Гонериль Регана умирает в своём шатре"),
    },
}

# Validate that every character and phase has context
for path in glob.glob("data/characters/*.json"):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    char_id = data["id"]
    if char_id not in character_phase_contexts:
        raise KeyError(f"Missing contexts for character {char_id}")
    for phase in data.get("journey_phases", []):
        phase_id = phase["id"]
        if phase_id not in character_phase_contexts[char_id]:
            raise KeyError(f"Missing context for {char_id}:{phase_id}")
        ctx_de, ctx_ru = character_phase_contexts[char_id][phase_id]
        for vocab in phase.get("vocabulary", []):
            vocab["sentence"] = add_prefix(vocab["sentence"], ctx_de)
            vocab["sentence_translation"] = add_prefix(vocab["sentence_translation"], ctx_ru)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Vocabulary contexts
THEME_CONTEXTS = {
    "король лир": ("Am Hof von König Lear erzählt man", "При дворе короля Лира рассказывают"),
    "Frankreich": ("Im Lager der französischen Cordelia berichtet man", "Во французском лагере Корделии рассказывают"),
    "Sturm": ("Auf der sturmgepeitschten Heide an Lears Seite flüstern wir", "На продуваемой бурей пустоши рядом с Лиром мы шепчем"),
    "Heide": ("Auf der sturmgepeitschten Heide an Lears Seite flüstern wir", "На продуваемой бурей пустоши рядом с Лиром мы шепчем"),
    "Dover": ("An den Klippen von Dover, wo Edgar seinen Vater führt, erinnert man sich", "У утёсов Дувра, где Эдгар ведёт отца, вспоминают"),
    "Klippe": ("An den Klippen von Dover, wo Edgar seinen Vater führt, erinnert man sich", "У утёсов Дувра, где Эдгар ведёт отца, вспоминают"),
    "Klippen": ("An den Klippen von Dover, wo Edgar seinen Vater führt, erinnert man sich", "У утёсов Дувра, где Эдгар ведёт отца, вспоминают"),
    "Gefängnis": ("Im Kerker von Dover, in dem Lear und Cordelia sitzen, sagt man", "В темнице Дувра, где сидят Лир и Корделия, говорят"),
    "Hütte": ("In der windschiefen Hütte, die den König birgt, murmeln wir", "В покосившейся хижине, где укрывается король, мы бормочем"),
    "Hut": ("In der windschiefen Hütte, die den König birgt, murmeln wir", "В покосившейся хижине, где укрывается король, мы бормочем"),
    "Burg": ("In den Hallen von Regans und Gonerils Burgen raunen die Diener", "В залах замков Реганы и Гонериль шепчутся слуги"),
    "Schloss": ("In den Hallen von Regans und Gonerils Burgen raunen die Diener", "В залах замков Реганы и Гонериль шепчутся слуги"),
    "Albany": ("In Albanys Lager nach Cordelias Landung beraten wir", "В лагере Олбани после высадки Корделии мы советуемся"),
    "Armee": ("Im Feldlager Cordelias vor Dover berichten Offiziere", "В полевом лагере Корделии под Дувром офицеры докладывают"),
    "König": ("Am Hof von König Lear erzählt man", "При дворе короля Лира рассказывают"),
    "Cordelia": ("Im französischen Gefolge Cordelias berichtet man", "В французском свите Корделии рассказывают"),
    "Goneril": ("In Gonerils Palast flüstern die Diener", "Во дворце Гонериль шепчутся слуги"),
    "Regan": ("In Regans Burg planen die Höflinge", "В замке Реганы замышляют придворные"),
    "Edmund": ("Im Zelt des ehrgeizigen Edmund prahlt man", "В шатре честолюбивого Эдмунда хвастаются"),
    "Edgar": ("Neben Edgar auf den Klippen von Dover schwören wir", "Рядом с Эдгаром на утёсах Дувра мы клянёмся"),
    "Gloucester": ("Im Haus des Grafen Gloucester erzählt man", "В доме графа Глостера рассказывают"),
    "Kent": ("An Kents Seite im Gefolge des Königs schwört man", "Рядом с Кентом в свите короля клянутся"),
    "Narr": ("Neben dem Narren, der Lear begleitet, singen wir", "Рядом с шутом, что сопровождает Лира, мы поём"),
    "Oswald": ("In Oswalds Dienersaal schmiedet man Pläne", "В слугской Освальда строят планы"),
    "Cornwall": ("In Cornwalls dunklem Hof befiehlt man", "Во мрачном дворе Корнуолла отдают приказы"),
    "Gift": ("In Regans Zelt, wo das Gift gemischt wird, flüstert man", "В шатре Реганы, где смешивают яд, шепчутся"),
    "vergiften": ("In Regans Zelt, wo das Gift gemischt wird, flüstert man", "В шатре Реганы, где смешивают яд, шепчутся"),
    "Blind": ("Seit Gloucester geblendet wurde, erzählt man in Dover", "После ослепления Глостера в Дувре рассказывают"),
    "blenden": ("Seit Gloucester geblendet wurde, erzählt man in Dover", "После ослепления Глостера в Дувре рассказывают"),
    "Treue": ("Bei Cordelias treuer Umarmung sagt man", "У верных объятий Корделии говорят"),
    "Wahnsinn": ("Im Kreis des wahnsinnigen Lear hört man", "В кругу обезумевшего Лира слышат"),
    "Verkleidung": ("Während Kent seine Verkleidung trägt, flüstert man", "Пока Кент носит маскировку, шепчутся"),
    "Intrige": ("In Edmunds Intrigenzelt tuscheln die Verbündeten", "В заговорщицком шатре Эдмунда перешёптываются союзники"),
    "Brief": ("Seit Edmund den falschen Brief schrieb, raunen die Diener", "С тех пор как Эдмунд написал фальшивое письмо, слуги шепчутся"),
    "Bastard": ("Im Schatten von Gloucester spricht man über den Bastard", "В тени Глостера говорят о бастарде"),
    "Rache": ("In den Plänen der Schwestern schwört man auf Rache", "В планах сестёр клянутся местью"),
    "Rivalität": ("Im Streitlager der Schwestern um Edmund zischt man", "В спорщем лагере сестёр из-за Эдмунда шипят"),
    "Duell": ("Vor dem Duell zwischen Edgar und Edmund erinnert man sich", "Перед дуэлью Эдгара и Эдмунда вспоминают"),
    "Armut": ("Unter armen Bettlern, die Edgar begegnen, erzählt man", "Среди нищих, что встречают Эдгара, рассказывают"),
    "Verzweiflung": ("An den Klippen bei Gloucesters Verzweiflung flüstert man", "У утёсов, где отчаялся Глостер, шепчутся"),
}

# Remove accidental duplicate keys by reassigning
THEME_CONTEXTS["Treue"] = ("Bei Cordelias treuer Umarmung sagt man", "У верных объятий Корделии говорят")
THEME_CONTEXTS["Armut"] = ("Unter armen Bettlern, die Edgar begegnen, erzählt man", "Среди нищих, что встречают Эдгара, рассказывают")

DEFAULT_CONTEXT = THEME_CONTEXTS["король лир"]

with open("data/vocabulary/vocabulary.json", encoding="utf-8") as f:
    vocabulary = json.load(f)

for entry in vocabulary.get("vocabulary", []):
    themes = entry.get("themes", []) or []
    context = None
    for theme in themes:
        if theme in THEME_CONTEXTS:
            context = THEME_CONTEXTS[theme]
            break
    if context is None:
        # try german-specific hints
        german_word = entry.get("german", "")
        for key, ctx in [
            ("Lear", THEME_CONTEXTS["король лир"]),
            ("Cordelia", THEME_CONTEXTS.get("Cordelia", DEFAULT_CONTEXT)),
            ("Edmund", THEME_CONTEXTS.get("Edmund", DEFAULT_CONTEXT)),
            ("Edgar", THEME_CONTEXTS.get("Edgar", DEFAULT_CONTEXT)),
        ]:
            if key and german_word and key.lower() in german_word.lower():
                context = ctx
                break
    if context is None:
        context = DEFAULT_CONTEXT
    ctx_de, ctx_ru = context
    for example in entry.get("example_sentences", []):
        example["de"] = add_prefix(example["de"], ctx_de)
        example["ru"] = add_prefix(example["ru"], ctx_ru)

with open("data/vocabulary/vocabulary.json", "w", encoding="utf-8") as f:
    json.dump(vocabulary, f, ensure_ascii=False, indent=2)
