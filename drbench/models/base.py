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
    input_tokens: int = 0           # all input, including the cached parts below
    cache_write_tokens: int = 0     # of input_tokens: written to the prompt cache (billed at 1.25x)
    cache_read_tokens: int = 0      # of input_tokens: read from the prompt cache
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
        self.price = price          # (input, output[, cache read]) in USD per million tokens, for estimates
        self.settings = settings    # base_url, api_key_env, timeout, max_retries, ...

    def complete(self, content, system=None, json_schema=None):
        """Send one user message and return a ModelResponse."""
        raise NotImplementedError

    def cost(self, response):
        """Estimated cost in USD of a response, from the preset's price; None without a price.
        Cache writes cost 1.25x the input price; cache reads cost the price's third value, or 0.1x
        the input price when it has none."""
        if not self.price:
            return None
        inp, out = self.price[0], self.price[1]
        read = self.price[2] if len(self.price) > 2 else inp * 0.1
        w, r = response.cache_write_tokens, response.cache_read_tokens
        uncached = response.input_tokens - w - r
        return round((uncached * inp + w * inp * 1.25 + r * read + response.output_tokens * out) / 1e6, 4)

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
