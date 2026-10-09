"""Site wording rules. Vivek: never say 'job'/'jobs' on the website (it reads as 'AI is taking jobs').
soften() rewrites user-visible text to 'task'/'workflow'; build.py applies it to every built file and fails if any remain."""
import re

PHRASES = [
    ("Start giving it jobs.", "Start giving it tasks."),
    ("Your job in one breath", "Your task in one breath"),
    ("Pick a job.", "Pick a task."), ("Pick the job", "Pick the task"), ("1 · The job", "1 · The task"),
    ("grouped by Medical Affairs job", "grouped by Medical Affairs workflow"),
    (", by job<", ", by workflow<"), (" by job;", " by workflow;"), (" by job)", " by workflow)"),
    ("Workflows — the jobs", "Workflows — the core tasks"),
    ("recurring Medical Affairs job", "recurring Medical Affairs workflow"),
    ("for one Medical Affairs job", "for one Medical Affairs task"),
    ("Ready-made jobs", "Ready-made tasks"),
    ("one skill doing one job", "one skill doing one task"),
    ("One skill does the job.", "One skill handles the whole task."),
    ("does the core job", "does the core task"),
    ("handed a job", "handed a task"),
    ("when the job reaches them", "when the task reaches them"),
    ("grouped by the job it serves", "grouped by the workflow it serves"),
    ("one-line job", "one-line purpose"),
    ("large jobs on weekends", "large batch runs on weekends"),
    ("skill-backed job", "skill-backed task"),
    ("does one job well", "does one task well"),
    ("the job and the standard", "the task and the standard"),
]
WORD = re.compile(r"(?<![/_\-.=#@\w])(jobs?|Jobs?|JOBS?)(?![\w/_\-=(])")
SAME = {"job": "task", "jobs": "tasks", "Job": "Task", "Jobs": "Tasks", "JOB": "TASK", "JOBS": "TASKS"}


def soften(text):
    for a, b in PHRASES:
        text = text.replace(a, b)
    return WORD.sub(lambda m: SAME[m.group(1)], text)


def remaining(text):
    return re.findall(r".{0,40}\bjobs?\b.{0,40}", text, flags=re.I)
