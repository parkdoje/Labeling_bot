'use static'

let data = {};
let repositories = ''
let currentRepo = '';

window.onload = function () {
    fetchRepositoriesInformation();
}

function fetchRepositoriesInformation() {
    $.ajax({
        type:'GET',
        url:'/RepositoriesInformation',
        dataType:'json',
        success: function (response) {
            repositories = Object.keys(response);
            spreadRepoName(repositories, response);
        },
        error: function (response) {
            return false;
        }
    })
}

function sendSelectedLabels() {
    data = JSON.stringify(data);
    $.ajax({
        type:'POST',
        url:'/RepositoriesInformation',
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

function spreadRepoName(repositories, response){
    let box = document.getElementById('RepositoriesBox');
    for (let i=0; i<repositories.length; i++) {
        let repositoryName = repositories[i];
        let labels = response[repositoryName];
        const repository = makeRepoDiv(repositoryName, labels, i);
        box.appendChild(repository);
    }
}

function spreadLabels(repository, labels) {
    let rangeNumber = 3;
    let labelsTableDiv = document.getElementById('LabelsTableDiv');
    labelsTableDiv.innerHTML = repository;

    let table = document.getElementById('LabelsTable');
    table = empty(table);

    for (let i=0; i<labels.length; i+=rangeNumber){
        row = makeLabelTableElement(repository, labels.slice(i, i+rangeNumber));
        table.appendChild(row);
    }
}

function makeRepoDiv(repositoryName, labels, i){
    const repository = document.createElement('div');
    repository.setAttribute("style", "display :block");
    repository.setAttribute("id", repositoryName);
    repository.innerHTML = repositoryName;
    repository.addEventListener("click", () => OnClickRepo(repositoryName, labels));
    if (i==0) {
        currentRepo = repositoryName; 
        spreadLabels(repositoryName, labels);
        $(repository).css('background', 'gray');
    }
    return repository;
}

function makeLabelTableElement(repository, labels) {
    const row_tr = document.createElement('tr');

    for (let i=0; i<labels.length; i++){
        const row_td = document.createElement('td');

        if (i>0) {
            row_td.setAttribute('class', 'td-2');
        }
        const row_input = document.createElement('input');
        const row_label = document.createElement('label');

        row_input.setAttribute('type', 'checkbox');
        row_input.setAttribute('name', 'label');
        row_input.setAttribute('id', labels[i]);
        row_input.checked=checkChecked(repository, labels[i]);

        row_label.setAttribute('for', labels[i]);
        row_label.innerHTML = labels[i];

        row_td.appendChild(row_input);
        row_td.appendChild(row_label);
        row_tr.appendChild(row_td);
    }
    return row_tr;
}

function empty(box){
    while (box.firstChild) {
        box.removeChild(box.firstChild);
    }
    return box;
}

function OnClickRepo(repository, labels){
    saveSelectedLabels(currentRepo);
    currentRepo = repository;
    changeColor(repository);
    spreadLabels(repository, labels);
}

function OnClickNext(){
    saveSelectedLabels(currentRepo);
    if(completeCheck()) {
        sendSelectedLabels();
    } else {
        alert("Set All Project");
    }
}

function checkChecked(repository, label){
    let keys = Object.keys(data)
    if (keys.includes(repository)) {
        let checkedLabels = data[repository];
        console.log(checkedLabels);
        if (checkedLabels.includes(label)) {
            return true;
        } else {
            return false;
        }
    } else {
        return false;
    }
}

function completeCheck() {
    keys = Object.keys(data);
    // console.log(keys);
    // console.log(repositories);
    if (keys.length == repositories.length) {
        return true;
    } else {
        return false;
    }
}

function saveSelectedLabels(repository) {
    let labels = document.getElementsByName('label');
    data[repository] = [];
    for (let i=0; i<labels.length; i++) {
        if(labels[i].checked) {
            data[repository].push(labels[i].id);
        }
    }
}

function changeColor(repository) {
    let box = document.getElementById('RepositoriesBox');
    for (let i=0; i<box.childElementCount; i++){
        let child = box.children[i];
        if (child.getAttribute('id') == repository) {
            $(child).css('background', 'gray');
        } else {
            $(child).css('background', 'white');
        }
    }
}
