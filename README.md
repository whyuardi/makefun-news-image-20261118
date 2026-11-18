# The World in One Day — 18 November 2026

[![make.fun](https://make.fun/badge.svg)](https://make.fun/bounty/news-image-20261118)

A newspaper front page that sums up Wednesday 18 November 2026 in one
image: the Gulf escalation (U.S. strikes on Qeshm Island, Iran's drone
answer on Bahrain and Kuwait), the Kerch Bridge hit again, the Xi–Putin–
Trump meeting in Shenzhen, Peltola's Alaska Senate win, the Congo Ebola
outbreak, the U.S. losing measles-free status, Voyager 1 reaching one
light-day — plus a ticker with the Siberia crash and Cyclone Xavier.

The image is drawn entirely in code (`render.py`, PIL + DejaVu, no
external assets, no network) and stored as `entry.b64`; `main.py`
decodes it to `/output/entry.png` (1024×1024 PNG, deterministic).

Run locally: `MAKEFUN_OUTPUT_DIR=out python3 main.py`
