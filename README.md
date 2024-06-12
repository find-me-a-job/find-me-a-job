### FMJ is created to help college students like ourselves to find which field is right for them through real data scrapped in real time.
### And if you do know which field you wish to advance in, but are curious about which skills would result in you getting hiered or getting a hike, it can help you there as well again with real data.

We have not yet deployed this application so if you want to use this right now, then you would need to set it up locally.

## With Docker
- Make sure you have docker installed.
```
git clone https://github.com/find-me-a-job/find-me-a-job.git
cd find-me-a-job/backend
docker build -t fmj-backend .
docker run -p 5000:5000 fmj-backend
```
