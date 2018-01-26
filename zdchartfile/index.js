var app = require('commander');
var Visualization = require('./visualization.js');
const KEY = "proto"

app.version('0.0.1')
    .option('-u, --user [user]', "Specifies the user")
    .option('-s, --host [host]', "Specifies the user")
    .option('-p, --passwd [passwd]', "Specifies the passwd")
    .option('-n, --visual [visual]', "Specifies the visualization")
    .option('-f, --file [file]', "Specifies the file")
    .parse(process.argv);

var main = function(){
    var vis = new Visualization(app.host, app.user, app.passwd, app.visual, app.file)
    vis.processVisualization()
}

main()

