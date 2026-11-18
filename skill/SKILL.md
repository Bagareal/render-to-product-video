---
name: render-to-product-video
description: From a grey 3D render plus real product photos, create a re-skin, a start frame in a described scene and a video that follows a reference camera move, keeping the product geometry locked. Use for product videos made from renders.
---

# render-to-product-video

Three generations, in order: re-skin of the render, start frame in a scene, video. The product geometry stays the one of the render in every step. Never generate the product from scratch.

The local scripts (in `scripts/`) cost no credits. Run them with `python3 -I`. Full documentation is in `docs/`.

## Fixed rules

- Images: always an editing model such as Nano Banana 2 or 2.1, with several input images. Do not use a general image generation model for the product: it deforms the product.
- Video: a model with a start image plus a motion-reference video (example: Seedance 2.5 reference-to-video). Audio off unless asked.
- Always show the start frame and wait for the user's approval before generating the video.
- If a check fails, say so and regenerate only that step. Never present a flawed result as good.
- Never describe the camera move from memory: inspect the reference every 0.5 s first.
- From the reference video copy only the camera path and timing.

## Step 0: inputs

1. Ask for attachments in chat (forms cannot carry files): the grey render, 1-2 real photos of the product (front and side), the camera reference video. If the real photos are missing, ask for them: they give the true colours.
2. Then use forms for: aspect ratio (16:9 by default, or 9:16 vertical), the environment (the user describes it or attaches photos; no presets), the light, the video duration and resolution, and scene content (a cup, steam, props).
3. Turn vague wishes into concrete light: direction, hardness, fall-off, what stays in shadow. A bare "edge light" produced random reflections.
4. 9:16: if the user provides a vertical reference video, use it. If the reference is 16:9, proceed but warn that the camera path is copied and the framing may change (the product can look narrower or get cropped); repeat the warning when showing the start frame.

## Step 1: canvas

If the render already has the target ratio, skip this. Otherwise pad it, never crop:

```
python3 -I scripts/pad_to_ratio.py render.png render_pad.png 16:9
```

Use `9:16` for vertical.

## Step 2: re-skin (plain background, no scene)

Image 1 = render, then the real photos. Prompt template in `docs/prompts.md` (section 1). Same aspect ratio as the canvas, 2K, high thinking level.

Verify:

```
python3 -I scripts/compare.py render_pad.png reskin.png side.png blend.png
```

The 50% overlay (`blend.png`) decides: contours, seams and proportions must line up with no double edges. The IoU is only a signal (a soft added shadow lowers it even when the product is right). If misaligned, regenerate this step.

## Step 3: start frame

Image 1 = re-skin, plus any photos of the desired environment. Prompt template in `docs/prompts.md` (section 2): the product stays completely unchanged, only the environment and light change.

Verify with the overlay against the re-skin. On a scene or dark background the IoU is meaningless: judge by eye.

Show the start frame to the user and wait for approval. Regenerate only this step if they want changes.

## Step 4: camera reference

```
python3 -I scripts/contact_sheet.py reference.mp4 reference_sheet.png 2
```

Look at every tile and write the camera path interval by interval. A continuous orbit passes the front view and keeps going. Do not speed up the reference to shorten the video: the first frame drifts. Reference limits: 1.8-30.2 s, 300-6000 px per side, aspect ratio 0.4-2.5, 24-60 fps, up to 200 MB.

## Step 5: video

Start frame = exact first frame, real photos for the sides the camera reveals, the reference as camera motion only. Prompt template in `docs/prompts.md` (section 3): assign a role to each input, say that the reference's grey look, plain background and framing must not be copied, state the camera path from step 4, that the product is static and rigid and only the camera moves, what stays constant, and that the light is slow, continuous and attached to the product with no flashes or random reflections. Parameters (Seedance 2.5): task `reference`, aspect ratio and resolution as chosen, duration as a string, audio off.

## Step 6: inspect the video

```
python3 -I scripts/contact_sheet.py video.mp4 sheet.png 2
```

Look at every tile. Report honestly: camera path against the reference, product rigidity, background constancy, legibility of text and logos, light behaviour, stray objects. Re-running never gives an identical result, so keep an accepted video.

Deliver in order: re-skin, start frame, video.

## Known failure modes

- General image models deform the product: use an editing model on the render.
- Material and scene changed in one edit shifts the perspective: re-skin first on the plain background, then the scene.
- Orbit described from first and last frame stops early: inspect every 0.5 s.
- Reference sped up 2x: the first frame drifts. Use the original.
- Grey look or plain background of the reference leaks: say explicitly that the reference is camera motion only.
- Random reflection or light streak: describe light attached to the product, slow, with direction and fall-off.
- Stray transparent object near the base, tiny coloured lights, a lighter front in the final frames: check on the contact sheet.
- Small panel text unreadable at 720p: use 1080p.
