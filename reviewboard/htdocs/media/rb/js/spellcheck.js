function getSuggestion(t) {
    rbApiCall({
        type: 'GET',
        url: SITE_ROOT + "api/dictionary?check=" + t.textContent,
        success: function(rsp,status){
            alert(rsp.dictionary.suggest);
        },
    });
};


function changeStyle(o) {
    if (o.className == 's_spellerr')
        {
        o.className = 's';
        }
    else
        {
        o.className = 'c';
        }
}


function ignoreOnce(t) {
    changeStyle(t);
}


function addToDict(t) {
    rbApiCall({
        type: 'POST',
        url: SITE_ROOT + "api/dictionary/",
        data: 'add_word='+ t.textContent,
        success: changeStyle(t),
    });
}


$('.s_spellerr').contextMenu('spellcheckMenu', {
    bindings: {
        'ignore': function(t){ignoreOnce(t)},
        'add': function(t){addToDict(t)},
    }
});

$('.c_spellerr').contextMenu('spellcheckMenu', {
    bindings: {
        'ignore': function(t){ignoreOnce(t)},
        'add': function(t){addToDict(t)},
    }
});
