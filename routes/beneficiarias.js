var express = require('express');
var paginate = require('express-paginate');
var hal = require('hal');
var _ = require('lodash');

var DAOBeneficiarias = require('../models/beneficiarias-mockup');

var router = express.Router();
var app = express();

router.use(function(req, res, next) {
  if (app.get('env') === 'production') {
    res.contentType('application/hal+json');
  }
  next();
});

router.get('/', function(req, res, next) {
  DAOBeneficiarias.paginate(
    req.query.page,
    req.query.limit,
    function(err, beneficiarias, pageCount, itemCount) {
      if(err) {
        return res.send(err.message, 404);
      }

      var embeds = _.map(beneficiarias, function(e){
        return new hal.Resource(e, "/vale-cultura/doc/beneficiaria/" + e.NR_CNPJ);
      });

      var beneficiariasCollection = new hal.Resource({
        geradoEm: (new Date()).toJSON(),
        total_de_registros: itemCount,
        registros_na_pagina: beneficiarias.length
      }, req.originalUrl);

      beneficiariasCollection.link("find", {href: "/vale-cultura/doc/beneficiaria/{?cnpj}", templated: true});

      if (res.locals.paginate.hasPreviousPages) {
        beneficiariasCollection.link("prev", {href: res.locals.paginate.href(prev=true)});
      }
      if (paginate.hasNextPages(req)(pageCount)) {
        beneficiariasCollection.link("next", {href: res.locals.paginate.href()});
      }
      beneficiariasCollection.embed("beneficiarias", embeds);

      res.json(beneficiariasCollection);
    }
  );
});

module.exports = router;
