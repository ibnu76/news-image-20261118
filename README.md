# One image: Wednesday 18 November 2026

Entry for the make.fun bounty "Sum up 18 November's world news in one image"
([news-image-20261118](https://make.fun/bounty/news-image-20261118)).

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/ibnu76/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/ibnu76/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

## The image

A flat editorial infographic (1024x1024 PNG) summing up the world's news of
Wednesday 18 November 2026:

- **Lead — APEC opens in Shenzhen:** Xi Jinping meets Vladimir Putin; a
  trilateral summit with Donald Trump follows on Thursday.
- **Middle East:** US jets strike an Iranian missile site on Qeshm Island as
  Iranian drones target US installations in Kuwait and Bahrain; tankers burn
  in the Strait of Hormuz.
- **Europe:** Ukraine hits the Kerch Bridge a second day; part of the span
  collapses into the strait.
- **United States:** Mary Peltola wins the Alaska Senate seat; Democrats are
  projected to take the Senate 56-44.
- **Technology:** Nvidia posts a record $115.8B quarter as its board rules
  out Jensen Huang's return as CEO.
- **Weather:** Cyclone Akvan bears down on Andhra Pradesh, landfall expected
  around Friday.
- **Asia:** India and Japan hold their 2+2 ministerial dialogue in Tokyo.
- **Also on the day:** Ebola in DR Congo passes 11,000 cases; the US loses
  its measles-free status after 26 years; cold kills displaced people in
  Gaza tents.

Every story is a real event of 18 November 2026 as reported that day; the
date is named in the masthead so the image stands alone.

## How it is built

`render.py` draws the image with Python Pillow (flat shapes, all text
rendered by Pillow so no letter is garbled). Re-render it with:

```sh
python3 render.py
```

`main.ts` (Node 22, standard library only) is the entry program: it copies
`entry.png` to the output directory byte for byte, with no network access,
so two runs always write identical bytes:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Files

- `entry.png` — the image the judge sees (1024x1024, under 1 MiB)
- `main.ts` — the entry program
- `render.py` — the script that drew the image
- `LICENSE` — MIT
