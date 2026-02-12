
import os
import json
import sys
from typing import List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich import print as rprint

try:
    import prompts
except ImportError:
    rprint("[bold red]Error:[/bold red] prompts.py not found. Please ensure it is in the same directory.")
    sys.exit(1)

console = Console()

# --- Pydantic Models for Validation ---

class CriterionScore(BaseModel):
    score: int
    reason: str

class CriteriaScores(BaseModel):
    task_management: CriterionScore
    communicative_design: CriterionScore
    formal_correctness: CriterionScore

class Correction(BaseModel):
    original: str
    correction: str
    type: str # Grammar, Vocabulary, etc.
    explanation: str

class GradingResult(BaseModel):
    criteria_scores: CriteriaScores
    total_score_explanation: str
    total_score: float
    corrections: List[Correction]
    general_feedback: str
    improved_version: str

# --- Main Logic ---

def get_api_key():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        rprint("[bold yellow]OPENAI_API_KEY not found in environment variables.[/bold yellow]")
        api_key = Prompt.ask("Please enter your OpenAI API Key", password=True)
    return api_key

def grade_text(client: OpenAI, text: str, level: str) -> GradingResult:
    system_prompt = prompts.get_system_prompt(level)
    rubric = prompts.get_rubric(level)
    
    user_message = f"""
Here is the student's text for a {level} exam.
Target Level: {level}
Rubric:
{rubric}

Student Text:
\"\"\"
{text}
\"\"\"

Grade this text specifically according to the provided rubric. Return ONLY valid JSON.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Or gpt-3.5-turbo if preferred/cheaper
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from API")
            
        data = json.loads(content)
        return GradingResult(**data)

    except Exception as e:
        rprint(f"[bold red]Error during grading:[/bold red] {e}")
        sys.exit(1)

def display_results(result: GradingResult, level: str):
    rprint(Panel.fit(f"[bold blue]Grading Results ({level})[/bold blue]", border_style="blue"))

    # 1. Scores Table
    table = Table(title="Detailed Scores")
    table.add_column("Criterion", style="cyan", no_wrap=True)
    table.add_column("Score", style="magenta")
    table.add_column("Reason", style="green")

    c = result.criteria_scores
    table.add_row("Task Management", str(c.task_management.score), c.task_management.reason)
    table.add_row("Communicative Design", str(c.communicative_design.score), c.communicative_design.reason)
    table.add_row("Formal Correctness", str(c.formal_correctness.score), c.formal_correctness.reason)
    
    console.print(table)
    rprint(f"[bold]Total Score:[/bold] {result.total_score} / 45")
    rprint(f"[italic]{result.total_score_explanation}[/italic]\n")

    # 2. General Feedback
    rprint(Panel(result.general_feedback, title="General Feedback", border_style="yellow"))

    # 3. Corrections
    if result.corrections:
        rprint("\n[bold]Corrections & Improvements:[/bold]")
        for corr in result.corrections:
            rprint(f"- [red]Original:[/red] '{corr.original}'")
            rprint(f"  [green]Correction:[/green] '{corr.correction}'")
            rprint(f"  [blue]Type:[/blue] {corr.type}")
            rprint(f"  [yellow]Explanation:[/yellow] {corr.explanation}")
            rprint("")

    # 4. Improved Version
    rprint(Panel(result.improved_version, title="Improved Version (Model Answer)", border_style="green"))


def main():
    rprint("[bold green]Welcome to the German Text Grader (telc Style)[/bold green]")
    
    api_key = get_api_key()
    client = OpenAI(api_key=api_key)

    level = Prompt.ask("Select Target Level", choices=["B1", "B2"], default="B1")
    
    rprint("\n[bold]Enter the text to grade (Press Ctrl+Z then Enter on Windows or Ctrl+D on Mac/Linux to finish):[/bold]")
    # Read multiline input
    text_lines = sys.stdin.readlines()
    text = "".join(text_lines).strip()
    
    if not text:
        rprint("[bold red]No text entered. Exiting.[/bold red]")
        sys.exit(0)

    with console.status("[bold green]Grading... Please wait...[/bold green]"):
        result = grade_text(client, text, level)
    
    display_results(result, level)

if __name__ == "__main__":
    main()
