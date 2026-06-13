---
name: virtual-influencer-fashion-tryon
description: Use when making photorealistic GPT Image 2 prompts for authorized AI influencer/model fashion try-on, outfit reference transfer, 실사 고퀄리티 이미지, identity-preserving lookbook images, or clothing/style changes while preserving face, hair, body proportions, and realistic photo texture.
---

# Virtual Influencer Fashion Try-On

## Overview

Use this when 사용자 provides a model identity image and one or more outfit/fashion references, then asks to change the model’s clothing/style. The proven pattern is: **identity image first, one fashion reference per run, strict invariants, outfit-specific garment details, and targeted negative prompts**.

## When to Use

- AI influencer/model outfit replacement or virtual try-on.
- “이 모델 의상을 이 레퍼런스처럼 바꿔줘.”
- Creating full-body lookbook images from a face/identity reference.
- Preserving bangs, face, makeup, body proportions, phone-flash realism while changing fashion styling.

Do not use for unrelated generic fashion moodboards or non-identity-preserving image generation.

## Input Roles

For each generation, label images explicitly:

1. **Image 1 — identity anchor:** the model face/body reference.
2. **Image 2 — fashion reference:** one outfit/style only.
3. **Image 3 — optional composition reference:** pose/background/framing if needed.

Avoid attaching many fashion references at once unless blending is intended. Multiple outfit references often merge garments incorrectly.

## Global Identity Lock

Use this at the top of every prompt:

```text
Use our model image as the strict identity anchor. Preserve the same woman: same face, same facial proportions, same long glossy black hair with straight bangs, same eye shape, same soft glam makeup, same glossy lips, same skin tone, same slim body proportions, same natural asymmetry, and same realistic phone-camera/direct-flash texture. Do not change her age impression, ethnicity, face shape, hairstyle, bangs, makeup style, body proportions, or skin texture. Only change the outfit, accessories, pose, and styling according to the fashion reference. Photorealistic, realistic fabric and shadows, no plastic skin, no doll look, no watermark, no text.
```

## Common Negative Prompt

```text
different person, identity drift, changed face, changed facial proportions, changed eye shape, changed hairstyle, missing bangs, short hair, blonde hair, changed makeup, plastic skin, doll-like face, exaggerated body, body shape change, bad anatomy, bad hands, extra fingers, missing fingers, warped legs, deformed feet, fake clothing, melted fabric, text, watermark, logo, cartoon, CGI, over-retouched skin
```

## Prompt Template — Existing Pose, Outfit Replacement Only

```text
Use the provided base model image as the strict identity and composition source. Preserve the same woman, same face, same facial proportions, same long glossy black hair with straight bangs, same makeup, same skin tone, same direct eye contact, same pose, same body proportions, same hands, same background, same direct flash phone-camera realism, and same vertical crop.

Change only her outfit and styling to match the attached fashion reference image: [describe exact garments: top, bottom, shoes, bag, accessories, colors, fabric, closures, silhouette]. Keep the outfit realistic on her body, with natural fabric tension, accurate seams, buttons, collar, pockets, skirt/pants texture, shoe details, and natural shadows. [style mood keywords].

Do not change her face, hair, expression, pose, background, camera angle, lighting, skin texture, or body proportions. No text, no watermark, no extra people.
```

## Prompt Template — Full-Body Lookbook

```text
Create a photorealistic full-body vertical 9:16 fashion photo of the exact same woman from the identity image. Preserve her same face, long glossy black hair with straight bangs, soft glam makeup, glossy lips, direct confident gaze, natural skin texture, and slim body proportions. Keep the same realistic phone-camera/direct-flash texture and candid editorial mood.

Dress her exactly in the outfit style from the attached fashion reference: [top], [bottom], [shoes], [bag/accessories], with accurate garment construction: [buttons/collar/placket/laces/eyelets/pockets/fabric texture]. Pose her [standing/seated/leaning] so the full outfit is visible from head to shoes. Use [simple studio/warm indoor/city] background. [mood keywords].

No change to identity, no face drift, no different person, no exaggerated body, no text, no watermark, no brand logo.
```

## Outfit Analysis Checklist

Before writing the prompt, extract:

- Top: neckline, sleeve length, fit, buttons/placket, fabric, transparency.
- Bottom: skirt/pants length, silhouette, waist, texture, pattern.
- Shoes: height, closure, sole, heel, material.
- Bag/accessories: glasses, jewelry, headphones, belts, straps.
- Pose/framing: full-body vs existing crop.
- Mood: Korean casual, Y2K, gothic, utilitarian, editorial, etc.

## Proven Style Examples

### Dark Y2K Korean Streetwear

```text
fitted charcoal gray short-sleeve button-up collared shirt, slim waist fit, slightly curved/asymmetrical button placket, black mini skirt with subtle tonal swirl embroidery, knee-high black lace-up combat boots with metal eyelets and thick soles, silver hoop earrings, layered silver necklaces, dark feminine Korean streetwear, Y2K casual gothic editorial style
```

Negative add-ons:

```text
leather crop top remaining, old belt remaining, pants remaining, missing collar, missing buttons, deformed shirt placket, distorted skirt pattern, missing laces, missing eyelets
```

### Clean City Casual

```text
light blue relaxed button-up shirt worn open, fitted black sleeveless tank top underneath, cream/off-white long straight midi skirt, thin black belt, black Mary Jane flats, large off-white canvas tote bag, silver headphones hanging from the bag strap, black rectangular glasses, delicate silver pendant necklace, Korean casual city minimal style
```

### Apron Utility Layering

```text
white short-sleeve crewneck T-shirt under a dark navy-black sleeveless apron dress / utility pinafore, long apron panels, side tie strings, large cargo-style pockets, loose wide black trousers, chunky beige-gray sneakers, pastel lavender shoulder bag, thin black choker, Japanese/Korean layered streetwear
```

### Romantic Gothic Editorial

```text
white short-sleeve collared blouse with delicate lace/crochet eyelet sleeve panels, long black layered tulle or lace skirt with sheer textured volume, black platform sandals, seated sideways on a modern chair, strong clean shadow on white wall, romantic gothic vintage feminine art-school editorial
```

## Common Mistakes

- Attaching five outfit references at once → mixed or hallucinated outfit. Generate one style at a time.
- Under-specifying garment construction → melted buttons, missing laces, wrong skirt length. Include seams/buttons/placket/laces/eyelets/pockets.
- Asking for boots in a cropped image → boots disappear. Use full-body lookbook template.
- Over-describing the model’s face in creative terms → identity drift. Use the fixed identity lock, not reinterpretation.
- Letting logos/text appear → include `no text, no watermark, no logo` unless exact text is required and separately controlled.

## Session References


## Verification

After generation, check:

- Face, bangs, makeup, and body proportions still match identity anchor.
- Outfit matches the reference as a coherent single look.
- Hands/legs/shoes are not distorted.
- Full-body prompt actually shows head-to-shoes when needed.
- Text/logos/watermarks are absent.
