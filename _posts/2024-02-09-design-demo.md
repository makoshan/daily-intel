---
title: Design Demo
description: A comprehensive demonstration of the Daily Intel design features, including sidenotes, popups, diverse typography, and interactive elements, serving as a testbed for the Gwern.net 1:1 replica.
created: 2024-02-09
status: in progress
confidence: log
importance: 10
css-extension: dropcaps-kanzlei
---

<div class="abstract">
> **Daily Intel** aims to be a high-performance, aesthetically pleasing, and functionally rich platform for knowledge sharing.
>
> This page serves as a live demonstration of the design system inherited from Gwern.net. It showcases the core capabilities: advanced typography, [sidenotes](/sidenote "Explaining the sidenote mechanism"), collapsible sections, and bidirectional linking. The goal is to verify that the ported build system correctly renders these complex features in the `Daily Intel` environment.
</div>

# Typography

<div class="epigraph">
> Type is speech made visible.
>
> *Type & Lettering*, [William Morris](https://en.wikipedia.org/wiki/William_Morris)
</div>

The foundation of the design is **typography**. We use specific font stacks to ensure readability and aesthetic appeal.

-   **Small Caps**: Used for [acronyms]{.smallcaps} like NASA or FBI, and for stylistic emphasis.
-   **Drop Caps**: The first letter of the article (and potentially sections) can be stylized.
-   **Monospace**: `Use for code` and technical terms.

## Sidenotes & Footnotes

Sidenotes are a key feature, allowing commentary without breaking the flow of the main text.

Here is a statement that requires elaboration.[^1]

[^1]: This is a sidenote. It appears in the margin on wide screens and as a popup/footer on smaller screens. It can contain *formatting*, [links](https://example.com/), and even images.

# Interactive Elements

<div class="collapse">
## Collapsible Section

This content is hidden by default. It is useful for:
1.  Long code blocks.
2.  Tangential details.
3.  Spoilers.

> The user controls the "semantic zoom" of the document.
</div>

# Mathematical Notation

The site works well with math, rendered via MathJax.

$$ e^{i\pi} + 1 = 0 $$

Inline math like $E = mc^2$ is also supported.

# Code Syntax Highlighting

```haskell
-- Example Haskell code
main :: IO ()
main = putStrLn "Hello, Daily Intel!"
```

# Conclusion

This document verifies that the *Daily Intel* build system is functioning as expected, reproducing the sophisticated "Gwern.net" design.
