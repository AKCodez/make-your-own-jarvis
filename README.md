<div align="center">

# 🤖 Make Your Own JARVIS

**Talk to your own Iron Man assistant, out loud, in the real JARVIS voice.**

A free OpenRouter model is the brain. [Fish Audio](https://ariacodez.ai/l/fish-audio) is the voice. You start it with one double-click.

⏱ About 10 minutes &nbsp;·&nbsp; 🪟 Windows &nbsp;·&nbsp; 🍎 Mac &nbsp;·&nbsp; 🐧 Linux &nbsp;·&nbsp; 🧑‍💻 No coding

</div>

---

## ✨ What you get

- 🎙️ **Hold Space and talk.** JARVIS answers out loud in the JARVIS voice from Fish Audio.
- 🧠 **Real answers.** An AI model does the thinking, so he can help with almost anything you ask.
- 🆓 **A free brain.** The brain runs on a free OpenRouter key.
- ⚡ **Protocols.** Say *"activate party protocol"* and he opens your music. Adding your own takes one line.
- 😏 **E-girl mode.** Say *"activate e-girl mode"* if you want to ruin JARVIS. *"Activate jarvis mode"* brings him back.
- 🔒 **Runs on your computer.** Your keys stay in one file on your machine.

## 🧰 What you need

1. A computer running Windows, Mac or Linux
2. **Python 3.10 or newer**, free at [python.org](https://www.python.org/downloads/)
3. A **Fish Audio API key** for the voice → **[get one here](https://ariacodez.ai/l/fish-audio)**
4. A **free OpenRouter API key** for the brain → [openrouter.ai/keys](https://openrouter.ai/keys)
5. **Chrome or Edge**, because they have voice input built in

---

## ⚡ The easy way: one prompt

If you have [Claude Code](https://claude.com/claude-code), open it, paste this, and swap in your two keys:

```text
Wake up, Claude. We're building JARVIS.

Repo: https://github.com/AKCodez/make-your-own-jarvis
Voice: Fish Audio model 41f0953d7a6b4c078445c7e65d620eeb (the JARVIS voice)
Fish Audio key: PASTE_YOUR_FISH_AUDIO_KEY
OpenRouter key: PASTE_YOUR_OPENROUTER_KEY

Set him up on my computer, bring him online, and tell me when he's ready.
```

Hit Enter and Claude does the whole setup. Boom, you've got JARVIS. 🎉

The voice line is the JARVIS voice on [Fish Audio](https://ariacodez.ai/l/fish-audio). Swap that model ID for any other Fish Audio voice and he'll sound like that instead.

If you'd rather not paste keys into a chat, use the manual way below.

<details>
<summary>🤖 Setup steps for Claude (or any AI assistant)</summary>

You were given this repo, a Fish Audio voice model ID and two keys. Do this:

1. Make sure Python 3.10 or newer is installed (`python --version`, or `python3 --version` on Mac and Linux). Install it if it's missing.
2. Clone this repo into the user's home folder, unless they named another place.
3. Copy `.env.example` to `.env` and fill in the keys before you start anything:
   - `FISH_API_KEY` is the Fish Audio key.
   - `FISH_VOICE_ID` is the Fish Audio model ID from the prompt.
   - `OPENROUTER_API_KEY` is the OpenRouter key.
4. Start JARVIS in his own window, so he keeps running after this chat is closed. On Windows, run `powershell -Command "Start-Process run.bat"` in the JARVIS folder. On Mac and Linux, run `nohup ./run.sh > jarvis.log 2>&1 &`. He is a local web server that runs until he's closed, so don't wait for him to exit. There is nothing to install, he only needs Python.
5. JARVIS opens his page in the default browser by himself. The address is `http://127.0.0.1:8765`, or the next port up (8766, 8767 and so on) if that one was taken. He prints it in his window, or in `jarvis.log` on Mac and Linux. Voice input needs Chrome or Edge.
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
| Iron Man colors | `Make the HUD glow red and gold instead of blue.` |
| A fix | `JARVIS shows this error, fix it: <paste the error>` |

---

## 🛠️ The manual way (no Claude Code needed)

### 1. Install Python

Download it from **[python.org/downloads](https://www.python.org/downloads/)** and run the installer.

> [!IMPORTANT]
> **Windows:** on the first installer screen, tick **"Add python.exe to PATH"** before you click Install. Nothing works without it.

### 2. Download JARVIS

Click the green **Code** button at the top of this page, then **Download ZIP**, and unzip it anywhere (your Desktop is fine).

Or with git: `git clone https://github.com/AKCodez/make-your-own-jarvis.git`

### 3. Get your two keys

- 🐟 **Fish Audio (the voice):** [create your account](https://ariacodez.ai/l/fish-audio), click your profile, open **API Keys**, click **Create**, and copy the key.
- 🧠 **OpenRouter (the brain):** go to [openrouter.ai/keys](https://openrouter.ai/keys), sign up, create a key, and copy it. It starts with `sk-or-`.

Fish Audio is pay-as-you-go. If JARVIS ever says his voice credit is empty, add a little on Fish Audio's billing page. The OpenRouter key runs a free model, with a limit of 50 questions a day.

### 4. Start JARVIS

- **Windows:** double-click **`run.bat`**
- **Mac or Linux:** open Terminal in the folder and run `chmod +x run.sh && ./run.sh`

The first run asks for your two keys. Paste each one (right-click or Ctrl+V) and press Enter. They're saved in a `.env` file on your computer, so you only do this once.

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
| `OPENROUTER_API_KEY` | Your OpenRouter key | |
| `FISH_VOICE_ID` | The voice he speaks with | JARVIS |
| `FISH_MODEL` | The Fish Audio speech model | `s2.1-pro` |
| `OPENROUTER_MODEL` | The model he thinks with. Any model ID from [openrouter.ai/models](https://openrouter.ai/models) works | `apodex/apodex-1.1-mini:free` |
| `JARVIS_CALLS_YOU` | What he calls you | `sir` |
| `PORT` | The local port. If it's busy, he picks the next free one | `8765` |

## 🆘 Troubleshooting

- **"python is not recognized":** reinstall Python and tick **"Add python.exe to PATH"**.
- **He doesn't hear me:** use Chrome or Edge and allow the microphone (click the icon at the left of the address bar). You can always type instead.
- **He sounds like a robot:** that's the backup voice. The red pop-up tells you why. It's usually a wrong Fish Audio key or empty Fish Audio credit.
- **"My brain key isn't working":** check the OpenRouter key in `.env`.
- **"I've used up today's free questions":** the free brain allows 50 questions a day. It resets the next day.
- **"OpenRouter won't run the model":** the JARVIS window shows the reason. Free models come and go. If this one is gone, pick another free model on [openrouter.ai/models](https://openrouter.ai/models) and paste its ID after `OPENROUTER_MODEL=` in `.env`. If the reason mentions your data policy, change it in your [OpenRouter privacy settings](https://openrouter.ai/settings/privacy).
- **Start over:** delete the `.env` file and start JARVIS again.
- **Anything else:** paste the error into Claude Code and ask it to fix your JARVIS.

## 🔒 Your keys

JARVIS saves your keys in the `.env` file on your computer. That file is in `.gitignore`, so it never gets uploaded anywhere. Don't share it or post it.

---

<div align="center">

Built by [@ariacodez](https://instagram.com/ariacodez) &nbsp;·&nbsp; Voice by [Fish Audio](https://ariacodez.ai/l/fish-audio) &nbsp;·&nbsp; Brain by [OpenRouter](https://openrouter.ai)

MIT License. Do whatever you want with it.

</div>
