const tasks = ['floor & corridor', 'surfaces', 'stove & sink'];
const persons = ['Michal', 'Alex', 'Brian']

var state = 0;

const list = document.getElementById('list');
const lastClicked = document.getElementById('lastClicked');

function recalculateAssignments(state) {
  while (list.firstChild) {
    list.removeChild(list.firstChild);
  }
  for (var i = 0; i < tasks.length; i++) {
    var newElement = document.createElement('li');
    var person = persons[i];
    var task = tasks[(i + state) % tasks.length];
    var html = person + ": <i>" + task + "</i>";
    newElement.innerHTML = html;
    list.appendChild(newElement);
  }
};

document.getElementById('button').addEventListener('click', function () {
  state = (state + 1) % tasks.length;
  recalculateAssignments(state);
  lastClicked.textContent = new Date();
})

recalculateAssignments(state);
