// console.log("imported");
// let id = document.getElementById("test");
// id.innerHTML = "sdsadsada sadsakd";

const Tweet = {
    BASE_API_URL: "",
    init: function () {
        Tweet.getTweets();
    },
    setBaseApi: function (apiPath) {
        Tweet.BASE_API_URL = apiPath;
    },
    loadTweetLists: function(data) {
        console.log("Data: ", data);
        let html = '';
        data.forEach(item => {
            html += '<div class="col-md-12 col-lg-12 col-sm-12 col-xs-12 border p-4 mb-3" style="min-height: 100px">' +
                            '<h5> ' + item.content + ' </h5> ' +
                            '<button class="btn btn-primary btn-sm" id="item-' + item.id + '"> Like 20 </button> ' +
                     '</div>';
        });
        $("#tweets-lists").append(html);
    },
    handleResponse: async function (response, functionName = "") {
        switch (functionName) {
            case "loadTweetLists": // after creating a tweet
                let msg = "Tweet is created successfully";
                console.log("res: ", response);
                if(response.responseType === 'success') { // for error handling
                    Tweet.loadTweetLists(response.result.response);
                } else {
                    msg = response.response.message;
                }

                // Spinner action
                // $("#newPocket").prop("disabled", false);
                // $("#spinner-overlay").hide();
                // $("#pocket-submit").text("Submit");
                //
                // Pocket.handleToast( msg, type);
                break;
            default:
                break;
        }
    },
    getTweets: function () {
        const url = Tweet.BASE_API_URL + "tweets";
        const response = Requests.getRequest(url, "loadTweetLists", Tweet.handleResponse);
        // if (response) {
        //     console.log("Result: ", response);
        //     Tweet.handleResponse(response, "loadTweetLists");
        // }
    },
    postRequest: function () {

    },
    getRequest: function (url, fnName) {
        const response = $.get(url)
            .fail(function (error) {
                const response = JSON.parse(error.responseText);
                console.log("Error: ", response);
                // Pocket.handleData(response, fnName, "error");
            })
            .done(function (result) {
                console.log("Result: ", result);
                // Pocket.handleData(result.data, fnName, "success");
            });
    }
};

jQuery(function($) {

    Tweet.init();
});