"""What every model provider has in common: one call, one response.

A model is called with the content of one user message (a string, or the parts made by
messages.py), an optional system prompt and an optional JSON schema the answer must follow. It
returns a ModelResponse. Providers differ only in how they send the request.
"""
from dataclasses import dataclass, field


class ModelError(Exception):
    """A call failed in a way retrying will not fix (bad key, unknown model, bad request), or
    failed again after the client's own retries."""


@dataclass
class ModelResponse:
    text: str                       # the answer (the JSON text, when a schema was given)
    reasoning: str = ""             # the model's reasoning, when the API returns it
    stop_reason: str = ""           # why it stopped: end_turn / stop, max_tokens / length, refusal, ...
    model: str = ""                 # the model that answered, as the API reports it
    usage: dict = field(default_factory=dict)   # token counts as the API reports them
    input_tokens: int = 0
    output_tokens: int = 0          # including reasoning
    reasoning_tokens: int = 0
    seconds: float = 0.0
    request_id: str = ""
    raw: dict = field(default_factory=dict)     # the whole API response


class ChatModel:
    """Base class of the providers. `name` is the preset name, `model` the id the API knows."""
    provider = ""

    def __init__(self, name, model, params=None, vision=True, price=None, **settings):
        self.name = name
        self.model = model
        self.params = dict(params or {})
        self.vision = vision
        self.price = price          # (input, output) in USD per million tokens, for estimates
        self.settings = settings    # base_url, api_key_env, timeout, max_retries, ...

    def complete(self, content, system=None, json_schema=None):
        """Send one user message and return a ModelResponse."""
        raise NotImplementedError

    def cost(self, response):
        """Estimated cost in USD of a response, from the preset's price; None without a price."""
        if not self.price:
            return None
        return round((response.input_tokens * self.price[0] + response.output_tokens * self.price[1]) / 1e6, 4)

    def _check(self, content):
        if isinstance(content, str):
            return [{"type": "text", "text": content}]
        if not self.vision and any(p["type"] == "image" for p in content):
            raise ModelError(f"{self.name} does not take images; build the message with images=False")
        return content

    def describe(self):
        return {"preset": self.name, "provider": self.provider, "model": self.model, "params": self.params,
                "vision": self.vision, "price_per_million": self.price,
                **{k: v for k, v in self.settings.items() if k in ("base_url", "api_key_env")}}
