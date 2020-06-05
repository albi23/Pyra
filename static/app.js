window.onload = function () {
    $('#task-add-success').hide();
    $('#task-add-failure').hide();
    $('#board-add-success').hide();
    $('#board-add-failure').hide();

    const list_items = document.querySelectorAll('.list-item');
    const lists = document.querySelectorAll('.list');
    let draggedItem = null;
    let currStateTile = null;

    for (let i = 0; i < list_items.length; i++) {
        const item = list_items[i];

        item.addEventListener('dragstart', function () {
            draggedItem = item;
            setTimeout(function () {
                item.style.display = 'none';
            }, 0)
        });

        item.addEventListener('dragend', function () {
            setTimeout(function () {
                draggedItem.style.display = 'block';
                let taskId = draggedItem.getAttribute('data-internalid');
                let newState = currStateTile.children[0].textContent;
                updateTaskState(newState, taskId);
                draggedItem = null;
            }, 0);
        })

        for (let j = 0; j < lists.length; j++) {
            const list = lists[j];

            list.addEventListener('dragover', function (e) {
                e.preventDefault();
            });

            list.addEventListener('dragenter', function (e) {
                e.preventDefault();
                currStateTile = list;
                this.style.backgroundColor = 'rgba(0, 0, 0, 0.2)';
            });

            list.addEventListener('dragleave', function () {
                this.style.backgroundColor = 'rgba(0, 0, 0, 0.1)';
            });

            list.addEventListener('drop', function () {
                this.append(draggedItem);
                this.style.backgroundColor = 'rgba(0, 0, 0, 0.1)';
            });
        }
    }
};


// END BLOCK
class Task {
    constructor(title, description, status, priority,
                board, created, last_modified, created_by) {
        this.title = title;
        this.description = description;
        this.status = status;
        this.priority = priority;
        this.board = board;
        this.created = created;
        this.last_modified = last_modified;
        this.created_by = created_by;
    }
}

// GLOBAL VARIABLE BLOCK
let currentUpdatedTask = new Task();
let statusMapping = new Map();
statusMapping.set('VH', ['#da1c2ed6', 'Very high'])
statusMapping.set('HIGH', ['#ffa500', 'High'])
statusMapping.set('NORMAL', ['#ffff00', 'Normal'])
statusMapping.set('LOW', ['#37bf37', 'Low'])
statusMapping.set('VL', ['#808080', 'Very low'])


function updateTaskState(newState, taskId) {
    $.post({
        url: '/update-task/',
        data: {
            'new_state': newState.toString().trim(),
            'task_id': taskId.toString().trim(),
        },
        dataType: 'json',
    });
}

function toggleMenu() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function createNewTask() {
    const title = $('#task-title').val();
    const description = $('#task-description').val();
    const state = $('#task-state').val();
    const priority = $('#task-priority').val();
    const url = window.location.href.split('/');
    const board_id = url[url.length - 2];

    if (!isTaskTitleValid(title) || !isTaskDescriptionValid(description)) {
        return;
    }

    $.post({
        url: '/create-task/',
        data: {
            'title': title,
            'description': description,
            'status': state,
            'priority': priority,
            'board_id': board_id,
        },
        dataType: 'json',
        success: () => {
            $('#task-add-failure').hide();
            $('#task-title').val('');
            $('#task-description').val('');
            $('#task-add-success').show();
            setTimeout(() => {
                $('#task-add-success').hide();
            }, 3000)
        }
    });
}

function closeNewTaskModal() {
    $('#task-state').val('TODO');
    $('#task-add-success').hide();
    document.getElementById("myDropdown").classList.toggle("show", false);
    location.reload();
}

function createNewBoard() {
    const name = $('#board-name').val();
    const description = $('#board-description').val();

    if (!isBoardNameValid(name) || !isBoardDescriptionValid(description)) {
        return;
    }

    $.post({
        url: '/create-board/',
        data: {
            'name': name,
            'description': description,
        },
        dataType: 'json',
        success: () => {
            $('#board-add-failure').hide();
            $('#board-name').val('');
            $('#board-description').val('');
            $('#board-add-success').show();
            setTimeout(() => {
                $('#board-add-success').hide();
            }, 3000);
        }
    });
}

function closeNewBoardModal() {
    $('#board-add-success').hide();
    document.getElementById("myDropdown").classList.toggle("show", false);
    location.reload();
}

function isTaskTitleValid(title) {
    if (!isStringLengthValid(title, 30)) {
        displayErrorMessage('task-add-failure', 'Title too long (max 30 characters)!');
        return false
    }

    if (!stringNotEmpty(title)) {
        displayErrorMessage('task-add-failure', 'Title can\'t be empty!');
        return false;
    }

    return true;
}

function isBoardNameValid(title) {
    if (!isStringLengthValid(title, 30)) {
        displayErrorMessage('board-add-failure', 'Name too long (max 30 characters)!');
        return false
    }

    if (!stringNotEmpty(title)) {
        displayErrorMessage('board-add-failure', 'Name can\'t be empty!');
        return false;
    }

    return true;
}

function isTaskDescriptionValid(title) {
    if (!isStringLengthValid(title, 200)) {
        displayErrorMessage('task-add-failure', 'Description too long (max 200 characters)!');
        return false
    }
    if (!stringNotEmpty(title)) {
        displayErrorMessage('task-add-failure', 'Description can\'t be empty!');
        return false;
    }

    return true;
}

function isBoardDescriptionValid(title) {
    if (!isStringLengthValid(title, 200)) {
        displayErrorMessage('board-add-failure', 'Description too long (max 200 characters)!');
        return false
    }
    if (!stringNotEmpty(title)) {
        displayErrorMessage('board-add-failure', 'Description can\'t be empty!');
        return false;
    }

    return true;
}

function isStringLengthValid(str, len) {
    return (str.length <= len);
}

function stringNotEmpty(str) {
    return str.length > 0;
}

function displayErrorMessage(alertBoxId, errorMessage) {
    const alertBox = $('#' + alertBoxId);
    alertBox.text(errorMessage);
    alertBox.show();
}

function loadTaskView(task) {
    this.currentUpdatedTask = task[0]['fields'];
    this.currentUpdatedTask.created = assignFormattedDate(this.currentUpdatedTask.created);
    this.currentUpdatedTask.last_modified = assignFormattedDate(this.currentUpdatedTask.last_modified);
    console.log(this.currentUpdatedTask)
    toggleTaskEditMode();
    passDataIntoEditTemplate();
}

function toggleTaskEditMode() {
    document.getElementById("edit-task-block").classList.toggle("hide");
}

function assignFormattedDate(data) {
    let dataArr = data.split('T');
    return dataArr[0].concat(' ').concat(dataArr[1].substr(0, 8))
}

function toggleTaskMenu() {
    document.getElementById('edit-task').classList.toggle("show");
}

function toggleTaskPriority() {
    document.getElementById('edit-priority').classList.toggle("show");
}

function updateMenuValue(id) {
    document.getElementById("taskDropDown").innerText = id.toUpperCase();
    toggleTaskMenu();
}

function setTaskOptionStatus(idKey) {
    assignNewPriority(idKey)
    toggleTaskPriority()
}

function assignNewPriority(idKey) {
    let statusObj = document.getElementById('priority-val');
    statusObj.innerText = statusMapping.get(idKey)[1];
    statusObj.style.background = statusMapping.get(idKey)[0];
}

function passDataIntoEditTemplate() {
    document.getElementById('title-value').value = this.currentUpdatedTask.title;
    document.getElementById('desc-value').value = this.currentUpdatedTask.description;
    assignNewPriority(this.currentUpdatedTask.priority)
    document.getElementById("taskDropDown").innerText = this.currentUpdatedTask.status;
    document.getElementById("create-val").innerText = this.currentUpdatedTask.created;
    document.getElementById("modify-val").innerText = this.currentUpdatedTask.last_modified;
}

