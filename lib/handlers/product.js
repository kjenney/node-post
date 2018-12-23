// Fake product database

var products = [
  { name: 'yoyo', description: 'goes up and down' },
  { name: 'doll', description: 'is cudly' }
];

exports.list = function(req, res){
  res.render('products', { title: 'products', products: products });
};

exports.load = function(req, res, next){
  var id = req.params.id;
  req.product = products[id];
  if (req.product) {
    next();
  } else {
    var err = new Error('cannot find product ' + id);
    err.status = 404;
    next(err);
  }
};

exports.view = function(req, res){
  res.render('products/view', {
    title: 'Viewing product ' + req.product.name,
    product: req.product
  });
};

exports.edit = function(req, res){
  res.render('products/edit', {
    title: 'Editing product ' + req.product.name,
    product: req.product
  });
};

exports.update = function(req, res){
  // Normally you would handle all kinds of
  // validation and save back to the db
  var product = req.body.product;
  req.product.name = product.name;
  req.product.description = product.description;
  res.redirect('back');
};
