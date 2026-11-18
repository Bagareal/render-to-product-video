# Troubleshooting

Failure modes seen while building this pipeline, with the fix for each.

## The product is deformed

**Cause.** The product shot was generated from a description plus a loose reference.
**Fix.** Use an image editing model on the render itself. Stage 2 repaints only materials; stage 3 changes only the environment. Verify each with the overlay.

## The perspective differs from the render

**Cause.** Material change and scene change done in one edit, or the model rebuilt the view. The result can look plausible and still be at a different angle.
**Fix.** Split into two edits (re-skin on the plain background, then the scene) and always check the overlay. Do not trust a quick visual comparison; overlay it.

## Low IoU but the product looks right

**Cause.** A soft shadow or reflection widened the silhouette, or the background changed.
**Fix.** Judge by the 50% overlay. See [verification.md](verification.md).

## The camera orbit stops early or does the wrong move

**Cause.** The move was described from the first and last frames or from memory.
**Fix.** Extract a frame every 0.5 s (`contact_sheet.py`), read the whole sheet, and describe the move interval by interval. A continuous orbit passes the front view and keeps going.

## The first frame drifts, or the clip looks wrong in time

**Cause.** The reference video was sped up to fit a shorter duration.
**Fix.** Use the original reference and a duration that matches it. For a full orbit use the full-length reference.

## The grey look or plain background of the reference leaks into the video

**Cause.** The prompt does not say that the reference is for camera motion only.
**Fix.** State it explicitly: the reference supplies the camera path and timing, not its grey look, plain background or framing.

## A random reflection or light streak crosses the product

**Cause.** Light described as something that "sweeps" or "passes" the product, with no anchor.
**Fix.** Describe the light as attached to the product, with a direction, a fall-off and slow, continuous changes, and say "no flashes or random reflections".

## A small stray object appears near the base

**Cause.** Model artefact, often in the last seconds.
**Fix.** Report it. If the user accepts the result, keep it. Re-runs are not identical, so an accepted video is worth keeping.

## Tiny coloured light or dot on a part of the product

**Cause.** The model amplifies small indicator details from the photos or render.
**Fix.** Check for it on the contact sheet. If it matters, regenerate or mention in the prompt that no indicator lights are lit.

## Text on the product is unreadable

**Cause.** Low resolution.
**Fix.** Render at 1080p. Small panel text is the first thing lost at 720p.

## Vertical (9:16) output looks cropped or the framing changed

**Cause.** The camera reference is 16:9, the output is 9:16.
**Fix.** Provide a vertical reference. Without one, the camera path is still followed but the framing can change; show the start frame in the target ratio first and warn the user.
