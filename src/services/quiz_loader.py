import json
from pathlib import Path
from typing import List, Dict, Any

def load_questions(path: str = "data/questions.json") -> List[Dict[str, Any]]:
    fp = Path(path)
    data = json.loads(fp.read_text(encoding="utf-8"))
    # валидация на всякий случай
    for i, q in enumerate(data):
        assert "question" in q and "options" in q and "correct_option" in q, f"Bad question #{i}"
    return data