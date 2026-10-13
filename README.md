# Clement’s technical notebook

Astro + Tailwind CSS + Markdown/MDX portfolio at https://poytaytoy.github.io.

## Develop

Use Node 22.19+. Run `npm ci`, then `npm run dev`. Validate with `npm run check`, `npm run build`, and `npm test`. Preview the production output with `npm run preview`.

## Write a note

Add a `.md` or `.mdx` file to `src/content/posts/`. Its filename becomes the URL under `/writing/`.

```yaml
---
title: "A descriptive title"
description: "A one-sentence summary."
date: 2026-10-12
category: "Software design"
tags: ["C++", "Systems"]
minutes: 5
draft: false
---
```

Use `##` and `###` headings for the automatic table of contents. Set `draft: true` to exclude a note from routes, archive, RSS, and sitemap. Dates display in UTC. Reading times are explicit editorial estimates.

Fenced code uses Shiki. Inline math uses `$...$`, and display math uses `$$...$$`. MDX can import `SignalLab.astro` for an interactive filter or `Diagram.astro` with a `code` prop containing Mermaid syntax. Diagram source remains available without JavaScript. Pass a unique `id` to each SignalLab when using several on a page.

```mdx
import Diagram from '../../components/Diagram.astro';
import SignalLab from '../../components/SignalLab.astro';

<Diagram code={`flowchart LR
  Input --> Filter --> Output
`} caption="A simple processing pipeline." />
<SignalLab id="example-filter" />
```

## Personalize

The homepage Donkey Kong animation converts the user-selected [Tenor GIF](https://tenor.com/view/donkey-kong-gif-9557225), found via [this Pinterest pin](https://www.pinterest.com/pin/donkey-kong-gif-donkeykong-discover-share-gifs--10625749111059803/), into colored text. `@chenglou/pretext` computes line breaks and glyph advances; Canvas samples and renders all 14 frames at their original 50 ms timing. The text frames are cached, so playback only copies the selected frame. Controls adjust detail, pause playback, and compare against the original at the same frame. Reduced-motion preferences pause initial playback, and animation sleeps offscreen or in a hidden tab.

Assets and timing metadata are checked in. To regenerate them, install Pillow and run `python scripts/prepare-kong.py` from the project root. The script composites GIF frames and removes near-white background at the image boundary and enclosed gaps below the face, preserving the eyes. The original media is third-party content, not an original project illustration.

Edit `src/pages/index.astro`, `src/pages/about.astro`, and pages under `src/pages/projects/`. Starter writing is explicitly labeled as examples; replace it with personal work when ready. Colors and typography live in `src/styles/global.css`. Fonts are self-hosted; no analytics are installed.

## Deploy

In repository Settings → Pages, select GitHub Actions as the source. Pushing to `main` runs checks, a static build, generated-site tests, and deployment. Pull requests validate without deploying. No personal token or repository secret is needed by the workflow. This root-domain repository needs no `base` path.

`npm test` checks built output, including local links, heading anchors, metadata, KaTeX, Shiki, the MDX demo, RSS, and sitemap. Run it after building. Browser checks should cover filtering, empty results, theme persistence, mobile layout, code copying, Mermaid rendering, and the interactive slider.
