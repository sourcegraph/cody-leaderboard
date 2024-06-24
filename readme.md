# Cody Leaderboard

This repo contains benchmarks to measure Cody quality for different language
models, programming languages and feature flags. This repo is a
work-in-progress. More documentation will be added later. In the meantime, reach
out to [@olafurpg](https://github.com/olafurpg) if you want to learn more.

## Streamlit

Setting up the virtual environment:

1. Install uv (A Python package installer and resolver): `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. To create a virtual environment: `uv venv`
3. To activate the virtual environment: `source .venv/bin/activate`
4. To install packages into the virtual environment: `uv pip install -r requirements.txt`

To run the leaderboard:

1. `streamlit run [leaderboard.py](http://leaderboard.py/)`
