# Prompt templates

Replace everything in `[brackets]`. The wording of the geometry-locking sentences matters: keep them.

## 1. Re-skin

Image model, inputs in this order: the padded render (image 1), then the real photos (image 2, image 3). Same aspect ratio as the canvas, 2K, high thinking level where available.

```
Re-skin image 1: turn the grey 3D render of the [product], seen from [camera angle,
e.g. a three-quarter high angle / straight from above / front], into a photorealistic
product photo WITHOUT changing its geometry at all. Every contour, edge, corner, curve,
seam line and the whole silhouette must stay at exactly the same pixel positions as in
image 1. Keep the plain [colour] background of image 1 unchanged: no scene, no props,
no extra objects. Only paint real materials and colours taken from images 2 and 3:
[for each part: material and colour, e.g. "the top surface and frame are warm taupe
matte plastic", "the front panel is glossy black with printed icons", "the drip tray
is brushed stainless steel", "the water tank is smoked transparent plastic"].
Keep small embossed marks and printed logos where they are.
```

## 2. Start frame

Image model, input: the re-skin (image 1), plus any photos of the desired environment.

```
Keep the [product] in image 1 COMPLETELY UNCHANGED: same camera angle, same geometry,
same silhouette, same position and size in the frame, same materials and colours.
Do not redraw, rotate, scale or reshape the product. Only change the environment:
[scene, e.g. "a light marble countertop against a cream wall, a small potted plant
on the right, an orange kitchen towel resting on the counter"], with
[light, e.g. "soft daylight coming from the left, and the soft shadow of a window
falling on the wall"]. [Scene content, e.g. "A small cup with a little coffee stands
under the spout, the stream still running, with a little steam"].
No text, no extra objects.
```

Low-key variant (dark, cinematic), for the light sentence:

```
Pure black studio, matte black surface, no visible floor reflection. Cinematic low-key
lighting: the product sits mostly in deep shadow, with a single thin, soft-edged
[cold-white] rim light grazing only the [left] edge of the product from behind,
drawing a fine luminous line along the contour. Everything else is dark. No other
highlights, no flares, no glow spreading into the background.
```

## 3. Video

Video model with reference inputs. Parameters used with Seedance 2.5: task `reference`, the chosen aspect ratio and resolution, `duration` as a string, audio off.

```
@Image1 is the exact first frame: [one-sentence description of the start frame].
@Image2 and @Image3 are real photos of the product: use them only to keep it identical
when the camera reveals its sides and front.
@Video1 is a camera-motion reference ONLY: copy its camera path and timing
([camera path observed in the 0.5 s contact sheet, interval by interval]),
but do NOT copy its grey look, its plain background or its framing.
The product stays completely static and rigid; only the camera moves, and the product
changes perspective accordingly.
[What stays constant in the scene.] [Light behaviour: slow, continuous, attached to the
product, no flashes or random reflections.] [Scene action, e.g. the cup slowly filling.]
No cuts, no text, no overlays, no extra objects.
```

### Writing the camera path

Describe motion in the order of the contact sheet and mention the timing:

- Good: "starts at a high three-quarter view on the left, orbits continuously to the right, passes the front view at about 6 s without stopping, and continues towards the right side until the end."
- Bad: "orbits to the front and holds."

### Writing the light

- Give a direction, a hardness, a fall-off and what stays dark.
- Describe moving light as attached to the product and slow. Words like "sweeps", "passes", "cinematic flare" tend to produce reflections that cross the product at random.
