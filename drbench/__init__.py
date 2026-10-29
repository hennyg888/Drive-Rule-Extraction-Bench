"""drbench: the Drive-Rule-Extraction-Bench toolkit.

Modules, in the order data flows through them:
    handbooks   the offline handbooks in handbooks/<id>/ (the source of truth)
    stats       text and image statistics of the handbooks
    sentences   sentence boundaries, and wrapping sentences in <span id>
    corpus      handbooks -> corpus/<id>/: clean HTML with an id on every block and sentence
    screening   places in the corpus a person should check
    messages    corpus -> the content of a chat message (HTML text with the images in place)
    models      calling a model: one interface, presets in configs/models.yaml (local vLLM, OpenRouter)
    run         one extraction run: build the message, call the model, save everything
    grounding   a model's citation (block id + quoted sentence) -> sentence ids in the corpus

Command line: `drbench --help` (or `python -m drbench --help`).
"""
