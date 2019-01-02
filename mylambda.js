const pg = require('pg')
const pool = new pg.Pool()
const https = require('https');

async function query (q) {
  const client = await pool.connect()
  let res
  try {
    await client.query('BEGIN')
    try {
      res = await client.query(q)
      await client.query('COMMIT')
    } catch (err) {
      await client.query('ROLLBACK')
      throw err
    }
  } finally {
    client.release()
  }
  return res
}

exports.handler = async (event, context, callback) => {
    https.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY', function(res) {
      console.log("Got response: " + res.statusCode);
      context.succeed();
    }).on('error', function(e) {
      console.log("Got error: " + e.message);
      context.done(null, 'FAILURE');
    });
    try {
      const { rows } = await query("select * from pg_tables")
      console.log(JSON.stringify(rows[0]))
      var response = {
          "statusCode": 200,
          "headers": {
              "Content-Type" : "application/json"
          },
          "body": JSON.stringify(rows),
          "isBase64Encoded": false
      };
      callback(null, response);
    } catch (err) {
      console.log('Database ' + err)
      callback(null, 'Database ' + err);
    }
};
