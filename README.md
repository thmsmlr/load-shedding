# Loading Shedding Strategies

This repo has a demo application that demonstrates the usefulness of load shedding strategies.
After a spike in traffic or a CPU spikes happens you want your services to recover as quickly as possible.
Load shedding helps improving the mean time to recovery of a web service.

## How it works

The idea is pretty simple, most networking stacks do naive first in first out queuing.
During a big traffic spike, you'll get tons of responses queued up for your server to process.
Often however, since your server is behind, by the time the server responds to the request, the client has already closed the connection and moved on.
In the worst case, the client has already moved on before you service took the request off the queue to process.

The fix however is pretty simple.
If you client adds a `X-Respond-By` header with a timestamp of `now() + timedelta(milliseconds=timeout)`,
then your server can check for this header before doing the expensive processing of the request.
If the current server time is beyond the `X-Respond-By` header, then you're safe to drop the request.
It is assumed that the client has already moved on from that request.

This however, increases the performance of your webserver because it isn't wasting precious CPU cycles on long forgotten requests.

![demonstration](https://media2.giphy.com/media/Kyac5iuJu0K4ZSPLfC/giphy.gif)

## Installation

Make sure you have Python 3.6+ installed.

```
 $ pip install -r requirements.txt
```

## Usage

In one tab, run the flask server by

```
 $ python service.py --with-load-shedding
```

Then in another tab you can run the load test by,

```
 $ python load_test.py
```

You can remove the `--with-load-shedding` flag from the service to see how it would've operated otherwise.


