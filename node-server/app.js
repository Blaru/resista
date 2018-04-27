var express = require('express');
var bodyParser = require('body-parser')
var multer  = require('multer');
var upload = multer({ dest: 'uploads/' });
var app = express();
var ReqN=0;
app.use( bodyParser.json({limit:'50mb'}) );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true,limit:'50mb'
}));

app.get('/', (req, res) => {
	console.log('GET recebido');
	res.send('<h1>Hello fucking World! Modafoca</h1>');
})
// Note: cache should not be re-used by repeated calls to JSON.stringify.

app.post('/', function(req,res){
	var cache = [];
  //console.log('POST recebido, data:\n' +JSON.stringify(req.body,undefined,2));
  console.log('POST recebido, data Size:\t' +JSON.stringify(req.body.data.length,undefined,2));
  cache = null; // Enable garbage collection
  res.send(JSON.stringify({"resposta":`Requisição N:${++ReqN}`}));
});

app.listen(3000, () => console.log('Node Server listening on port 3000!'))