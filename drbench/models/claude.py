"""Claude through the Anthropic API (the official `anthropic` SDK).

Credentials: ANTHROPIC_API_KEY (from the environment or .env), or a login made with
`ant auth login`, which the SDK finds by itself.

Params (in configs/models.yaml or --set):
    max_tokens        output limit (default 64000; requests are streamed, so large values are fine)
    effort            low | medium | high | xhigh | max: how much the model thinks
    thinking_display  summarized (default: a summary of the reasoning is returned and saved) | omitted
    fallbacks         "default": if Claude's safety classifiers decline the request, the API reruns it
                      on a fallback model chosen by Anthropic (Opus and Sonnet only)
    cache             true: cache the prompt, so a second run on the same pages reads it at a tenth of
                      the price (the first run pays 1.25 times for writing it)
"""
import time

import anthropic

from .base import ChatModel, ModelError, ModelResponse

FALLBACK_BETA = "server-side-fallback-2026-07-01"


def to_blocks(parts):
    out = []
    for p in parts:
        if p["type"] == "text":
            out.append({"type": "text", "text": p["text"]})
        else:
            out.append({"type": "image", "source": {"type": "base64", "media_type": p["media_type"], "data": p["data"]}})
    return out


class ClaudeModel(ChatModel):
    provider = "anthropic"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._client = None

    @property
    def client(self):
        if self._client is None:
            opts = {"max_retries": self.settings.get("max_retries", 2), "timeout": self.settings.get("timeout", 3600)}
            if self.settings.get("base_url"):
                opts["base_url"] = self.settings["base_url"]
            self._client = anthropic.Anthropic(**opts)
        return self._client

    def request(self, content, system=None, json_schema=None):
        """The keyword arguments of the request (without the beta options)."""
        p = self.params
        kw = {"model": self.model, "max_tokens": p.get("max_tokens", 64000),
              "messages": [{"role": "user", "content": to_blocks(self._check(content))}],
              "thinking": {"type": "adaptive", "display": p.get("thinking_display", "summarized")}}
        if system:
            kw["system"] = system
        output_config = {}
        if p.get("effort"):
            output_config["effort"] = p["effort"]
        if json_schema:
            output_config["format"] = {"type": "json_schema", "schema": json_schema}
        if output_config:
            kw["output_config"] = output_config
        if p.get("cache"):
            kw["cache_control"] = {"type": "ephemeral"}
        return kw

    def count_tokens(self, content, system=None):
        """Input tokens of a request, counted by the API (free)."""
        kw = self.request(content, system)
        args = {k: kw[k] for k in ("model", "messages", "system", "thinking") if k in kw}
        return self.client.messages.count_tokens(**args).input_tokens

    def complete(self, content, system=None, json_schema=None):
        kw = self.request(content, system, json_schema)
        start = time.time()
        try:
            if self.params.get("fallbacks"):
                stream = self.client.beta.messages.stream(**kw, betas=[FALLBACK_BETA], fallbacks=self.params["fallbacks"])
            else:
                stream = self.client.messages.stream(**kw)
            with stream as s:
                msg = s.get_final_message()
                request_id = s.request_id or ""
        except anthropic.AuthenticationError as e:
            raise ModelError(f"{self.name}: the API key was not accepted. Set ANTHROPIC_API_KEY in .env "
                             "or run `ant auth login`.") from e
        except anthropic.PermissionDeniedError as e:
            raise ModelError(f"{self.name}: this key may not use {self.model}: {e.message}") from e
        except anthropic.NotFoundError as e:
            raise ModelError(f"{self.name}: unknown model {self.model}: {e.message}") from e
        except anthropic.BadRequestError as e:
            raise ModelError(f"{self.name}: the request was refused: {e.message}") from e
        except anthropic.RateLimitError as e:
            raise ModelError(f"{self.name}: rate limited, also after retries: {e.message}") from e
        except anthropic.APIStatusError as e:
            raise ModelError(f"{self.name}: API error {e.status_code}: {e.message}") from e
        except anthropic.APIConnectionError as e:
            raise ModelError(f"{self.name}: cannot reach the Anthropic API: {e}") from e
        raw = msg.to_dict()
        usage = raw.get("usage") or {}
        return ModelResponse(
            text="".join(b.text for b in msg.content if b.type == "text"),
            reasoning="\n\n".join(b.thinking for b in msg.content if b.type == "thinking" and b.thinking),
            stop_reason=msg.stop_reason or "",
            model=msg.model,
            usage=usage,
            input_tokens=(usage.get("input_tokens") or 0) + (usage.get("cache_creation_input_tokens") or 0)
            + (usage.get("cache_read_input_tokens") or 0),
            output_tokens=usage.get("output_tokens") or 0,
            reasoning_tokens=(usage.get("output_tokens_details") or {}).get("thinking_tokens") or 0,
            seconds=round(time.time() - start, 1),
            request_id=request_id,
            raw=raw,
        )
