FROM python:3.9-slim

WORKDIR mle-sprint-5

# установим необходимые библиотеки
RUN apt-get update && apt-get install -y libgomp1

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . ./mle-sprint-5
# COPY # ваш код здесь

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

# Соберём его:
# docker build -t uplift-model . 

# Запустим:
# docker run -p 5000:5000 uplift-model 

# Итак, сервис поднялся. Снова можно протестировать его запросом. Для разнообразия сделаем это с помощью curl:
# curl -X POST -H "Content-Type: application/json" -d '{"features": [10, 95.49,  0,  1,  1,  1,  0,  0,  0, 0,  1]}' http://localhost:5000/predict 

# Запуск Graphite из готового образа graphiteapp/graphite-statsd. Пояснения портов:
#     80: административный веб-интерфейс,
#     2003/8125: порты для сбора метрик по разным протоколам (newline delimited, pickle),
#     7002: порт для получения метрик.
# docker run -d \
#   --name graphite \
#   -p 80:80 \
#   -p 2003:2003 \
#   -p 8125:8125/udp \
#   -p 8126:8126 \
#   graphiteapp/graphite-statsd
# После запуска Graphite вы можете открыть его веб-интерфейс по адресу http://<ip address вашей ВМ>:80/.

# Запуск нашего сервиса.
# docker build -t uplift-model .
# docker run -p 5000:5000 --link graphite1:graphite uplift-model 

# Вы можете протестировать сервис, отправив запрос через curl или python:
# curl -X POST -H "Content-Type: application/json" \
# -d '{"features": [10, 95.49,  0,  1,  1,  1,  0,  0,  0, 0,  1]}' \
# http://localhost:5000/predict 