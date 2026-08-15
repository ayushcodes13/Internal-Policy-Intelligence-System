# Free Domain Options

CANON should use a free deployment subdomain first, then a cleaner alias if the demo starts getting real traffic.

## Recommended Primary URL

Use Cloudflare Workers:

```text
canon-policy.<your-cloudflare-subdomain>.workers.dev
```

Why this fits:

- the app has a full-stack API route, not just static pages
- Workers gives a free `workers.dev` hostname
- the project name `canon-policy` is short, clear, and likely to look good in a deployment URL
- Cloudflare can later attach a custom domain without changing the app

## Good Backup URL

Use Cloudflare Pages:

```text
canon-policy.pages.dev
```

This is cleaner visually, but Workers is the better match if the app is deployed through OpenNext Cloudflare as a full-stack Next.js Worker.

## Best Custom-Looking Free Alias

Use `is-a.dev` after the app has a live target:

```text
canon.is-a.dev
```

This requires a GitHub PR to the `is-a-dev/register` repository with a DNS record that points to the deployed app. Do this only after a stable `workers.dev`, `pages.dev`, or `vercel.app` target exists.

## Avoid

Avoid free root-domain offers such as `.tk`, `.ml`, or old Freenom-style domains for a serious portfolio project. They often have reliability, reputation, or ownership issues.

## Cloudflare Deploy Commands

Install and authenticate Wrangler:

```bash
npx wrangler login
```

Set production secrets:

```bash
npx wrangler secret put GROQ_API_KEY
npx wrangler secret put GEMINI_API_KEY
```

Build and deploy:

```bash
npm run build:index
npm run cf:deploy
```

The Worker name is configured in `wrangler.jsonc`:

```text
canon-policy
```
