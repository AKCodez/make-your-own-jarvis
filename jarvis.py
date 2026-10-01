"""J.A.R.V.I.S. - your own Iron Man assistant.

Claude is the brain (or a free OpenRouter model), Fish Audio is the voice, your browser is the HUD.
Start it with run.bat (Windows) or ./run.sh (Mac/Linux).
"""
from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    import anthropic
except ImportError:  # run.bat / run.sh install it; this catches a bare "python jarvis.py"
    print("\n  A package is missing. Start JARVIS with run.bat (Windows) or ./run.sh (Mac/Linux).\n")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"
INDEX_HTML = ROOT / "web" / "index.html"
PROTOCOLS_FILE = ROOT / "protocols.json"

FISH_TTS_URL = "https://api.fish.audio/v1/tts"
FISH_SIGNUP_URL = "https://ariacodez.ai/l/fish-audio"
CLAUDE_KEYS_URL = "https://console.anthropic.com/settings/keys"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_KEYS_URL = "https://openrouter.ai/keys"

DEFAULTS = {
    "FISH_VOICE_ID": "41f0953d7a6b4c078445c7e65d620eeb",  # "JARVIS" in the Fish Audio voice library
    "FISH_MODEL": "s2.1-pro",
    "JARVIS_MODEL": "claude-opus-5-5",
    "OPENROUTER_MODEL": "apodex/apodex-1.1-mini:free",  # the free brain, used with an OpenRouter key
    "JARVIS_CALLS_YOU": "sir",
    "PORT": "8765",
}

# Models that take output_config.effort ("low" keeps spoken replies quick).
EFFORT_MODELS = {
    "claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5", "claude-sonnet-5",
    "claude-fable-5-1", "claude-fable-5", "claude-opus-4-8", "claude-opus-4-7",
    "claude-opus-4-6", "claude-sonnet-4-6",
}
# Models that accept the server-side refusal fallback ("default" routing).
FALLBACK_MODELS = {"claude-fable-5-1", "claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5"}

NO_BROWSER = os.environ.get("JARVIS_NO_BROWSER") == "1"  # for testing: never open browser tabs


def log(message: str) -> None:
    print(f"  {time.strftime('%H:%M:%S')}  {message}", flush=True)


# ---------------------------------------------------------------- settings

def read_env_file() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_FILE.exists():
        for raw in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_settings() -> dict[str, str]:
    cfg = dict(DEFAULTS)
    cfg.update({k: v for k, v in read_env_file().items() if v})
    # Keys come from the .env file only, so a key another app left in the system environment
    # never gets used (or billed) by surprise. The other settings can be overridden for testing.
    for key in DEFAULTS:
        if os.environ.get(key):
            cfg[key] = os.environ[key].strip()
    return cfg


def which_brain(cfg: dict[str, str]) -> str:
    """ "claude", "openrouter", or "" when there's no brain key yet. Claude wins if both keys are set."""
    if cfg.get("ANTHROPIC_API_KEY"):
        return "claude"
    if cfg.get("OPENROUTER_API_KEY"):
        return "openrouter"
    return ""


def brain_label(cfg: dict[str, str]) -> tuple[str, str]:
    """(name, model) of the brain in use, for the banner and the HUD."""
    brain = which_brain(cfg)
    if brain == "openrouter":
        return "OpenRouter", cfg["OPENROUTER_MODEL"]
    return ("Claude", cfg["JARVIS_MODEL"]) if brain else ("", "")


def save_to_env(updates: dict[str, str]) -> None:
    if ENV_FILE.exists():
        template = ENV_FILE.read_text(encoding="utf-8-sig")
    elif ENV_EXAMPLE.exists():
        template = ENV_EXAMPLE.read_text(encoding="utf-8")
    else:
        template = ""
    lines = template.splitlines()
    written = set()
    for i, line in enumerate(lines):
        if "=" not in line or line.lstrip().startswith("#"):
            continue
        key = line.split("=", 1)[0].strip()
        if key in updates:
            lines[i] = f"{key}={updates[key]}"
            written.add(key)
    lines += [f"{key}={value}" for key, value in updates.items() if key not in written]
    ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ask(prompt: str) -> str:
    try:
        return input(prompt).strip().strip('"').strip("'")
    except EOFError:
        return ""


def first_run(cfg: dict[str, str]) -> dict[str, str]:
    """Ask for any missing key in the console and save it to .env."""
    need_voice = not cfg.get("FISH_API_KEY")
    need_brain = not which_brain(cfg)
    if not (need_voice or need_brain):
        return cfg
    print("\n  Welcome. JARVIS needs two keys, then he's yours.")
    print("  Paste each one and press Enter (right-click or Ctrl+V pastes).")
    updates: dict[str, str] = {}
    if need_voice:
        print("\n  1) THE VOICE - your Fish Audio API key")
        print(f"     Get it here: {FISH_SIGNUP_URL}  (profile > API Keys > Create)")
        key = ask("     Fish Audio key: ")
        if key:
            updates["FISH_API_KEY"] = key
    if need_brain:
        print("\n  2) THE BRAIN - a Claude API key, or a free OpenRouter key. Either one works.")
        print(f"     Claude:      {CLAUDE_KEYS_URL}  (Create Key, it starts with sk-ant-)")
        print(f"     Free option: {OPENROUTER_KEYS_URL}  (sign up and create a key, it starts with sk-or-)")
        key = ask("     Brain key: ")
        if key.startswith("sk-or-"):
            updates["OPENROUTER_API_KEY"] = key
        elif key:
            if not key.startswith("sk-ant-"):
                print("     That doesn't look like a Claude key (sk-ant-) or an OpenRouter key (sk-or-). Saving it as a Claude key.")
            updates["ANTHROPIC_API_KEY"] = key
    if updates:
        save_to_env(updates)
        print("\n  Saved to the .env file in this folder. You won't be asked again.")
    cfg = load_settings()
    still = [name for name, absent in (("the Fish Audio key", not cfg.get("FISH_API_KEY")), ("a brain key", not which_brain(cfg))) if absent]
    if still:
        print(f"\n  Still missing: {' and '.join(still)}. JARVIS will start, and tells you what's missing.")
    return cfg


# ---------------------------------------------------------------- brain (Claude, or a free OpenRouter model)

_history: list[dict] = []
_lock = threading.Lock()
_client: anthropic.Anthropic | None = None
_client_key = ""


def system_prompt(cfg: dict[str, str]) -> str:
    title = cfg["JARVIS_CALLS_YOU"]
    return (
        "You are J.A.R.V.I.S., the AI assistant from Iron Man, now running on the user's computer. "
        f'Address the user as "{title}". Be calm, precise, quietly witty and loyal. '
        "Everything you write is spoken aloud by a voice engine, so reply in one or two short "
        "sentences of plain spoken English. Never use markdown, lists, emojis, URLs, code, or "
        "anything in square brackets or asterisks. If asked to do something on the computer that "
        "you can't do from here, say so briefly and stay in character. "
        f"The local date and time is {time.strftime('%A, %B %d, %Y, %I:%M %p')}."
    )


def get_client(cfg: dict[str, str]) -> anthropic.Anthropic:
    global _client, _client_key
    key = cfg.get("ANTHROPIC_API_KEY", "")
    if _client is None or key != _client_key:
        _client = anthropic.Anthropic(api_key=key, timeout=60.0, max_retries=2)
        _client_key = key
    return _client


def ask_claude(cfg: dict[str, str], messages: list[dict]) -> str:
    model = cfg["JARVIS_MODEL"]
    params: dict = {"model": model, "max_tokens": 16000, "system": system_prompt(cfg), "messages": messages}
    if model in EFFORT_MODELS:
        params["output_config"] = {"effort": "low"}
    client = get_client(cfg)
    if model in FALLBACK_MODELS:
        # If the model declines a request, Anthropic re-runs it on a fallback model in the same call.
        response = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **params)
    else:
        response = client.messages.create(**params)
    if response.stop_reason == "refusal":
        return f"I'm afraid I can't help with that one, {cfg['JARVIS_CALLS_YOU']}."
    return " ".join(b.text for b in response.content if b.type == "text" and b.text)


class OpenRouterError(Exception):
    def __init__(self, status: int, detail: str) -> None:
        super().__init__(f"{status}: {detail}")
        self.status = status
        self.detail = detail


def openrouter_post(cfg: dict[str, str], payload: dict) -> dict:
    request = urllib.request.Request(OPENROUTER_URL, data=json.dumps(payload).encode("utf-8"), method="POST", headers={
        "Authorization": f"Bearer {cfg['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 - fixed https URL
            data = json.loads(response.read())
    except urllib.error.HTTPError as err:
        raise OpenRouterError(err.code, err.read()[:400].decode("utf-8", "replace")) from err
    except (urllib.error.URLError, TimeoutError) as err:
        raise OpenRouterError(0, str(err)) from err
    except json.JSONDecodeError as err:
        raise OpenRouterError(502, "unreadable reply") from err
    # OpenRouter reports some failures inside a 200 response.
    choices = data.get("choices") or [{}]
    problem = data.get("error") or choices[0].get("error")
    if isinstance(problem, dict):
        code = problem.get("code")
        raise OpenRouterError(code if isinstance(code, int) else 502, str(problem.get("message") or problem))
    return data


def ask_openrouter(cfg: dict[str, str], messages: list[dict]) -> str:
    payload = {
        "model": cfg["OPENROUTER_MODEL"],
        "messages": [{"role": "system", "content": system_prompt(cfg)}, *messages],
        "max_tokens": 4000,
        "reasoning": {"effort": "none"},  # skip the thinking step, so spoken replies come back fast
    }
    try:
        data = openrouter_post(cfg, payload)
    except OpenRouterError as err:
        if err.status != 400:
            raise
        del payload["reasoning"]  # some models can't switch their thinking off
        data = openrouter_post(cfg, payload)
    choices = data.get("choices") or [{}]
    content = (choices[0].get("message") or {}).get("content")
    return content if isinstance(content, str) else ""


def think(cfg: dict[str, str], text: str) -> str:
    with _lock:
        messages = list(_history) + [{"role": "user", "content": text}]
    reply = ask_openrouter(cfg, messages) if which_brain(cfg) == "openrouter" else ask_claude(cfg, messages)
    reply = " ".join(reply.split()) or f"I'm not sure what to say to that, {cfg['JARVIS_CALLS_YOU']}."
    with _lock:
        _history.extend([{"role": "user", "content": text}, {"role": "assistant", "content": reply}])
        del _history[:-16]  # keep the last 8 exchanges
    return reply


def brain_error(err: Exception, cfg: dict[str, str]) -> str:
    title = cfg["JARVIS_CALLS_YOU"]
    if isinstance(err, anthropic.AuthenticationError):
        return f"My brain key isn't working, {title}. Check ANTHROPIC_API_KEY in the .env file."
    if isinstance(err, anthropic.PermissionDeniedError):
        return f"My Claude key isn't allowed to use that model, {title}."
    if isinstance(err, anthropic.NotFoundError):
        return f"I can't find the model {cfg['JARVIS_MODEL']}, {title}. Check JARVIS_MODEL in the .env file."
    if isinstance(err, anthropic.RateLimitError):
        return f"I'm being rate limited, {title}. Give me a moment and try again."
    if isinstance(err, anthropic.BadRequestError):
        detail = str(getattr(err, "message", err)).lower()
        if "credit" in detail or "billing" in detail:
            return f"Your Claude account is out of credit, {title}. Add some at console.anthropic.com."
        return f"Claude rejected that request, {title}. The details are in the JARVIS window."
    if isinstance(err, anthropic.APIConnectionError):
        return f"I can't reach my brain, {title}. Check your internet connection."
    return f"Claude is having a moment, {title}. Try again shortly."


def openrouter_error(err: OpenRouterError, cfg: dict[str, str]) -> str:
    title = cfg["JARVIS_CALLS_YOU"]
    if err.status == 401:
        return f"My brain key isn't working, {title}. Check OPENROUTER_API_KEY in the .env file."
    if err.status == 402:
        return f"Your OpenRouter account is out of credit, {title}. Check it at openrouter.ai."
    if err.status == 429:
        if "per-day" in err.detail:
            return f"I've used up today's free questions, {title}. They reset tomorrow."
        return f"I'm being rate limited, {title}. Give me a moment and try again."
    if err.status == 403:
        return f"OpenRouter blocked that request, {title}. The reason is in the JARVIS window."
    if err.status in (400, 404):
        return f"OpenRouter won't run the model {cfg['OPENROUTER_MODEL']}, {title}. The reason is in the JARVIS window."
    if err.status == 0:
        return f"I can't reach my brain, {title}. Check your internet connection."
    return f"OpenRouter is having a moment, {title}. Try again shortly."


# ---------------------------------------------------------------- voice (Fish Audio)

_voice_override: str | None = None  # set by a protocol with a "voice" field, until restart


def speak(cfg: dict[str, str], text: str) -> tuple[bytes | None, str | None]:
    key = cfg.get("FISH_API_KEY")
    if not key:
        return None, "No Fish Audio key yet, so you're hearing the backup voice. Add FISH_API_KEY to the .env file."
    body = json.dumps({
        "text": text,
        "reference_id": _voice_override or cfg["FISH_VOICE_ID"],
        "format": "mp3",
        "mp3_bitrate": 128,
        "normalize": True,
        "latency": "balanced",
    }).encode("utf-8")
    request = urllib.request.Request(FISH_TTS_URL, data=body, method="POST", headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "model": cfg["FISH_MODEL"],
    })
    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 - fixed https URL
            return response.read(), None
    except urllib.error.HTTPError as err:
        detail = err.read()[:300].decode("utf-8", "replace")
        log(f"Fish Audio error {err.code}: {detail}")
        if err.code in (401, 403):
            return None, "Fish Audio didn't accept the key. Check FISH_API_KEY in the .env file."
        if err.code == 402:
            return None, "Your Fish Audio API credit is empty. Add credit on fish.audio and JARVIS gets his voice back."
        if err.code in (400, 404, 422):
            return None, "Fish Audio couldn't use that voice. Check FISH_VOICE_ID and FISH_MODEL in the .env file."
        return None, f"Fish Audio returned an error ({err.code}). Using the backup voice for now."
    except (urllib.error.URLError, TimeoutError):
        return None, "Can't reach Fish Audio right now. Using the backup voice."


# ---------------------------------------------------------------- protocols

def load_protocols() -> list[dict]:
    try:
        data = json.loads(PROTOCOLS_FILE.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as err:
        log(f"protocols.json has a typo ({err}). Ignoring it until it's fixed.")
        return []
    return [p for p in data if isinstance(p, dict) and p.get("say")] if isinstance(data, list) else []


def _words(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", text.lower()).split())


def match_protocol(text: str) -> dict | None:
    said = f" {_words(text)} "
    for protocol in load_protocols():
        if f" {_words(protocol['say'])} " in said:
            return protocol
    return None


def open_url(url: str) -> None:
    if NO_BROWSER:
        log(f"(would open) {url}")
    else:
        webbrowser.open(url)


# ---------------------------------------------------------------- web server

class Handler(BaseHTTPRequestHandler):
    server_version = "JARVIS"

    def log_message(self, format: str, *args) -> None:  # keep the window readable
        pass

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        try:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, code: int, payload: dict) -> None:
        self._send(code, json.dumps(payload).encode("utf-8"), "application/json")

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > 100_000:
            return {}
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self._send(200, INDEX_HTML.read_bytes(), "text/html; charset=utf-8")
        elif path == "/api/status":
            cfg = load_settings()
            brain_name, model = brain_label(cfg)
            self._json(200, {
                "voice": bool(cfg.get("FISH_API_KEY")),
                "brain": bool(brain_name),
                "brain_name": brain_name,
                "model": model,
                "calls": cfg["JARVIS_CALLS_YOU"],
                "protocols": [p["say"] for p in load_protocols()],
            })
        elif path == "/favicon.ico":
            self._send(204, b"", "image/x-icon")
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        global _voice_override
        path = self.path.split("?", 1)[0]
        cfg = load_settings()
        data = self._read_json()
        text = str(data.get("text") or "").strip()[:2000]
        title = cfg["JARVIS_CALLS_YOU"]

        if path == "/api/chat":
            if not text:
                self._json(400, {"error": "Say something first."})
                return
            log(f"You:    {text}")
            protocol = match_protocol(text)
            if protocol:
                for url in protocol.get("open") or []:
                    open_url(str(url))
                if protocol.get("voice"):
                    voice_id = str(protocol["voice"]).strip()
                    _voice_override = None if voice_id == "default" else voice_id
                reply = str(protocol.get("reply") or "Right away, {you}.").replace("{you}", title)
                log(f"JARVIS: {reply}  (protocol)")
                self._json(200, {"reply": reply, "protocol": protocol["say"]})
                return
            if not which_brain(cfg):
                self._json(200, {"reply": f"My brain isn't connected yet, {title}. Add a Claude or OpenRouter key to the .env file and restart me.", "error": "brain"})
                return
            try:
                reply = think(cfg, text)
            except anthropic.APIError as err:
                log(f"Claude error: {err}")
                self._json(200, {"reply": brain_error(err, cfg), "error": "claude"})
                return
            except OpenRouterError as err:
                log(f"OpenRouter error {err}")
                self._json(200, {"reply": openrouter_error(err, cfg), "error": "openrouter"})
                return
            except Exception as err:  # noqa: BLE001 - keep JARVIS alive and report it
                log(f"Unexpected error: {err!r}")
                self._json(200, {"reply": f"Something went wrong in my head, {title}. The details are in the JARVIS window.", "error": "internal"})
                return
            log(f"JARVIS: {reply}")
            self._json(200, {"reply": reply})
            return

        if path == "/api/tts":
            if not text:
                self._json(400, {"error": "Nothing to say."})
                return
            audio, problem = speak(cfg, text)
            if audio:
                self._send(200, audio, "audio/mpeg")
            else:
                self._json(502, {"error": problem})
            return

        if path == "/api/reset":
            with _lock:
                _history.clear()
            self._json(200, {"ok": True})
            return

        self._json(404, {"error": "not found"})


BANNER = r"""
       _   _    ____  __     __ ___  ____
      | | / \  |  _ \ \ \   / /|_ _|/ ___|
   _  | |/ _ \ | |_) | \ \ / /  | | \___ \
  | |_| / ___ \|  _ <   \ V /   | |  ___) |
   \___/_/   \_\_| \_\   \_/   |___||____/
"""


def main() -> None:
    try:
        # Line-buffered, so the address shows up right away even when the output goes to a log file.
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except (AttributeError, ValueError):
        pass
    print(BANNER)
    cfg = first_run(load_settings())

    port = int(cfg.get("PORT") or 8765)
    server = None
    for candidate in range(port, port + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", candidate), Handler)
            break
        except OSError:
            continue
    if server is None:
        print(f"\n  Couldn't find a free port near {port}. Close other apps or set PORT in .env.\n")
        sys.exit(1)

    url = f"http://127.0.0.1:{server.server_address[1]}"
    brain_name, model = brain_label(cfg)
    print("\n  ==================================================")
    print("    J.A.R.V.I.S. is online")
    print(f"    Open {url}  (Chrome or Edge, for voice input)")
    print(f"    Voice: Fish Audio {cfg['FISH_VOICE_ID']} ({cfg['FISH_MODEL']})")
    print(f"    Brain: {brain_name} {model}" if brain_name else "    Brain: not connected yet")
    print("    Close this window to shut JARVIS down.")
    print("  ==================================================\n")
    if not NO_BROWSER:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  JARVIS offline. Goodbye.\n")


if __name__ == "__main__":
    main()
