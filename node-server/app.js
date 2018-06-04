var express = require('express');
var bodyParser = require('body-parser')
var multer  = require('multer');
var upload = multer({ dest: 'uploads/' });
var app = express();
var fs = require('fs');
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
	
	//console.log('POST recebido, data:\n' +JSON.stringify(req.body,undefined,2));
	console.log('POST recebido, data :\t' +JSON.stringify(req.body.data.length,undefined,2));
	var data = req.body.data;
	RandomKey='';
	for(i=0;i<16;i++){
		id = Math.floor(Math.random() * 16);
		RandomKey += (id===0)?'0':dec2hex(id);
	}
	fs.writeFile(`./photos/${RandomKey}.txt`, data,(err)=>{if(err){console.log(err)}else{console.log(`Goota\t${RandomKey}`)}});
	cmd.get(
		`sudo python script.py -data ${RandomKey}`,
		function(err, data, stderr){
			console.log('err',err);
			console.log('stderr',stderr);
			console.log('Saida\n',data)
			res.send(JSON.stringify({"resposta":`Requisição N:${++ReqN}\t${data}`}));
		}
	);  
});

app.listen(3000, () => console.log('Node Server listening on port 3000!'))

var cmd=require('node-cmd');



function dec2hex(str){ // .toString(16) only works up to 2^53
    var dec = str.toString().split(''), sum = [], hex = [], i, s
    while(dec.length){
        s = 1 * dec.shift()
        for(i = 0; s || i < sum.length; i++){
            s += (sum[i] || 0) * 10
            sum[i] = s % 16
            s = (s - sum[i]) / 16
        }
    }
    while(sum.length){
        hex.push(sum.pop().toString(16))
    }
    return hex.join('')
}
