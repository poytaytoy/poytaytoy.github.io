# Clement's notebook

Hugo + PaperMod at https://poytaytoy.github.io/.

## Run locally

Install Hugo **0.168.0** (standard edition is sufficient) and Git. Clone with the theme:

```sh
git clone --recurse-submodules https://github.com/poytaytoy/poytaytoy.github.io.git
cd poytaytoy.github.io
hugo server -D
```

For an existing clone, run `git submodule update --init --recursive` first. PaperMod is pinned to the commit recorded in Git; do not replace it with a floating download.

## Write

Create a draft with `hugo new content posts/my-post.md`. Edit the Markdown file in `content/posts/`, set its title, date, and description, and change `draft: true` to `draft: false` when ready. Future-dated posts are excluded until their publication date.

Edit `content/about.md` and `content/projects.md` for the main pages. Site title, introduction, navigation, and theme options are in `hugo.toml`.

## Validate and publish

```sh
hugo --gc --minify
```

Push to `main` to build and publish through GitHub Actions. Pull requests run the build and generated-site checks without deploying. Repository Settings → Pages must use **GitHub Actions** (already configured during migration). No personal token is required by the workflow.

The site uses the root URL, so no repository-name URL prefix is needed. Generated `public/` output stays out of Git.

With Hugo 0.168.0, the pinned PaperMod version emits upstream deprecation warnings for `LanguageDirection` and `LanguageCode`. These are non-fatal; the production build and generated-site checks still run normally.

## Theme updates and history

To update PaperMod deliberately, run `git submodule update --remote themes/PaperMod`, run the validation above, and commit the changed theme reference. Hugo is pinned in the workflow; test locally before changing that version.

The former Astro site remains in Git history through commit `f9d1e0e`. This migration replaces its active pages and interactive demos with a minimal Hugo site. Use Git history to recover old content if desired.


## Profile homepage

Edit `content/_index.md` to change the homepage heading and introduction using Markdown. The homepage uses PaperMod profile mode; posts appear on `/posts/`. Navigation and social links stay in `hugo.toml`. The homepage loads the avatar directly from GitHub using the profile image URL in `hugo.toml`; avatar changes appear after GitHub/browser caches refresh. The small `layouts/_partials/index_profile.html` override renders the Markdown introduction, and `assets/css/extended/profile.css` controls its width and avatar shape.
