"""drbench: the Drive-Rule-Extraction-Bench toolkit.

Modules, in the order data flows through them:
    handbooks   the offline handbooks in handbooks/<id>/ (the source of truth)
    stats       text and image statistics of the handbooks
    sentences   sentence boundaries, and wrapping sentences in <span id>
    corpus      handbooks -> corpus/<id>/: clean HTML with an id on every block and sentence
    screening   places in the corpus a person should check

The program that uses them is build_corpus.py, at the top level of the repository. The extraction
pipeline (messages, models, runs, grounding) is on the branch extraction-pipeline.
"""
