
const Tweet = {
    BASE_API_URL: "",
    init: function () {
        Tweet.getTweets(); // get all tweets

         // Create new tweet
        $("#tweet-create-form").submit( function (event) {
            event.preventDefault();
            const data = $(this).serializeArray();
            Tweet.newTweet(data);
        });

    },
    setBaseApi: function (apiPath) {
        Tweet.BASE_API_URL = apiPath;
    },
    getTweets: function () { // GET All Tweets api request
        const url = Tweet.BASE_API_URL + "tweets";
        Requests.getRequest(url, "loadTweetLists", Tweet.handleResponse);
    },
    loadHtml: function (item) { // Create HTML to Load Each Tweet Lists
        const html = '<div class="col-md-12 col-lg-12 col-sm-12 col-xs-12 border p-4 mb-3" style="min-height: 100px">' +
                            '<h5> ' + item.content + ' </h5> ' +
                            '<button class="btn btn-primary btn-sm" id="item-' + item.id + '"> Like 20 </button> ' +
                     '</div>';
        return html;
    },
    loadTweetLists: function(data) { // Initial Load Html of All Tweets
        console.log("Data: ", data);
        let html = '';
        data.forEach(item => {
            html += Tweet.loadHtml(item);
        });
        $("#tweets-lists").append(html);
    },
    newTweet: function (data) { // POST A New Tweets API request
        const formData = {};
        data.forEach(elem => {
            formData[elem.name] = elem.value;
        });
        const url = Tweet.BASE_API_URL + "create-tweet";
        Requests.postRequest(url, formData,"CreateTweet", Tweet.handleResponse);
    },
    addTweet: function (data) { // After Create a Tweet; add in the tweet lists html
        const html = Tweet.loadHtml(data);
         $("#tweets-lists").prepend(html);
    },
    handleResponse: async function (response, functionName = "") {
        switch (functionName) {
            case "loadTweetLists": // after creating a tweet
                let msg = "Tweet is created successfully";
                console.log("res: ", response);
                if(response.responseType === 'success') { // for error handling
                    Tweet.loadTweetLists(response.result.response);
                } else {
                    msg = "Something went wrong";
                }

                // Spinner action
                // $("#newPocket").prop("disabled", false);
                // $("#spinner-overlay").hide();
                // $("#pocket-submit").text("Submit");
                //
                // Pocket.handleToast( msg, type);
                break;
            case "CreateTweet":
                const data = response.result;
                console.log("new tweet: ",  data[Object.keys(data)[0]][0]);
                // $("#content-spinner").hide(); // Spinner action
                // $('#content-url').val(""); // make modal field empty
                let message = "Tweet created successfully";
                if(response.responseType === 'success') { // for error handling
                    Tweet.addTweet(response.result);
                     $("#tweet-create-form")[0].reset();
                } else {
                    const errors = data[Object.keys(data)[0]] // take the first error, that is 1st element of object
                    message = errors[0]
                }
                Tweet.handleToast( message, response.responseType);
                // Spinner action
                // $("#newTweet").prop("disabled", false);
                // $("#spinner-overlay").hide();
                // $("#tweet-submit").text("Submit");
                break;
            default:
                break;
        }
    },
    handleToast: function (message, status) {
        switch (status) {
            case "success":
                $('#toast-heading').text("Success");
                $('.toast-body').css("background-color", "#a4d6a4");
                $('.toast-body').text(message);
                $('.toast').toast('show');

                setTimeout(function() {
                    $('.toast').toast('hide');
                }, 4000);
                break;
            case "error":
                $('#toast-heading').text("Error");
                $('.toast-body').css("background-color", "#e49b9b");
                $('.toast-body').text(message);
                $('.toast').toast('show');

                setTimeout(function() {
                    $('.toast').toast('hide');
                }, 4000);
                break;
            default:
                break;
        }
    }

};

jQuery(function($) {

    Tweet.init();
});