---
name: Jekyll Local Dev Setup
overview: Set up local Jekyll development environment and create a "Getting Started" wiki page to demonstrate the contribution workflow.
todos:
  - id: check-ruby
    content: Verify Ruby is installed and check version
    status: completed
  - id: create-gemfile
    content: Create Gemfile with Jekyll and plugins
    status: completed
    dependencies:
      - check-ruby
  - id: bundle-install
    content: Run bundle install to install dependencies
    status: in_progress
    dependencies:
      - create-gemfile
  - id: start-server
    content: Start Jekyll local server
    status: pending
    dependencies:
      - bundle-install
  - id: create-wiki-page
    content: Create _wiki/getting-started.md with content
    status: pending
    dependencies:
      - start-server
  - id: verify-demo
    content: Verify page appears and renders correctly
    status: pending
    dependencies:
      - create-wiki-page

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Jekyll Local Dev + Demo Wiki Page

## Phase 1: Environment Setup

1. **Check Ruby availability** - Run `ruby -v` to verify Ruby is installed (macOS ships with it)

2. **Create Gemfile** - Add a [`Gemfile`](Gemfile) with Jekyll and required plugins:
   - jekyll
   - jekyll-feed
   - jekyll-sitemap
   - webrick (required for Ruby 3.0+)

3. **Install dependencies** - Run `bundle install` to install gems

4. **Start local server** - Run `bundle exec jekyll serve` to start at http://localhost:4000

## Phase 2: Create Demo Wiki Page

5. **Create new wiki page** - Add [`_wiki/getting-started.md`](_wiki/getting-started.md) with:
   - Front matter (title)
   - Welcome content for new CFL members
   - Basic info about the space, hours, how to join
   - Links to other wiki pages

6. **Verify locally** - Check that the new page appears on the homepage and renders correctly

## File Changes

```mermaid
flowchart LR
    subgraph new_files [New Files]
        Gemfile
        GettingStarted[_wiki/getting-started.md]
    end
    subgraph existing [Existing - No Changes]
        Config[_config.yml]
        Index[index.html]
        Layout[_layouts/default.html]
    end
    Gemfile --> Jekyll[Jekyll Server]
    Jekyll --> Preview[localhost:4000]
    GettingStarted --> Preview
```

## Expected Result

- Local Jekyll server running at http://localhost:4000
- Homepage lists 3 wiki pages: CFL Kiosk, CFL Task Dashboard, Getting Started
- New "Getting Started" page accessible at /wiki/getting-started