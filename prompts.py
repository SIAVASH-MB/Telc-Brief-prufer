from typing import Dict


B1_TOPICS = [
    {
        "id": 1,
        "subject": "Einladung zur Geburtstagsparty",
        "description": "Sie haben bald Geburtstag und möchten eine Party feiern. Schreiben Sie eine Einladung an Ihre Freunde.",
        "points": [
            "Grund für das Schreiben",
            "Wann und wo die Party ist",
            "Bitte um Antwort (Zu-/Absage)",
            "Was die Gäste mitbringen sollen (Essen/Getränke)"
        ]
    },
    {
        "id": 2,
        "subject": "Entschuldigung für den Kurs",
        "description": "Sie können nächste Woche nicht in den Deutschkurs kommen. Schreiben Sie eine E-Mail an Ihre Lehrerin, Frau Müller.",
        "points": [
            "Grund für Ihr Fehlen",
            "Entschuldigung",
            "Frage nach den Hausaufgaben",
            "Wann Sie wieder kommen"
        ]
    },
    {
        "id": 3,
        "subject": "Antwort auf eine Wohnungsanzeige",
        "description": "Sie haben eine interessante Wohnungsanzeige in der Zeitung gelesen. Schreiben Sie eine E-Mail an den Vermieter, Herrn Schneider.",
        "points": [
            "Grund für das Schreiben",
            "Informationen über sich selbst (Alter, Beruf, etc.)",
            "Frage nach einem Besichtigungstermin",
            "Frage nach den Nebenkosten"
        ]
    },
    {
        "id": 4,
        "subject": "Beschwerde über den Urlaub",
        "description": "Sie waren im Urlaub in einem Hotel, aber Sie waren nicht zufrieden. Schreiben Sie einen Beschwerdebrief an den Reiseveranstalter 'Sonne & Meer'.",
        "points": [
            "Grund für das Schreiben",
            "Was im Hotel nicht gut war (Essen, Zimmer, Lautstärke)",
            "Ihre Enttäuschung ausdrücken",
            "Forderung nach einer Entschädigung"
        ]
    }
]

def get_system_prompt(level: str, topic: Dict = None) -> str:
    topic_instruction = ""
    if topic:
        topic_instruction = f"""
IMPORTANT: You must grade the text based on its RATIONAL CONNECTION to the following topic:
Subject: {topic['subject']}
Description: {topic['description']}
Required Points (Leitpunkte):
1. {topic['points'][0]}
2. {topic['points'][1]}
3. {topic['points'][2]}
4. {topic['points'][3]}

Task Management Score (Criterion I) MUST strictly reflect whether these 4 specific points were addressed. 
If the text is about a completely different topic, Criterion I must be 0 (D).
"""

    return f"""You are a certified telc examiner for the German language, specifically for the {level} level (Zertifikat Deutsch).
Your task is to grade a student's written exam (Schriftlicher Ausdruck) according to the official telc marking criteria.
You must be strict, objective, and constructive.
{topic_instruction}

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
