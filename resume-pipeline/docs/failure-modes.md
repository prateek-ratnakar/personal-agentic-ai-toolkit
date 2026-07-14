# Documented failure modes

1. **Silent truncation.** One unclosed div: renderer clips everything past a point mid-word, emits no warning, and `pdfinfo` still reports 1 page. Page-count checks alone are worthless. Fix: programmatic tag-balance check + end-anchor grep on extracted text.
2. **Font-swap dead-end.** Swapping font-family to "fix" a viewer blank-page report just substitutes another embedded subsetted CID font and changes metrics (breaking the one-page fit). Real triage: pdffonts, rasterize-and-check-size, ghostscript parse, then a flattened image PDF as a delivery-vs-rendering diagnostic.
3. **Editor/sandbox sync gap.** Rapid successive editor writes can leave a stale partial file visible to the build shell. Fix: rewrite via heredoc in the build shell itself and re-verify byte count.
