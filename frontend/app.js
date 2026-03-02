const API_BASE = 'http://127.0.0.1:8000';
let token = '';

function setToken(t){ token = t; document.getElementById('tokenPreview').textContent = token ? token.slice(0,40)+"..." : '(none)'; }

function showError(elemId, error) {
  document.getElementById(elemId).textContent = `ERROR: ${error}`;
}

async function postJson(path, body, useAuth=true){
  const headers = {'Content-Type':'application/json'};
  if(useAuth && token) headers['Authorization'] = `Bearer ${token}`;
  try {
    const res = await fetch(API_BASE + path, { method:'POST', headers, body: JSON.stringify(body) });
    return res;
  } catch(e) {
    throw new Error(`Network error: ${e.message}`);
  }
}

async function getJson(path, params={}, useAuth=true){
  const headers = {};
  if(useAuth && token) headers['Authorization'] = `Bearer ${token}`;
  const qs = new URLSearchParams(params).toString();
  const url = qs ? `${API_BASE}${path}?${qs}` : `${API_BASE}${path}`;
  try {
    const res = await fetch(url, { headers });
    return res;
  } catch(e) {
    throw new Error(`Network error: ${e.message}`);
  }
}

// Register
document.getElementById('btnRegister').onclick = async ()=>{
  try {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    if(!email || !password) { alert('Email and password required'); return; }
    const r = await postJson('/auth/register', {email, password}, false);
    const json = await r.json();
    if(r.ok && json.access_token){ setToken(json.access_token); alert('Registered!'); }
    else alert('Register failed: ' + JSON.stringify(json));
  } catch(e) {
    alert('Register error: ' + e.message);
  }
}

// Login
document.getElementById('btnLogin').onclick = async ()=>{
  try {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    if(!email || !password) { alert('Email and password required'); return; }
    const r = await postJson('/auth/login', {email, password}, false);
    const json = await r.json();
    if(r.ok && json.access_token){ setToken(json.access_token); alert('Logged in!'); }
    else alert('Login failed: ' + JSON.stringify(json));
  } catch(e) {
    alert('Login error: ' + e.message);
  }
}

// Add Memory
document.getElementById('btnAddMemory').onclick = async ()=>{
  try {
    if(!token) { alert('Please register/login first'); return; }
    const text = document.getElementById('memoryText').value;
    if(!text) { alert('Enter memory text'); return; }
    const memory_type = document.getElementById('memoryType').value;
    const emotion = document.getElementById('memoryEmotion').value;
    const importance = parseFloat(document.getElementById('memoryImportance').value || '0.5');
    const res = await postJson('/memory/add', { text, memory_type, emotion, importance }, true);
    const json = await res.json();
    document.getElementById('addResult').textContent = JSON.stringify({status: res.status, body: json}, null, 2);
  } catch(e) {
    showError('addResult', e.message);
  }
}

// Search
document.getElementById('btnSearch').onclick = async ()=>{
  try {
    if(!token) { alert('Please register/login first'); return; }
    const q = document.getElementById('searchQuery').value;
    if(!q) { alert('Enter search query'); return; }
    const res = await getJson('/memory/search', {query: q}, true);
    const json = await res.json();
    document.getElementById('searchResult').textContent = JSON.stringify({status: res.status, body: json}, null, 2);
  } catch(e) {
    showError('searchResult', e.message);
  }
}

document.getElementById('btnSyncEmails').onclick = async ()=>{
  try {
    if(!token) { alert('Please register/login first'); return; }
    const res = await postJson('/emails/sync', {}, true);
    const json = await res.json();
    document.getElementById('emailResult').textContent = JSON.stringify({status: res.status, body: json}, null, 2);
  } catch(e) {
    showError('emailResult', e.message);
  }
};

document.getElementById('btnListEmails').onclick = async ()=>{
  try {
    if(!token) { alert('Please register/login first'); return; }
    const res = await getJson('/emails/', {}, true);
    const json = await res.json();
    document.getElementById('emailResult').textContent = JSON.stringify({status: res.status, body: json}, null, 2);
  } catch(e) {
    showError('emailResult', e.message);
  }
};

document.getElementById('btnDashboard').onclick = async ()=>{
  try {
    if(!token) { alert('Please register/login first'); return; }
    const res = await getJson('/dashboard/overview', {}, true);
    const json = await res.json();
    document.getElementById('dashboardResult').textContent = JSON.stringify({status: res.status, body: json}, null, 2);
  } catch(e) {
    showError('dashboardResult', e.message);
  }
};

document.getElementById('btnRunEmailAgent').onclick = async ()=>{
  try {
    if(!token) { alert('Please register/login first'); return; }
    const res = await postJson('/agents/run-email-agent', {}, true);
    const json = await res.json();
    document.getElementById('agentResult').textContent = JSON.stringify({status: res.status, body: json}, null, 2);
  } catch(e) {
    showError('agentResult', e.message);
  }
};

document.getElementById('btnRunMonitoring').onclick = async ()=>{
  try {
    if(!token) { alert('Please register/login first'); return; }
    const res = await postJson('/agents/run-monitoring', {}, true);
    const json = await res.json();
    document.getElementById('agentResult').textContent = JSON.stringify({status: res.status, body: json}, null, 2);
  } catch(e) {
    showError('agentResult', e.message);
  }
};

document.getElementById('btnUploadDoc').onclick = async ()=>{
  try {
    if(!token) { alert('Please register/login first'); return; }
    const fileInput = document.getElementById('docFile');
    if(!fileInput.files.length){ alert('choose a file'); return; }
    const fd = new FormData();
    fd.append('file', fileInput.files[0]);
    const headers = {};
    if(token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(API_BASE + '/documents/upload', { method:'POST', headers, body: fd });
    const json = await res.json();
    document.getElementById('docResult').textContent = JSON.stringify({status: res.status, body: json}, null, 2);
  } catch(e) {
    showError('docResult', e.message);
  }
};

document.getElementById('btnReason').onclick = async ()=>{
  try {
    if(!token) { alert('Please register/login first'); return; }
    const q = document.getElementById('reasonQuery').value;
    if(!q) { alert('Enter a question'); return; }
    const res = await getJson('/reasoning/analyze', {query: q}, true);
    const json = await res.json();
    document.getElementById('reasonResult').textContent = JSON.stringify({status: res.status, body: json}, null, 2);
  } catch(e) {
    showError('reasonResult', e.message);
  }
};

console.log('LifeOS frontend loaded. API: ' + API_BASE);
