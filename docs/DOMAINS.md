# Free Domain Options

CANON now deploys as two pieces:

```text
Static frontend  -> Vite build output in dist/
Python API       -> api.main:app
```

That means the cleanest free setup is a static-site host for the frontend plus a Python host for the API.

## Recommended Primary URL

Use Cloudflare Pages for the frontend:

```text
canon-policy.pages.dev
```

Why this fits:

- Vite produces static files in `dist/`
- the frontend is easy to host for free
- the URL is cleaner than many platform subdomains
- a future custom domain can point at the same Pages project

## Python API URL

Host the Python API separately on a Python-capable platform such as Render, Fly.io, Railway, or a VPS:

```text
https://canon-policy-api.<host>.com
```

Then set this during frontend build:

```bash
VITE_API_BASE_URL=https://canon-policy-api.<host>.com
```

For local development, leave `VITE_API_BASE_URL` empty and let Vite proxy `/api` to `http://127.0.0.1:8000`.

## Best Custom-Looking Free Alias

Use `is-a.dev` after the app has a live target:

```text
canon.is-a.dev
```

This requires a GitHub PR to the `is-a-dev/register` repository with a DNS record that points to the deployed frontend. Do this only after a stable `pages.dev` or equivalent frontend target exists.

## Avoid

Avoid free root-domain offers such as `.tk`, `.ml`, or old Freenom-style domains for a serious portfolio project. They often have reliability, reputation, or ownership issues.
