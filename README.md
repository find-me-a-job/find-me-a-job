### [FMJ](https://findmeajob.info) is created to help college students like ourselves to find which field is right for them through real data scrapped in real time.
### And if you do know which field you wish to advance in, but are curious about which skills would result in you getting hiered or getting a hike, it can help you there as well again with real data.

# Setup Locally

## With Docker
Make sure you have [docker](https://docs.docker.com/engine/install/) installed.
```
git clone https://github.com/find-me-a-job/find-me-a-job.git
cd find-me-a-job
docker build -t fmj-backend -f docker/Dockerfile.backend .
docker run -p 5000:5000 fmj-backend
```
If your terminal is hung after a docker command then you might need to use sudo
```
sudo docker build -t fmj-backend -f docker/Dockerfile.backend .
sudo docker run -p 5000:5000 fmj-backend
```

## Without Docker
### Mac & Linux
- Install a non-ancient version of [python](https://www.python.org/downloads/)
- Install poetry
```
# igonre if poetry is already installed
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
## Usage
You would need to send post request to
```
http://127.0.0.1:5000/api/v1/known-field-data
```
Request body:
```
{
    "title": string,
    "experience": int,
    "location": string
}
```
Request body example
```
{
    "title": "web development",
    "experience": 0,
    "location": "banglore"
}
```