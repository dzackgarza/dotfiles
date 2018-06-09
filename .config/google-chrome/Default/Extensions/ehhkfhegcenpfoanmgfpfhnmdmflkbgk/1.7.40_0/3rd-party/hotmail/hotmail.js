"use strict";

(function () {

// from X-notifier Neo

function dout(text) { console.log('hotmail: ' + text); }

// handler.js

const MAX_MSG = 5;

const ST_COOKIE      = 200;
const ST_COOKIE_RES  = 201;
const ST_INFO        = 300;
const ST_INFO_RES    = 301;
const ST_DATA        = 400;
const ST_DATA_RES    = 401;
const ST_DATA2       = 500;
const ST_DATA2_RES   = 501;

(function() {

function Handler(main){
  this.main=main;
}
Handler.prototype={
  inboxOnly: true,

  stage: 0,
  initStage: ST_INFO,
  count:-1,
  user:"",
  started:false,
  retry:0,
  lastCheck:null,

  initHandler:function(){
    this.initStage=this.config.cookies?ST_COOKIE:ST_INFO;
    this.count=-1;
    this.retry=0;
    delete this.dataURL;
    this.init();
    if(!this.dataURL)this.dataURL=this.infoURL; 
    if(!this.config.iconURL){
      try{
        var url=this.viewURL.match(/(((\S+):\/\/([^/]+))(\S*\/)?)([^/]*)/);
        if(url)this.config.iconURL=url[2]+"/favicon.ico";
      }catch(e){}
    }    
  },
  
  reset : function(){
    this.count=-1;
    this.stage=this.initStage;
  },
  
  check : function(){
    if(!this.enabled)return;
if(this.started)dout("started "+this.user+" "+this.lastCheck);
    if(this.started && this.lastCheck!=null && (new Date()-this.lastCheck<6000))return; //prevent duplicate check;
    this.lastCheck=new Date();    
    this.stop();
    if(this.count<0)this.reset();
    else this.stage=ST_DATA;
    this.started=true;
    this.doNext("");
  },
  stop : function(){
    if(this.xhr){
      this.xhr.onreadystatechange=null;
      this.xhr.abort();
      delete this.xhr;
    }
  },
  doNext:function(aData,aHttp){
    if(aData==null){//suspend
      if(this.checkRetry())return;
      this.onError(aData);
      return;
    }
    try{
      if(!this.process(aData,aHttp))++this.stage;
      delete this.xhr;
    }catch(e){
      this.onError(aData);
      if(e&&e.stack)console.info(e.stack);
    }
  },
  checkRetry:function(){
    if(this.retry<1){
      ++this.retry;
      this.count=-1;
      this.started=false;
      this.check();
      return true;
    }else return false;
  },
  process:function(aData,aHttp){
//dout(this.stage);
//dout(this.stage+" "+aData);
    switch(this.stage){
    case ST_COOKIE:
      this.checkCookies();
      return false;
    case ST_COOKIE_RES://no cookie
      this.reset();
      this.setResult(null);
      return true;
    case ST_INFO:
      this.getHtml(this.infoURL);
      return false;
    case ST_INFO_RES:
      var user=this.getUser(aData);
      if(this.user!=user)this.setUser(user);    
      if(!this.getInfo(aData)){
        if(this.checkRetry())return true;
        else break;          
      }
      this.stage=this.reuseInfo?ST_DATA_RES:ST_DATA;  
      this.doNext(aData,aHttp);
      return true;
      /*if(this.user==user){
        if(!this.getInfo(aData)){
          if(checkRetry())return true;
          else break;          
        }
        this.stage=this.reuseInfo?ST_DATA_RES:ST_DATA;
        return this.process(aData,aHttp);
      }else{
        this.setUser(user);
        this.check();
        return true;
      }*/      
    case ST_DATA:
      this.getHtml(this.dataURL);
      return false;
    case ST_DATA_RES:
      //var n=parseInt(this.getCount(aData));
      //this.count=isNaN(n)?-1:n;
      this.count=-1;
      var data;
      if(aData!=null)data=this.getData(aData);

      /////////// ADDED /////////////////////////////////////
      try {
        updateUnreadCount(data.count);
        getMailsFromArray(data.msg);
      } catch (e) {

      }
      /////////// ADDED /////////////////////////////////////

      if(this.count<0){
        if(this.checkRetry()){
          return true;
        }else{
          data=null;
          this.reset();
        }
      }else{
        if(this.dataURL2){
          this.stage=ST_DATA2;
          this.data=data;
          return this.process("");
        }else{
          this.retry=0;          
          this.stage=ST_DATA;
        }
      }
      this.setResult(data,aData==null);
      return true;
    case ST_DATA2:
      this.getHtml(this.dataURL2);
      return false;      
    case ST_DATA2_RES:
      var data=this.data;
      if(!this.getData2(aData,data)){
        if(this.checkRetry()){
          return true;
        }else{
          data=null;
        }
      }
      delete this.data;
      
      this.retry=0;
      this.stage=ST_DATA;      
      this.setResult(data,aData==null);
      return true;
    }
    this.onError(aData);
    return true;
  },
  onError : function(aData){
console.log(new Error("[onError] "+this.id+" "+this.user+" "+this.stage+" "+new Date().toISOString()));
    this.reset();
    this.setResult(null,aData==null);
  },

  getHtml:function(req) {
    this.xhr = getHtml(req,this.doNext.bind(this));
  },

  getViewURL : function(aFolder){
    return this.viewURL;
  },

  getCount : function(aData){
    return -1;
  },
  getData : function(aData){
    return {};
  },
  getUser : function(aData){
    return this.user;
  },
  getInfo : function(aData){
    return true;
  },  
  getData2 : function(aData,rs){
    return true;
  },  

  getForm:function(data,name,action){
    var url=null;
    if(name){
      var reg=new RegExp("<form([^>]+?id\\s*=\\s*[\"\']"+name+"[\"\'][\\S\\s]+?)<\/form>","i");
      var s=data.match(reg);
      if(!s)return "";
      data=s[1];
    }
    if(action){
      var fnd=data.match(/action\s*=\s*[\"\'](\S+?)[\"\']/);
      if(fnd)url=fnd[1];
    }
    var re=/<input[^>]+?name\s*=\s*[\"\'](\S+?)[\"\'][^>]+?value\s*=s*[\"\']([\s\S]*?)[\"\'][\s\S]*?>/ig;
    var o;
    var post="";
    while ((o = re.exec(data)) != null){
      if(o[0].match(/type\s*=\s*[\"\']?hidden[\"\']?/i)){
        if(post)post+="&";
        post+=o[1]+"="+encodeURIComponent(o[2]);
      }
    }
    if(action)return url?[url,post]:null;
    return post;
  },

  delay:function(sec){
    var self=this;
    window.setTimeout(function(){self.doNext("");},sec);
  },
  setResult:function(data,error){
    this.started=false;
    this.main.setResult(this,data,error);
  },
  setUser:function(user){
    this.main.setUser(this,user);
  },
  setOption:function(){
  },
  checkCookies:function(){
    var cks=this.config.cookies;
    this.cookieCount=cks.length;
    this.cookieFound=false;
    var self=this;
    for(var i=0;i<cks.length;i++){
      chrome.cookies.getAll({domain:cks[i].domain,name:cks[i].name,storeId:"0"},
        function(cookies){
          self.onCheckCookie(cookies);
        }
      );
    }
  },
  onCheckCookie:function(cookies){
    if(this.cookieCount<0)return;
    if(cookies&&cookies.length>0)this.cookieFound=true;
    --this.cookieCount;
    if(this.cookieCount==0){
      this.cookieCount=-1;
      this.stage=this.cookieFound?ST_INFO:ST_COOKIE_RES;
      this.doNext("");
    }
  }
}
Handler.prototype.baseProcess=Handler.prototype.process;

function getHtml(req,func){
  var aURL,aPostData,aHeaders,aMethod;
  if(req instanceof Array){
    aURL=req[0];
    aPostData=req[1];
    aHeaders=req[2];
    aMethod=req[3];
  }else aURL=req;

  var xhr = new XMLHttpRequest();
  if(func){
    xhr.func=func;
    xhr.onreadystatechange=function(){
      if(this.readyState==4){
        //this.status==0 when supended
        func(this.status==0?null:this.responseText,this);
      }
    };
  }
  var setContentType=false;
  if(aPostData||aPostData==""){
    xhr.open(aMethod?aMethod:"POST", aURL, true);
    setContentType=true;
  }else xhr.open(aMethod?aMethod:"GET", aURL, true);
  if(aHeaders){
    for(var t in aHeaders){
      if(t=="Content-Type")setContentType=false;
      xhr.setRequestHeader(t,aHeaders[t]);
    }
  }
  if(setContentType)xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  try{
    xhr.send(aPostData);
  }catch(e){
    if(func)func(null,xhr);
    dout(e);
  }
  return xhr;
}

window.Handler = Handler;

})();







// hotmail.js

/***********************************************************
Hotmail
***********************************************************/
//scripts["hotmail"]={
var hotmailScript = {
  config:{
    inboxOnly:true,
    showFolders:true,
    showSnippets:true,
    includeSpam:true,

    cookies:[{domain:".live.com",name:"WLSSC"}],

    iconURL:"https://outlook.live.com/owa/favicon.ico"
  },
  
  init:function(){ 
    this.infoURL="https://outlook.live.com/owa/";
    this.dataURL=["https://outlook.live.com/owa/sessiondata.ashx?appcacheclient=0","appcacheclient=0"];
    this.viewURL="https://outlook.live.com/owa/";
  },

  process:function(aData,aHttp){
    switch(this.stage){
    case ST_INFO_RES:
      var fnd=aData.match(/window\.clientId/);
      if(fnd){
        this.dataURL=["https://outlook.live.com/owa/sessiondata.ashx?appcacheclient=0","appcacheclient=0"];
        this.reuseInfo=true;
        this.getHtml(this.dataURL);
        return false;
      }      
    case ST_DATA_RES:
      var fnd=aData.match(/window\.location\.replace\("(\S+?)"/);
      if(fnd){//old UI
dout("redirect "+fnd[1]+" "+new Date().toISOString());
        this.getHtml(fnd[1]);
        return false;
      }
      var f=this.getForm(aData,"fmHF",true);
      if(f){//login timeout
dout("fmHF "+f[0]+" "+new Date().toISOString());
        this.stage=ST_INFO;
        this.getHtml(f);
        return true;
      }        
      break;
    case ST_INFO_RES+1:
      this.stage=ST_INFO_RES;
      break;
    case ST_DATA_RES+1:
      this.stage=ST_DATA_RES;
      break;
    }
    return this.baseProcess(aData,aHttp);
  },

  getUser:function(aData){
    var fnd=aData.match(/"LogonEmailAddress":"(\S+?)"/);
    if(fnd){
      delete this.oldUI;
      return fnd[1];
    }
    var fnd=aData.match(/"userEmail":"(\S+?)"/);
    if(fnd){//old UI
      this.oldUI=true;
      return unescape(fnd[1].replace(/\\x40/g,"@"));
    }
    return null;
  },
  
  getInfo:function(aData){
    if(!this.oldUI){
      this.config.iconURL="https://outlook.live.com/owa/favicon.ico";
      return true;
    }
    
    //old UI
    this.dataURL=this.inboxOnly?"https://mail.live.com/?fid=flinbox&fltid=1":"https://mail.live.com/?fid=flsearch&srch=1&scat=1&sdr=10&satt=0";
    this.config.iconURL="https://a.gfx.ms/OLFav.ico";
    
    var fnd=aData.match(/<base\s+href="(\S+?)"/);
    if(fnd){
      var url=fnd[1].match(/(((\S+):\/\/([^/]+))(\S*\/)?)([^/]*)/);
      if(url){
        this.baseHost=url[2];
        this.dataURL=this.dataURL.replace("https://mail.live.com",this.baseHost);
        this.viewURL=this.baseHost+"/";
      }
      
      fnd=aData.match(/"fppConfig":(\{\S+?\})/);
      if(fnd){
        fnd=unescape(fnd[1].replace(/\\u/g,"%u").replace(/\\x/g,"%"));
        var o=JSON.parse(fnd);
        this.authUser=o.AuthUser;
        this.sessionId=o.SessionId;
        return true;
      }
    }
    return false;
  },
    
  getData:function(aData){
    var obj=[];
    var folders=[];
    
    if(!this.oldUI){
      delete this.reuseInfo;

      var o;
      try{
        o=JSON.parse(aData);
      }catch(e){
        ++this.retry;//prevent retry
        return null;
      }
      var l=o.findFolders.Body.ResponseMessages.Items[0].RootFolder.Folders;
      this.count=0;
      this.spam=0;
      var flds={};      
      for(var i in l){
        var f=l[i];
        flds[f.FolderId.Id]=f.DisplayName;
        if(f.FolderClass!="IPF.Note")continue;
        var fid=f.DistinguishedFolderId?f.DistinguishedFolderId:f.FolderId.Id;
        if(fid=="sentitems"||fid=="drafts"||fid=="deleteditems"||fid=="outbox")continue;
        var n=f.UnreadCount;
        if(fid=="junkemail"){
          this.spam=n;
        }else if(this.inboxOnly){
          if(fid=="inbox")this.count+=n;
        }else this.count+=n;
        if(n>0&&fid!="inbox"){
          var fname;
          if(flds[f.ParentFolderId.Id])fname=flds[f.ParentFolderId.Id]+"/"+f.DisplayName;
          else fname=f.DisplayName;
          var t={id:fid,title:fname,count:n,url:this.viewURL};
          folders.push(t);
        }
      }      
      
      var conv=o.findConversation.Body.Conversations;
      for(var i=0;i<conv.length;i++){
        var m=conv[i];
        if(m.GlobalUnreadCount==0)continue;
        var d={};
        d.mid=m.ConversationId.Id;
        //d.email=
        d.name=m.UniqueSenders[0];
        d.title=m.ConversationTopic;
        d.content=m.Preview;
        d.time=new Date(m.LastDeliveryTime).getTime();
        d.url=this.viewURL;
        obj.push(d);
      }    
      
      var rs={count:this.count,user:this.user,folders:folders,msg:obj,spam:this.spam};
      return rs;
    }

    var fnd=aData.match(/HM.ContainerPoolData\(\S+?,0,\{([\s\S]+?)\},\s*\[([\S\s]+?)\]/);
    if(fnd){
      var order=fnd[2].split(",");
      fnd=fnd[1];
      var re=/Folder\("(\S+?)","(\S+?)".+?"([^"]+?)",(\d+)\)\)/g;
      var o;
      var num=0;
      while ((o = re.exec(fnd)) != null){
        if(o[1]=="fldrafts"||o[1]=="flsent"||o[1]=="fltrash")continue;
        var n=parseInt(o[4]);
        if(o[1]=="fljunk"){
          this.spam=n;
        }else if(o[1]=="flinbox"||!this.inboxOnly)num+=n;
        if(n>0&&o[1]!="flinbox"){
          var name=o[3];
          name=unescape(name.replace(/\\u/g,"%u").replace(/\\x/g,"%"));
          var i=order.indexOf("\""+o[1]+"\"");
          var t={id:o[1],title:name,count:n,url:this.baseHost+"/?fid="+o[1]};
          if(i>=0)folders[i]=t;
          else folders.push(t);
        }
      }
      this.count=num;

      var re=/ItemListData\(0,null,\{([^\}]+?)\},\{[^\}]*?\},(\[\S+?\])/g;
      while ((fnd = re.exec(aData)) != null){      
        var order=JSON.parse(fnd[2]);
        fnd=fnd[1].replace(/new HM\.[^\(]+?\(/g,"[").replace(/\)/g,"]");
        //fnd="var o={"+fnd+"}";
        //eval(fnd);
        fnd="{"+fnd+"}";
        fnd=fnd.replace(/\\x22/g,"\\\"").replace(/\\x/g,"%").replace(/\\u/g,"%u");
        var o=JSON.parse(unescape(fnd));
        for(var i=0;i<order.length&&i<MAX_MSG;i++){
          var m=o[order[i]][0];
          var d={};
          d.mid=m[0];
          d.email=m[7][0][2];
          d.name=m[7][0][0];
          d.title=m[9];
          //var time=m[28]; //28: "6/26/2015" 29: "Friday, June 26, 2015 10:15:39 AM" 36: 1435281339373
          d.time=m[36];
          d.url=this.viewURL+"?tid="+d.mid;

          obj.push(d);
        }
      }
    }
    var rs={count:this.count,user:this.user,folders:folders,msg:obj,spam:this.spam};
    rs.action={};
    rs.action["read"]=this.getActionUrl("read");
    rs.action["spam"]=this.getActionUrl("spam");
    rs.action["del"]=this.getActionUrl("del");
    return rs;
  },

  getActionUrl:function(act){
    var rs=[];
    switch(act){
    case "read":
      act="MarkMessagesReadState";
      rs[1]=["cn=Microsoft.Msn.Hotmail.Ui.Fpp.MailBox&mn="+act+"&d=true,[",
            "%22","%s",",","%22",  "],[",
            "{","%r","",",","}",   "],[",
            "{","%r","",",","}",   "],true,{[],[],[],[],[],[]},null&v=1"];
      break;
    case "spam":
      act="MarkMessagesForJmr";
      rs[1]=["cn=Microsoft.Msn.Hotmail.Ui.Fpp.MailBox&mn="+act+"&d=%22flinbox%22,[",
            "%22","%s",",","%22",  "],[",
            "{","%r","",",","}",   "],0,false,0,false,false,[",
            "{","%r","",",","}",   "],true,{[],[],[],[],[],[]},null&v=1"];
      break;
    case "del":
      act="MoveMessagesToFolder";
      rs[1]=["cn=Microsoft.Msn.Hotmail.Ui.Fpp.MailBox&mn="+act+"&d=%22fltrash%22,[",
            "%22","%s",",","%22",  "],[",
            "{","%r","",",","}",   "],[",
            "{","%r","",",","}",   "],false,false,false,true,{[],[],[],[],[],[]},null&v=1"];
      break;
    }
    rs[0]=this.viewURL+"ol/mail.fpp?cnmn=Microsoft.Msn.Hotmail.Ui.Fpp.MailBox."
        +act+"&ptid=0&a="+this.sessionId+"&au="+this.authUser;
    return rs;
  }
};


//////////////////////////////////////////////////////

var pollInterval = FETCH_INTERVAL || 1 * MINUTES;
var inboxOnly = false; 
var MAX_HOTMAIL = 20;

stored.hotmail || (stored.hotmail = "[]");

var fetchTimer;
var fetchDelay = pollInterval;
var MAX_BACKOFF_DELAY = 1 * HOURS;




var user;
var h = new Handler();
h.main=window;
h.id="hotmail";
h.nid = 0;
h.enabled=true;
//if(nid!=null)h.nid=nid; // 0
var s=hotmailScript; //scripts[id];
for(var i in s){
  h[i]=s[i];
}

h.initHandler();

/*
// currently we have embedded updateUnreadCount into the 3rd party code
h._count = h.count;
Object.defineProperty(h, "count", { 
  set: function (newCount) { 
    this._count = newCount;
    updateUnreadCount(newCount);
  },
  get: function () { return this._count; }
});
*/


// init background fetching
check();

function scheduleRequest() {
  clearTimeout(fetchTimer);
  fetchTimer = window.setTimeout(check, fetchDelay);
}

function check() {
  scheduleRequest();
  if (!navigator.onLine) return;
  isNotificationsEnabled() ? h.check() : updateUnreadCount("");
}

function delayNextFetchByBackoff() {
  fetchDelay = Math.min(2 * fetchDelay, MAX_BACKOFF_DELAY);
  scheduleRequest();
  console.log("Hotmail: delaying next fetch (probably logged out)", fetchDelay);
}

function resetFetchDelayToNormal() {
  if (fetchDelay == pollInterval) return;
  fetchDelay = pollInterval;
  scheduleRequest();
  console.log("Hotmail: resuming normal fetching (probably logged in)", fetchDelay);
}

function updateUnreadCount(unread) {
  set_indicator("hotmail", unread);
}

function isNotificationsEnabled() {
  return is_notification_enabled('hotmail');
}


function getMailsFromArray(rows) {
  if (!rows) return;

  var first_id, is_first = true;
  var since_id = stored.hotmail_since_id;
  var new_items = [];
  var notifications = [];

  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var id = row.mid;

    if (is_first) {
      is_first = false;
      first_id = id;
    }

    if (id == since_id) break;

    var link = row.url; 
    var subject = row.title;
    var name = row.name;

    new_items.push({
      //email: email,
      name: row.name,
      //date: date,
      subject: row.title
    });
    notifications.push(['hotmail', "<a href='"+link+"' target='_blank'>" + name + "</a> " + subject, ""]);
  }


  // going backwards intentionally for notifications to appear in order
  for (var i = notifications.length; i--;) {  
    create_notification.apply(null, notifications[i]);
  }

  stored.hotmail_since_id = first_id;

  var old_items = [];
  try {
    old_items = JSON.parse(stored.hotmail);
  } catch (e) {
    logError(new Error("ERROR: stored hotmail has invalid JSON: "));
    console.log('ERROR: stored hotmail has invalid JSON: ' + stored.hotmail);
    //  throw new Error('ERROR: stored hotmail has invalid JSON: ' + stored.hotmail);
  }
  new_items.concat(old_items);
  new_items = new_items.slice(0, MAX_HOTMAIL);

  setTimeout(function() {
    stored.hotmail = JSON.stringify(new_items);
  }, 1000);
}

})();

// these are called on the global object at some point
function setUser(hdl,user){ 
}

function setResult(hdl,data,error){
}



