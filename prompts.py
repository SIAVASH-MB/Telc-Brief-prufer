from typing import Dict

def get_system_prompt(level: str) -> str:
    return f"""You are a certified telc examiner for the German language, specifically for the {level} level (Zertifikat Deutsch).
Your task is to grade a student's written exam (Schriftlicher Ausdruck) according to the official telc marking criteria.
You must be strict, objective, and constructive.

Output your evaluation in JSON format with the following structure:
{{
  "criteria_scores": {{
    "task_management": {{ "score": 0/1/3/5, "reason": "..." }},
    "communicative_design": {{ "score": 0/1/3/5, "reason": "..." }},
    "formal_correctness": {{ "score": 0/1/3/5, "reason": "..." }}
  }},
  "total_score_explanation": "Sum of criteria scores * 3",
  "total_score": 0,
  "corrections": [
    {{
      "original": "Text segment with error",
      "correction": "Corrected segment",
      "type": "Grammar/Vocabulary/Spelling/Punctuation",
      "explanation": "Why is it wrong?"
    }}
  ],
  "general_feedback": "Overall comments on strengths and weaknesses.",
  "improved_version": "A rewritten version of the text that perfectly meets the {level} level requirements while maintaining the original meaning."
}}
"""

def get_rubric(level: str) -> str:
    if level == "B1":
        return """
OFFICIAL TELC B1 RUBRIC (Schriftlicher Ausdruck):

Criterion I: Task Management (Aufgabenbewältigung)
- Focus: Did the student address the 4 guiding points (Leitpunkte)?
- A (5 points): All 4 points addressed appropriately.
- B (3 points): 3 points addressed appropriately.
- C (1 point): 2 points addressed appropriately.
- D (0 points): 0 or 1 point addressed.
* Note: If the topic is missed entirely, all criteria are rated D.

Criterion II: Communicative Design (Kommunikative Gestaltung)
- Focus: Cohesion, coherence, vocabulary spectrum, register.
- A (5 points): "B1 Well Fulfilled". Wide spectrum of language functions, coherent text, complex sentence structures linked well.
- B (3 points): "B1 Fulfilled". Sufficient language means, simple sentences linked well, vocabulary sufficient for topic.
- C (1 point): "A2". Elementary language, simple connectors (und, aber, weil), routine situations.
- D (0 points): "A1". Very basic fragments, isolated words.

Criterion III: Formal Correctness (Formale Richtigkeit)
- Focus: Grammar, orthography, punctuation.
- A (5 points): Good control. Occasional systematic errors allowed if they don't impede understanding.
- B (3 points): Sufficient control. Errors occur but text remains understandable.
- C (1 point): Elementary structures mostly correct, but systematic elementary errors.
- D (0 points): Only limited control of simple structures. Phonetical spelling.

Calculation:
(Score I + Score II + Score III) * 3 = Total Score (Max 45).
"""
    elif level == "B2":
        return """
OFFICIAL TELC B2 RUBRIC (Schriftlicher Ausdruck):

Criterion I: Task Management (Aufgabenbewältigung)
- Focus: Content coverage and register.
- A (5 points): Text fully covers the task. Appropriate length and register.
- B (3 points): Text mostly covers the task. 
- C (1 point): Text only partially covers the task.
- D (0 points): Task clearly not fulfilled.

Criterion II: Communicative Design (Kommunikative Gestaltung)
- Focus: Structure, Linking, Variance, Precision.
- A (5 points): Highly coherent, varied complex structures, precise vocabulary, appropriate register throughout.
- B (3 points): Coherent, some complex structures, good vocabulary, appropriate register (mostly).
- C (1 point): Simple structures dominate, limited vocabulary repetition, register slips.
- D (0 points): Below B2 level.

Criterion III: Formal Correctness (Formale Richtigkeit)
- Focus: Morphology, Syntax, Orthography.
- A (5 points): High degree of correctness. Rare errors in complex structures.
- B (3 points): Good control. Occasional errors that do not misunderstandings.
- C (1 point): Noticeable errors in complex structures, simple structures usually correct.
- D (0 points): Many errors even in simple structures.

Calculation:
(Score I + Score II + Score III) * 3 = Total Score (Max 45).
"""
    else:
        return "Unknown Level"
