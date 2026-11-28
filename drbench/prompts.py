"""Prompts: one folder in prompts/ per prompt.

    prompts/<name>/system.md     the system prompt: what the task is for, what to extract, how to cite
    prompts/<name>/task.md       the request placed after the handbook pages, at the end of the user
                                 message (optional)
    prompts/<name>/schema.json   the JSON schema the answer must follow (optional); Claude and vLLM
                                 enforce it, other servers may only be asked for it
    prompts/<name>/options.yaml  how the corpus is sent with this prompt (optional). Keys:
                                 figures: false   remove every <figure> (image, alt text, caption)

The user message is: table of contents, handbook pages (with images), then task.md. Long documents
go first and the request last, which is the order models handle best.

task.md may hold placeholders, filled in by load():
    {{topic}}       the topic sentence, from TOPICS (load(topic="overtaking"))
    {{situations}}  the topic's situations, for the closed-book final check, from TOPICS
    {{region}}      the region, from REGIONS (load(region="mto")). A prompt with {{region}} is a
                    closed-book prompt: no handbook pages are sent, only task.md.
"""
import hashlib
import json
import os
from dataclasses import dataclass

import yaml

from .handbooks import ROOT

PROMPTS = os.path.join(ROOT, "prompts")
DEFAULT = "formal-rules"

# --topic choices: the words that fill {{topic}} ("Topic: ... only.") and {{situations}}.
TOPICS = {
    "overtaking": {
        "topic": "overtaking (passing another vehicle, and being passed)",
        "situations": "where passing is and is not allowed, how to pass, passing particular road users, "
                      "being passed",
    },
    "turning": {
        "topic": "turning (right turns, left turns and U-turns, at intersections and elsewhere)",
        "situations": "where and when turns are and are not allowed, lane position and signalling, turn "
                      "lanes and markings, yielding while turning, U-turns, turning near particular road users",
    },
    "parking": {
        "topic": "parking (parking, stopping and standing a vehicle, and where each is not allowed)",
        "situations": "where parking, stopping and standing are and are not allowed, distances from "
                      "hydrants, crossings and intersections, parking on hills and roadsides, curb "
                      "markings and signs, leaving a parked vehicle",
    },
}

# --region choices (closed-book prompts only): the words that fill {{region}}. Same ids as corpus/.
REGIONS = {
    "ca": "California, United States",
    "tx": "Texas, United States",
    "mto": "Ontario, Canada",
}


@dataclass(frozen=True)
class Prompt:
    name: str
    folder: str
    system: str
    task: str = ""
    schema: dict = None
    topic: str = None
    region: str = None
    closed_book: bool = False       # task.md had {{region}}: send task.md alone, no handbook pages
    figures: bool = True            # options.yaml figures: false: send the pages with every <figure> removed

    @property
    def sha256(self):
        """One hash of the three files together, to tell prompt versions apart in runs."""
        h = hashlib.sha256()
        for part in (self.system, self.task, json.dumps(self.schema, sort_keys=True) if self.schema else ""):
            h.update(part.encode() + b"\0")
        return h.hexdigest()


def fill(name, task, topic=None, region=None):
    """task.md with its placeholders filled. A topic or region is an error if the prompt has no
    place for it, and a missing one is an error if it does."""
    for key, value, choices, flag in (("topic", topic, TOPICS, "--topic"), ("region", region, REGIONS, "--region")):
        has = "{{" + key + "}}" in task
        if value is not None and value not in choices:
            raise SystemExit(f"unknown {key} {value!r}; choose from {', '.join(choices)}")
        if has and value is None:
            raise SystemExit(f"prompt {name!r} needs a {key} ({flag} {'|'.join(choices)})")
        if value is not None and not has:
            raise SystemExit(f"prompt {name!r} takes no {key} ({flag} {value})")
    if topic is not None:
        task = task.replace("{{topic}}", TOPICS[topic]["topic"]).replace("{{situations}}", TOPICS[topic]["situations"])
    if region is not None:
        task = task.replace("{{region}}", REGIONS[region])
    return task


def folder_of(name):
    return name if os.path.isdir(name) else os.path.join(PROMPTS, name)


def takes(name, key):
    """Whether the prompt's task.md has a {{key}} placeholder ("topic" or "region")."""
    path = os.path.join(folder_of(name), "task.md")
    return os.path.exists(path) and "{{" + key + "}}" in open(path, encoding="utf-8").read()


def load(name=DEFAULT, topic=None, region=None):
    """The prompt in prompts/<name>/, or in a folder given by its path, with task.md's {{topic}} and
    {{region}} filled in (keys of TOPICS and REGIONS)."""
    folder = folder_of(name)
    if not os.path.exists(os.path.join(folder, "system.md")):
        found = sorted(d for d in os.listdir(PROMPTS) if os.path.isdir(os.path.join(PROMPTS, d)))
        raise SystemExit(f"no prompt {name!r}: a prompt is a folder with system.md; prompts/ has {', '.join(found)}")

    def read(f):
        path = os.path.join(folder, f)
        return open(path, encoding="utf-8").read().strip() if os.path.exists(path) else ""

    schema = read("schema.json")
    pname, task = os.path.basename(os.path.normpath(folder)), read("task.md")
    options = yaml.safe_load(read("options.yaml")) or {}
    unknown = set(options) - {"figures"}
    if unknown:
        raise SystemExit(f"prompt {pname!r}: unknown option(s) in options.yaml: {', '.join(sorted(unknown))}")
    return Prompt(pname, folder, read("system.md"), fill(pname, task, topic, region),
                  json.loads(schema) if schema else None, topic, region, "{{region}}" in task,
                  bool(options.get("figures", True)))
