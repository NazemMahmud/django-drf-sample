// ALL POST and GET type API Requests will be here

const Requests = {
    postRequest: function (url, data, fnName, callback) {
        // console.log(data);
        const response = $.post(url, data)
            .done(function (result) {
                const data = {
                    result: result,
                    responseType: "success"
                };
                callback(data, fnName);
            })
            .fail(function (error) {
                const response = JSON.parse(error.responseText);
                console.log("Error: ", response);
                const data = {
                    result: response,
                    responseType: "error"
                };
                callback(data, fnName);
            });
    },
    getRequest: function (url, fnName, callback) {
        const response = $.get(url)
            .fail(function (error) {
                const response = JSON.parse(error.responseText);
                console.log("Error: ", response);
                const data =  {
                    result: response,
                    responseType:"error"
                };
                callback (data, fnName);
            })
            .done(function (result) {
                const data =  {
                    result: result,
                    responseType:"success"
                };
                callback (data, fnName);
            });
    }
};
