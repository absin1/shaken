fetchSnippets = function () {
    var req = new XMLHttpRequest();
    req.open('GET', '/read?page=' + $('#page').val()
     +'&q='+encodeURIComponent($('#search').val())
     + '&page_size='+$('#page_size').val(), true);
    req.onreadystatechange = function (aEvt) {
        if (req.readyState == 4) {
            if (req.status == 200) {
                init(req.response);
            } else {
                alert('failed loading audio');
            }
        }
    };
    req.send(null);
}

init = function (response) {
    var resp = JSON.parse(response);
    resp.forEach(function (item, index, arr) {
        snippets.push(item);
    });
    fetch('/assets/asrrow.template').then((response) => response.text())
        .then((template) => {
            var rendered = Mustache.render(template, { "snippets": snippets });
            document.getElementById('list').innerHTML += rendered;
        });

}
play = function (snippet_id) {
    var snippet = undefined;
    snippets.forEach(function (s, index, arr) {
        if(s.sid == snippet_id)
            snippet = s;
    });
    if(snippet){
        var url = window.location.origin + '/audio/' + snippet.path.split('files/')[1];
        if(audio && !audio.paused){
            audio.pause();
            if(audio.currentSrc.includes(snippet.sid))
                return
        }
        audio = new Audio(url);
        audio.addEventListener('timeupdate', (event) => {
            var prog = parseInt(audio.currentTime/audio.duration*100.0);
            var proge = $('.progress-barzz[snippet="'+snippet.sid+'"]')[0]
            proge.style.width = prog*12;
            if(audio.currentTime>snippet.to_time)
                audio.pause();
        });
        audio.play();
    }
}


function like(snippet_id) {
    var req = new XMLHttpRequest();
    req.open('GET', '/update?snippet_id=' + encodeURIComponent(snippet_id) + '&text='
        + encodeURIComponent(event.target.parentElement.parentElement.children[2].children[0].innerText), true);
    req.onreadystatechange = function (aEvt) {
        if (req.readyState == 4) {
            if (req.status == 200) {
                alert('Saved successfully');
            } else {
                alert('failed loading audio');
            }
        }
    };
    req.send(null);
}

function delete_snippet(snippet_id) {
    var req = new XMLHttpRequest();
    req.open('GET', '/delete?snippet_id=' + encodeURIComponent(snippet_id), true);
    req.onreadystatechange = function (aEvt) {
        if (req.readyState == 4) {
            if (req.status == 200) {
                alert('deleted successfully');
            } else {
                alert('failed loading audio');
            }
        }
    };
    req.send(null);
}

function scrolled(o) {
    //visible height + pixel scrolled = total height
    if (o.offsetHeight + o.scrollTop == o.scrollHeight) {
        alert("End");
        page++;
        fetchSnippets();
    }
}

changeaudioduration = function(){
    console.log($('.progress-barzz').offset().left);
    console.log(event.offsetX);
    audio.currentTime = event.offsetX/1155*audio.duration;
}

var channels = 1;
var page = 0;
var whoami;
var snippets = [];
var audio;
$(document).ready(function () {
    //fetchSnippets();
});
