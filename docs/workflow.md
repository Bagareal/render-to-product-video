# Workflow

The pipeline has six stages. Stages 2, 3 and 5 are generations (they cost credits); the others, and every verification, are local code or review.

## Stage 0: collect inputs

Required:

1. **Grey render** of the product at the exact camera angle wanted. Proportions and perspective in this image are final: nothing downstream is allowed to change them.
2. **Real photos** of the product (ideally front and side). They define true colours and materials, and they let the models keep the product correct when the camera later reveals sides that the render does not show well.
3. **Reference video** of the camera move: a clip where a camera does what you want (orbit, push-in, tilt). Only its camera path and timing are used.
4. **Scene and light description**, or photos of the desired environment.

Decisions to settle up front:

- **Aspect ratio.** 16:9 by default, 9:16 for vertical. If a vertical video is wanted but the camera reference is 16:9, the path is still copied but the framing may change (the product can look narrower or get cropped). Say so before generating.
- **Video duration and resolution.** Match the reference duration where possible. Use 1080p when panel text must stay readable.
- **Scene content.** Props, steam, a cup being filled and so on.

Translate vague wishes into concrete light: where it comes from, whether it is hard or soft, where it falls, what stays in shadow. "Cinematic edge light" on its own produced random reflections; "a thin soft rim light from behind-left grazing only the left edge, everything else in deep shadow" did not.

## Stage 1: prepare the canvas

If the render is not already at the target ratio, pad it with its own background colour. Never crop or rescale the product.

```bash
python3 -I scripts/pad_to_ratio.py render.png render_16x9.png 16:9
```

## Stage 2: re-skin (generation 1)

Edit the padded render with real materials. Keep the plain grey background and add no scene, no props, no shadows beyond what the render has.

Inputs to the image model: the render first, then the real photos. The prompt states that every contour, edge, seam and the silhouette must stay at the same pixel positions, and lists the real material and colour of each part, read from the photos.

**Verify** (local):

```bash
python3 -I scripts/compare.py render_16x9.png reskin.png side_by_side.png blend.png
```

Open `blend.png` (crop to the product if needed). If contours, seams and proportions line up with no double edges, continue. If not, regenerate this step only.

## Stage 3: start frame (generation 2)

Edit the re-skin: keep the product completely unchanged and change only the environment and light. The prompt repeats the "do not redraw, rotate, scale or reshape" rule and then describes the scene.

**Verify** with the same overlay. On a scene or dark background the IoU is meaningless (the background mask no longer works), so judge the overlay by eye.

**Stop and show the frame to the user.** The video is the most expensive generation, so the user approves the start frame first. If they want changes, regenerate only this step.

## Stage 4: study the camera reference

Never describe the camera move from memory or from the first and last frame. Extract a frame every 0.5 s and look at all of them:

```bash
python3 -I scripts/contact_sheet.py reference.mp4 reference_sheet.png 2
```

Write down, per interval, what the camera does: where it starts, how it turns, whether it passes the front and keeps going or stops, and when the move ends. Two lessons from earlier runs:

- A continuous orbit does not stop at the front view. Describing it as "ends frontal and holds" produced a video that stopped early.
- Do not speed up the reference to fit a shorter duration. It makes the first frame drift. If a full orbit is wanted, use the full-length reference and the matching duration.

Reference video limits (Seedance 2.5): 1.8 to 30.2 s, 300 to 6000 px per side, aspect ratio 0.4 to 2.5, 24 to 60 fps, up to 200 MB.

## Stage 5: video (generation 3)

Inputs: the approved start frame as the exact first frame, the real photos for the sides the camera will reveal, and the reference video as camera motion only. The prompt must say explicitly, per input, what it is for, and must say that the reference's grey look, plain background and framing are not to be copied.

State the camera path from stage 4, that the product is static and rigid and only the camera moves, what stays constant in the scene, and how the light behaves (slow, continuous, attached to the product, no flashes). Disable audio unless wanted.

## Stage 6: inspect the video

```bash
python3 -I scripts/contact_sheet.py output.mp4 output_sheet.png 2
```

Look at every tile and report honestly: camera path against the reference, product rigidity, background constancy, legibility of text and logos, light behaviour, stray objects. Do not present a flawed result as good: list the defects, then let the user decide whether to keep or regenerate. Re-running never gives the same result, so an accepted video should be kept.

## Delivery

Deliver, in order: the re-skin, the start frame, the video.
