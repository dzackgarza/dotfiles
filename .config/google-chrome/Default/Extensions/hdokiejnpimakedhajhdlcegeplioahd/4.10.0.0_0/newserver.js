LPServer=function(){var e,t,n=null,r=null,o=function(e,t){e&&e.error&&e.error(t)},i=(e=function(t,n){t=function(e){var t={};for(var n in e){var r=e[n];if(null!==r&&void 0!==r||(r=""),"object"==typeof r)for(var o in r)r.hasOwnProperty(o)&&(t[n+"["+o+"]"]=r[o]);else t[n]=r}return t}(t),n=n||"";var r=[];for(var o in t){var i=t[o];"object"==typeof i?r=r.concat(e(i,o)):(n&&(o=n+"["+o+"]"),r.push(o+"="+encodeURIComponent(i)))}return r},function(t){return e(t).join("&")}),a=function(e){var t=new XMLHttpRequest,n=e.contentType||"application/x-www-form-urlencoded";e.success&&(t.onload=function(){!function(e,t){if(4===e.readyState)if(200===e.status)switch(t.dataType){case"xml":t.success(e.responseXML,e.responseText);break;case"json":var n=null;try{n=JSON.parse(e.responseText)}catch(e){}t.success(n,e.responseText);break;default:t.success(e.responseText)}else t.error&&t.error(e,e.statusText)}(t,e)}),e.error&&(t.onerror=function(){e.error(t,t.statusText)});var r=function(t){return"application/json"===n?"GET"===t?"":JSON.stringify(e.data):i(e.data)},o=e.url;if("GET"===e.type){var a=r(e.type);o=e.url+(a.length>0?"?"+a:"")}t.open(e.type||"GET",o,!0),"POST"===e.type?(t.setRequestHeader("Content-Type",n),e.beforeSend&&e.beforeSend(t,e),t.send(r())):(e.beforeSend&&e.beforeSend(t,e),t.send())},u=function(e,t){E.ajax({type:"POST",url:E.getBaseURL()+"getCSRFToken.php",success:function(t){e(n=t||null)},error:c(t)})},c=function(e){return function(t,n,r){"function"==typeof e?e():console.error(r)}},s=function(e,t,n,r){f(e,t,n,r)||o(t,n)},f=(t=function(e,t,n,r){if(e){var o=e[n];if("function"==typeof o)return o(r,t),!0}return!1},function(e,n,r,o){var i=t(e,n,r,o);return i=t(n.callbacks,n,r,o)||i}),p=function(e,t){try{E.logException(e)}catch(e){}if(e instanceof A?o(t,e.message):o(t),LPServer.throwExceptions)throw e},l=function(e,t){return function(n,r){try{if(f(e,t,r))return;if(null===n&&r&&"undefined"!=typeof DOMParser)try{n=(new DOMParser).parseFromString(r,"application/xml")}catch(e){}null===n?o(t,"invalidxml"):S(n,e,t)}catch(e){p(e,t)}}},d=function(e,t){return e.getElementsByTagName(t)},y=function(e,t){var n=d(e,t);return n.length>0?n[0]:null},v=function(e,t){var n=y(e,t);return n?n.textContent:""},S=function(e,t,n){var r=y(e,"result"),i=y(e,"ok"),a=y(e,"error"),u=y(e,"failed");if(r){var c=r.getAttribute("rc"),p=r.getAttribute("msg"),l=r.getAttribute("success"),d=r.getAttribute("ok");if(c)return void s(t,n,c,r);if(p)return void s(t,n,p,r);if(l)return void s(t,n,l,r);if(d)return void s(t,n,"ok");var S=r.textContent.trim();if("ok"===S)return void(f(t,n,"ok")||s(t,n,v(e,"status")));if("bad"===S)return void o(n,v(e,"message"))}else{if(i)return void s(t,n,"ok",i);if(a)return void(f(t,n,a.getAttribute("cause"),a)||s(t,n,a.getAttribute("message"),a));if(u)return void s(t,n,u.getAttribute("reason"),u)}o(n)},b=function(e,t){return function(n,r){try{if(null===n&&r)o(t,"invalidjson");else{if(n.error)return void(f(e,t,n.error,n)||o(t,n.errortxt||n.error));if(n.hasOwnProperty("success")){if(n.success&&f(e,t,"success",n))return;if(!n.success)return void o(t)}else if(n.res){if("success"!==n.res)return void(f(e,t,n.res,n)||o(t,n.errortxt));if(f(e,t,n.res,n))return}else{if(f(e,t,n.reason,n))return;if(f(e,t,n.status,n))return;if(f(e,t,n.cmd,n))return}}e&&"function"==typeof e.default?e.default(n,t):"function"==typeof t.success&&t.success(n)}catch(e){p(e,t)}}},g=function(e){e.userSupplied=e.userSupplied||{},e.type=void 0===e.type?"POST":e.type,e.url=E.getBaseURL()+e.url,e.data=T(e.data,e.userSupplied.requestArgs),e.data&&void 0===e.data.lpversion&&"undefined"!=typeof lpversion&&(e.data.lpversion=lpversion),void 0===e.error&&e.userSupplied.error&&(e.error=c(e.userSupplied.error)),!e.data||void 0!==e.data.token||void 0!==e.CSRFToken&&!e.CSRFToken||null!==n?E.ajax(e):u(function(){E.ajax(e)},e.userSupplied.error)},k=function(e,t){var n={},r=t.userSupplied;switch("object"!=typeof r&&(r=t.userSupplied={}),typeof t.success){case"string":return n[t.success]=r.success,e(n,r);case"function":return n.default=t.success,e(n,r);default:if(t.callbacks||r.success||r.callbacks)return e(t.callbacks,r)}return null},x=function(e,t){t.data&&void 0===t.data.token&&(void 0===t.CSRFToken||t.CSRFToken)&&(t.data.token=n)},h=function(e,t,n){for(var r in n=n||[],t){var o=e[r],i=t[r];if("object"==typeof i)h(o,i,n.concat(r));else if(typeof o!==i)throw n.push(r),"Extension is missing the following property: "+n.join(".")+" ("+i+")"}},m=function(e,t,n){var r=e.getAttribute(t);return void 0===r?n:r},T=function(e){e=e||{};for(var t=1,n=arguments.length;t<n;++t){var r=arguments[t];for(var o in r)e[o]=r[o]}return e},_=function(e,t){return e?function(){var n=t.apply(window,arguments);e.apply(window,n||arguments)}:t},R={StringUtils:{translate:"function"},AES:{Encrypt:"function",Decrypt:"function",hex2bin:"function",bin2hex:"function"},enc:"function",dec:"function",RSAKey:"function",createRandomHexString:"function",parse_public_key:"function",parse_private_key:"function",enccbc:"function",make_lp_key_iterations:"function",make_lp_hash_iterations:"function",get_random_password:"function"},w={RSAKey:!0},E={ajax:a,translate:function(){return r.StringUtils.translate.apply(r.StringUtils,arguments)},logException:function(){},hex2bin:function(){return r.AES.hex2bin.apply(r.AES,arguments)},bin2hex:function(){return r.AES.bin2hex.apply(r.AES,arguments)},encryptAES:function(e,t){return e.length>0?r.AES.Encrypt({pass:t,data:e,b64:!0,bits:256}):e},decryptAES:function(e,t){return r.AES.Decrypt({pass:t,data:e,b64:!0,bits:256})},encrypt:function(e,t){return r.enc(e,t)},decrypt:function(e,t){try{return r.dec(e,t)}catch(e){return""}},createRandomHexString:function(){return r.createRandomHexString.apply(r,arguments)},parsePublicKey:function(){return r.parse_public_key.apply(r,arguments)},parsePrivateKey:function(e,t){if(!(t=t||r.rsaprivatekeyhex))throw"rsaprivatekeyhex required for this action.";return r.parse_private_key(e,t)},extractPrivateKey:function(e,t){return r.rsa_extract_privatekey(e,t)},encryptCBC:function(){return r.enccbc.apply(r,arguments)},makeKey:function(){return r.make_lp_key_iterations.apply(r,arguments)},makeHash:function(){return r.make_lp_hash_iterations.apply(r,arguments)},makeRandomPassword:function(){return r.get_random_password.apply(r,arguments)},getBaseURL:function(){return r.base_url||""},getLocalKey:function(){return r.g_local_key},setLocalKey:function(e){r.g_local_key=e}},A=function(e){this.message=e,this.stack=(new Error).stack};A.prototype=Object.create(Error.prototype),A.prototype.name="ClientException",A.prototype.constructor=A;var j,C=(j=function(e){e.setRequestHeader("X-CSRF-TOKEN",n)},{jsonRequest:function(e){var t,n;e.dataType="json",e.contentType="application/json",e.beforeSend=_(e.beforeSend,j),e.error=(t=e.callbacks,n=e.userSupplied||{},function(e,r){var i;try{i=JSON.parse(e.responseText)}catch(e){return void o(n,"invalidjson")}f(t,n,i.code,i)||o(n,i.message)}),g(e)}});return{ajax:a,getRecordsFromResponse:function(e,t,n){for(var r=[],o=0;o<n;++o)r.push(m(e,t+o));return r},jsonRequest:function(e){e.dataType="json",e.beforeSend=_(e.beforeSend,x),e.success=k(b,e),g(e)},xmlRequest:function(e){e.dataType="xml",e.beforeSend=_(e.beforeSend,x),e.success=k(l,e),g(e)},textRequest:function(e){e.dataType="text",e.beforeSend=_(e.beforeSend,x),g(e)},initialize:function(e,t){for(var n in h(e,R),t)E[n]=t[n];for(var o in w)E[o]=e[o];r=e},ext:E,getNodes:d,getNode:y,getNodeText:v,getAttr:m,getAttrInt:function(e,t,n){var r=parseInt(m(e,t,n));return isNaN(r)?n:r},extend:T,extendCallback:_,ClientException:A,clearCSRFToken:function(){n=null},getCSRFToken:u,callback:function(e,t){e.callbacks&&"function"==typeof e.callbacks[t]&&e.callbacks[t].apply(window,Array.prototype.slice.call(arguments,2))},lmiapi:C}}();
//# sourceMappingURL=sourcemaps/newserver.js.map
