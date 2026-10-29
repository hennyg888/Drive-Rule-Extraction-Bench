"""Prompts: one folder in prompts/ per prompt.

    prompts/<name>/system.md     the system prompt: what the task is for, what to extract, how to cite
    prompts/<name>/task.md       the request placed after the handbook pages, at the end of the user
                                 message (optional)
    prompts/<name>/schema.json   the JSON schema the answer must follow (optional); Claude and vLLM
                                 enforce it, other servers may only be asked for it

The user message is: table of contents, handbook pages (with images), then task.md. Long documents
go first and the request last, which is the order models handle best.
"""
import hashlib
import json
import os
from dataclasses import dataclass

from .handbooks import ROOT

PROMPTS = os.path.join(ROOT, "prompts")
DEFAULT = "extract-rules"


@dataclass(frozen=True)
class Prompt:
    name: str
    folder: str
    system: str
    task: str = ""
    schema: dict = None

    @property
    def sha256(self):
        """One hash of the three files together, to tell prompt versions apart in runs."""
        h = hashlib.sha256()
        for part in (self.system, self.task, json.dumps(self.schema, sort_keys=True) if self.schema else ""):
            h.update(part.encode() + b"\0")
        return h.hexdigest()


def load(name=DEFAULT):
    """The prompt in prompts/<name>/, or in a folder given by its path."""
    folder = name if os.path.isdir(name) else os.path.join(PROMPTS, name)
    if not os.path.exists(os.path.join(folder, "system.md")):
        found = sorted(d for d in os.listdir(PROMPTS) if os.path.isdir(os.path.join(PROMPTS, d)))
        raise SystemExit(f"no prompt {name!r}: a prompt is a folder with system.md; prompts/ has {', '.join(found)}")

    def read(f):
        path = os.path.join(folder, f)
        return open(path, encoding="utf-8").read().strip() if os.path.exists(path) else ""

    schema = read("schema.json")
    return Prompt(os.path.basename(os.path.normpath(folder)), folder, read("system.md"), read("task.md"),
                  json.loads(schema) if schema else None)
