var editor = {};

function p(str, color)
{
  if(color == undefined)
  {
    $('#console').append($("<pre>"+str+"</pre>"));
  }
  else {
    $('#console').append($('<pre style="color:'+color+'">'+str+"</pre>"));
  }

  consoleAutoScroll();
}

function consoleAutoScroll()
{
  el = document.getElementById("console");
  el.scrollTop = Math.max(el.clientHeight, el.scrollHeight);
}

function clearConsole()
{
  $('#console').html("");
  consoleAutoScroll();
}

function compileHandler()
{
  editor.compile();
}

var Editor = function (URL, port)
{
  p("Starting smart contract editor...", "#00ff00");
  this.init();
  p("Connecting to " + 'http://'+URL+':'+port);
  this.web3 = new Web3();
  this.web3.setProvider(new this.web3.providers.HttpProvider('http://'+URL+':'+port));
  p("testing connection...");
  try {
    this.account = this.web3.eth.coinbase;
    p("Connected, coinbase is: " + this.account, "#00FF00")
  } catch (e) {
    this.account = null;
    p(e.message, "#ff0000");
  }
};

Editor.prototype.init = function ()
{
  this.editorEl = ace.edit("editor");
  this.editorEl.setTheme("ace/theme/monokai");
  this.editorEl.getSession().setMode("ace/mode/javascript");
  this.editorEl.setShowPrintMargin(false);
  this.editorEl.focus();
};

Editor.prototype.removeWhitespace = function ()
{
  var noBreaks = this.editorEl.getValue().replace(/(\n)+/g, '');
  var noTabs = noBreaks.replace(/(\t)+/g, '');
  return noTabs.replace(/ +/g, ' ');
}

Editor.prototype.compile = function ()
{
  p("Compiling...");
  var source = this.editorEl.getValue();
  var compiled = this.web3.eth.compile.solidity(source);
  compiledContracts = [];
  for (var c in compiled)
  {
    p("Compiled contract " + c);
    compiledContracts[compiledContracts.length] = c;
  }
  if (compiledContracts.length == 1)
  {
    this.mainContractName = compiledContracts[0];
    var code = compiled[compiledContracts[0]].code;
    var abi = compiled[compiledContracts[0]].info.abiDefinition;
  }
  this.currentContract;
  this.web3.eth.defaultAccount = this.account;

  p("Sending transaction to blockchain. Waiting to be mined...");
  this.web3.eth.contract(abi).new({data: code}, function (err, contract) {
            if(err) {
                p(err, "#ff0000");
                return;
            // callback fires twice, we only want the second call when the contract is deployed
            } else if(contract.address){
                editor.currentContract = contract;
                p('Contract has been mined!');
                p('new contract address: ' + editor.currentContract.address, "#00FF00");
                p("Done, Downloading contract file...");
                editor.downloadContract();
            }
        });
};

Editor.prototype.downloadContract = function ()
{
  var filename = editor.mainContractName + ".json";
  var element = document.createElement('a');
  var text = JSON.stringify(editor.currentContract);
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
};

$(function () {
  editor = new Editor("localhost", "8000");
  $('#compile').click(compileHandler);
  $('#clearConsole').click(clearConsole);
  window.onerror = function(error, url, line) {
    p('ERROR:'+error+' URL:'+url+' L:'+line, "#FF0000");
  };
});
