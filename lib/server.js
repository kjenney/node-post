// server.js
const express = require('express')
const app = express()
const port = 3000
var product = require(./handlers/product)

module.exports = app;

// Home

app.get('/', (req, res) => res.send('Hello World!'))

// Product

app.get('/product', product.list);
app.all('/product/:id/:op?', product.load);
app.get('/product/:id', product.view);
app.get('/product/:id/view', product.view);
app.get('/product/:id/edit', product.edit);
app.put('/product/:id/edit', product.update);


app.listen(port, () => console.log(`Example app listening on port ${port}!`))
