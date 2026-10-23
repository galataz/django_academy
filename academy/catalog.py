import json
from pathlib import Path
ROOT = Path(__file__).parent
LESSONS = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
UNITS = json.loads((ROOT / 'units.json').read_text(encoding='utf-8'))
NARRATIVE = json.loads((ROOT / 'narrative.json').read_text(encoding='utf-8'))
VISUALS = json.loads((ROOT / 'visuals.json').read_text(encoding='utf-8'))
LESSONS.sort(key=lambda lesson: lesson.get('order', lesson['id']))
for position, lesson in enumerate(LESSONS, 1):
    lesson['position'] = position
    lesson['narrative'] = NARRATIVE['scenes'][str(lesson['id'])]
    lesson['visual'] = dict(VISUALS[str(lesson['id'])])
    lesson['visual']['illustration'] = f"cards/lesson-{lesson['id']:02}.webp"
    lesson['visual_template'] = f"academy/visual_maps/map_{lesson['id']}.html"
for unit in UNITS:
    unit['illustration'] = f"cards/unit-{unit['id']:02}.webp"

def get_lesson(pk):
    return next((lesson for lesson in LESSONS if lesson['id'] == pk), None)

STORY = json.loads((ROOT / "story.json").read_text(encoding="utf-8"))
for chapter in STORY:
    chapter["topics"] = [get_lesson(pk) for pk in chapter["lessons"]]
