var langs =
[['Afrikaans',       ['af-ZA']],
 ['Bahasa Indonesia',['id-ID']],
 ['Bahasa Melayu',   ['ms-MY']],
 ['Català',          ['ca-ES']],
 ['Čeština',         ['cs-CZ']],
 ['Dansk',           ['da-DK']],
 ['Deutsch',         ['de-DE']],
 ['English',         ['en-AU', 'Australia'],
                     ['en-CA', 'Canada'],
                     ['en-IN', 'India'],
                     ['en-NZ', 'New Zealand'],
                     ['en-ZA', 'South Africa'],
                     ['en-GB', 'United Kingdom'],
                     ['en-US', 'United States']],
 ['Español',         ['es-AR', 'Argentina'],
                     ['es-BO', 'Bolivia'],
                     ['es-CL', 'Chile'],
                     ['es-CO', 'Colombia'],
                     ['es-CR', 'Costa Rica'],
                     ['es-EC', 'Ecuador'],
                     ['es-SV', 'El Salvador'],
                     ['es-ES', 'España'],
                     ['es-US', 'Estados Unidos'],
                     ['es-GT', 'Guatemala'],
                     ['es-HN', 'Honduras'],
                     ['es-MX', 'México'],
                     ['es-NI', 'Nicaragua'],
                     ['es-PA', 'Panamá'],
                     ['es-PY', 'Paraguay'],
                     ['es-PE', 'Perú'],
                     ['es-PR', 'Puerto Rico'],
                     ['es-DO', 'República Dominicana'],
                     ['es-UY', 'Uruguay'],
                     ['es-VE', 'Venezuela']],
 ['Euskara',         ['eu-ES']],
 ['Filipino',        ['fil-PH']],
 ['Français',        ['fr-FR']],
 ['Galego',          ['gl-ES']],
 ['Hrvatski',        ['hr_HR']],
 ['IsiZulu',         ['zu-ZA']],
 ['Íslenska',        ['is-IS']],
 ['Italiano',        ['it-IT', 'Italia'],
                     ['it-CH', 'Svizzera']],
 ['Lietuvių',        ['lt-LT']],
 ['Magyar',          ['hu-HU']],
 ['Nederlands',      ['nl-NL']],
 ['Norsk bokmål',    ['nb-NO']],
 ['Polski',          ['pl-PL']],
 ['Português',       ['pt-BR', 'Brasil'],
                     ['pt-PT', 'Portugal']],
 ['Română',          ['ro-RO']],
 ['Slovenščina',     ['sl-SI']],
 ['Slovenčina',      ['sk-SK']],
 ['Suomi',           ['fi-FI']],
 ['Svenska',         ['sv-SE']],
 ['Tiếng Việt',      ['vi-VN']],
 ['Türkçe',          ['tr-TR']],
 ['Ελληνικά',        ['el-GR']],
 ['български',       ['bg-BG']],
 ['Pусский',         ['ru-RU']],
 ['Српски',          ['sr-RS']],
 ['Українська',      ['uk-UA']],
 ['한국어',            ['ko-KR']],
 ['中文',             ['cmn-Hans-CN', '普通话 (中国大陆)'],
                     ['cmn-Hans-HK', '普通话 (香港)'],
                     ['cmn-Hant-TW', '中文 (台灣)'],
                     ['yue-Hant-HK', '粵語 (香港)']],
 ['日本語',           ['ja-JP']],
 ['हिन्दी',            ['hi-IN']],
 ['ภาษาไทย',         ['th-TH']]];

for (var i = 0; i < langs.length; i++) {
  select_language.options[i] = new Option(langs[i][0], i);
}

var language_index = 7;
var dialect_index  = 6;

// show lang setting
if (localStorage.VS_lang) {
  for (var i = 0; i < langs.length; i++) {
    var dialects = langs[i].slice(1);
    var found_dialect_index = dialects.findIndex(function (dialect_info) {
      return dialect_info[0] == localStorage.VS_lang;
    });
    if (found_dialect_index != -1) {
      language_index = i;
      dialect_index  = found_dialect_index;
      break;
    }
  }
}

select_language.selectedIndex = language_index;
updateCountry();
select_dialect.selectedIndex  = dialect_index;

showInfo('info_start');

function updateCountry(event) {
  for (var i = select_dialect.options.length - 1; i >= 0; i--) {
    select_dialect.remove(i);
  }
  var list = langs[select_language.selectedIndex];
  for (var i = 1; i < list.length; i++) {
    select_dialect.options.add(new Option(list[i][1], list[i][0]));
  }
  select_dialect.style.visibility = list[1].length == 1 ? 'hidden' : 'visible';

  if (recognizing) recognition.stop();
  if (event) localStorage.VS_lang = select_dialect.value;
  //setTimeout(startSpeechSearch, 500);
}

function updateDialect() {
  if (recognizing) recognition.stop();
  localStorage.VS_lang = select_dialect.value;
  //setTimeout(startSpeechSearch, 500);
}

var start_button = document.getElementById('microphone-button');
var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;
if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
  upgrade();
} else {
  start_button.style.display = 'inline-block';
  var SpeachRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognition = new SpeachRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onstart = function() {
    recognizing = true;
    showInfo('info_speak_now');
    start_button.className = 'button recording-start';
  };

  recognition.onerror = function(event) {
    if (event.error == 'no-speech') {
      start_button.className = 'button';
      showInfo('info_no_speech');
      ignore_onend = true;
    }
    if (event.error == 'audio-capture') {
      start_button.className = 'button';
      showInfo('info_no_microphone');
      ignore_onend = true;
    }
    if (event.error == 'not-allowed') {
      if (event.timeStamp - start_timestamp < 100) {
        showInfo('info_blocked');
      } else {
        showInfo('info_denied');
      }
      ignore_onend = true;
    }
  };
   //TODO:"aborted", "network", "service-not-allowed", 
   //      "bad-grammar", "language-not-supported"

  recognition.onend = function() {
    recognizing = false;
    if (ignore_onend) {
      return;
    }
    start_button.className = 'button';
    if (!final_transcript) {
      showInfo('info_start');
      return;
    }
    showInfo('');

    parent.postMessage({name: 'speechSearchEnded', content: final_transcript}, '*');
  };

  var timeout;
  
  recognition.onresult = function(event) {
    //console.log('onresult')
    showInfo('');
    var interim_transcript = '';
    if (typeof(event.results) == 'undefined') {
      recognition.onend = null;
      recognition.stop();
      upgrade();
      return;
    }
    
    start_button.className = 'button recording-results';
    clearTimeout(timeout);
    timeout = setTimeout(recognition.stop.bind(recognition), 1000);
    
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    final_transcript = capitalize(final_transcript);
    final_span.innerHTML = linebreak(final_transcript);
    interim_span.innerHTML = linebreak(interim_transcript);
    if (final_transcript || interim_transcript) {
      // first results are in...
    }
  };
  
  window.addEventListener('unload', function (){
    recognition.onend = null;
    recognition.stop();
  })

}

function upgrade() {
  start_button.style.visibility = 'hidden';
  showInfo('info_upgrade');
}

var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
  return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

var first_char = /\S/;
function capitalize(s) {
  return s.replace(first_char, function(m) { return m.toUpperCase(); });
}

function startSpeechSearch(event) {
  if (!recognition) return;

  if (recognizing) {
    recognition.stop();
    return;
  }
  final_transcript = '';
  recognition.lang = select_dialect.value;
  recognition.start();
  ignore_onend = false;
  final_span.innerHTML = '';
  interim_span.innerHTML = '';
  start_button.className = 'button disabled';
  showInfo('info_allow');
  start_timestamp = Date.now();
}

function showInfo(s) {
  if (s) {
    for (var child = info.firstChild; child; child = child.nextSibling) {
      if (child.style) {
        child.style.display = child.id == s ? 'inline' : 'none';
      }
    }
    info.style.visibility = 'visible';
  } else {
    info.style.visibility = 'hidden';
  }
}



start_button.onclick = startSpeechSearch;
document.getElementById('select_language').onchange = updateCountry;
document.getElementById('select_dialect').onchange = updateDialect;

startSpeechSearch();

document.getElementById('close-button').onclick = function () {
  parent.postMessage({name: 'speechClose'}, '*');
}







  /*
   recognition.onaudiostart = function(event) {
     console.log('onaudiostart', event)
   };
   recognition.onsoundstart = function(event) {
      console.log('onsoundstart', event)
   };
  recognition.onspeechstart = function(event) {
     console.log('onspeechstart', event)

   };
  recognition.onspeechend = function(event) {
     console.log('onspeechend', event)
   };
  recognition.onsoundend = function(event) {
      console.log('onsoundend', event)
   };
  recognition.onaudioend = function(event) {
     console.log('onaudioend', event) 
   };
    recognition.onnomatch = function(event) {
      console.log('onnomatch', event)
   };
   */
 