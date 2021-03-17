# weird-text
## Running
locally: `python main.py` launches a local web server

remote: The app is available on https://weird-text-1112.herokuapp.com

## RESTful API
The app provides 2 endpoints:
- `/v1/encode` (POST)
- `/v1/decode` (POST)

in both cases `Content-Type: text/plain` is expected and the response will also have this content type set

## Example use
Windows:

`curl -Method Post "https://weird-text-1112.herokuapp.com/v1/encode" -Body "test this app!" -ContentType "text/plain; charset=UTF-8"`

[Try it out online!](https://stylishtriangles.github.io/weird-text/)