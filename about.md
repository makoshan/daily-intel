---
title: About Daily Intel
description: A 1:1 replica of Gwern.net design principles applied to Daily Intel.
created: 2026-02-09
status: finished
confidence: highly likely
importance: 10
css-extension: dropcaps-kanzlei
---

# Introduction

Welcome to **Daily Intel**, a project built with the design philosophy of [Gwern.net](https://gwern.net/). This site uses the powerful Hakyll static site generator to provide advanced features like:

-   **Sidenotes**: Marginal notes for better readability.
-   **Popups**: Hover over links to see previews.
-   **Typography**: High-quality typography with dropcaps and small caps.

## Design Philosophy

> [!NOTE]
> This page demonstrates the "1:1 replica" of the design.

As noted in the [Design Guide](/gwern-net-design), the goal is to create a reading experience that respects the reader's attention.

### Features

1.  **Semantic Zoom**: Drill down into content.
2.  **Transclusion**: Include content from other pages.
3.  **Backlinks**: See what links here.
4.  **[Live Demo](/posts/2024-02-09-design-demo)**: See these features in action.

<div class="collapse">
### Collapse Example

This section is collapsed by default. You can expand it to read more details about the implementation.

The build system uses Haskell and Pandoc to compile Markdown files into HTML, applying complex transformations for typography and interlinking.
</div>

## Technical Details

The site is built using:
-   [Hakyll](https://jaspervdj.be/hakyll/)
-   [Pandoc](https://pandoc.org/)
-   CSS framwork from Gwern.net

See the [Build Guide](/BUILD_INSTRUCTIONS) for how to build this site.
