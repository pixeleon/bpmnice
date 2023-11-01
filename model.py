from dataclasses import dataclass
from typing import List


@dataclass
class LabelScore:
    label: str
    score: int


@dataclass
class AnalysisResultDto:
    filename: str
    score: float
    total_tasks: int
    invalid_tasks: int
    labels_score: List[LabelScore]
