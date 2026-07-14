# resume-pipeline

Deterministic build-and-verify pipeline for one-page ATS-clean resume PDFs. Extracted from a real senior-level job search where "looks fine" repeatedly wasn't.

## Build
- HTML templates with a shared stylesheet; per-archetype accent colors
- `display:table` for right-aligned date rows (survives pagination edge cases where flex can misbehave)
- Binary-search on line-height to land exactly one page at **94-97% vertical fill with real content** - never spacing inflation; if fill is low, the fix is more content, not more leading

## Verify (a build is unfinished until all pass)
1. **Tag balance** - count open vs close for div/ul/li/span; an imbalance of one silently truncates output in some renderers with no warning and a correct page count
2. **Non-ASCII scan** - arrows, em-dashes, and middle dots break ATS parsers
3. **End-anchor grep** - the last words of the final section must appear in `pdftotext` output, proving nothing was silently clipped
4. **Fill measurement** - rasterize page 1, find the lowest content row, assert 94-97%
5. **Visual pass** - render to PNG and actually look at it

## Hard-won failure modes documented in docs/
- Silent truncation from a single unclosed div (page count stays 1; content vanishes mid-word)
- Font-swap as a dead-end fix for viewer blank-page reports
- Editor-to-sandbox file sync gaps under rapid successive writes
