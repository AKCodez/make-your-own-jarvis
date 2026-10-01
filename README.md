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
- ⚡ **Protocols.** Say *"activate party protocol"* and he opens your music. Adding your own takes one line.
- 😏 **E-girl mode.** Say *"activate e-girl mode"* if you want to ruin JARVIS. *"Activate jarvis mode"* brings him back.
- 🔒 **Runs on your computer.** Your keys stay in one file on your machine.

## 🧰 What you need

1. A computer running Windows, Mac or Linux
2. **Python 3.10 or newer**, free at [python.org](https://www.python.org/downloads/)
3. A **Fish Audio API key** for the voice → **[get one here](https://ariacodez.ai/l/fish-audio)**
4. A **Claude API key** for the brain → [console.anthropic.com](https://console.anthropic.com/settings/keys)
5. **Chrome or Edge**, because they have voice input built in

---

## ⚡ The easy way: let Claude set it up

If you have [Claude Code](https://claude.com/claude-code), open it and paste this:

```text
Set up JARVIS for me from https://github.com/AKCodez/make-your-own-jarvis

1. Check that Python 3.10 or newer is installed. If it isn't, install it for me.
2. Clone the repo into my home folder.
3. Copy .env.example to .env and open it in Notepad (TextEdit on Mac) so I can paste my
   Fish Audio key and my Claude key myself. Don't ask me for the keys in this chat.
4. When I say "done", start JARVIS in the background (run.bat on Windows, ./run.sh on
   Mac or Linux) and open the address it prints in Chrome.
```

Paste your two keys into the file that opens, save it, and type **done**. Boom, you've got JARVIS. 🎉

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
- 🧠 **Claude (the brain):** go to [console.anthropic.com](https://console.anthropic.com/settings/keys), click **Create Key**, and copy it. It starts with `sk-ant-`.

Both are pay-as-you-go. If JARVIS ever says he's out of credit, add a little on that site's billing page.

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
| `FISH_VOICE_ID` | The voice he speaks with | JARVIS |
| `FISH_MODEL` | The Fish Audio speech model | `s2.1-pro` |
| `JARVIS_MODEL` | The Claude model. `claude-haiku-4-5` answers faster and costs less | `claude-opus-5-5` |
| `JARVIS_CALLS_YOU` | What he calls you | `sir` |
| `PORT` | The local port. If it's busy, he picks the next free one | `8765` |

## 🆘 Troubleshooting

- **"python is not recognized":** reinstall Python and tick **"Add python.exe to PATH"**.
- **He doesn't hear me:** use Chrome or Edge and allow the microphone (click the icon at the left of the address bar). You can always type instead.
- **He sounds like a robot:** that's the backup voice. The red pop-up tells you why. It's usually a wrong Fish Audio key or empty Fish Audio credit.
- **"My brain key isn't working":** check the Claude key in `.env` and that your Claude account has credit.
- **Start over:** delete the `.env` file and start JARVIS again.
- **Anything else:** paste the error into Claude and ask it to fix your JARVIS.

## 🔒 Your keys

Your keys only live in the `.env` file on your computer. That file is in `.gitignore`, so it never gets uploaded anywhere. Don't share it or post it.

---

<div align="center">

Built by [@ariacodez](https://instagram.com/ariacodez) &nbsp;·&nbsp; Voice by [Fish Audio](https://ariacodez.ai/l/fish-audio) &nbsp;·&nbsp; Brain by [Claude](https://claude.com)

MIT License. Do whatever you want with it.

</div>
