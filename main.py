# Задание 1 из 2
# Дополните код скрипта. Скрипт сохраните как main.py. 
# Для этого вам нужно загрузить ранее сохранённую модель, извлечь признаки из данных и получить предсказания.
# Добавьте метрики в сервис

from fastapi import FastAPI, HTTPException, Request
from statsd import StatsClient
import pickle
import numpy as np

# загружаем модель
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# создаём приложение FastAPI
app = FastAPI(title="uplift")

stats_client = StatsClient(host="localhost", port=8125, prefix="uplift")

@app.post("/predict")
async def predict(request: Request):

    # запомните время начала обработки запроса
    start_time = # ваш код здесь

    stats_client.incr("requests")

	# все данные передаются в json
    try:
        data = await request.json()
    except Exception as e:
        stats_client.incr("errors.invalid_json")
        raise HTTPException(status_code=400, detail="Invalid JSON format")

	# признаки лежат в features, в массиве
    # извлекаем и преобразуем признаки
    # извлекаем и преобразуем признаки
    try:
        features = data["features"]
        features = np.array(features).reshape(1, -1)
    except Exception as e:
        stats_client.incr("errors.invalid_features")
        raise HTTPException(status_code=400, detail="Invalid features format")

    # получаем предсказания
    try:
        prediction = model.predict(features)[0][0]
    except Exception as e:
        stats_client.incr("errors.model_prediction")
        raise HTTPException(status_code=500, detail="Model prediction error")

    # посчитайте время обработки запроса в секундах как разницу 
    # между текущим временем и start_time
    response_time = # ваш код здесь

    stats_client.timing("response_time", response_time)
    stats_client.incr("response_code.200")
    stats_client.gauge("predictions", prediction)

    return {"prediction": prediction.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)