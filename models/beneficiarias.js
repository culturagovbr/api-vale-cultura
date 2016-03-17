var _ = require('lodash');
var sql = require('mssql');

exports.findByCNPJ = function(cnpj, callback) {
  new sql.Request().query("SELECT * FROM VW_DADOS_BRUTOS_BENEFICIARIA where CNPJ_BENEFICIARIA = \'" + cnpj + "\'").then(

    function(recordset) {
      callback(recordset[0]);

    }).catch(function(err) {
      // ... query error checks
      console.log(err);
  });
};

exports.paginate = function (reqPage, reqLimit, callback) {
  new sql.Request().query("SELECT count(1) as count FROM VW_DADOS_BRUTOS_BENEFICIARIA").then( function(recordset){

    var itemCount = recordset[0].count;
    var pageCount = _.ceil(itemCount / reqLimit);

    if (pageCount <= (reqPage - 1)) {
      callback(new Error("Não existem registros suficientes para a página solicitada"));

    } else {
      var offset = (reqPage -1) * reqLimit;
      var queryStr = "SELECT * FROM VW_DADOS_BRUTOS_BENEFICIARIA order by ID_BENEFICIARIA ASC OFFSET "+ offset +" ROWS FETCH FIRST "+ reqLimit +" ROWS ONLY";
      new sql.Request().query(queryStr).then( function(recordset){
        callback(null, recordset, pageCount, itemCount);

      }).catch(function(err) {
    		// ... query error checks
        console.log(err);
    	});
    }
  });
};
