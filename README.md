<div align="center">

# 🤖 Make Your Own JARVIS

**Talk to your own Iron Man assistant, out loud, in the real JARVIS voice.**

Claude is the brain. [Fish Audio](https://ariacodez.ai/l/fish-audio) is the voice. You start it with one double-click.

⏱ About 10 minutes &nbsp;·&nbsp; 🪟 Windows &nbsp;·&nbsp; 🍎 Mac &nbsp;·&nbsp; 🐧 Linux &nbsp;·&nbsp; 🧑‍💻 No coding

</div>

---

## ✨ What you get

- 🎙️ **Hold Space and talk.** JARVIS answers out loud in the JARVIS voice from Fish Audio.
- 🧠 **Real answers.** Claude does the thinking, so he can help with almost anything you ask.
- 🆓 **A free brain option.** Skip the Claude key and use a free OpenRouter key instead.
- ⚡ **Protocols.** Say *"activate party protocol"* and he opens your music. Adding your own takes one line.
- 😏 **E-girl mode.** Say *"activate e-girl mode"* if you want to ruin JARVIS. *"Activate jarvis mode"* brings him back.
- 🔒 **Runs on your computer.** Your keys stay in one file on your machine.

## 🧰 What you need

1. A computer running Windows, Mac or Linux
2. **Python 3.10 or newer**, free at [python.org](https://www.python.org/downloads/)
3. A **Fish Audio API key** for the voice → **[get one here](https://ariacodez.ai/l/fish-audio)**
4. A **key for the brain**. Pick one:
   - A **Claude API key** → [console.anthropic.com](https://console.anthropic.com/settings/keys)
   - A **free OpenRouter key** → [openrouter.ai/keys](https://openrouter.ai/keys)
5. **Chrome or Edge**, because they have voice input built in

---

## ⚡ The easy way: one prompt

If you have [Claude Code](https://claude.com/claude-code), open it, paste this, and swap in your two keys:

```text
Set up JARVIS for me and start it: https://github.com/AKCodez/make-your-own-jarvis

Fish Audio key: PASTE_YOUR_FISH_AUDIO_KEY
Claude or OpenRouter key: PASTE_YOUR_BRAIN_KEY
```

Hit Enter and Claude does the whole setup. Boom, you've got JARVIS. 🎉

If you'd rather not paste keys into a chat, use the manual way below.

<details>
<summary>🤖 Setup steps for Claude (or any AI assistant)</summary>

You were given this repo and two keys. Do this:

1. Make sure Python 3.10 or newer is installed (`python --version`, or `python3 --version` on Mac and Linux). Install it if it's missing.
2. Clone this repo into the user's home folder, unless they named another place.
3. Copy `.env.example` to `.env` and fill in the keys before you start anything:
   - `FISH_API_KEY` is the Fish Audio key.
   - The brain key goes in `ANTHROPIC_API_KEY` if it starts with `sk-ant-`, or in `OPENROUTER_API_KEY` if it starts with `sk-or-`. Leave the other one empty.
4. Start JARVIS in the background with `run.bat` on Windows or `./run.sh` on Mac and Linux. It is a local web server that keeps running, so don't wait for it to exit. The first start takes about 30 seconds because it builds `.venv` and installs one package.
5. JARVIS prints his address (`http://127.0.0.1:8765`, or the next free port) and opens it in the default browser by himself. Voice input needs Chrome or Edge.
6. Test both keys for real. `/api/status` only shows that the keys are filled in, not that they work. Send `POST /api/chat` with `{"text": "Are you online?"}` and check the reply has no `"error"` field. Then send `POST /api/tts` with `{"text": "Online."}` and check it returns audio. If one fails, its message says which key is wrong.
7. Tell the user to click the page once to wake JARVIS, then hold Space to talk. Next time they start him by double-clicking `run.bat` or running `./run.sh`.

If `.env` is missing a key, the launcher asks for it in the terminal, so write `.env` first. JARVIS reads keys from `.env` only, never from environment variables. On a machine with no screen, set the environment variable `JARVIS_NO_BROWSER=1` so he doesn't open a browser. Don't repeat the keys back to the user and don't commit `.env`.

</details>

### 💬 Then change anything with one sentence

Open Claude Code in the JARVIS folder and paste any of these:

| You want | Say this to Claude |
|---|---|
| A new name for you | `Make JARVIS call me "boss" instead of "sir".` |
| A new personality | `Make JARVIS more sarcastic, like he's tired of my questions.` |
| Your own protocol | `Add a protocol: when I say "activate study mode", open YouTube lofi and Notion.` |
| A different voice | `Switch JARVIS to the Fish Audio voice 612b878b113047d9a770c069c8b4fdfe.` |
| Your own voice | `Help me clone my voice on Fish Audio and make it JARVIS's voice.` |
| Faster replies | `Make JARVIS answer faster.` |
| The free brain | `Switch JARVIS to the free OpenRouter brain. I'll paste the key into .env myself.` |
| Iron Man colors | `Make the HUD glow red and gold instead of blue.` |
| A fix | `JARVIS shows this error, fix it: <paste the error>` |

---

## 🛠️ The manual way (no Claude needed)

### 1. Install Python

Download it from **[python.org/downloads](https://www.python.org/downloads/)** and run the installer.

> [!IMPORTANT]
> **Windows:** on the first installer screen, tick **"Add python.exe to PATH"** before you click Install. Nothing works without it.

### 2. Download JARVIS

Click the green **Code** button at the top of this page, then **Download ZIP**, and unzip it anywhere (your Desktop is fine).

Or with git: `git clone https://github.com/AKCodez/make-your-own-jarvis.git`

### 3. Get your two keys

- 🐟 **Fish Audio (the voice):** [create your account](https://ariacodez.ai/l/fish-audio), click your profile, open **API Keys**, click **Create**, and copy the key.
- 🧠 **The brain.** Pick one:
  - **Claude:** go to [console.anthropic.com](https://console.anthropic.com/settings/keys), click **Create Key**, and copy it. It starts with `sk-ant-`.
  - **The free option, OpenRouter:** go to [openrouter.ai/keys](https://openrouter.ai/keys), sign up, create a key, and copy it. It starts with `sk-or-`.

Fish Audio and Claude are pay-as-you-go. If JARVIS ever says he's out of credit, add a little on that site's billing page. The OpenRouter key runs a free model, with a limit of 50 questions a day.

### 4. Start JARVIS

- **Windows:** double-click **`run.bat`**
- **Mac or Linux:** open Terminal in the folder and run `chmod +x run.sh && ./run.sh`

The first run sets everything up in about 30 seconds, then asks for your two keys. Paste each one (right-click or Ctrl+V) and press Enter. They're saved in a `.env` file on your computer, so you only do this once.

### 5. Talk to him

Your browser opens to JARVIS. Click once to wake him up and allow the microphone. Now **hold Space** (or click the glowing core), talk, and let go.

> [!TIP]
> **You don't have to pick a voice.** The JARVIS voice is already set. The moment your Fish Audio key is in, he sounds like JARVIS.

---

## 🎭 Voices

JARVIS speaks with whatever Fish Audio voice is set as `FISH_VOICE_ID` in your `.env` file.

| Voice | Voice ID |
|---|---|
| JARVIS (default) | `41f0953d7a6b4c078445c7e65d620eeb` |
| Jarvis (MCU) | `612b878b113047d9a770c069c8b4fdfe` |
| E-girl 😏 | `98655a12fa944e26b274c535e5e03842` |

There are thousands more in the [Fish Audio voice library](https://ariacodez.ai/l/fish-audio). You can also clone your own voice there and paste its ID.

## ⚡ Protocols

Protocols are instant commands. JARVIS hears the phrase and does it right away, no thinking needed. They live in `protocols.json`:

```json
{
  "say": "activate party protocol",
  "reply": "Right away, {you}. Initiating the party protocol.",
  "open": ["https://open.spotify.com"]
}
```

- `say` is the phrase he listens for.
- `reply` is what he says back. `{you}` becomes sir, boss, or whatever you picked.
- `open` is a list of websites to open. It's optional.
- `voice` switches to another Fish Audio voice. It's optional, and `"default"` switches back.

Built in: *"activate e-girl mode"*, *"activate jarvis mode"*, *"activate party protocol"* and *"activate work mode"*.

## ⚙️ Settings

All settings live in the `.env` file. Close the JARVIS window and start it again after you change one.

| Setting | What it does | Default |
|---|---|---|
| `FISH_API_KEY` | Your Fish Audio key | |
| `ANTHROPIC_API_KEY` | Your Claude key | |
| `OPENROUTER_API_KEY` | A free OpenRouter key. JARVIS uses it when there's no Claude key | |
| `FISH_VOICE_ID` | The voice he speaks with | JARVIS |
| `FISH_MODEL` | The Fish Audio speech model | `s2.1-pro` |
| `JARVIS_MODEL` | The Claude model. `claude-haiku-4-5` answers faster and costs less | `claude-opus-5-5` |
| `OPENROUTER_MODEL` | The OpenRouter model, used with an OpenRouter key | `apodex/apodex-1.1-mini:free` |
| `JARVIS_CALLS_YOU` | What he calls you | `sir` |
| `PORT` | The local port. If it's busy, he picks the next free one | `8765` |

## 🆘 Troubleshooting

- **"python is not recognized":** reinstall Python and tick **"Add python.exe to PATH"**.
- **He doesn't hear me:** use Chrome or Edge and allow the microphone (click the icon at the left of the address bar). You can always type instead.
- **He sounds like a robot:** that's the backup voice. The red pop-up tells you why. It's usually a wrong Fish Audio key or empty Fish Audio credit.
- **"My brain key isn't working":** check the Claude or OpenRouter key in `.env`. With Claude, check that your account has credit too.
- **"I've used up today's free questions":** the free OpenRouter brain allows 50 questions a day. It resets the next day, or you can switch to a Claude key.
- **"OpenRouter won't run the model":** the JARVIS window shows the reason. Free models come and go. If this one is gone, pick another free model on [openrouter.ai/models](https://openrouter.ai/models) and paste its ID after `OPENROUTER_MODEL=` in `.env`. If the reason mentions your data policy, change it in your [OpenRouter privacy settings](https://openrouter.ai/settings/privacy).
- **Start over:** delete the `.env` file and start JARVIS again.
- **Anything else:** paste the error into Claude and ask it to fix your JARVIS.

## 🔒 Your keys

JARVIS saves your keys in the `.env` file on your computer. That file is in `.gitignore`, so it never gets uploaded anywhere. Don't share it or post it.

---

<div align="center">

Built by [@ariacodez](https://instagram.com/ariacodez) &nbsp;·&nbsp; Voice by [Fish Audio](https://ariacodez.ai/l/fish-audio) &nbsp;·&nbsp; Brain by [Claude](https://claude.com) or [OpenRouter](https://openrouter.ai)

MIT License. Do whatever you want with it.

</div>
