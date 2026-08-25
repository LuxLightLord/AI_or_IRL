# AI or IRL — project guidelines

This project builds a live workplace quiz where teams guess whether images/video/audio/text are AI-generated or real. See `QUIZ_BUILD_INSTRUCTIONS.md` for the current task brief — read it before doing any work here.

## Standing rules

- **Language**: all quiz-facing content — UI text, host instructions, and the audio/text passage content itself — must be in Swedish. This is for a Swedish workplace.
- **Licensing**: only public-domain, Creative-Commons, or self-generated media may be embedded. The app is a single self-contained page with no backend, so this isn't optional — copyrighted content (viral clips, news/movie footage, scraped social media) cannot legally be embedded and must never be used.
- **Deployment context**: this runs live, once, at an in-person event — one shared screen (projector) plus ~18-24 people's phones/laptops as team devices. No external backend beyond Claude Artifact runtime capabilities. It needs to just work on the day, not be a maintained product.
- **Difficulty calibration**: any content added to this quiz (now or later) should mix "impressive-looking but real" and "unremarkable-looking but AI" examples in both directions per modality. The target is the best team landing ~60-70% correct — pairs that are obviously one or the other defeat the point.
