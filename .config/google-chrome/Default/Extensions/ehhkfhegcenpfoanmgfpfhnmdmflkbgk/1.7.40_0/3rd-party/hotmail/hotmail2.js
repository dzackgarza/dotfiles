/***********************************************************
Live(Hotmail)
***********************************************************/
(function(){

var hostString="hotmail.com";
var supportInboxOnly=true;
var supportShowFolders=true;

function init(){
  this.initStage=ST_PRE;
  this.loginData=["","login","passwd","KMSI=1&LoginOptions=1"];
  this.dataURL="http://mail.live.com/default.aspx?rru=inbox";
  this.mailURL="http://mail.live.com/default.aspx?rru=inbox";
  this.mailDomain="mail.live.com";
  if(this.password.length>16)this.password=this.password.substring(0,16);

  this.cookieDomain="live.com";

  this.logoutURL="http://login.live.com/logout.srf";
}
function getIconURL(){
  return "http://gfx2.hotmail.com/mail/w4/pr04/ltr/mfav.ico";
}
function process(aHttpChannel, aData) {
  switch(this.stage){
  case ST_PRE:
    this.getHtml("http://mail.live.com");
    return false;
  case ST_PRE_RES:
    var fnd=aData.match(/srf_uPost=\'([\s\S]+?)\'/);
    if(fnd){
      this.loginData[LOGIN_URL]=fnd[1];
      fnd=aData.match(/PPFT[\s\S]+?value=\"(\S+?)\"/);
      if(fnd){
        this.stage=ST_LOGIN;
        this.getHtml(this.loginData[LOGIN_URL],this.loginData[LOGIN_POST]+"&PPFT="+encodeURIComponent(fnd[1]));
        return false;
      }
    }
    this.onError();
    return true;
  case ST_LOGIN_RES:
    var fnd=aData.match(/window.location.replace\([\'\"](\S+?)[\'\"]/);
    if(fnd){
      this.getHtml(fnd[1]);
      return false;
    }
    ++this.stage;
  case ST_LOGIN_RES+1:
    var fnd=aData.match(/"afu":"(\S+?InboxLight.aspx\S+?)"/);
    if(fnd){
      fnd=unescape(fnd[1].replace(/\\u/g,"%u"));
      this.dataURL=fnd;
      var url=this.dataURL.match(/(((\S+):\/\/([^/]+))(\S*\/)?)([^/]*)/);
      if(url)this.mailHost=url[2];
      this.stage=ST_DATA_RES;
    }else{
      fnd=aData.match(/href="(\S+?InboxLight.aspx\S+?)">/);
      if(fnd){//Thunderbird(browser check)
        fnd=fnd[1].replace(/&#(\d+);/g,function(){return String.fromCharCode(RegExp.$1);});
        this.stage=ST_LOGIN_RES+2;
        this.getHtml(fnd);
        return true;
      }
    }
    break;
  case ST_LOGIN_RES+2:
    var fnd=aData.match(/<base\s+href="(\S+?)"/);
    if(fnd){
      var url=fnd[1].match(/(((\S+):\/\/([^/]+))(\S*\/)?)([^/]*)/);
      if(url)this.mailHost=url[2];
    }
    this.stage=ST_DATA_RES;
    break;
  }
  return this.baseProcess(aHttpChannel, aData);
}
function getData(aData){
  var obj={};
  var ar=[];
  this.folders={};//used for direct link
  var fnd=aData.match(/<ul.+?class="List FolderList.+?>([\s\S]+?)<\/ul>/g);
  if(fnd){
    fnd=fnd.toString();
    var re=/<li.+?\s+id="(.+?([^-]+?))"\s+nm="(.+?)"\s+count="(\d+)"/g;
    var o;
    this.mailCount=0;
    while ((o = re.exec(fnd)) != null){
      if(o[2]=="000000000005"||o[2]=="000000000004"
        ||o[2]=="000000000003"||o[2]=="000000000002")continue;
      var n=parseInt(o[4]);
      if(this.inboxOnly){
        if(o[2]=="000000000001")this.mailCount=n;
      }else this.mailCount+=n;
      if(n>0&&o[2]!="000000000001"){
        var name=o[3];
        name=name.replace(/&#(\d+);/g,function(){return String.fromCharCode(RegExp.$1);});
        this.folders[name]=o[1].replace(/-/g,"");
        ar.push(name);
        ar.push(n);
      }
    }
    if(this.showFolders){
      if(ar)obj.folders=ar;
    }
    return obj;
  }
  this.mailCount=-1;
  return obj;
}
function getMailURL(aFolder){
  if(aFolder&&this.mailHost){
    var url=this.mailHost+"/mail/InboxLight.aspx?fid="+this.folders[aFolder]
              +"&n="+parseInt(Math.random()*1000000000);
    return url;
  }
  return this.mailURL;
}

})();