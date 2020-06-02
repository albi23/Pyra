window.onload = function () {
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
                if (currStateTile && currStateTile.children[0] && currStateTile.children[0].textContent) {
                    let newState = currStateTile.children[0].textContent;
                    updateTaskState(newState, taskId);
                }
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

            list.addEventListener('dragleave', function (e) {
                currStateTile = null;
                this.style.backgroundColor = 'rgba(0, 0, 0, 0.1)';
            });

            list.addEventListener('drop', function (e) {
                this.append(draggedItem);
                this.style.backgroundColor = 'rgba(0, 0, 0, 0.1)';
            });
        }
    }
};

function updateTaskState(newState, taskId) {
    $.post({
        url: '/update-task',
        data: {
            'newState': newState.toString().trim(),
            'task_id': taskId.toString().trim(),
        },
        dataType: 'json',
    });
}

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}