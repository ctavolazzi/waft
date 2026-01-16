/**
 * Renderer Process - UI Logic
 */

const { electronAPI } = window;

// DOM Elements
const apiStatus = document.getElementById('api-status');
const statusDot = apiStatus.querySelector('.status-dot');
const statusText = apiStatus.querySelector('.status-text');
const projectPathInput = document.getElementById('project-path');
const browseBtn = document.getElementById('browse-btn');
const generateBtn = document.getElementById('generate-btn');
const outputSection = document.getElementById('output-section');
const loadingSection = document.getElementById('loading-section');
const resultsDiv = document.getElementById('results');

// Check API health on load
checkApiHealth();

// Set up interval to check API health every 30 seconds
setInterval(checkApiHealth, 30000);

async function checkApiHealth() {
  try {
    const result = await electronAPI.checkApiHealth();
    if (result.healthy) {
      statusDot.classList.add('healthy');
      statusDot.classList.remove('unhealthy');
      statusText.textContent = 'API Connected';
      generateBtn.disabled = false;
    } else {
      statusDot.classList.add('unhealthy');
      statusDot.classList.remove('healthy');
      statusText.textContent = 'API Disconnected';
      generateBtn.disabled = true;
    }
  } catch (error) {
    statusDot.classList.add('unhealthy');
    statusDot.classList.remove('healthy');
    statusText.textContent = 'API Error';
    generateBtn.disabled = true;
  }
}

browseBtn.addEventListener('click', async () => {
  try {
    const result = await electronAPI.showOpenDialog({
      properties: ['openDirectory'],
      title: 'Select Project Directory',
    });
    
    if (!result.canceled && result.filePaths && result.filePaths.length > 0) {
      projectPathInput.value = result.filePaths[0];
    }
  } catch (error) {
    await electronAPI.showErrorBox('Error', `Failed to open directory dialog: ${error.message}`);
  }
});

generateBtn.addEventListener('click', async () => {
  // Show loading
  loadingSection.style.display = 'block';
  outputSection.style.display = 'none';
  generateBtn.disabled = true;

  try {
    const projectPath = projectPathInput.value.trim() || null;
    
    const result = await electronAPI.recapAndReview({
      project_path: projectPath,
      output_path: null,
    });

    // Hide loading
    loadingSection.style.display = 'none';
    generateBtn.disabled = false;

    // Show results
    displayResults(result);

  } catch (error) {
    loadingSection.style.display = 'none';
    generateBtn.disabled = false;
    displayError(error.message);
  }
});

function displayResults(result) {
  outputSection.style.display = 'block';
  resultsDiv.innerHTML = '';

  if (result.success) {
    const successDiv = document.createElement('div');
    successDiv.className = 'result-item';
    successDiv.innerHTML = `
      <h3>✅ Success!</h3>
      <p><strong>Mindspace review generated successfully</strong></p>
      ${result.markdown_file ? `<p>Markdown: <a href="#" onclick="openFile('${result.markdown_file}')">${result.markdown_file}</a></p>` : ''}
      ${result.pdf_file ? `<p>PDF: <a href="#" onclick="openFile('${result.pdf_file}')">${result.pdf_file}</a></p>` : ''}
    `;
    resultsDiv.appendChild(successDiv);

    if (result.mindspace_data) {
      const dataDiv = document.createElement('div');
      dataDiv.className = 'result-item';
      dataDiv.innerHTML = `
        <h3>Mindspace Data</h3>
        <p><strong>Thoughts:</strong> ${result.mindspace_data.thoughts?.length || 0} captured</p>
        <p><strong>Decisions:</strong> ${result.mindspace_data.decisions?.length || 0} documented</p>
        <p><strong>Work in Progress:</strong> ${result.mindspace_data.work_in_progress?.length || 0} items</p>
        <p><strong>Questions:</strong> ${result.mindspace_data.questions?.length || 0} open</p>
      `;
      resultsDiv.appendChild(dataDiv);
    }
  } else {
    displayError(result.error || 'Unknown error occurred');
  }
}

function displayError(message) {
  outputSection.style.display = 'block';
  resultsDiv.innerHTML = `
    <div class="result-item">
      <h3 class="error">❌ Error</h3>
      <p>${message}</p>
    </div>
  `;
}

async function openFile(filePath) {
  try {
    const result = await electronAPI.openFile(filePath);
    if (!result.success) {
      await electronAPI.showErrorBox('Error', `Failed to open file: ${result.error || 'Unknown error'}`);
    }
  } catch (error) {
    await electronAPI.showErrorBox('Error', `Error opening file: ${error.message}`);
  }
}

// Make openFile available globally for onclick handlers
window.openFile = openFile;

// Listen for menu events
electronAPI.onMenuGenerateReview(() => {
  generateBtn.click();
});

// Theme support
let currentTheme = 'light';

async function initTheme() {
  currentTheme = await electronAPI.getTheme();
  updateTheme(currentTheme);
}

function updateTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  currentTheme = theme;
}

electronAPI.onThemeChanged((theme) => {
  updateTheme(theme);
});

// Initialize theme on load
initTheme();

// Recent documents
async function loadRecentDocuments() {
  try {
    const recent = await electronAPI.getRecentDocuments();
    if (recent && recent.length > 0) {
      // Could display recent documents in UI
      console.log('Recent documents:', recent);
    }
  } catch (error) {
    console.error('Error loading recent documents:', error);
  }
}

// Load recent documents on startup
loadRecentDocuments();
