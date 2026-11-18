# Verification

All checks run locally. They cost no generation credits and never regenerate anything. If a check fails you regenerate that single step, and that is the only cost.

## Geometry: overlay and IoU

```bash
python3 -I scripts/compare.py reference.png generated.png side_by_side.png blend.png
```

- `side_by_side.png`: reference on the left, generated on the right, at half size.
- `blend.png`: 50% overlay. This is the verdict. If the product's contours, seam lines and proportions line up, the geometry is preserved. Double contours or ghosting mean the model moved or reshaped something: regenerate.
- **IoU** (Intersection over Union): the area shared by the two silhouettes divided by the area covered by either. 1.0 means identical silhouettes. The silhouette is every pixel that differs from the background colour sampled at the top-left corner.

### Reading the IoU honestly

The IoU is a signal, not the verdict:

- It drops when the generator adds a soft shadow or a reflection, because the silhouette grows. A re-skin with a correct product and a soft added shadow scored 0.646.
- It becomes meaningless when the background changes (a scene, a dark backdrop), because the mask no longer isolates the product. A scene start frame compared with its re-skin scored 0.25 with the product perfectly aligned.

Use the number only to catch large problems (a very low value on a plain-background re-skin), and decide with the overlay.

## Camera reference and video: contact sheet

```bash
python3 -I scripts/contact_sheet.py video.mp4 sheet.png 2
```

Extracts a frame every 0.5 s (argument `2` is frames per second), labels each with its timestamp and tiles them. The script only prepares the image; the judgement is yours (or Claude's, looking at it).

Checklist for a generated video:

1. **Camera path** matches the reference: same start, same direction, same timing, no early stop.
2. **Product** stays rigid: no parts moving, melting or changing shape between frames.
3. **Background and scene** stay constant, and the first frame matches the approved start frame.
4. **Text and logos** stay legible when they should be.
5. **Light** behaves as described, without flashes, random reflections or glow in the background.
6. **Stray objects**: transparent shapes near the base, small coloured lights, extra props.
7. **Cup / liquid / steam** (if any) behave naturally.

Report defects plainly. A result with known defects is not presented as good.

## When to regenerate

| Observation | Action |
|---|---|
| Overlay shows double contours after the re-skin | Regenerate the re-skin |
| Overlay on the start frame shows the product moved or resized | Regenerate the start frame |
| Start frame fine, video drifts from the first frame | Check that the reference was not sped up; regenerate the video |
| Small artefact the user accepts | Keep the video; re-runs will not be identical |
