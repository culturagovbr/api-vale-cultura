var express = require('express');
var _ = require('lodash');
var router = express.Router();

var app = express();

router.use(function(req, res, next) {
  if (app.get('env') === 'production') {
    res.contentType('application/hal+json');
  }
  next();
});

/* GET home page. */
router.get('/:cnpj', function(req, res, next) {
  var DAOBeneficiarias = require('../models/beneficiarias-mockup');

  var beneficiaria = DAOBeneficiarias.findByCNPJ(req.params.cnpj);

  if (_.isUndefined(beneficiaria)) {
    res.send("CNPJ inválido ou inexistente na base. Recurso não encontrado.", 404);
  } else {

    var links = {self: "/vale-cultura/doc/beneficiaria/" + beneficiaria.NR_CNPJ};
    res.hal({data: beneficiaria, links: links});
  }
});

module.exports = router;
