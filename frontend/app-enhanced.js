const API_BASE = 'http://127.0.0.1:8000';
let token = '';

function setToken(t) {
  token = t;
  const preview = document.getElementById('tokenPreview');
  if (t) {
    preview.textContent = 'Token: ' + t.slice(0, 50) + '...';
    preview.style.color = '#28a745';
  } else {
    preview.textContent = 'No token';
    preview.style.color = '#999';
  }
}

function showMessage(elemId, msg, type = 'info') {
  const elem = document.getElementById(elemId);
  if (!elem) return;
  elem.innerHTML = `<div class="message ${type}">${escapeHtml(msg)}</div>`;
}

function showError(elemId, error) {
  showMessage(elemId, `Error: ${error}`, 'error');
}

function showOutput(elemId, data) {
  const elem = document.getElementById(elemId);
  if (!elem) return;
  elem.innerHTML = `<div class="output">${escapeHtml(JSON.stringify(data, null, 2))}</div>`;
}

function showMemoryResults(elemId, results) {
  const elem = document.getElementById(elemId);
  if (!elem) return;
  
  if (!results || results.length === 0) {
    elem.innerHTML = '<div class="message info">No memories found</div>';
    return;
  }
  
  let html = '<div>';
  results.forEach((mem, i) => {
    const emotion_badge = `<span class="badge ${mem.emotion}">${mem.emotion}</span>`;
    const score_pct = Math.round(mem.similarity_score * 100);
    html += `
      <div class="memory-result">
        <h4>#${mem.id} • ${mem.memory_type.toUpperCase()} • ${emotion_badge} • Relevance: ${score_pct}%</h4>
        <p>"${mem.text}"</p>
        <p style="font-size:0.8rem; color:#999;">Importance: ${mem.importance.toFixed(1)}/1.0</p>
      </div>
    `;
  });
  html += '</div>';
  elem.innerHTML = html;
}

function escapeHtml(text) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return text.replace(/[&<>"']/g, m => map[m]);
}

async function apiCall(path, method = 'GET', body = null, useAuth = true) {
  const headers = {};
  if (method !== 'GET') headers['Content-Type'] = 'application/json';
  if (useAuth && token) headers['Authorization'] = `Bearer ${token}`;
  
  try {
    const opts = { method, headers };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(API_BASE + path, opts);
    const json = await res.json();
    return { status: res.status, ok: res.ok, data: json };
  } catch (e) {
    throw new Error(`Network error: ${e.message}`);
  }
}

// ============ AUTH ============
document.getElementById('btnRegister').onclick = async () => {
  try {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    if (!email || !password) { alert('Enter email and password'); return; }
    
    const res = await apiCall('/auth/register', 'POST', { email, password }, false);
    if (res.ok && res.data.access_token) {
      setToken(res.data.access_token);
      showMessage('authStatus', `Welcome ${email}!`, 'success');
      document.getElementById('password').value = '';
    } else {
      showError('authStatus', res.data.detail || 'Registration failed');
    }
  } catch (e) {
    showError('authStatus', e.message);
  }
};

document.getElementById('btnLogin').onclick = async () => {
  try {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    if (!email || !password) { alert('Enter email and password'); return; }
    
    const res = await apiCall('/auth/login', 'POST', { email, password }, false);
    if (res.ok && res.data.access_token) {
      setToken(res.data.access_token);
      showMessage('authStatus', `Logged in as ${email}`, 'success');
      document.getElementById('password').value = '';
    } else {
      showError('authStatus', res.data.detail || 'Login failed');
    }
  } catch (e) {
    showError('authStatus', e.message);
  }
};

// ============ MEMORY ============
document.getElementById('memoryImportance').oninput = (e) => {
  document.getElementById('impValue').textContent = e.target.value;
};

document.getElementById('btnAddMemory').onclick = async () => {
  try {
    if (!token) { alert('Please register/login first'); return; }
    const text = document.getElementById('memoryText').value.trim();
    if (!text) { alert('Enter memory text'); return; }
    
    const res = await apiCall('/memory/add', 'POST', {
      text,
      memory_type: document.getElementById('memoryType').value,
      emotion: document.getElementById('memoryEmotion').value,
      importance: parseFloat(document.getElementById('memoryImportance').value)
    });
    
    if (res.ok) {
      showMessage('addResult', `Memory #${res.data.id} saved successfully!`, 'success');
      document.getElementById('memoryText').value = '';
    } else {
      showError('addResult', res.data.detail || 'Failed to save');
    }
  } catch (e) {
    showError('addResult', e.message);
  }
};

document.getElementById('btnSearch').onclick = async () => {
  try {
    if (!token) { alert('Please register/login first'); return; }
    const query = document.getElementById('searchQuery').value.trim();
    if (!query) { alert('Enter search query'); return; }
    
    const res = await apiCall(`/memory/search?query=${encodeURIComponent(query)}`);
    if (res.ok) {
      showMemoryResults('searchResult', res.data);
    } else {
      showError('searchResult', res.data.detail || 'Search failed');
    }
  } catch (e) {
    showError('searchResult', e.message);
  }
};

// ============ DASHBOARD ============
document.getElementById('btnDashboard').onclick = async () => {
  try {
    if (!token) { alert('Please register/login first'); return; }
    const res = await apiCall('/dashboard/overview');
    if (res.ok) {
      const data = res.data;
      let html = `<div class="message info">`;
      html += `<strong>Memory Count:</strong> ${data.memory_count}<br>`;
      if (data.emotion_distribution && data.emotion_distribution.length > 0) {
        html += `<strong>Emotions:</strong> `;
        html += data.emotion_distribution.map(e => `${e.emotion}(${e.count})`).join(', ');
      }
      html += `</div>`;
      document.getElementById('dashboardResult').innerHTML = html;
    } else {
      showError('dashboardResult', res.data.detail || 'Failed');
    }
  } catch (e) {
    showError('dashboardResult', e.message);
  }
};

// ============ EMAILS ============
document.getElementById('btnSyncEmails').onclick = async () => {
  try {
    if (!token) { alert('Please register/login first'); return; }
    const res = await apiCall('/emails/sync', 'POST', {});
    if (res.ok) {
      showMessage('emailResult', `Email sync initiated: ${res.data.message || 'OK'}`, 'info');
    } else {
      showError('emailResult', res.data.detail || 'Sync failed');
    }
  } catch (e) {
    showError('emailResult', e.message);
  }
};

document.getElementById('btnListEmails').onclick = async () => {
  try {
    if (!token) { alert('Please register/login first'); return; }
    const res = await apiCall('/emails/');
    if (res.ok) {
      if (res.data.length === 0) {
        showMessage('emailResult', 'No emails yet', 'info');
      } else {
        showOutput('emailResult', res.data);
      }
    } else {
      showError('emailResult', res.data.detail || 'Failed');
    }
  } catch (e) {
    showError('emailResult', e.message);
  }
};

// ============ AGENTS ============
document.getElementById('btnRunEmailAgent').onclick = async () => {
  try {
    if (!token) { alert('Please register/login first'); return; }
    const res = await apiCall('/agents/run-email-agent', 'POST', {});
    if (res.ok) {
      showMessage('agentResult', res.data.status, 'success');
    } else {
      showError('agentResult', res.data.detail || 'Failed');
    }
  } catch (e) {
    showError('agentResult', e.message);
  }
};

document.getElementById('btnRunMonitoring').onclick = async () => {
  try {
    if (!token) { alert('Please register/login first'); return; }
    const res = await apiCall('/agents/run-monitoring', 'POST', {});
    if (res.ok) {
      showMessage('agentResult', res.data.status, 'success');
    } else {
      showError('agentResult', res.data.detail || 'Failed');
    }
  } catch (e) {
    showError('agentResult', e.message);
  }
};

// ============ REASONING ============
document.getElementById('btnReason').onclick = async () => {
  try {
    if (!token) { alert('Please register/login first'); return; }
    const query = document.getElementById('reasonQuery').value.trim();
    if (!query) { alert('Ask a question'); return; }
    
    const res = await apiCall(`/reasoning/analyze?query=${encodeURIComponent(query)}`);
    if (res.ok) {
      const data = res.data;
      let html = '<div class="output" style="max-height:500px; overflow-y:auto;">';
      if (data.llm_explanation) {
        html += `<strong>Reasoning Result:</strong><br>${escapeHtml(data.llm_explanation)}<br><br>`;
      }
      if (data.message) {
        html += `<p>${escapeHtml(data.message)}</p>`;
      }
      html += '</div>';
      document.getElementById('reasonResult').innerHTML = html;
    } else {
      showError('reasonResult', res.data.detail || 'Reasoning failed');
    }
  } catch (e) {
    showError('reasonResult', e.message);
  }
};

// ============ DOCUMENTS ============
document.getElementById('btnUploadDoc').onclick = async () => {
  try {
    if (!token) { alert('Please register/login first'); return; }
    const file = document.getElementById('docFile').files[0];
    if (!file) { alert('Choose a file'); return; }
    
    const fd = new FormData();
    fd.append('file', file);
    
    const opts = { 
      method: 'POST', 
      headers: { 'Authorization': `Bearer ${token}` },
      body: fd 
    };
    const res = await fetch(API_BASE + '/documents/upload', opts);
    const json = await res.json();
    
    if (res.ok) {
      showMessage('docResult', `Document uploaded: ${file.name}`, 'success');
    } else {
      showError('docResult', json.detail || 'Upload failed');
    }
  } catch (e) {
    showError('docResult', e.message);
  }
};

console.log('LifeOS Frontend Ready - API: ' + API_BASE);
