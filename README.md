### FMJ is created to help college students like ourselves to find which field is right for them through real data scrapped in real time.
### And if you do know which field you wish to advance in, but are curious about which skills would result in you getting hiered or getting a hike, it can help you there as well again with real data.

We are actively working on this project but we have'nt yet deployed this application so if you want to use this right now, then you would need to set it up locally.

# Installation

## With Docker
Make sure you have [docker](https://docs.docker.com/engine/install/) installed.
```
git clone https://github.com/find-me-a-job/find-me-a-job.git
cd find-me-a-job/backend
docker build -t fmj-backend .
docker run -p 5000:5000 fmj-backend
```
If your terminal is hung after a docker command then you might need to use sudo
```
sudo docker build -t fmj-backend .
sudo docker run -p 5000:5000 fmj-backend
```

## Without Docker
### Mac & Linux
- Install a non-ancient version of [python](https://www.python.org/downloads/)
- Install poetry
```
# igonre if already installed
curl -sSL https://install.python-poetry.org | python3 -
```
  
```
git clone https://github.com/find-me-a-job/find-me-a-job.git
cd find-me-a-job/backend
poetry install
cd backend
poetry run python3 main.py
```
This would just startup the backend server, you would still need to use a service like postman to send http requests to server inorder to get an output. We are working on providing a docker-compose file so that the whole project can be setted up locally with one single command...
