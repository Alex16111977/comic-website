import json

# Показываем примеры проблемных подсказок
file_path = r"F:\AiKlientBank\KingLearComic\data\characters\king_lear.json"

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("[ПРИМЕРЫ ТЕКУЩИХ ПРОБЛЕМНЫХ ПОДСКАЗОК В king_lear.json]")
print("=" * 70)

count = 0
for phase in data.get("journey_phases", []):
    phase_name = phase.get("name", "")
    for vocab in phase.get("vocabulary", []):
        if vocab.get("russian_hint"):
            print(f"{vocab['german']:25} -> {vocab['russian_hint']}")
            count += 1
            if count >= 15:
                break
    if count >= 15:
        break

print("\n[ПРОБЛЕМА]: Все подсказки содержат названия фаз в скобках!")
print("[РЕШЕНИЕ]: Применить лингвистический словарь подсказок")
