let currentTask = '';
let currentStep = 0;
let maxSteps = 5;
let isDone = false;
let selectedLine = null;
let flaggedLine = null;

async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    if (body) {
        options.body = JSON.stringify(body);
    }
    const response = await fetch(endpoint, options);
    if (!response.ok) {
        alert('API Error: ' + await response.text());
        throw new Error('API Error');
    }
    return await response.json();
}

function parseAndRenderDiff(diffContent) {
    const tbody = document.getElementById('diff-table').querySelector('tbody');
    tbody.innerHTML = '';
    
    const lines = diffContent.split('\n');
    let currentLineNum = 1;

    for (let line of lines) {
        if (line.startsWith('---') || line.startsWith('+++')) {
            continue;
        }
        if (line.startsWith('@@')) {
            const match = line.match(/\+([0-9]+)/);
            if (match) {
                currentLineNum = parseInt(match[1]);
            }
            continue;
        }

        const tr = document.createElement('tr');
        tr.className = 'diff-row';
        
        const tdNum = document.createElement('td');
        tdNum.className = 'line-num';
        const tdCode = document.createElement('td');
        tdCode.className = 'line-content';
        
        if (line.startsWith('-')) {
            tr.classList.add('diff-del');
            tdCode.textContent = line;
            tdNum.textContent = '';
        } else if (line.startsWith('+')) {
            tr.classList.add('diff-add');
            tdCode.textContent = line;
            tdNum.textContent = currentLineNum;
            tr.dataset.line = currentLineNum;
            currentLineNum++;
        } else {
            tdCode.textContent = line.startsWith(' ') ? line : (' ' + line);
            tdNum.textContent = currentLineNum;
            tr.dataset.line = currentLineNum;
            currentLineNum++;
        }

        if (tr.dataset.line) {
            if (flaggedLine && parseInt(tr.dataset.line) === flaggedLine) {
                tr.classList.add('flagged');
            }

            tr.addEventListener('click', () => {
                if (currentTask === 'task1_easy' && !isDone) {
                    document.querySelectorAll('.diff-row').forEach(r => r.classList.remove('selected'));
                    tr.classList.add('selected');
                    selectedLine = parseInt(tr.dataset.line);
                    document.getElementById('selected-line').value = selectedLine;
                }
            });
        }
        
        tr.appendChild(tdNum);
        tr.appendChild(tdCode);
        tbody.appendChild(tr);
    }
}

function updateUI(obs, state) {
    currentTask = obs.task_id;
    currentStep = state ? state.current_step : obs.step;
    isDone = state ? state.done : false;
    flaggedLine = obs.flagged_line || null;

    document.getElementById('task-badge').textContent = obs.task_id;
    document.getElementById('goal-text').textContent = obs.goal;
    document.getElementById('step-count').textContent = currentStep;
    
    if (obs.task_id === 'task1_easy') {
        document.getElementById('task1-controls').style.display = 'block';
        document.getElementById('task2-controls').style.display = 'none';
    } else {
        document.getElementById('task1-controls').style.display = 'none';
        document.getElementById('task2-controls').style.display = 'block';
        if (flaggedLine) {
            document.getElementById('flagged-line').value = flaggedLine;
        }
    }

    parseAndRenderDiff(obs.diff_content);
}

function updateFeedback(reward, done) {
    document.getElementById('score-text').textContent = reward.score.toFixed(2);
    document.getElementById('done-text').textContent = done ? 'True' : 'False';
    document.getElementById('feedback-text').textContent = reward.feedback;
}

function renderHistory(history) {
    const list = document.getElementById('history-list');
    list.innerHTML = '';
    history.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        list.appendChild(li);
    });
}

document.getElementById('btn-reset').addEventListener('click', async () => {
    const taskId = document.getElementById('task-select').value;
    const obs = await apiCall('/reset', 'POST', { task_id: taskId });
    updateUI(obs, { current_step: 0, done: false });
    updateFeedback({ score: 0.0, feedback: '-' }, false);
    document.getElementById('history-list').innerHTML = '';
    selectedLine = null;
    document.getElementById('selected-line').value = '';
    document.getElementById('fix-code').value = '';
});

async function sendAction(actionObj) {
    if (isDone) {
        alert("Environment is done. Please reset.");
        return;
    }
    const result = await apiCall('/step', 'POST', actionObj);
    const state = await apiCall('/state');
    
    updateUI(result.observation, state);
    updateFeedback(result.reward, result.done);
    renderHistory(state.history);
}

document.getElementById('btn-flag').addEventListener('click', () => {
    if (selectedLine === null) {
        alert("Please select a line first.");
        return;
    }
    const bugType = document.getElementById('bug-type').value;
    sendAction({
        action_type: 'click_line',
        line_number: selectedLine,
        bug_type: bugType
    });
});

document.getElementById('btn-fix').addEventListener('click', () => {
    const fixCode = document.getElementById('fix-code').value;
    if (!fixCode) {
        alert("Please enter a fix.");
        return;
    }
    sendAction({
        action_type: 'submit_fix',
        line_number: flaggedLine,
        fix_code: fixCode
    });
});

document.getElementById('btn-noop').addEventListener('click', () => {
    sendAction({ action_type: 'noop' });
});

window.onload = async () => {
    try {
        const obs = await apiCall('/reset', 'POST', { task_id: 'task1_easy' });
        updateUI(obs, { current_step: 0, done: false });
    } catch(e) {
        console.error("Make sure server is running.");
    }
};
