"""Any server that speaks the OpenAI chat-completions API: a local vLLM server, or OpenRouter
(which serves Qwen, Gemini, GPT, Claude and others behind one key).

Settings (in configs/models.yaml): base_url, api_key_env (the environment variable holding the key;
none for a local server), timeout (seconds, default 3600), max_retries (default 2).

Params are sent as they are (max_tokens, temperature, top_p, seed, reasoning_effort, ...), except
extra_body, whose keys are added to the request body for options only that server knows: for vLLM
{"chat_template_kwargs": {"enable_thinking": false}} turns Qwen's thinking off; for OpenRouter
{"reasoning": {"effort": "high"}} or {"provider": {"order": [...]}}.
"""
import os
import time

import openai

from .base import ChatModel, ModelError, ModelResponse


def to_openai(parts):
    out = []
    for p in parts:
        if p["type"] == "text":
            out.append({"type": "text", "text": p["text"]})
        else:
            out.append({"type": "image_url", "image_url": {"url": f"data:{p['media_type']};base64,{p['data']}"}})
    return out


class OpenAICompatibleModel(ChatModel):
    provider = "openai"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._client = None

    @property
    def client(self):
        if self._client is None:
            env = self.settings.get("api_key_env")
            key = os.environ.get(env) if env else "none"
            if not key:
                raise ModelError(f"{self.name}: set {env} (in the environment or in .env)")
            self._client = openai.OpenAI(base_url=self.settings["base_url"], api_key=key,
                                         timeout=self.settings.get("timeout", 3600),
                                         max_retries=self.settings.get("max_retries", 2))
        return self._client

    def request(self, content, system=None, json_schema=None):
        messages = ([{"role": "system", "content": system}] if system else []) + \
                   [{"role": "user", "content": to_openai(self._check(content))}]
        kw = {"model": self.model, "messages": messages, **self.params}
        if json_schema:
            kw["response_format"] = {"type": "json_schema",
                                     "json_schema": {"name": "answer", "schema": json_schema, "strict": True}}
        return kw

    def complete(self, content, system=None, json_schema=None):
        kw = self.request(content, system, json_schema)
        start = time.time()
        try:
            resp = self.client.chat.completions.create(**kw)
        except openai.AuthenticationError as e:
            raise ModelError(f"{self.name}: the API key was not accepted ({self.settings.get('api_key_env')})") from e
        except openai.NotFoundError as e:
            raise ModelError(f"{self.name}: unknown model {self.model} at {self.settings['base_url']}: {e.message}") from e
        except openai.BadRequestError as e:
            raise ModelError(f"{self.name}: the request was refused: {e.message}") from e
        except openai.RateLimitError as e:
            raise ModelError(f"{self.name}: rate limited, also after retries: {e.message}") from e
        except openai.APIStatusError as e:
            raise ModelError(f"{self.name}: API error {e.status_code}: {e.message}") from e
        except openai.APIConnectionError as e:
            raise ModelError(f"{self.name}: cannot reach {self.settings['base_url']} (is the server running?)") from e
        raw = resp.model_dump()
        choice = raw["choices"][0] if raw.get("choices") else {}
        msg = choice.get("message") or {}
        usage = raw.get("usage") or {}
        return ModelResponse(
            text=msg.get("content") or "",
            reasoning=msg.get("reasoning_content") or msg.get("reasoning") or "",   # vLLM / OpenRouter
            stop_reason=choice.get("finish_reason") or "",
            model=raw.get("model") or self.model,
            usage=usage,
            input_tokens=usage.get("prompt_tokens") or 0,
            output_tokens=usage.get("completion_tokens") or 0,
            reasoning_tokens=(usage.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0,
            seconds=round(time.time() - start, 1),
            request_id=raw.get("id") or "",
            raw=raw,
        )
