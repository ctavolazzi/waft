const API_URL = 'http://localhost:8002/api';

let currentResults = null;

// DOM elements
const runTestsBtn = document.getElementById('runTests');
const clearResultsBtn = document.getElementById('clearResults');
const statusDiv = document.getElementById('status');
const resultsDiv = document.getElementById('results');

// Event listeners
runTestsBtn.addEventListener('click', runTests);
clearResultsBtn.addEventListener('click', clearResults);

async function runTests() {
    // Disable button and show status
    runTestsBtn.disabled = true;
    statusDiv.classList.remove('hidden');
    resultsDiv.innerHTML = '';

    try {
        const response = await fetch(`${API_URL}/run-tests`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        currentResults = data;
        displayResults(data);
    } catch (error) {
        console.error('Error running tests:', error);
        displayError(error.message);
    } finally {
        runTestsBtn.disabled = false;
        statusDiv.classList.add('hidden');
    }
}

function clearResults() {
    resultsDiv.innerHTML = '';
    currentResults = null;
    
    // Add empty state
    resultsDiv.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">🧪</div>
            <div class="empty-state-text">No tests run yet. Click "Run Tests" to get started!</div>
        </div>
    `;
}

function displayResults(data) {
    resultsDiv.innerHTML = '';

    // Summary
    const summary = createSummary(data);
    resultsDiv.appendChild(summary);

    // Test items
    if (data.tests && data.tests.length > 0) {
        data.tests.forEach((test, index) => {
            setTimeout(() => {
                const testItem = createTestItem(test, index);
                resultsDiv.appendChild(testItem);
            }, index * 100); // Stagger animation
        });
    } else {
        resultsDiv.innerHTML += `
            <div class="empty-state">
                <div class="empty-state-icon">📝</div>
                <div class="empty-state-text">No tests found to run.</div>
            </div>
        `;
    }
}

function createSummary(data) {
    const summary = document.createElement('div');
    summary.className = 'summary';
    
    const total = data.summary?.total || 0;
    const passed = data.summary?.passed || 0;
    const failed = data.summary?.failed || 0;
    const skipped = data.summary?.skipped || 0;
    const duration = data.summary?.duration || 0;

    summary.innerHTML = `
        <h2>${getSummaryEmoji(passed, failed, total)} Test Results</h2>
        <div class="summary-stats">
            <div class="stat">
                <div class="stat-value">${total}</div>
                <div class="stat-label">Total</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #10b981;">${passed}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #ef4444;">${failed}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #f59e0b;">${skipped}</div>
                <div class="stat-label">Skipped</div>
            </div>
            <div class="stat">
                <div class="stat-value">${duration.toFixed(2)}s</div>
                <div class="stat-label">Duration</div>
            </div>
        </div>
    `;

    return summary;
}

function getSummaryEmoji(passed, failed, total) {
    if (total === 0) return '📝';
    if (failed === 0) return '🎉';
    if (passed === 0) return '😢';
    return '📊';
}

function createTestItem(test, index) {
    const item = document.createElement('div');
    item.className = `test-item ${test.status}`;
    
    const icon = getStatusIcon(test.status);
    const duration = test.duration ? `${test.duration.toFixed(3)}s` : '';

    item.innerHTML = `
        <div class="test-header">
            <span class="test-icon">${icon}</span>
            <span class="test-name">${escapeHtml(test.name)}</span>
            ${duration ? `<span class="test-duration">${duration}</span>` : ''}
        </div>
        ${test.message ? `<div class="test-message">${escapeHtml(test.message)}</div>` : ''}
        ${test.error ? `<div class="test-error">${escapeHtml(test.error)}</div>` : ''}
    `;

    return item;
}

function getStatusIcon(status) {
    switch (status) {
        case 'passed':
            return '✅';
        case 'failed':
            return '❌';
        case 'skipped':
            return '⏭️';
        default:
            return '❓';
    }
}

function displayError(message) {
    resultsDiv.innerHTML = `
        <div class="test-item failed">
            <div class="test-header">
                <span class="test-icon">⚠️</span>
                <span class="test-name">Error</span>
            </div>
            <div class="test-error">${escapeHtml(message)}</div>
        </div>
    `;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize with empty state
clearResults();
