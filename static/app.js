window.onload = function () {
    $('#task-add-success').hide();
    $('#board-add-success').hide();

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

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function createNewTask() {
    const title = $('#task-title').val();
    const description = $('#task-description').val();
    const state = $('#task-state').val();
    const priority = $('#task-priority').val();
    const url = window.location.href.split('/');
    const board_id = url[url.length - 2];

    $.post({
        url: '/create-task/',
        data: {
            'title': title,
            'description': description,
            'state': state,
            'priority': priority,
            'board_id': board_id,
        },
        dataType: 'json',
        success: () => {
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
}

function createNewBoard() {
    const name = $('#board-name').val();
    const description = $('#board-description').val();

    $.post({
        url: '/create-board/',
        data: {
            'name': name,
            'description': description,
        },
        dataType: 'json',
        success: () => {
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
}