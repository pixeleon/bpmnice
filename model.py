from dataclasses import dataclass


@dataclass
class AnalysisResultDto:
    filename: str
    score: float
    total_tasks: int
    invalid_tasks: int
    labels: [str] = None