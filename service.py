import sys
import random
import datetime

from flask import Flask, request
from dateutil.parser import parse

app = Flask(__name__)

WITH_LOAD_SHEDDING = False

@app.route('/')
def handle_expensive_route():
    #
    # If we're load shedding, before the request is processed
    # check a custom X-Respond-By header that the client attaches
    # to the request. This will set as NOW + Timeout + Epsilon.
    #
    # If the server starts handling the request after that datetime
    # its safe to assume the client has already moved on to it's timeout
    # error handler and you can avoid computing the expensive request,
    # freeing CPU time to handle other requests in the queue.
    #
    if WITH_LOAD_SHEDDING:
        respond_by = request.headers.get('X-Respond-By')
        if respond_by:
            respond_by = parse(respond_by)
            if datetime.datetime.now() > respond_by:
                return 'Request expired before processing', 419

    # Aritifical spinlock to illustrate a CPU expensive endpoint
    work_until = datetime.datetime.now() + datetime.timedelta(
        milliseconds=random.randint(50, 200)
    )

    while datetime.datetime.now() < work_until:
        # print('here')
        x = 1 + 1

    return 'Computed something expensive'


if __name__ == '__main__':
    WITH_LOAD_SHEDDING = '--with-load-shedding' in sys.argv
    print(WITH_LOAD_SHEDDING)
    app.run(threaded=False, processes=1)
