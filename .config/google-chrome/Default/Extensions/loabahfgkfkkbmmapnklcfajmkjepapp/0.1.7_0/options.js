var optionsTemplate =
    `<form class="form-horizontal" onsubmit="{ save }">
        <div class="{'form-group': true, 'has-warning': !options.apiKey}">
            <label for="apiKey" class="col-xs-12 col-sm-4 control-label">API key:</label>
            <div class="col-xs-12 col-sm-8">
                <input type="text" id="apiKey" class="form-control" onkeyup="{ changed }" value="{ options.apiKey }" />
                <div if="{ !options.apiKey }">
                    <br>
                </div>
                <div class="alert alert-warning" if="{ !options.apiKey }">
                    Please enter your API key. You can find your API key here: <a href="http://my.pomodoneapp.com/profile/settings/" target="_blank">http://my.pomodoneapp.com/profile/settings/</a>
                </div>
                <div if="{ isKeyChanged && options.apiKey }">
                    <br>
                    <a class="btn btn-default" href="#" onclick="{ reload }">Reload extension for all open tabs</a>
                </div>
            </div>
        </div>
        <div class="form-group">
            <label for="blackList" class="col-xs-12 col-sm-4 control-label">Open in:</label>
            <div class="col-xs-12 col-sm-8">
                <select id="openIn" class="form-control" onchange="{ changed }">
                    <option value="{ 'app' }" selected="{ options.openIn == 'app' }">Desktop App</option>
                    <option value="{ 'web' }" selected="{ options.openIn == 'web' }">Web App</option>
                </select>
                <span if="{ openIn.value == 'app' }" class="help-block">Desktop App can be download from here: <a href="http://pomodoneapp.com/" target="_blank">http://pomodoneapp.com/</a></span>
            </div>
        </div>
        <div class="form-group">
            <label for="blockerIsActive" class="col-xs-12 col-sm-4 control-label">
                Block domains if timer running:
            </label>
            <div class="col-xs-12 col-sm-8">
                <div class="checkbox">
                    <label for="blockerIsActive">
                        <input type="checkbox" id="blockerIsActive" checked="{ options.blockerIsActive }" onchange="{ changed }" /> Activate blocking
                    </label>
                </div>
            </div>
        </div>
        <div if="{ blockerIsActive.checked }" class="form-group">
            <label for="blackList" class="col-xs-12 col-sm-4 control-label">
                Domains black list:
            </label>
            <div class="col-xs-12 col-sm-8">
                <textarea id="blackList" class="form-control" style="min-height: 140px;" oninput="{ changed }">{ options.blackList }</textarea>
            </div>
        </div>
        <div class="form-group">
            <div class="col-xs-12 col-sm-4"></div>
            <div class="col-xs-12 col-sm-8">
                <div class="{ 'btn': true, 'btn-info': isSaved, 'btn-success': !isSaved }">
                    <span if="{ !isSaved }"><span class="btn-icon btn-icon-rotate">&#x21bb;</span>Saving...</span>
                    <span if="{ isSaved }">Saved</span>
                </div>
            </div>
        </div>
    </form>`;

riot.tag('options', optionsTemplate, function(opts) {
    var component = this;

    component.options = {
        apiKey: '',
        blackList: 'twitter.com\nfacebook.com',
        openIn: 'web',
        blockerIsActive: false
    };

    component.isKeyChanged = false;
    component.message = '';
    component.isSaved = true;

    component.save = function () {
        component.isSaved = false;

        chrome.storage.sync.set({
            options: component.options
        }, function() {
            // component.message = 'Options saved...';
            // component.update();

            setTimeout(function () {
                // component.message = '';
                component.isSaved = true;
                component.update();
            }, 2000);
        });

        return false;
    };

    component.reload = function () {
        chrome.runtime.reload();
    };

    component.changed = function () {
        /*if (component.options.apiKey != component.apiKey.value) {
            component.isSaved = false;
        }

        if (component.options.blackList != component.blackList.value) {
            component.isSaved = false;
        }

        if (component.options.openIn != component.openIn.value) {
            component.isSaved = false;
        }

        if (component.options.blockerIsActive != component.blockerIsActive.checked) {
            component.isSaved = false;
        }*/

        component.options.apiKey = component.apiKey.value;
        component.options.blackList = component.blackList.value;
        component.options.openIn = component.openIn.value;
        component.options.blockerIsActive = component.blockerIsActive.checked;

        component.isKeyChanged = component.options.apiKey == component.apiKey.value;

        component.save();
    };

    chrome.storage.sync.get({
        options: component.options
    }, function(data) {
        component.options = data.options;
        component.update();
    });
});

riot.mount('*');
