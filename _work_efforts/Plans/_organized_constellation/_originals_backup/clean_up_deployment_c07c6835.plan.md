---
name: Clean Up Deployment
overview: Remove the unnecessary Workers deployment and fix the auto-deploy so only Pages (fogsift.com) gets deployed on git push.
todos: []
---

# Clean Up

Deployment

## Current State

- fogsift.com is live via Cloudflare Pages (working)
- localhost:5050 works via `wrangler pages dev` (working)
- A separate Workers deployment exists that you don't need

## Changes

1. **Delete the Worker** - Remove the `fogsift` Worker from your Cloudflare account (it deploys to fogsift.ctavolazzi.workers.dev which you don't need)
2. **Remove Worker files** - Delete these files that are only for the Worker:

- [src/index.js](src/index.js)
- [wrangler.jsonc](wrangler.jsonc)

3. **Fix Cloudflare Pages build command** - In the Cloudflare dashboard, change the build command from `npx wrangler deploy` to nothing (Pages just serves static files from `dist/`)