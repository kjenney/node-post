// Fake product database

var products = [
  { name: 'yoyo', description: 'goes up and down' },
  { name: 'doll', description: 'is cudly' }
];

exports.list = (event, context, callback) => {
    var response = {
        "statusCode": 200,
        "headers": {
            "Content-Type" : "application/json"
        },
        "body": JSON.stringify(products),
        "isBase64Encoded": false
    };
    callback(null, response);
};
