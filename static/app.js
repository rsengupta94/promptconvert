const promptInput = document.getElementById('promptInput');
const convertButton = document.getElementById('convertButton');
const output = document.getElementById('output');
const copyButton = document.getElementById('copyButton');

function setBusy(isBusy) {
  convertButton.disabled = isBusy;
  convertButton.textContent = isBusy ? 'Generating...' : 'Get System Prompt';
}

async function convertPrompt() {
  const prompt = promptInput.value.trim();
  if (!prompt) {
    output.value = 'Please enter a prompt first.';
    return;
  }

  setBusy(true);
  output.value = '';

  try {
    const res = await fetch('/api/convert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });

    const data = await res.json();
    if (!res.ok) {
      output.value = data.detail || 'Request failed. Check your API key and settings.';
      return;
    }

    output.value = data.system_prompt || '';
  } catch (err) {
    output.value = 'Network error. Ensure the server is running and your model endpoint is reachable.';
  } finally {
    setBusy(false);
  }
}

async function copyOutput() {
  const text = output.value;
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    copyButton.textContent = 'Copied!';
    setTimeout(() => (copyButton.textContent = 'Copy'), 1400);
  } catch (err) {
    copyButton.textContent = 'Failed';
    setTimeout(() => (copyButton.textContent = 'Copy'), 1400);
  }
}

convertButton.addEventListener('click', convertPrompt);
copyButton.addEventListener('click', copyOutput);

promptInput.addEventListener('keydown', (e) => {
  if (e.metaKey && e.key === 'Enter') {
    convertPrompt();
  }
});
