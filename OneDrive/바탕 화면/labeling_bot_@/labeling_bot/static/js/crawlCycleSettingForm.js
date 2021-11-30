'use static'

let data = {};

function OnClickDone(){
    saveSelectedDay();
    saveSelectedTime();
    if (completeCheck()) {
        alert("The model training will take several times");
        sendSelectedLabels();
    } else {
        alert("Select All");
    }
}

function completeCheck(){
    keys = Object.keys(data);
    for (let i=0; i<keys.length; i++) {
        if (data[keys[i]].length == 0) {
            return false;
        }
    }
    return true;
}

function saveSelectedDay() {
    let days = document.getElementsByName('day');
    data['day'] = []
    for (let i=0; i<days.length; i++) {
        if(days[i].checked) {
            data['day'].push(days[i].value);
        }
    }
}

function saveSelectedTime() {
    let times = document.getElementsByName('time');
    data['time'] = []
    for (let i=0; i<times.length; i++) {
        if(times[i].checked) {
            data['time'].push(times[i].value);
        }
    }
}

function sendSelectedLabels() {
    data = JSON.stringify(data);
    $.ajax({
        type:'POST',
        url:'/crawlCycleSetting/submit',
        dataType:'json',
        data: data,
        success: function (response) {
            location.href=response.page;
        },
        error: function (response) {
            return false;
        }
    })
}