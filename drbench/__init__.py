"""drbench: the Drive-Rule-Extraction-Bench toolkit.

Modules, in the order data flows through them:
    handbooks   the offline handbooks in handbooks/<id>/ (the source of truth)
    stats       text and image statistics of the handbooks
    sentences   sentence boundaries, and wrapping sentences in <span id>
    corpus      handbooks -> corpus/<id>/: clean HTML with an id on every block and sentence
    screening   places in the corpus a person should check
    prompts     the prompt folders in prompts/ (system.md, task.md, schema.json)
    messages    corpus -> the user message (HTML text with the images in place, then the task)
    models      calling a model: one interface, presets in models.yaml (Anthropic API, local vLLM, OpenRouter)
    run         one extraction run: build the message, call the model, save everything
    grounding   a model's citation (block id + quoted sentence) -> sentence ids in the corpus

The programs that use these modules are at the top level of the repository: build_corpus.py,
build_messages.py, run_extraction.py, models.py.
"""
