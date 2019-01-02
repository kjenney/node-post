var hello = [
  { name: 'hellow', description: 'world' }
];

exports.list = (event, context, callback) => {
    var response = {
        "statusCode": 200,
        "headers": {
            "Content-Type" : "application/json"
        },
        "body": JSON.stringify(hello),
        "isBase64Encoded": false
    };
    callback(null, response);
};
