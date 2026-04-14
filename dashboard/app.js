// ROOT injected server-side, safe const
const ROOT = document.body.dataset.root;
let _advanceSystem = null;
let _cmdQueue = Promise.resolve(); // serialise commands to avoid race conditions
let _cachedState = null;
let _subagentMap = {};
let _docPreviewPath = null;
let _advanceMode = 'advance';
let _cmdStatusTimer = null;
let _cmdStatusStartedAt = 0;
let _toastTimer = null;

function defaultCommandDetail() {
  return 'Use the console for validation, smoke checks, and workflow commands.';
}

function setCommandStatus(title, detail = defaultCommandDetail()) {
  document.getElementById('cmd-label').textContent = title;
  document.getElementById('cmd-detail').textContent = detail;
}

function stopCommandTimer(finalDetail = '') {
  if (_cmdStatusTimer) {
    clearInterval(_cmdStatusTimer);
    _cmdStatusTimer = null;
  }
  _cmdStatusStartedAt = 0;
  if (finalDetail) document.getElementById('cmd-detail').textContent = finalDetail;
}

function startCommandTimer(title, detailPrefix) {
  stopCommandTimer();
  _cmdStatusStartedAt = Date.now();
  const render = () => {
    const elapsedSeconds = Math.max(0, Math.round((Date.now() - _cmdStatusStartedAt) / 1000));
    setCommandStatus(title, `${detailPrefix} ${elapsedSeconds}s elapsed.`);
  };
  render();
  _cmdStatusTimer = setInterval(render, 1000);
}

function finishCommandStatus(title, detailPrefix) {
  const elapsedSeconds = _cmdStatusStartedAt ? Math.max(0, Math.round((Date.now() - _cmdStatusStartedAt) / 1000)) : 0;
  stopCommandTimer(`${detailPrefix}${elapsedSeconds ? ` ${elapsedSeconds}s total.` : ''}`.trim());
  document.getElementById('cmd-label').textContent = title;
}

function showToast(message, kind = 'info') {
  const toast = document.getElementById('app-toast');
  toast.textContent = message;
  toast.className = `app-toast ${kind}`;
  if (_toastTimer) clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => {
    toast.className = 'app-toast hidden';
  }, 2200);
}

function getRecentProjects() {
  return JSON.parse(localStorage.getItem('programstartRecentProjects') || '[]');
}

function setRecentProjects(items) {
  localStorage.setItem('programstartRecentProjects', JSON.stringify(items));
}

function currentStepEntry(system) {
  const sys = _cachedState?.[system];
  if (!sys) return null;
  return { step: sys.active, entry: sys.entries?.[sys.active] || {} };
}

function sliceStatusBadge(status) {
  const value = String(status || 'Pending');
  if (value === 'Ready' || value === 'Completed') return `<span class="badge ok">${esc(value)}</span>`;
  if (value === 'Blocked') return `<span class="badge blocker">${esc(value)}</span>`;
  return `<span class="badge active">${esc(value)}</span>`;
}

function getActiveProject() {
  const projects = getRecentProjects();
  const activeDest = localStorage.getItem('programstartActiveProjectDest');
  return projects.find((item) => item.dest === activeDest) || projects[0] || null;
}

function addRecentProject(project) {
  const existing = getRecentProjects().filter((item) => item.dest !== project.dest);
  const next = [project, ...existing].slice(0, 8);
  setRecentProjects(next);
  localStorage.setItem('programstartActiveProjectDest', project.dest);
}

// ── State loading ──────────────────────────────────────────────────
async function loadAll() {
  try {
    const r = await fetch('/api/state');
    const data = await r.json();
    if (data.error) { console.error(data.error); return; }
    _cachedState = data;
    renderFocusPanel(data);
    renderSystem('pb', data.programbuild);
    renderSystem('uj', data.userjourney);
    renderControlDocs(data.catalog, data.programbuild);
    renderSubagents(data.catalog, data.programbuild);
    renderKickoffHandoff(data.catalog, data.programbuild);
    renderUserJourneyExecution(data.catalog);
    renderDriftDashboard(data.catalog);
    // Status bar
    const pbPct = data.programbuild.total > 0 ? Math.round((data.programbuild.completed / data.programbuild.total) * 100) : 0;
    const ujPct = data.userjourney.total > 0 ? Math.round((data.userjourney.completed / data.userjourney.total) * 100) : 0;
    document.getElementById('sb-pb').textContent = `${data.programbuild.active} (${pbPct}%)`;
    document.getElementById('sb-uj').textContent = data.userjourney.attached ? `${data.userjourney.active} (${ujPct}%)` : 'optional';
    const oq = data.userjourney.attached ? (data.userjourney.open_questions || 0) : 0;
    const blockerEl = document.getElementById('sb-blockers');
    const ujBlockerBadge = document.getElementById('uj-blockers');
    if (!data.userjourney.attached) {
      blockerEl.innerHTML = `<span class="dot yellow"></span> USERJOURNEY is optional and not attached`;
      ujBlockerBadge.style.display = 'none';
    } else if (oq > 0) {
      blockerEl.innerHTML = `<span class="dot red"></span> ${oq} external decision${oq>1?'s':''} unresolved`;
      ujBlockerBadge.textContent = `${oq} blocker${oq>1?'s':''}`;
      ujBlockerBadge.style.display = '';
    } else {
      blockerEl.innerHTML = `<span class="dot green"></span> No active blockers`;
      ujBlockerBadge.style.display = 'none';
    }
    const now = new Date().toLocaleTimeString();
    document.getElementById('lastUpdated').textContent = now;
    document.getElementById('sb-updated').textContent = `Updated ${now}`;
    // Update status dots
    updateDot('dot-pb', data.programbuild);
    updateDot('dot-uj', data.userjourney);
  } catch (e) { console.error('loadAll failed', e); }
}

function updateDot(id, sys) {
  const el = document.getElementById(id);
  if (sys.completed === sys.total) el.className = 'dot green';
  else if (sys.blocked > 0) el.className = 'dot red';
  else el.className = 'dot yellow';
}

function jumpToSection(id) {
  const tabMap = {
    'control-section': 'references',
    'subagent-section': 'references',
    'kickoff-section': 'setup',
    'uj-execution-section': 'execution',
    'drift-section': 'diagnostics',
    'console-section': 'diagnostics',
  };
  if (tabMap[id]) activateTab(tabMap[id]);
  const el = document.getElementById(id);
  if (!el) return;
  el.scrollIntoView({behavior: 'smooth', block: 'start'});
}

function activateTab(name) {
  const tabs = ['references', 'setup', 'execution', 'diagnostics'];
  for (const tab of tabs) {
    document.getElementById(`tab-btn-${tab}`).classList.toggle('active', tab === name);
    document.getElementById(`tab-panel-${tab}`).classList.toggle('hidden', tab !== name);
  }
}

function openGuide(system) {
  jumpToSection('guide-section');
  runCmd(system === 'programbuild' ? 'guide.programbuild' : 'guide.userjourney');
}

function renderFocusPanel(data) {
  const pb = data.programbuild;
  const uj = data.userjourney;
  const pbDesc = (pb.descriptions || {})[pb.active] || 'Review the current PROGRAMBUILD step and confirm the required evidence before advancing.';
  const pbNote = pb.completed === pb.total
    ? 'PROGRAMBUILD is complete.'
    : `Current stage: ${pb.active}. ${pb.completed} of ${pb.total} complete.`;
  const pbFiles = (pb.step_files || {})[pb.active] || [];
  const pbDeliverables = pbFiles.length
    ? `<div class="focus-deliverables"><div class="focus-meta" style="margin-bottom:4px">Key deliverables for this stage:</div><ul style="margin:0 0 0 16px;padding:0">${pbFiles.slice(0, 6).map(f => `<li class="meta">${esc(f)}</li>`).join('')}</ul></div>`
    : '';
  document.getElementById('focus-pb').innerHTML = `
    <div class="focus-kicker">PROGRAMBUILD</div>
    <div class="focus-title">Stay on the active stage</div>
    <div class="focus-body">${esc(pbDesc)}</div>
    ${pbDeliverables}
    <div class="focus-meta">${esc(pbNote)}</div>
    <div class="focus-actions">
      <button class="btn primary" onclick="openGuide('programbuild')">Review Next Step</button>
      <button class="btn ghost" onclick="jumpToSection('control-section')">Open References</button>
    </div>`;

  if (!uj.attached) {
    document.getElementById('focus-uj').innerHTML = `
      <div class="focus-kicker">USERJOURNEY</div>
      <div class="focus-title">Keep this optional until it is needed</div>
      <div class="focus-body">Attach USERJOURNEY only when the product includes onboarding, consent, activation, or first-run routing that needs explicit planning.</div>
      <div class="focus-meta">Current mode: PROGRAMBUILD-only.</div>
      <div class="focus-actions">
        <button class="btn primary" onclick="jumpToSection('kickoff-section')">Review Attachment Rules</button>
        <button class="btn ghost" onclick="openBootstrapModal()">New Project</button>
      </div>`;
    return;
  }

  const ujDesc = (uj.descriptions || {})[uj.active] || 'Review the active USERJOURNEY phase and the current delivery slice before advancing.';
  const openQuestions = uj.open_questions || 0;
  const blockerText = openQuestions > 0
    ? `${openQuestions} external decision${openQuestions > 1 ? 's' : ''} still block progress.`
    : 'No blocking external decisions are currently recorded.';
  document.getElementById('focus-uj').innerHTML = `
    <div class="focus-kicker">USERJOURNEY</div>
    <div class="focus-title">Resolve the active phase with less context switching</div>
    <div class="focus-body">${esc(ujDesc)}</div>
    <div class="focus-meta">${esc(blockerText)}</div>
    <div class="focus-actions">
      <button class="btn primary" onclick="openGuide('userjourney')">Review Next Step</button>
      <button class="btn ghost" onclick="jumpToSection('uj-execution-section')">Open Delivery Tracker</button>
    </div>`;
}

function renderSystem(prefix, sys) {
  const isPB = prefix === 'pb';
  if (!sys.attached && !isPB) {
    document.getElementById(`${prefix}-active`).textContent = 'Optional attachment not present';
    document.getElementById(`${prefix}-bar`).style.width = '0%';
    document.getElementById(`${prefix}-progress-label`).textContent = 'optional';
    document.getElementById(`${prefix}-summary`).textContent = 'USERJOURNEY is not active in this workspace. Attach it only when the product needs onboarding, consent, activation, or first-run routing design.';
    document.getElementById(`${prefix}-steps`).innerHTML = '<div class="meta">Attach USERJOURNEY only for projects that need interactive onboarding, consent, activation, or first-run routing.</div>';
    document.getElementById('uj-continue-btn').disabled = true;
    document.getElementById('uj-advance-btn').disabled = true;
    document.getElementById('uj-refresh-guide-btn').disabled = true;
    document.getElementById('uj-status-btn').disabled = true;
    document.getElementById('uj-drift-btn').disabled = true;
    document.getElementById('uj-signoff-btn').disabled = true;
    document.getElementById('uj-dry-run-btn').disabled = true;
    document.getElementById('uj-more-actions').open = false;
    return;
  }
  if (!isPB) {
    document.getElementById('uj-continue-btn').disabled = false;
    document.getElementById('uj-advance-btn').disabled = false;
    document.getElementById('uj-refresh-guide-btn').disabled = false;
    document.getElementById('uj-status-btn').disabled = false;
    document.getElementById('uj-drift-btn').disabled = false;
    document.getElementById('uj-signoff-btn').disabled = false;
    document.getElementById('uj-dry-run-btn').disabled = false;
  }
  document.getElementById(`${prefix}-active`).textContent =
    (isPB ? 'Stage: ' : 'Phase: ') + sys.active;
  const pct = sys.total > 0 ? Math.round((sys.completed / sys.total) * 100) : 0;
  document.getElementById(`${prefix}-bar`).style.width = pct + '%';
  document.getElementById(`${prefix}-progress-label`).textContent =
    `${sys.completed}/${sys.total} (${pct}%)`;
  const currentDesc = (sys.descriptions || {})[sys.active] || '';
  const blockedCount = sys.blocked || 0;
  document.getElementById(`${prefix}-summary`).textContent = currentDesc
    ? `${currentDesc} ${blockedCount > 0 ? `${blockedCount} blocked item${blockedCount > 1 ? 's' : ''} need attention.` : `Progress is ${pct}% complete.`}`
    : `Current ${isPB ? 'stage' : 'phase'}: ${sys.active}. ${blockedCount > 0 ? `${blockedCount} blocked item${blockedCount > 1 ? 's' : ''} need attention.` : `Progress is ${pct}% complete.`}`;
  if (isPB && sys.variant) {
    document.getElementById('pb-variant').textContent = sys.variant;
  }
  const container = document.getElementById(`${prefix}-steps`);
  container.innerHTML = '';
  for (const step of sys.steps) {
    const entry = sys.entries[step] || {};
    const status = entry.status || 'planned';
    const isActive = step === sys.active;
    const signoff = entry.signoff || {};
    const desc = (sys.descriptions || {})[step] || '';
    const div = document.createElement('div');
    div.className = `step${isActive ? ' active' : ''}`;
    const dot = `<span class="step-dot ${status}"></span>`;
    let nameHtml = `<span class="step-name${isActive ? ' active' : ''}">${step}</span>`;
    if (desc) nameHtml += `<div class="step-desc">${esc(desc)}</div>`;
    let sig = '';
    if (signoff.decision && signoff.date) {
      sig = `<span class="step-signoff">${signoff.decision} · ${signoff.date}</span>`;
    }
    div.innerHTML = `${dot}<div class="step-body">${nameHtml}</div>${sig}`;
    container.appendChild(div);
  }
}

function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

function vscodeHref(absPath) {
  return `vscode://file/${encodeURIComponent(absPath.replace(/\\/g, '/'))}`;
}

function workspaceAbsPath(relativePath) {
  return ROOT.replace(/\\/g, '/') + '/' + relativePath;
}

function renderControlDocs(catalog, programbuild) {
  const list = document.getElementById('control-docs-list');
  const meta = document.getElementById('control-meta');
  const docs = catalog?.control_docs || [];
  meta.textContent = `${docs.length} recognized control docs. The current variant is ${programbuild.variant || 'product'}.`;
  list.innerHTML = '';
  for (const doc of docs) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    const isVariant = programbuild.variant && doc.name === `PROGRAMBUILD_${programbuild.variant.toUpperCase()}.md`;
    div.innerHTML = `
      <h3>${esc(doc.name)} ${isVariant ? '<span class="badge variant">active variant</span>' : ''}</h3>
      <p>${esc(doc.purpose || 'No purpose recorded.')}</p>
      <div class="catalog-meta">Canonical for: ${esc(doc.canonical_for || 'n/a')} · ${esc(doc.type || 'n/a')} · ${esc(doc.status || 'n/a')}</div>
      <div class="link-row">
        <button class="btn ghost" onclick="openDocPreview(${JSON.stringify(doc.file)})">Preview</button>
        <a class="btn ghost" href="${vscodeHref(workspaceAbsPath(doc.file))}">Open</a>
      </div>`;
    list.appendChild(div);
  }
}

function renderSubagents(catalog, programbuild) {
  const summary = document.getElementById('subagent-summary');
  const req = document.getElementById('subagent-report-req');
  const cards = document.getElementById('subagent-cards');
  const badge = document.getElementById('subagent-variant-badge');
  const subagents = catalog?.subagents || [];
  const variant = (programbuild.variant || 'product').toLowerCase();
  const stageRecs = catalog?.stage_subagents?.[programbuild.active] || [];
  const variantRecs = catalog?.variant_subagents?.[variant] || [];
  const variantOnly = catalog?.variant_only_subagents?.[variant] || [];
  const gate = catalog?.variant_gate_model?.[variant] || null;

  _subagentMap = Object.fromEntries(subagents.map((item) => [item.name, item]));
  badge.style.display = '';
  badge.textContent = `${variant} mode`;
  summary.textContent = gate
    ? `Current stage: ${programbuild.active}. ${variant} gates use ${gate.gate_style}. Evidence expectation: ${gate.evidence_expectation}`
    : `Current stage: ${programbuild.active}.`;

  req.innerHTML = '';
  for (const item of (catalog?.subagent_report_requirements || [])) {
    req.innerHTML += `<span class="pill dim">${esc(item)}</span>`;
  }

  cards.innerHTML = '';
  for (const agent of subagents) {
    const tags = [];
    if (stageRecs.includes(agent.name)) tags.push('<span class="pill rec">stage recommended</span>');
    if (variantRecs.includes(agent.name)) tags.push('<span class="pill variant">variant recommended</span>');
    const useItems = (agent.use_for || []).map((item) => `<li>${esc(item)}</li>`).join('');
    const div = document.createElement('div');
    div.className = 'subagent-card';
    div.innerHTML = `
      <h3>${esc(agent.name)}</h3>
      <div class="pill-row">${tags.join('')}</div>
      <p>${agent.use_for?.length ? 'Use for:' : 'No use-cases listed.'}</p>
      <ul class="catalog-meta" style="margin:6px 0 0 16px">${useItems}</ul>
      <details class="subagent-details">
        <summary>Show prompt</summary>
        <div class="terminal" style="max-height:160px;margin-top:8px">${esc(agent.prompt || 'No canonical prompt available.')}</div>
      </details>
      <div class="link-row">
        <button class="btn ghost" onclick='copySubagentPrompt(${JSON.stringify(agent.name)})'>Copy Prompt</button>
        <button class="btn ghost" onclick="openDocPreview('PROGRAMBUILD/PROGRAMBUILD_SUBAGENTS.md')">Preview Catalog</button>
        <a class="btn ghost" href="${vscodeHref(workspaceAbsPath('PROGRAMBUILD/PROGRAMBUILD_SUBAGENTS.md'))}">Open Catalog</a>
      </div>`;
    cards.appendChild(div);
  }

  for (const name of variantOnly) {
    const div = document.createElement('div');
    div.className = 'subagent-card';
    div.innerHTML = `
      <h3>${esc(name)}</h3>
      <div class="pill-row"><span class="pill variant">variant-only role</span></div>
      <p>This role is recommended by the ${esc(variant)} playbook, but there is no canonical prompt for it yet in PROGRAMBUILD_SUBAGENTS.md.</p>
      <div class="link-row">
        <a class="btn ghost" href="${vscodeHref(workspaceAbsPath(`PROGRAMBUILD/PROGRAMBUILD_${variant.toUpperCase()}.md`))}">Open Variant Playbook</a>
      </div>`;
    cards.appendChild(div);
  }
}

function kickoffProjectLinks(dest, variant) {
  const links = [
    { label: 'Canonical', path: `${dest}/PROGRAMBUILD/PROGRAMBUILD_CANONICAL.md` },
    { label: 'File Index', path: `${dest}/PROGRAMBUILD/PROGRAMBUILD_FILE_INDEX.md` },
    { label: 'Kickoff Packet', path: `${dest}/PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md` },
    { label: 'Variant Playbook', path: `${dest}/PROGRAMBUILD/PROGRAMBUILD_${variant.toUpperCase()}.md` },
    { label: 'Feasibility', path: `${dest}/PROGRAMBUILD/FEASIBILITY.md` },
    { label: 'Decision Log', path: `${dest}/PROGRAMBUILD/DECISION_LOG.md` },
  ];
  return links;
}

function kickoffStartCommands(dest) {
  const safe = dest.replaceAll('"', '');
  return `cd "${safe}"\n.\\scripts\\pb.ps1 next\n.\\scripts\\pb.ps1 validate`;
}

function renderKickoffHandoff(catalog, programbuild) {
  const summary = document.getElementById('kickoff-summary');
  const files = document.getElementById('kickoff-files');
  const checklist = document.getElementById('kickoff-checklist');
  const lastProject = document.getElementById('kickoff-last-project');
  const activeProject = getActiveProject();
  const lastBootstrap = activeProject || JSON.parse(localStorage.getItem('programstartLastBootstrap') || 'null');
  const variant = (lastBootstrap?.variant || programbuild.variant || 'product').toLowerCase();
  const gate = catalog?.variant_gate_model?.[variant];
  const recentProjects = getRecentProjects();
  const recentEl = document.getElementById('recent-projects');

  summary.textContent = gate
    ? `After bootstrap, lock product shape, USERJOURNEY need, and variant first. Then start with canonical + file index + ${variant} playbook. ${variant} gates use ${gate.gate_style}.`
    : 'After bootstrap, lock product shape, USERJOURNEY need, and your chosen playbook before stage work.';

  files.innerHTML = '';
  for (const item of (catalog?.kickoff?.files || [])) {
    const div = document.createElement('div');
    div.className = 'handoff-card';
    const target = lastBootstrap ? `${lastBootstrap.dest}/PROGRAMBUILD/${item.replace(/\\/g, '/')}` : workspaceAbsPath(`PROGRAMBUILD/${item}`);
    div.innerHTML = `<h3>${esc(item)}</h3><div class="link-row"><button class="btn ghost" onclick="openDocPreview('PROGRAMBUILD/${item}')">Preview</button><a class="btn ghost" href="${vscodeHref(target)}">Open</a></div>`;
    files.appendChild(div);
  }

  checklist.innerHTML = '';
  const decisionRows = catalog?.kickoff?.decision_matrix || [];
  if (decisionRows.length) {
    const matrixRows = decisionRows.map((row) => `
      <tr>
        <td>${esc(row.Decision || '')}</td>
        <td>${esc(row['Choose this when'] || '')}</td>
        <td>${esc(row['Primary effect'] || '')}</td>
      </tr>`).join('');
    const matrixCard = document.createElement('div');
    matrixCard.className = 'handoff-card';
    matrixCard.innerHTML = `
      <h3>Kickoff Decision Matrix</h3>
      <details class="kickoff-details" open>
        <summary>Show decision matrix</summary>
        <div style="overflow:auto;margin-top:8px">
          <table class="data-table">
            <thead>
              <tr><th>Decision</th><th>Choose this when</th><th>Primary effect</th></tr>
            </thead>
            <tbody>${matrixRows}</tbody>
          </table>
        </div>
      </details>`;
    checklist.appendChild(matrixCard);
  }
  for (const section of (catalog?.kickoff?.startup_sections || [])) {
    const div = document.createElement('div');
    div.className = 'handoff-card';
    const items = (section.items || []).map((item) => `<li>${esc(item)}</li>`).join('');
    div.innerHTML = `
      <h3>${esc(section.title)}</h3>
      <details class="kickoff-details" open>
        <summary>Show checklist</summary>
        <ul class="catalog-meta" style="margin:8px 0 0 16px">${items}</ul>
      </details>`;
    checklist.appendChild(div);
  }

  if (!lastBootstrap) {
    const preflight = (catalog?.kickoff?.preflight || []).map((item) => `<li>${esc(item)}</li>`).join('');
    lastProject.innerHTML = `
      <h3>No recent bootstrap in this browser</h3>
      <p>Use <span class="inline-code">+ New Project</span>, then come back here for the first documents and startup checklist.</p>
      <details class="kickoff-details" open>
        <summary>Pre-bootstrap requirements</summary>
        <ul class="catalog-meta" style="margin:8px 0 0 16px">${preflight}</ul>
      </details>`;
    recentEl.innerHTML = '<span class="meta">No recent projects yet.</span>';
    return;
  }

  const links = kickoffProjectLinks(lastBootstrap.dest.replace(/\\/g, '/'), lastBootstrap.variant)
    .map((item) => `<a class="btn ghost" href="${vscodeHref(item.path)}">${esc(item.label)}</a>`)
    .join('');
  const startCommands = kickoffStartCommands(lastBootstrap.dest);
  lastProject.innerHTML = `
    <h3>Last Bootstrap: ${esc(lastBootstrap.project_name)}</h3>
    <p>Destination: <span class="inline-code">${esc(lastBootstrap.dest)}</span></p>
    <div class="pill-row">
      <span class="pill variant">${esc(lastBootstrap.variant)}</span>
      <span class="pill dim">USERJOURNEY attach separately if needed</span>
      <span class="pill dim">${esc(new Date(lastBootstrap.created_at).toLocaleString())}</span>
    </div>
    <div class="link-row">
      <a class="btn primary" href="${vscodeHref(lastBootstrap.dest.replace(/\\/g, '/'))}">Open Project Folder</a>
      <button class="btn ghost" onclick='copyText(${JSON.stringify(startCommands)}, "Starter commands copied")'>Copy Starter Commands</button>
      <button class="btn ghost" onclick='showStarterCommands(${JSON.stringify(startCommands)})'>Show Starter Commands</button>
    </div>
    <div class="link-row">${links}</div>
    <div class="launcher-grid">
      <div class="launcher-card">
        <h4>Start Here</h4>
        <p>Open Canonical, File Index, Kickoff Packet, and your variant playbook first. Then run <span class="inline-code">pb next</span> inside the new project.</p>
      </div>
      <div class="launcher-card">
        <h4>First Commands</h4>
        <div class="terminal" style="max-height:100px">${esc(startCommands)}</div>
      </div>
    </div>`;

  recentEl.innerHTML = '';
  for (const project of recentProjects) {
    const active = project.dest === lastBootstrap.dest;
    const div = document.createElement('div');
    div.className = 'recent-project';
    div.innerHTML = `
      <div class="title">${esc(project.project_name)} ${active ? '<span class="badge active">active</span>' : ''}</div>
      <div class="path">${esc(project.dest)}</div>
      <button class="btn ghost" onclick='selectRecentProject(${JSON.stringify(project.dest)})'>Select</button>
      <a class="btn ghost" href="${vscodeHref(project.dest.replace(/\\/g, '/'))}">Open</a>
      <button class="btn ghost" onclick='removeRecentProject(${JSON.stringify(project.dest)})'>Remove</button>`;
    recentEl.appendChild(div);
  }
}

function renderUserJourneyExecution(catalog) {
  const summary = document.getElementById('uj-exec-summary');
  const phaseOverview = document.getElementById('uj-phase-overview');
  const sliceFocus = document.getElementById('uj-slice-focus');
  const fileReview = document.getElementById('uj-file-review');
  const risks = document.getElementById('uj-risks');
  const phaseSelect = document.getElementById('uj-phase-select');
  const phaseStatus = document.getElementById('uj-phase-status');
  const phaseBlockers = document.getElementById('uj-phase-blockers');
  const sliceSelect = document.getElementById('uj-slice-select');
  const sliceStatus = document.getElementById('uj-slice-status');
  const sliceNote = document.getElementById('uj-slice-note');
  const exec = catalog?.userjourney_execution || {};
  if (!exec.attached) {
    summary.textContent = 'USERJOURNEY is not attached. This workspace is operating in PROGRAMBUILD-only mode.';
    phaseOverview.innerHTML = '<div class="catalog-item"><p>No USERJOURNEY execution data. Attach it only for interactive end-user products.</p></div>';
    sliceFocus.innerHTML = '';
    fileReview.innerHTML = '';
    risks.innerHTML = '';
    phaseSelect.innerHTML = '';
    sliceSelect.innerHTML = '';
    phaseStatus.value = 'Planned';
    phaseBlockers.value = '';
    sliceStatus.value = 'Pending';
    sliceNote.value = '';
    return;
  }
  const phases = exec.phase_overview || [];
  const sliceReadiness = exec.slice_readiness || [];
  const slices = exec.slice_sections || [];
  const mappings = exec.slice_mapping || [];
  const files = exec.file_sections || [];
  const phase0 = phases.find((row) => String(row.Phase || '').trim() === '0') || phases[0];
  const currentSliceRow = sliceReadiness.find((row) => ['Selected', 'Ready', 'Blocked'].includes(String(row.Status || '').trim())) || sliceReadiness[0];
  const currentSliceName = String(currentSliceRow?.Slice || 'Slice 1');
  const slice1 = slices.find((row) => row.title.startsWith(`${currentSliceName}:`)) || slices[0];
  const map1 = mappings.find((row) => String(row.Slice || '').trim() === currentSliceName) || mappings[0];

  summary.textContent = phase0
    ? `Current planning phase: ${phase0.Phase} (${phase0.Status}). Current slice: ${currentSliceName} (${String(currentSliceRow?.Status || 'Pending')}).`
    : 'Execution data loaded.';

  phaseSelect.innerHTML = phases.map((row) => `<option value="${esc(String(row.Phase || ''))}">Phase ${esc(String(row.Phase || ''))}</option>`).join('');
  if (phase0) {
    phaseSelect.value = String(phase0.Phase || '0');
    phaseStatus.value = String(phase0.Status || 'Planned');
    phaseBlockers.value = String(phase0.Blockers || '');
  }
  const sliceOptions = sliceReadiness.length
    ? sliceReadiness.map((row) => String(row.Slice || ''))
    : slices.map((row) => row.title.split(':')[0]);
  sliceSelect.innerHTML = sliceOptions.length
    ? sliceOptions.map((name) => `<option value="${esc(name)}">${esc(name)}</option>`).join('')
    : '<option disabled selected>No slices loaded</option>';
  sliceSelect.value = currentSliceName;
  sliceStatus.value = String(currentSliceRow?.Status || 'Pending');
  sliceNote.value = String(currentSliceRow?.Notes || '');

  phaseOverview.innerHTML = '';
  for (const row of phases.slice(0, 5)) {
    const div = document.createElement('div');
    div.className = 'table-row phase';
    div.innerHTML = `
      <div><div class="label">Phase</div><div class="value">${esc(String(row.Phase || ''))}</div></div>
      <div><div class="label">Status</div><div class="value">${esc(String(row.Status || ''))}</div></div>
      <div><div class="label">Goal</div><div class="value">${esc(String(row.Goal || ''))}</div></div>
      <div><div class="label">Exit Gate</div><div class="value">${esc(String(row['Exit Gate'] || ''))}</div></div>`;
    phaseOverview.appendChild(div);
  }

  sliceFocus.innerHTML = '';
  if (slice1) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `
      <h3>${esc(slice1.title)} ${sliceStatusBadge(currentSliceRow?.Status || 'Pending')}</h3>
      <p>${esc(slice1.outcome || '')}</p>
      <div class="catalog-meta">Primary risk: ${esc(slice1.risk || 'n/a')}</div>
      <div class="catalog-meta">Readiness gate: ${esc(String(currentSliceRow?.['Readiness Gate'] || 'n/a'))}</div>
      <div class="catalog-meta">Notes: ${esc(String(currentSliceRow?.Notes || '')) || 'none'}</div>
      <details class="doc-details" open>
        <summary>Show scope and tests</summary>
        <div class="pill-row">${(slice1.scope || []).map((item) => `<span class="pill">${esc(item)}</span>`).join('')}</div>
        <div class="pill-row">${(slice1.test_scope || []).map((item) => `<span class="pill dim">${esc(item)}</span>`).join('')}</div>
      </details>
    `;
    sliceFocus.appendChild(div);
  }
  if (map1) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `
      <h3>First File Review Path</h3>
      <p>${esc(String(map1['Primary Files To Review First'] || ''))}</p>
      <div class="link-row">
        <button class="btn ghost" onclick="openDocPreview('USERJOURNEY/FILE_BY_FILE_IMPLEMENTATION_CHECKLIST.md')">Preview Checklist</button>
        <button class="btn ghost" onclick="openDocPreview('USERJOURNEY/EXECUTION_SLICES.md')">Preview Slices</button>
      </div>`;
    sliceFocus.appendChild(div);
  }

  fileReview.innerHTML = '';
  for (const section of files.slice(0, 4)) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `
      <h3>${esc(section.file)}</h3>
      <div class="catalog-meta">${esc(section.status || 'Status unknown')}</div>
      <details class="doc-details">
        <summary>Show checks</summary>
        <ul class="catalog-meta" style="margin:8px 0 0 16px">${(section.items || []).map((item) => `<li>${esc(item)}</li>`).join('')}</ul>
      </details>`;
    fileReview.appendChild(div);
  }

  risks.innerHTML = '';
  for (const row of (exec.critical_risks || []).slice(0, 4)) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `
      <h3>${esc(String(row.Risk || 'Risk'))}</h3>
      <div class="catalog-meta">Severity: ${esc(String(row.Severity || 'n/a'))}</div>
      <p>${esc(String(row['Why It Matters'] || ''))}</p>
      <details class="doc-details"><summary>Mitigation</summary><div class="catalog-meta">${esc(String(row.Mitigation || ''))}</div></details>`;
    risks.appendChild(div);
  }
}

function renderDriftDashboard(catalog) {
  const summary = document.getElementById('drift-summary');
  const violationsEl = document.getElementById('drift-violations');
  const filesEl = document.getElementById('drift-files');
  const rulesEl = document.getElementById('drift-rules');
  const drift = catalog?.drift || { violations: [], notes: [], changed_files: [], sync_rules: [], status: 'passed' };

  summary.textContent = drift.status === 'failed'
    ? `${drift.violations.length} drift violation(s) detected across ${drift.changed_files.length} changed file(s).`
    : `Drift check currently passes. ${drift.changed_files.length} changed file(s) in the workspace.`;

  violationsEl.innerHTML = '';
  for (const item of [...(drift.violations || []), ...(drift.notes || [])]) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `<p>${esc(item)}</p>`;
    violationsEl.appendChild(div);
  }
  if (!violationsEl.innerHTML) {
    violationsEl.innerHTML = '<div class="catalog-item"><p>No sync notes or violations right now.</p></div>';
  }

  filesEl.innerHTML = '';
  for (const file of (drift.changed_files || [])) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    div.innerHTML = `<h3>${esc(file)}</h3><div class="link-row"><button class="btn ghost" onclick="openDocPreview(${JSON.stringify(file)})">Preview</button><a class="btn ghost" href="${vscodeHref(workspaceAbsPath(file))}">Open</a></div>`;
    filesEl.appendChild(div);
  }
  if (!filesEl.innerHTML) {
    filesEl.innerHTML = '<div class="catalog-item"><p>No changed files detected.</p></div>';
  }

  rulesEl.innerHTML = '';
  for (const rule of (drift.sync_rules || []).slice(0, 6)) {
    const div = document.createElement('div');
    div.className = 'catalog-item';
    const authorities = (rule.touched_authority || []);
    const dependents = (rule.touched_dependents || []);
    div.innerHTML = `
      <h3>${esc(rule.name)}</h3>
      <div class="catalog-meta">system: ${esc(rule.system || 'n/a')}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:6px">
        <div>
          <div class="meta" style="margin-bottom:4px;font-weight:500">Authority files</div>
          ${authorities.length ? authorities.map(item => `<div class="pill" style="margin:2px 0">${esc(item)}</div>`).join('') : '<div class="meta">none</div>'}
        </div>
        <div>
          <div class="meta" style="margin-bottom:4px;font-weight:500">Dependent files</div>
          ${dependents.length ? dependents.map(item => `<div class="pill dim" style="margin:2px 0">${esc(item)}</div>`).join('') : '<div class="meta">none</div>'}
        </div>
      </div>`;
    rulesEl.appendChild(div);
  }
  if (!rulesEl.innerHTML) {
    rulesEl.innerHTML = '<div class="catalog-item"><p>No sync rules recorded.</p></div>';
  }
}

async function updateUserJourneyPhase() {
  const phase = document.getElementById('uj-phase-select').value;
  const status = document.getElementById('uj-phase-status').value;
  const blockers = document.getElementById('uj-phase-blockers').value;
  const r = await fetch('/api/uj-phase', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({phase, status, blockers}),
  });
  const result = await r.json();
  const out = document.getElementById('output');
  out.className = `terminal ${(result.exit_code === 0) ? 'success' : 'error'}`;
  out.textContent = result.output || '(no output)';
  const ok = result.exit_code === 0;
  document.getElementById('cmd-label').textContent = ok ? 'USERJOURNEY phase updated' : 'USERJOURNEY phase update failed';
  showToast(ok ? `Phase ${phase} set to ${status}` : 'Phase update failed', ok ? 'success' : 'error');
  if (ok) await loadAll();
}

async function updateUserJourneySlice() {
  const slice = document.getElementById('uj-slice-select').value;
  const status = document.getElementById('uj-slice-status').value;
  const notes = document.getElementById('uj-slice-note').value;
  const r = await fetch('/api/uj-slice', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({slice, status, notes}),
  });
  const result = await r.json();
  const out = document.getElementById('output');
  out.className = `terminal ${(result.exit_code === 0) ? 'success' : 'error'}`;
  out.textContent = result.output || '(no output)';
  const ok = result.exit_code === 0;
  document.getElementById('cmd-label').textContent = ok ? 'USERJOURNEY slice updated' : 'USERJOURNEY slice update failed';
  showToast(ok ? `${slice} set to ${status}` : 'Slice update failed', ok ? 'success' : 'error');
  if (ok) await loadAll();
}

async function postWorkflowAction(path, body, successLabel, failureLabel) {
  const r = await fetch(path, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body),
  });
  const result = await r.json();
  const out = document.getElementById('output');
  out.className = `terminal ${(result.exit_code === 0) ? 'success' : 'error'}`;
  out.textContent = result.output || '(no output)';
  document.getElementById('cmd-label').textContent = result.exit_code === 0 ? successLabel : failureLabel;
  if (result.exit_code === 0 && !body.dry_run) {
    await loadAll();
    await _runCmdImpl('guide.programbuild');
    await _runCmdImpl('guide.userjourney');
  }
  return result;
}

function selectRecentProject(dest) {
  localStorage.setItem('programstartActiveProjectDest', dest);
  if (_cachedState?.catalog) renderKickoffHandoff(_cachedState.catalog, _cachedState.programbuild);
}

function removeRecentProject(dest) {
  const next = getRecentProjects().filter((item) => item.dest !== dest);
  setRecentProjects(next);
  if (localStorage.getItem('programstartActiveProjectDest') === dest) {
    localStorage.setItem('programstartActiveProjectDest', next[0]?.dest || '');
  }
  if (_cachedState?.catalog) renderKickoffHandoff(_cachedState.catalog, _cachedState.programbuild);
}

async function copySubagentPrompt(name) {
  const prompt = _subagentMap[name]?.prompt || '';
  if (!prompt) return;
  await copyText(prompt, `${name} prompt copied`, `Clipboard blocked for ${name}`);
}

async function copyText(text, okLabel, failLabel = 'Clipboard blocked') {
  try {
    await navigator.clipboard.writeText(text);
    setCommandStatus(okLabel, 'Clipboard updated for the next manual step.');
    showToast(okLabel, 'success');
  } catch {
    setCommandStatus(failLabel, 'Copy failed. Use the visible output panel text instead.');
    showToast(failLabel, 'error');
  }
}

function showStarterCommands(text) {
  const out = document.getElementById('output');
  out.className = 'terminal success';
  out.textContent = text;
  setCommandStatus('Starter commands', 'Copied commands can be pasted into a fresh terminal in the new repo.');
}

async function openDocPreview(relativePath) {
  const panel = document.getElementById('doc-preview');
  const title = document.getElementById('doc-preview-title');
  const meta = document.getElementById('doc-preview-meta');
  const body = document.getElementById('doc-preview-body');
  const openBtn = document.getElementById('doc-preview-open');
  _docPreviewPath = relativePath;
  panel.className = 'doc-preview';
  title.textContent = relativePath;
  meta.textContent = 'Loading preview...';
  body.textContent = '';
  openBtn.onclick = () => window.open(vscodeHref(workspaceAbsPath(relativePath)), '_self');
  const r = await fetch(`/api/doc?path=${encodeURIComponent(relativePath)}`);
  const result = await r.json();
  if (result.error) {
    meta.textContent = result.error;
    body.textContent = '';
    return;
  }
  meta.textContent = `${result.line_count} lines${result.truncated ? ' · preview truncated to first 220 lines' : ''}`;
  body.textContent = result.content || '(empty file)';
}

function closeDocPreview() {
  document.getElementById('doc-preview').className = 'doc-preview hidden';
  _docPreviewPath = null;
}

// ── Command execution (serialised) ─────────────────────────────────
function runCmd(key, extraArgs) {
  _cmdQueue = _cmdQueue.then(() => _runCmdImpl(key, extraArgs));
  return _cmdQueue;
}

async function _runCmdImpl(key, extraArgs) {
  const spinner = document.getElementById('cmd-spinner');
  const out = document.getElementById('output');
  startCommandTimer(`Running: ${key}`, 'Executing command in the workspace console.');
  spinner.className = 'spinner active';
  out.className = 'terminal';
  out.textContent = '';
  jumpToSection('console-section');
  const body = {command: key};
  if (extraArgs) body.args = extraArgs;
  try {
    const r = await fetch('/api/run', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    });
    const result = await r.json();
    spinner.className = 'spinner';
    const ok = result.exit_code === 0;
    finishCommandStatus(
      `${key} — ${ok ? 'OK' : 'FAILED (exit ' + result.exit_code + ')'}`,
      ok ? 'Command completed.' : 'Command failed.'
    );
    out.textContent = result.output || '(no output)';
    out.className = `terminal ${ok ? 'success' : 'error'}`;
    out.scrollTop = out.scrollHeight;

    // Parse guide output into guide panels
    if (key === 'guide.programbuild') renderGuide('pb', result.output);
    if (key === 'guide.userjourney') renderGuide('uj', result.output);

    // After a real advance: refresh state + guides + regenerate dashboard
    if (key.startsWith('advance.') && !key.endsWith('.dry') && ok) {
      await loadAll();
      await _runCmdImpl('guide.programbuild');
      await _runCmdImpl('guide.userjourney');
      // Fire dashboard regen silently
      fetch('/api/run', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({command:'dashboard'})});
    }
    return result;
  } catch (e) {
    spinner.className = 'spinner';
    finishCommandStatus(`${key} — ERROR`, 'Network error while reaching the dashboard API.');
    out.textContent = 'Network error: ' + e.message;
    out.className = 'terminal error';
    showToast(`${key} failed`, 'error');
    return {output: e.message, exit_code: -1};
  }
}

function renderGuide(prefix, raw) {
  const titleEl = document.getElementById(`guide-${prefix}-title`);
  const descEl = document.getElementById(`guide-${prefix}-desc`);
  const contentEl = document.getElementById(`guide-${prefix}-content`);
  const lines = (raw || '').split('\n');

  // First line is the title (e.g., "PROGRAMBUILD Stage: inputs_and_mode_selection")
  titleEl.textContent = lines[0] || (prefix === 'pb' ? 'PROGRAMBUILD' : 'USERJOURNEY');

  // Look up description from cached state
  const sys = prefix === 'pb' ? 'programbuild' : 'userjourney';
  if (_cachedState && _cachedState[sys]) {
    const d = (_cachedState[sys].descriptions || {})[_cachedState[sys].active] || '';
    if (d) { descEl.textContent = d; descEl.style.display = ''; }
    else { descEl.style.display = 'none'; }
  }

  let html = '';
  let inSection = false;
  for (const line of lines.slice(1)) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    if (trimmed.endsWith(':') && !trimmed.startsWith('-')) {
      if (inSection) html += '</div>';
      const sectionName = trimmed.slice(0, -1);
      html += `<div class="guide-label">${esc(sectionName)}</div><div class="guide-items">`;
      inSection = true;
    } else if (trimmed.startsWith('- ') && inSection) {
      const val = trimmed.slice(2);
      let display = val;
      // Make file paths clickable vscode:// links
      if (val.match(/\.(md|json|py|ps1|yml|yaml|txt)$/i)) {
        const absPath = ROOT.replace(/\\/g, '/') + '/' + val;
        display = `<a href="vscode://file/${encodeURIComponent(absPath)}" title="Open in VS Code">${esc(val)}</a>`;
      } else {
        display = esc(val);
      }
      html += `<div class="guide-item">${display}</div>`;
    }
  }
  if (inSection) html += '</div>';
  contentEl.innerHTML = html || `<span class="meta">No guide data</span>`;
}

// ── Pre-flight check (validate + drift + state-check) ─────────────
let _lastPreflightResult = null;
let _lastPreflightTime = 0;
const _PREFLIGHT_CACHE_MS = 60000;

async function preflightCheck() {
  const now = Date.now();
  if (_lastPreflightResult && (now - _lastPreflightTime) < _PREFLIGHT_CACHE_MS) {
    const out = document.getElementById('output');
    out.textContent = _lastPreflightResult.output;
    out.className = `terminal ${_lastPreflightResult.ok ? 'success' : 'error'}`;
    setCommandStatus(
      _lastPreflightResult.ok ? 'Pre-flight: ALL PASSED (cached)' : 'Pre-flight: ISSUES FOUND (cached)',
      `Cached result from ${Math.round((now - _lastPreflightTime) / 1000)}s ago. Re-run after ${Math.round((_PREFLIGHT_CACHE_MS - (now - _lastPreflightTime)) / 1000)}s.`
    );
    return;
  }
  const out = document.getElementById('output');
  const spinner = document.getElementById('cmd-spinner');
  out.className = 'terminal';
  out.textContent = '';
  startCommandTimer('Pre-flight check', 'Running validate, state check, then drift.');
  spinner.className = 'spinner active';

  let allOutput = '';
  let allOk = true;
  const commands = ['validate', 'validate.workflow-state', 'drift'];
  for (let idx = 0; idx < commands.length; idx += 1) {
    const cmd = commands[idx];
    setCommandStatus('Pre-flight check', `Running ${cmd} (${idx + 1}/${commands.length}).`);
    const body = {command: cmd};
    const r = await fetch('/api/run', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)});
    const result = await r.json();
    const ok = result.exit_code === 0;
    allOutput += `━━━ ${cmd} ${ok ? '✓' : '✗'} ━━━\n${result.output}\n\n`;
    if (!ok) allOk = false;
  }
  spinner.className = 'spinner';
  finishCommandStatus(
    allOk ? 'Pre-flight: ALL PASSED' : 'Pre-flight: ISSUES FOUND',
    allOk ? 'Validation, state check, and drift all completed.' : 'Review the console output before advancing.'
  );
  out.textContent = allOutput.trim();
  out.className = `terminal ${allOk ? 'success' : 'error'}`;
  out.scrollTop = out.scrollHeight;
  _lastPreflightResult = { output: allOutput.trim(), ok: allOk };
  _lastPreflightTime = Date.now();
}

// ── Advance modal ──────────────────────────────────────────────────
function openAdvanceModal(system, mode = 'advance') {
  _advanceSystem = system;
  _advanceMode = mode;
  const label = system === 'programbuild' ? 'Stage' : 'Phase';
  const current = currentStepEntry(system);
  const signoff = current?.entry?.signoff || {};
  document.getElementById('modal-title').textContent = mode === 'advance'
    ? `Advance ${system.toUpperCase()} ${label}`
    : `Save ${system.toUpperCase()} ${label} Signoff`;
  document.getElementById('modal-desc').textContent = mode === 'advance'
    ? 'This will mark the active step as completed and move the next step to in_progress.'
    : 'This will save signoff metadata for the active step without advancing the workflow.';
  document.getElementById('modal-decision').value = signoff.decision || 'approved';
  document.getElementById('modal-date').value = signoff.date || new Date().toISOString().slice(0, 10);
  document.getElementById('modal-notes').value = signoff.notes || '';
  // Populate signoff history
  const history = current?.entry?.signoff_history || [];
  const histSection = document.getElementById('modal-history-section');
  const histDiv = document.getElementById('modal-history');
  if (history.length > 0) {
    histDiv.innerHTML = history.slice().reverse().map((h) => {
      const decision = esc(h.decision || '\u2014');
      const dt = esc(h.date || '\u2014');
      const saved = esc(h.saved_at || '');
      const noteHtml = h.notes ? `<div style="font-size:10px;margin-top:2px;white-space:pre-wrap">${esc(h.notes)}</div>` : '';
      return `<div style="padding:3px 0;border-bottom:1px solid var(--border)">
        <span style="color:var(--text);font-weight:500">${decision}</span>
        &middot; <span>${dt}</span>
        ${saved ? `<span style="color:var(--dim)"> (saved ${saved})</span>` : ''}
        ${noteHtml}</div>`;
    }).join('');
  } else {
    histDiv.innerHTML = '<span class="meta">No previous signoffs recorded.</span>';
  }
  document.getElementById('modal-preflight').innerHTML = '';
  document.getElementById('advance-modal').className = 'modal-overlay';
  document.getElementById('modal-dry-btn').style.display = mode === 'advance' ? '' : 'none';
  document.getElementById('modal-confirm-btn').textContent = mode === 'advance' ? 'Advance' : 'Save Signoff';

  function setAdvanceModalPending(isPending) {
    for (const id of ['modal-decision', 'modal-date', 'modal-notes', 'modal-dry-btn', 'modal-confirm-btn']) {
      const node = document.getElementById(id);
      if (node) node.disabled = isPending;
    }
  }

  (async () => {
    const pf = document.getElementById('modal-preflight');
    if (mode !== 'advance') {
      pf.innerHTML = current ? `Active ${label.toLowerCase()}: ${esc(current.step)}` : 'No cached workflow state loaded yet.';
      document.getElementById('modal-confirm-btn').disabled = false;
      return;
    }
    setAdvanceModalPending(true);
    pf.innerHTML = '<span style="color:var(--dim)">Running pre-flight (validate + state check)...</span>';
    let checks = [];
    for (const cmd of ['validate.workflow-state', `advance.${system}.dry`]) {
      const r = await fetch('/api/run', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({command:cmd})});
      const result = await r.json();
      const ok = result.exit_code === 0;
      checks.push({cmd, ok, output: result.output});
    }
    const allOk = checks.every(c => c.ok);
    let html = '';
    for (const c of checks) {
      const icon = c.ok ? `<span style="color:var(--green)">✓</span>` : `<span style="color:var(--red)">✗</span>`;
      html += `<div>${icon} ${esc(c.cmd)}: ${esc(c.output.split('\n')[0])}</div>`;
    }
    if (!allOk) html += `<div style="color:var(--red);margin-top:4px">Fix issues before advancing.</div>`;
    pf.innerHTML = html;
    setAdvanceModalPending(false);
    document.getElementById('modal-confirm-btn').disabled = !allOk;
  })();
}

function closeAdvanceModal() {
  document.getElementById('advance-modal').className = 'modal-overlay hidden';
  _advanceSystem = null;
}

async function dryRunFromModal() {
  if (!_advanceSystem) return;
  const system = _advanceSystem;
  const decision = document.getElementById('modal-decision').value;
  const dateValue = document.getElementById('modal-date').value;
  const notes = document.getElementById('modal-notes').value;
  closeAdvanceModal();
  await postWorkflowAction(
    '/api/workflow-advance',
    {system, decision, date: dateValue, notes, dry_run: true},
    `${system} advance dry-run complete`,
    `${system} advance dry-run failed`,
  );
}

async function confirmAdvanceFromModal() {
  if (!_advanceSystem) return;
  const system = _advanceSystem;
  const decision = document.getElementById('modal-decision').value;
  const dateValue = document.getElementById('modal-date').value;
  const notes = document.getElementById('modal-notes').value;
  closeAdvanceModal();
  if (_advanceMode === 'signoff') {
    await postWorkflowAction(
      '/api/workflow-signoff',
      {system, decision, date: dateValue, notes},
      `${system} signoff saved`,
      `${system} signoff failed`,
    );
    return;
  }
  await postWorkflowAction(
    '/api/workflow-advance',
    {system, decision, date: dateValue, notes},
    `${system} advanced`,
    `${system} advance failed`,
  );
}

// ── Bootstrap / New Project modal ─────────────────────────────────
function openBootstrapModal() {
  document.getElementById('bs-name').value = '';
  const destEl = document.getElementById('bs-dest');
  destEl.value = '';
  delete destEl.dataset.manual;
  document.getElementById('bs-preview-wrap').style.display = 'none';
  document.getElementById('bs-create-btn').disabled = true;
  document.querySelector('input[name="bsVariant"][value="product"]').checked = true;
  document.getElementById('bootstrap-modal').className = 'modal-overlay';
  setTimeout(() => document.getElementById('bs-name').focus(), 50);
}

function bsNameChanged(input) {
  const name = input.value.trim();
  const dest = document.getElementById('bs-dest');
  if (!dest.dataset.manual && name) dest.value = `C:\\Projects\\${name}`;
  document.getElementById('bs-create-btn').disabled = true;
  const errEl = document.getElementById('bs-name-err');
  if (!name) { errEl.textContent = ''; return; }
  const safeNameRe = /^[A-Za-z0-9][A-Za-z0-9 _.-]{0,63}$/;
  errEl.textContent = safeNameRe.test(name) ? '' : 'Name must start with a letter or digit and contain only letters, digits, spaces, underscores, hyphens, or dots (max 64 chars).';
  if (dest.value) bsDestChanged(dest);
}

function bsDestChanged(input) {
  input.dataset.manual = '1';
  document.getElementById('bs-create-btn').disabled = true;
  const dest = input.value.trim();
  const errEl = document.getElementById('bs-dest-err');
  if (!dest) { errEl.textContent = ''; return; }
  const safePathRe = /^[A-Za-z]:\\[A-Za-z0-9 \\_.-]{1,259}$|^\/[A-Za-z0-9 \/._-]{1,259}$/;
  errEl.textContent = safePathRe.test(dest) ? '' : 'Path must be a valid absolute Windows (C:\\...) or Unix (/...) path with safe characters.';
}

function closeBootstrapModal() {
  document.getElementById('bootstrap-modal').className = 'modal-overlay hidden';
}

function _getBootstrapParams(dryRun) {
  return {
    dest: document.getElementById('bs-dest').value.trim(),
    project_name: document.getElementById('bs-name').value.trim(),
    variant: document.querySelector('input[name="bsVariant"]:checked')?.value || 'product',
    dry_run: !!dryRun,
  };
}

async function previewBootstrap() {
  const wrap = document.getElementById('bs-preview-wrap');
  const out = document.getElementById('bs-preview-out');
  const createBtn = document.getElementById('bs-create-btn');
  wrap.style.display = '';
  out.textContent = 'Previewing workspace creation...';
  out.className = 'terminal';
  createBtn.disabled = true;
  setCommandStatus('Previewing bootstrap', 'Checking destination, variant, and generated file plan.');
  const r = await fetch('/api/bootstrap', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(_getBootstrapParams(true)),
  });
  const result = await r.json();
  out.textContent = result.output || '(no output)';
  const ok = result.exit_code === 0;
  out.className = `terminal ${ok ? 'success' : 'error'}`;
  createBtn.disabled = !ok;
  setCommandStatus(
    ok ? 'Bootstrap preview ready' : 'Bootstrap preview failed',
    ok ? 'Review the preview, then create the new workspace.' : 'Fix the reported preview issues before creating the workspace.'
  );
}

async function createProject() {
  const params = _getBootstrapParams(false);
  closeBootstrapModal();
  const spinner = document.getElementById('cmd-spinner');
  const out = document.getElementById('output');
  startCommandTimer(`Creating: ${params.project_name}...`, 'Scaffolding the new workspace and recording local handoff metadata.');
  spinner.className = 'spinner active';
  out.className = 'terminal';
  out.textContent = '';
  const r = await fetch('/api/bootstrap', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(params),
  });
  const result = await r.json();
  spinner.className = 'spinner';
  const ok = result.exit_code === 0;
  finishCommandStatus(
    ok ? `Project created: ${params.project_name}` : `Bootstrap failed (exit ${result.exit_code})`,
    ok ? 'Workspace scaffold completed.' : 'Bootstrap did not complete cleanly.'
  );
  out.textContent = result.output || '(no output)';
  if (ok) {
    const created = { ...params, created_at: new Date().toISOString() };
    localStorage.setItem('programstartLastBootstrap', JSON.stringify(created));
    addRecentProject(created);
    if (_cachedState?.catalog) renderKickoffHandoff(_cachedState.catalog, _cachedState.programbuild);
    out.innerHTML += `<br><br>─────<br>Workspace created. Next steps:<br>  1. <a href="${vscodeHref(params.dest)}" style="color:var(--link)">Open the new repo in VS Code</a><br>  2. Start with Canonical, File Index, Kickoff Packet, and your chosen variant playbook.<br>  3. Define what you are building in those docs.<br>  4. Run the first planning step from the new repo:<br>     .\\scripts\\pb.ps1 next<br>     .\\scripts\\pb.ps1 validate`;
    activateTab('setup');
    showToast(`Workspace created for ${params.project_name}`, 'success');
  } else {
    showToast(`Bootstrap failed for ${params.project_name}`, 'error');
  }
  out.className = `terminal ${ok ? 'success' : 'error'}`;
  out.scrollTop = out.scrollHeight;
}

function clearOutput() {
  const out = document.getElementById('output');
  out.className = 'terminal hidden';
  out.textContent = '';
  stopCommandTimer();
  setCommandStatus('Ready');
}

// ── Init ───────────────────────────────────────────────────────────
(async () => {
  await loadAll();
  // Load both guides sequentially (avoid racing for the output panel)
  await runCmd('guide.programbuild');
  await runCmd('guide.userjourney');
})();

// Auto-refresh state every 30s (gated on command queue to avoid mid-operation refresh)
let _loadAllPending = false;
setInterval(() => {
  if (_loadAllPending) return;
  _loadAllPending = true;
  _cmdQueue = _cmdQueue.then(() => loadAll()).finally(() => { _loadAllPending = false; });
}, 30000);

// Escape key dismisses modals and doc preview
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeAdvanceModal();
    closeBootstrapModal();
    closeDocPreview();
  }
});