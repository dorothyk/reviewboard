var gSpellCheck
gSpellCheck = new RB.SpellCheck

$('.s_spellerr').contextMenu('spellcheckMenu', {
    bindings: {
        'spellcheck_ignore': function(t) { gSpellCheck.ignoreOnce(t); },
        'spellcheck_add': function(t) { gSpellCheck.addToDict(t); },
    },
});

$('.c_spellerr').contextMenu('spellcheckMenu', {
    bindings: {
        'spellcheck_ignore': function(t) { gSpellCheck.ignoreOnce(t); },
        'spellcheck_add': function(t) { gSpellCheck.addToDict(t); },
    },
});
