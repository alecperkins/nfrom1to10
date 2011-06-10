### 
Example vote fetching code for the Pick A Number API.
http://nfrom1to10.appspot.com/results/api/
###

request     = require 'request'
url         = require 'url'

# The URL of the API endpoint
URL =
    protocol    : 'http:'
    hostname    : 'nfrom1to10.appspot.com'
    pathname    : '/data/votes/'

    # Add your parameters here
    # query       :
    #     number     : 1
    #     method     : 'input'


fetchBatch = (cursor) ->

    # Add the cursor parameter to the request URL
    if cursor?
        URL.query ?= {}
        URL.query.cursor = cursor

    request_url = url.format(URL)

    # Make the request to the API
    request { uri: request_url }, (error, response, body) ->
        if response?
            if not error? and response.statusCode is 200
                result = JSON.parse(body)
                
                # Make sure the result wasn't throttled
                if result.status isnt 'throttled'
                    votes = result.objects

                    #####################################
                    # DO SOMETHING WITH THE RESULT HERE #
                    #####################################

                # Delay the next request, for rate limiting
                setTimeout ->
                    if result.next_cursor?
                        fetchBatch(result.next_cursor)
                , 30 * 1000

            else
                console.log response.statusCode
                console.log error


# Replace this with the next_cursor of the last batch, if any
last_cursor = null

fetchBatch(last_cursor)