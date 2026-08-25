# Handover: build "AI or IRL" quiz — Phase B (approved content, ready to build)

You're starting fresh with no memory of the prior session. Everything you need is below plus two files in this directory:

1. Read `CLAUDE.md` in this directory first (standing guidelines).
2. Read `QUIZ_BUILD_INSTRUCTIONS.md` in this directory — the full build brief. Phase A (content sourcing) is done and approved by Leo; **skip straight to "Phase B — Build and publish"** using the approved content below instead of re-sourcing anything.

## Tool-capability findings from Phase A (still true, don't re-check)

- **No image-generation or video-generation tool** was available in that session. All AI images/video below are sourced from existing openly-licensed content, not self-generated. If your session *does* have image/video generation available, that's a nice-to-have upgrade but not required — the sourced content was already approved.
- **Swedish TTS IS available natively**, no external tool needed: Windows ships a built-in neural voice, `Microsoft Bengt` (sv-SE), via the modern WinRT speech API (`Windows.Media.SpeechSynthesis`) — richer than the classic `System.Speech` SAPI voices (which are English-only on this machine). Confirmed working: synthesizing a Swedish sentence produced a valid 16-bit/16kHz mono PCM WAV. Working PowerShell snippet (uses the `AsTask` WinRT-await trick since PowerShell can't natively `await`):

```powershell
function Await($WinRtTask, $ResultType) {
    $asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
    $asTaskGeneric = $asTask.MakeGenericMethod($ResultType)
    $netTask = $asTaskGeneric.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.SpeechSynthesis,ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.Streams.DataReader,Windows.Storage.Streams,ContentType=WindowsRuntime] | Out-Null

$synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
$synth.Voice = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices | Where-Object { $_.Language -eq 'sv-SE' }
$streamOp = $synth.SynthesizeTextToStreamAsync("Din svenska text här.")
$stream = Await $streamOp ([Windows.Media.SpeechSynthesis.SpeechSynthesisStream])
$reader = New-Object Windows.Storage.Streams.DataReader($stream.GetInputStreamAt(0))
$size = [uint32]$stream.Size
Await ($reader.LoadAsync($size)) ([uint32]) | Out-Null
$buffer = New-Object byte[] $size
$reader.ReadBytes($buffer)
[System.IO.File]::WriteAllBytes("out.wav", $buffer)
```

- **No `ffmpeg`, no `ezycopy`** on this machine (checked, not installed). Plan around this: pick source video/audio clips that are already short and small rather than relying on re-encoding. If you need format conversion (e.g. WAV → compressed for embedding) and no converter is available, either embed the WAV as-is (a few seconds of 16-bit/16kHz mono is only ~500KB–1MB, fine within the 16MB budget for ~2-3 clips) or check whether ffmpeg/imageio-ffmpeg can be installed via pip/winget — ask Leo before installing new tooling.

## Approved content list, in final running order

Order was chosen so video opens and closes the quiz, and no two consecutive questions share a modality (pattern V-I-A-T-I-V-T-A-I-T-A-V). 6 AI / 6 Real overall, no answer-streak longer than 2.

| Order | Modality | Content / generation plan | Answer | Source & license | Why it's calibrated to be hard |
|---|----|----|----|----|----|
| 1 | Video | "Example of Sora AI-Generated Police Body Camera Footage", ~10s, mundane bodycam-style clip | **AI** | Wikimedia Commons, Category:AI-generated videos — **verify exact license tag on the file page before embedding**, Commons AI-media licensing is inconsistently tagged; swap to another file in that category if this one isn't reusable | Bodycam footage is deliberately dull/shaky — no obvious AI artifacts |
| 2 | Image | "Light pillars over Laramie, Wyoming in winter night" — real atmospheric optical phenomenon | **Real** | Wikimedia Commons, NOAA/NWS photo, public domain | Looks like AI-generated alien light beams but is a real, documented optical phenomenon |
| 3 | Audio | Swedish TTS reading a short passage | **AI** | Self-generate via the WinRT `Microsoft Bengt` (sv-SE) snippet above — write/choose the passage text, keep it ~15-25s read aloud | Modern neural TTS sounds fairly natural — not the choppy robotic voice people expect |
| 4 | Text | Short public-domain Swedish prose excerpt (Strindberg, Lagerlöf, or similar), mundane everyday topic | **Real** | Litteraturbanken (litteraturbanken.se) or Project Runeberg (runeberg.org) — public domain, author dead 70+ years | Older/formal literary Swedish reads as "unnaturally polished" to a modern eye |
| 5 | Image | "Maria and Steve work on the new logo of the Netscape Internet browser (fictional photo)" — 1990s office scene, Midjourney + Photoshop, part of Joseph Ayerle's "1995 – Birth of Web" project | **AI** | Wikimedia Commons — page shows CC-BY-SA 3.0 in structured data but also a contradictory PD claim in the text; **pin down the actual applicable license before embedding** | Boring office scene, no fantastical AI tells |
| 6 | Video | Short (5-8s) CC0 stock clip of a mundane everyday action (pouring coffee, typing, walking) | **Real** | Pexels or Pixabay, CC0 — **specific clip not yet picked**, search pexels.com/search/videos/boring or pixabay.com/videos/search/boring and choose one | Nothing remarkable happens — plain enough to suspect "generic = AI stock footage" |
| 7 | Text | AI-written Swedish passage on an everyday topic (e.g. a short reflection on morning routines), competent but slightly generic | **AI** | Write it yourself (you're the LLM) | Grammatical, on-topic, no obvious AI tells, deliberately not flowery or robotic |
| 8 | Audio | LibriVox Swedish recording — e.g. "Göteborgsflickor" (Sigge Strömberg) or "Ja och Nej" (Helena Nyblom), volunteer-read | **Real** | librivox.org — public domain recordings of public-domain texts; pick a short chapter/section, download the mp3 | Amateur narration can sound stilted or oddly theatrical — easy to mistake for synthetic prosody |
| 9 | Image | A polished/professional-looking AI "fashion studio portrait" image | **AI** | Wikimedia Commons, Category:AI-generated images / AI-generated photographs — **specific file not yet picked**, browse that category for a fashion/portrait-style photorealistic result and verify its license | Impressive/polished — breaks the "too perfect = AI" pattern-match together with item 5 doing the opposite |
| 10 | Text | AI-written Swedish passage in a warmer, more personal/anecdotal style (mimicking a blog post) | **AI** | Write it yourself | Deliberately feels human/anecdotal — targets teams who assume "personality = human" |
| 11 | Audio | Mozilla Common Voice Swedish (sv-SE) validated clip, ordinary contributor reading a sentence | **Real** | commonvoice.mozilla.org, CC0 — dataset is on Hugging Face (`mozilla-foundation/common_voice_*`, sv-SE split); **check whether the split requires a HF login/gating** before relying on it, have LibriVox as a fallback real-audio source if so | Plain, clear, well-enunciated — could pass as "too clean" TTS |
| 12 | Video | NASA ISS aurora timelapse (Aurora Australis/Borealis from the Space Station) | **Real** | NASA Scientific Visualization Studio (svs.gsfc.nasa.gov) or images.nasa.gov — US government work, public domain | Otherworldly, saturated colors — looks exactly like an AI showcase reel but is real orbital footage |

## Remaining sourcing work (flagged in Phase A, not yet done)

A few items above still need a concrete file picked and downloaded, not just a category/source pointed at:
- **#1**: confirm exact license on the Sora bodycam file (or pick an alternate from the same Commons category).
- **#5**: confirm which license actually applies (CC-BY-SA 3.0 vs. the page's PD claim).
- **#6**: pick one specific Pexels/Pixabay clip.
- **#9**: pick one specific AI-generated portrait file from Commons and confirm its license.
- **#11**: confirm Common Voice sv-SE clips are fetchable without auth gating; fall back to a second LibriVox real-audio item if not.
- **#3, #7, #10**: text/passage content itself still needs to be actually written (the AI ones) and the exact excerpt chosen (the real one, #4).

## What Phase B actually requires (from QUIZ_BUILD_INSTRUCTIONS.md — read that file for full detail)

1. Load the `artifact-design` skill before writing any artifact content.
2. Load the `artifact-capabilities` skill before picking a runtime capability — this quiz needs state shared live across viewer devices (team votes, current question, leaderboard, host-controlled advancement).
3. Build one self-contained Artifact: host/shared-screen view + team view, all quiz-facing UI/content in **Swedish**, using the approved content above in the order given.
4. Respect the **16MB total size cap** — check actual embedded asset sizes as you go, not just at the end. No ffmpeg locally, so favor already-small source clips over needing to compress.
5. Publish the artifact.

## Verification before declaring done

- Dry-run: open host view, join as a simulated team from a second tab/device, submit an answer, reveal on host view, confirm leaderboard updates.
- Confirm all four modalities render/play correctly.
- Confirm published page is under the size cap.
- Report the published Artifact link back to Leo.
