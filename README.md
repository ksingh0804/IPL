# IPL
### Founded in 2008 by the Board of Control for Cricket in India (BCCI), the IPL is a professional Twenty20 cricket competition. IPL Data Visualization and Analysis Project will investigate interesting insights from IPL data such as the most runs scored by a player, the most wickets taken by a player, and much more from the IPL seasons 2008-2017.

## Development setup

This project is a Jupyter notebook analysis built around `IPL.ipynb` and the
CSV data files in the repository.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/bootstrap_legacy_data.py
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser
```

Then open `http://127.0.0.1:8888/tree` and launch `IPL.ipynb`.

`scripts/bootstrap_legacy_data.py` restores the missing companion
`Deliveries.csv` file and the legacy ThinkStats helper modules used by the
notebook.
