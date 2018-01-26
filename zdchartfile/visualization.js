var fs = require('fs');
var axios = require('axios');
var _ = require('lodash');

class Visualization{

    constructor(host, user, passwd, visual, file){
        this.base_path = "/Users/eduardo/Documents/Pincha/AKTIUN/Repos/gs-filter-control/" 
        this.host = host || "https://prototype.zoomdata.com/zoomdata"
        this.user = user
        this.pswd = passwd
        this.name = visual
        this.file = file
        this.auth = { username: this.user, password: this.pswd }
        this.headers = { "Content-Type": "application/json" }
        this.definition = {}
    }

    getVisualizationFromServer(){
        //Request the visualization current definition from the server
        const service = this.host + '/service/visualizations?name=' + encodeURI(this.name)
        const request = axios.get(service, { auth: this.auth })
        request
            .then((res)=>{ return res.data })
            .catch((error)=>{ console.log(error.response.data); })
        return request
    }

    updateVisualizationContent(data){
        if(data.length > 0){
            let _this = this;
            let visual_json = data[0];
            let file = this.base_path + this.file;
            fs.readFile(file, (err, buffer) => {
                let fcontent = buffer.toString()
                let component = _.filter(visual_json.components, c => {
                    return file.indexOf(c.name) > -1
                })
                if(component.length > 0){
                    component.body = fcontent;
                }
            });
            return visual_json
        }
    }

    updateVisualizationInServer(visualization){
        //Request the visualization current definition from the server
        const vid = visualization.id
        const service = this.host + '/service/visualizations/' + vid
        axios.put(service, visualization, { auth: this.auth, headers: this.headers })
            .then((res)=>{ 
                console.log("...updated!");
            })
            .catch((error)=>{ console.log(error.response.data); })
    }

    processVisualization(){
        var _this = this;
        console.log("Updating", this.file, "for", this.name)
        this.getVisualizationFromServer()
            .then(res => {
                let upd_visual_json= _this.updateVisualizationContent(res.data)
                _this.updateVisualizationInServer(upd_visual_json)
            })
    }
}

module.exports = Visualization
