# 75-second demo storyboard

> **Production safety:** Keep the persistent corner label `FULLY SYNTHETIC · NO REAL CITATIONS` visible from first frame to last. Do not present the toy hydrogel as a scientific result. Do not animate a Crossref “verified” state; the placeholder DOIs are deliberately non-resolving.

Target duration: 75 seconds. Format: 16:9 screen recording; the same sequence can be exported as a silent GIF by replacing narration with the listed on-screen copy.

| Time | Screen action | Voice-over | On-screen copy |
|---:|---|---|---|
| 0–6 s | Open the example README, then zoom to the synthetic notice. | “This is a fully synthetic paper demo—no real experiments, people, citations, or resolvable DOIs.” | `FULLY SYNTHETIC · NO REAL CITATIONS` |
| 6–15 s | Split screen: highlight the input title and the phrases “universally safe,” “closed loop,” and “clinical readiness.” | “The same toy numbers are made to claim universal safety, autonomous discovery, and clinical readiness.” | `Fluent prose ≠ supported science` |
| 15–24 s | Run `cns_audit.py` on the input; pause on `FAIL (4 defect hits)` and `7` high-risk sentences. | “The audit finds four reader-visible production defects and seven high-risk claim sentences.” | `TODO + editor note + author query + output label` |
| 24–34 s | Open the claim-citation report; animate CC-02 and CC-04 from red to resolved. | “Claim review separates retrospective ranking from a real experimental loop—and removes a wound-healing claim that was never measured.” | `Retrospective ≠ closed loop` |
| 34–44 s | Show cross-reference report: Figure 2 missing; Figure 1 and Table 1 orphaned. Then reveal the clean after state. | “Figure and table references are repaired, with every display introduced in the text.” | `3 cross-reference issues → 0` |
| 44–55 s | Pan across the revised abstract and Methods sentences naming 12 training rows, six holdout rows, one batch, and three technical wells. | “The revision keeps the values but restores their limits: one fictional batch, technical wells, descriptive outcomes, and no inferential statistics.” | `Keep the number. Narrow the inference.` |
| 55–63 s | Reveal `figure-1.svg`; point to circle/square encoding and the caption’s no-error-bar explanation. | “The figure remains auditable: editable source, frozen data, shape-plus-color encoding, and an explicit uncertainty boundary.” | `No independent replicates → no error bars` |
| 63–70 s | Run `reproduce_demo.py --check`; hold on PASS and the H-07 ranking. | “A standard-library script regenerates all 18 rows and reproduces the retrospective ranking.” | `18 deterministic rows · zero external packages` |
| 70–75 s | Run strict clean-copy and cross-reference checks on the revised Markdown; end on both PASS states and the repository name. | “The after copy passes the Markdown gates. DOCX rendering and page-by-page QA still come next.” | `Evidence-calibrated. Auditable. Still honest about what remains.` |

## Silent GIF variant

Use frames at 0, 7, 16, 25, 35, 45, 56, 64, and 71 seconds. Hold each frame for 2.5–4 seconds, use a 0.25-second cross-fade, and keep captions under 11 words. End with a two-line boundary rather than a marketing superlative:

```text
Stronger writing cannot replace missing evidence.
CNS Skills makes that boundary visible.
```

## Recording checklist

- Record only this public synthetic fixture; close unrelated files and notifications.
- Keep terminal paths cropped to the repository-relative portion.
- Do not show account tokens, Git configuration, usernames, or unpublished documents.
- Use the actual audit output; do not mock PASS states.
- If the DOCX has not yet been rendered and inspected, say “DOCX QA pending,” exactly as shown above.
- Add captions to the video and alt text to the thumbnail.
