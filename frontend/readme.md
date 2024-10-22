0. Clone repo
1. Install python 3.12
2. Install poetry, run cmd as admin and type:
```
pip install python3-poetry
```
3. Install dependencies:
```
poetry install
poetry shell
```

4. Install docker desktop.
5. Run docker container with posgreSQL DB:
```
docker compose up -d
```
6. Create `.env` file in the root of the project.
   This file will be contain secret data for DB access.
7. Start server
```
python ./backend/main.py
```
8. Go to the swagger `http://127.0.0.1:8000/docs`
All endpoints described here.

9. Write code