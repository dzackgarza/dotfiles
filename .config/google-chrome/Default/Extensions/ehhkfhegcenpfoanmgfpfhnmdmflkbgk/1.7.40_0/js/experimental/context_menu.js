
// panel


function Panel(context_elem) {

  context_elem = context_elem || document;
  context_elem.addEventListener('contextmenu', context_click, false);

  document.addEventListener('click',   hide, false);
  document.addEventListener('keydown', hide, false);

  var panel = document.createElement('ul');
  panel.className = 'panel';
  panel.style.display = 'none';
  panel.addEventListener('click', panel_click, false);
  document.body.appendChild(panel);

  function show() {
    //document.body.appendChild(panel);
    panel.style.webkitTransition = '';
    panel.style.opacity = 1;
    panel.style.display = 'block';
  }

  function hide() {
    panel.style.webkitTransition = 'opacity .2s ease-out';
    panel.style.opacity = 0;
    setTimeout(function () {
      panel.style.display = 'none';
      //document.body.removeChild(panel);
    }, 200);
  }

  function context_click(e) {
    // only care for right mouse clicks
    if (!e.button == 2) return;
    if (self.is_context_click(e)) {
      panel.style.left = e.pageX + 'px';
      panel.style.top  = e.pageY + 'px';
      show();
      e.preventDefault();
      e.stopPropagation();
    } else {
      hide();
    }
  }

  function panel_click(e) {
    self.panel_click(e);
  }

  function is_context_click(e) { 
    //return !/input|textarea/i.test(e.target.nodeName) &&
  }

  function always_true(e) { 
    return true; 
  }

  var self = {
    data  : {},
    panel : panel,
    show  : show,
    hide  : hide,
    is_context_click : is_context_click,
    context_click    : context_click,
    panel_click      : always_true
  };
  return self;
}

panel = (new Panel(byId('page'))).panel; 


function ApplicationPanel(context_elem) {

  context_elem = context_elem || document;
  context_elem.addEventListener('contextmenu', context_click, false);

  function is_context_click(e) {
    return (e.target.nodeName == 'IMG' || /^cal/.test(e.target.id));
  }

  function context_click(e) {
    if (is_context_click(e)) {
      var el = e.target.parentNode.parentNode;
      var app = apps[el.id];
      panel.dataset.appid = el.id;
      panel.innerHTML = '' +
        '<li class="panel-app-name">'+ app.name +'</li>' +
        '<hr />' +
        '<li '+ (!app.optionsUrl ? 'class="disabled"' : '') +'>Options</li>' +
        '<li class="disabled">Hide</li>' +
        '<hr />' +
        '<li>Remove</li>';
    } 
    panel.context_click(e);
  }

  panel.panel_click = function (e) {
    var id = panel.dataset.appid;
    var action = e.target.innerHTML;
    var className = e.target.className;
    var app = apps[id];
    if (id) {
      if (className && className == 'panel-app-name') {
        chrome.tabs.create({ 'url': app.appLaunchUrl });
      }
      else if (action == 'Options') {
        if (app.optionsUrl)
          chrome.tabs.create({ 'url': app.optionsUrl });
      }
      else if (action == 'Hide') {
        /// TODO: ...
      }
      else if (action == 'Remove') {
        /// TODO: prompt, animation
        panel.hide();
        if (confirm('Remove "' + apps[id].name + '"?')) {
          chrome.management.uninstall(id, function () {
            bg.onUninstalled(id);
            location.reload();
          });
        }
      }
    }
  };

  return self;
}




function SystemPanel() {
  
  
}
