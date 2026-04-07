<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Visual SOP Creator</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <style>
    body { font-family: Inter, sans-serif; background:#f8fafc; }
    .tab-btn.active { border-bottom: 2px solid #000080; color:#000080; font-weight:700; }
    .tool-btn.active { background:#000080; color:white; }
    .marker,.blue-marker{ position:absolute; width:30px; height:30px; border-radius:9999px; color:white; font-size:13px; font-weight:700; display:flex; align-items:center; justify-content:center; transform:translate(-50%,-50%); border:2px solid white; }
    .marker{ background:#ef4444; }
    .blue-marker{ background:#3b82f6; cursor:pointer; }
  </style>
</head>
<body class="p-4 md:p-8">
<div class="max-w-6xl mx-auto space-y-6">
  <div class="bg-white border rounded-xl p-4 md:p-6 shadow-sm space-y-4">
    <div class="flex flex-wrap items-center gap-2 justify-between">
      <h1 class="font-bold text-xl text-[#000080]">Visual SOP Creator (Supabase)</h1>
      <div class="flex gap-2">
        <button id="modeEditor" class="px-3 py-1.5 rounded bg-[#000080] text-white text-sm">Editor</button>
        <button id="modeLibrary" class="px-3 py-1.5 rounded bg-slate-100 text-sm">Library</button>
      </div>
    </div>

    <div class="grid md:grid-cols-2 gap-2 text-sm" id="supabaseConfig">
      <input id="supabaseUrl" class="border rounded p-2" placeholder="Supabase URL (https://xxxx.supabase.co)" />
      <input id="supabaseKey" class="border rounded p-2" placeholder="Supabase anon key" />
    </div>

    <div id="editorScreen" class="space-y-4">
      <div class="grid md:grid-cols-2 gap-3">
        <input id="sopTitleInput" class="border rounded p-2 font-semibold" placeholder="Ana Başlık" />
        <input id="sopSubtitleInput" class="border rounded p-2" placeholder="Alt Başlık" />
      </div>

      <div class="flex flex-wrap gap-2">
        <button id="saveSopBtn" class="px-3 py-2 bg-emerald-600 text-white rounded text-sm">Save SOP</button>
        <button id="newSopBtn" class="px-3 py-2 bg-slate-700 text-white rounded text-sm">New SOP</button>
        <label class="px-3 py-2 bg-indigo-600 text-white rounded text-sm cursor-pointer">Upload MP4
          <input id="videoInput" type="file" accept="video/mp4" class="hidden" />
        </label>
        <span id="statusText" class="text-xs text-slate-500 self-center">Hazır</span>
      </div>

      <div id="videoInfo" class="text-xs text-slate-600"></div>

      <div class="bg-white rounded-xl border p-4">
        <div class="flex border-b mb-3">
          <button id="tab0" class="tab-btn active px-3 py-2 text-sm">Görsel 1</button>
          <button id="tab1" class="tab-btn px-3 py-2 text-sm">Görsel 2</button>
        </div>
        <div id="uploadArea" class="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer text-slate-500">Görsel yüklemek için tıkla<input id="fileInput" type="file" accept="image/*" class="hidden" /></div>
        <div id="editorArea" class="hidden space-y-3">
          <div class="flex gap-2">
            <button id="toolInstruction" class="tool-btn active px-3 py-1 rounded border text-xs">Marker1 (Kırmızı / SOP)</button>
            <button id="toolMarker" class="tool-btn px-3 py-1 rounded border text-xs">Marker2 (Mavi / Gösterim)</button>
          </div>
          <div class="relative" id="canvasContainer">
            <canvas id="mainCanvas" class="w-full rounded"></canvas>
            <div id="markersOverlay" class="absolute inset-0"></div>
          </div>
        </div>
      </div>

      <div class="grid lg:grid-cols-2 gap-4">
        <div class="bg-white border rounded-xl p-4">
          <div class="flex justify-between items-center mb-2"><h3 class="font-bold">SOP Adımları</h3><button id="addManualBtn" class="text-xs px-2 py-1 bg-blue-600 text-white rounded">+ Add Manual Step</button></div>
          <div id="tableBody" class="space-y-2"></div>
        </div>
        <div class="bg-white border rounded-xl p-4">
          <div class="flex justify-between items-center mb-2"><h3 class="font-bold text-red-700">Warnings</h3><button id="addWarningBtn" class="text-xs px-2 py-1 bg-red-600 text-white rounded">+ Add Warning</button></div>
          <div id="warningsContainer" class="space-y-2"></div>
        </div>
      </div>
    </div>

    <div id="libraryScreen" class="hidden">
      <div class="flex justify-between items-center mb-3">
        <h2 class="font-bold text-lg">SOP Library</h2>
        <button id="refreshLibraryBtn" class="px-3 py-1 text-sm rounded bg-slate-100">Refresh</button>
      </div>
      <div id="libraryList" class="grid md:grid-cols-2 lg:grid-cols-3 gap-3"></div>
    </div>

    <div id="viewerScreen" class="hidden fixed inset-0 z-50 bg-slate-900/95 p-6 overflow-auto">
      <div class="max-w-6xl mx-auto text-white space-y-4">
        <div class="flex justify-between items-center">
          <h2 id="viewerTitle" class="text-2xl font-bold"></h2>
          <button id="closeViewerBtn" class="px-3 py-1 bg-white/20 rounded">Kapat</button>
        </div>
        <p id="viewerSubtitle" class="text-slate-200"></p>
        <video id="viewerVideo" class="w-full max-h-[320px] rounded hidden" controls></video>
        <img id="viewerImage" class="w-full max-h-[520px] object-contain bg-black rounded" />
        <div class="bg-white text-slate-900 rounded-lg p-6 min-h-[140px]"><p id="viewerStepText" class="text-3xl font-semibold leading-tight"></p></div>
        <div class="flex justify-between">
          <button id="prevStepBtn" class="px-5 py-3 bg-white/20 rounded text-xl">← Geri</button>
          <span id="viewerStepCounter" class="text-lg self-center"></span>
          <button id="nextStepBtn" class="px-5 py-3 bg-blue-600 rounded text-xl">İleri →</button>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  const $ = (id) => document.getElementById(id);
  lucide.createIcons();

  let activeIdx = 0, currentMode = 'instruction', currentSopId = null;
  let images = [null, null], imagesBase64 = [null, null];
  let steps = [], markers2 = [], warnings = [], videoUrl = null;
  let supabaseClient = null, viewerSteps = [], viewerStepIndex = 0, viewerSop = null;

  const initSupabase = () => {
    const url = $('supabaseUrl').value.trim();
    const key = $('supabaseKey').value.trim();
    if (!url || !key) return false;
    localStorage.setItem('sb_url', url); localStorage.setItem('sb_key', key);
    supabaseClient = window.supabase.createClient(url, key);
    return true;
  };

  const setMode = (mode) => {
    $('editorScreen').classList.toggle('hidden', mode !== 'editor');
    $('libraryScreen').classList.toggle('hidden', mode !== 'library');
    $('modeEditor').className = `px-3 py-1.5 rounded text-sm ${mode==='editor'?'bg-[#000080] text-white':'bg-slate-100'}`;
    $('modeLibrary').className = `px-3 py-1.5 rounded text-sm ${mode==='library'?'bg-[#000080] text-white':'bg-slate-100'}`;
  };

  const normalizeStepIds = () => {
    let no = 0;
    steps.forEach((s) => { s.id = ++no; });
    markers2.forEach((m, i) => { m.id = i + 1; });
  };

  const refreshEditor = () => {
    const img = images[activeIdx];
    if (!img) { $('uploadArea').classList.remove('hidden'); $('editorArea').classList.add('hidden'); return; }
    $('uploadArea').classList.add('hidden'); $('editorArea').classList.remove('hidden');
    const c = $('mainCanvas');
    const ctx = c.getContext('2d');
    const w = 1100, scale = w / img.width;
    c.width = w; c.height = img.height * scale;
    ctx.drawImage(img, 0, 0, c.width, c.height);
    renderMarkers();
  };

  const renderMarkers = () => {
    $('markersOverlay').innerHTML = '';

    steps.forEach((s, idx) => {
      if (s.isManual || s.imgIdx !== activeIdx || s.px == null || s.py == null) return;
      const d = document.createElement('div');
      d.className = 'marker';
      d.style.left = `${s.px}%`; d.style.top = `${s.py}%`; d.textContent = s.id;
      d.title = 'markers1 (SOP adımı)';
      d.oncontextmenu = (e) => { e.preventDefault(); steps.splice(idx, 1); updateAndRender(); };
      $('markersOverlay').appendChild(d);
    });

    markers2.forEach((m, idx) => {
      if (m.imgIdx !== activeIdx) return;
      const d = document.createElement('div');
      d.className = 'blue-marker';
      d.style.left = `${m.px}%`; d.style.top = `${m.py}%`; d.textContent = m.id;
      d.title = 'markers2 (gösterim noktası)';
      d.oncontextmenu = (e) => { e.preventDefault(); markers2.splice(idx, 1); updateAndRender(); };
      $('markersOverlay').appendChild(d);
    });
  };

  const renderTable = () => {
    $('tableBody').innerHTML = '';
    steps.forEach((s, idx) => {
      const row = document.createElement('div');
      const markerType = s.isManual ? 'Manual' : `Marker1 / Görsel ${s.imgIdx + 1}`;
      row.className = 'grid grid-cols-[46px_1fr_70px_32px] gap-2 items-start';
      row.innerHTML = `<div class="text-sm font-bold text-red-600">${s.id}</div>
        <textarea class="border rounded p-2 text-sm" rows="2">${s.description||''}</textarea>
        <div class="text-[10px] text-slate-500 self-center">${markerType}</div>
        <button class="text-red-600">✕</button>`;
      row.querySelector('textarea').oninput = (e)=>{ steps[idx].description=e.target.value; };
      row.querySelector('button').onclick = ()=>{ steps.splice(idx,1); updateAndRender(); };
      $('tableBody').appendChild(row);
    });
  };

  const renderWarnings = () => {
    $('warningsContainer').innerHTML = '';
    warnings.forEach((w, idx)=>{
      const d=document.createElement('div'); d.className='flex gap-2';
      d.innerHTML=`<input class="border rounded p-2 text-sm flex-1" value="${w.text||''}"/><button class="text-red-600">✕</button>`;
      d.querySelector('input').oninput=(e)=>warnings[idx].text=e.target.value;
      d.querySelector('button').onclick=()=>{warnings.splice(idx,1); renderWarnings();};
      $('warningsContainer').appendChild(d);
    });
  };

  const updateAndRender = () => {
    normalizeStepIds();
    refreshEditor();
    renderTable();
    renderWarnings();
  };

  const readAsDataUrl = (file) => new Promise((resolve) => {
    const fr = new FileReader();
    fr.onload=(e)=>resolve(e.target.result);
    fr.readAsDataURL(file);
  });

  $('uploadArea').onclick = ()=>$('fileInput').click();
  $('fileInput').onchange = async (e)=>{
    const file = e.target.files[0]; if(!file) return;
    const base64 = await readAsDataUrl(file); const img = new Image();
    img.onload = ()=>{ images[activeIdx]=img; imagesBase64[activeIdx]=base64; refreshEditor(); };
    img.src = base64;
  };

  $('videoInput').onchange = async (e)=>{
    const file=e.target.files[0]; if(!file) return;
    videoUrl = await readAsDataUrl(file);
    $('videoInfo').textContent = `Video yüklendi: ${file.name}`;
  };

  $('mainCanvas').addEventListener('click',(e)=>{
    if(!images[activeIdx]) return;
    const r = $('mainCanvas').getBoundingClientRect();
    const px=((e.clientX-r.left)/r.width)*100, py=((e.clientY-r.top)/r.height)*100;

    if (currentMode === 'instruction') {
      steps.push({ id:null, px, py, description:'', isManual:false, imgIdx:activeIdx });
    } else {
      markers2.push({ id:null, px, py, imgIdx:activeIdx });
    }

    updateAndRender();
  });

  $('toolInstruction').onclick = ()=>{
    currentMode='instruction';
    $('toolInstruction').classList.add('active');
    $('toolMarker').classList.remove('active');
  };

  $('toolMarker').onclick = ()=>{
    currentMode='marker2';
    $('toolMarker').classList.add('active');
    $('toolInstruction').classList.remove('active');
  };

  $('tab0').onclick=()=>{activeIdx=0; $('tab0').classList.add('active'); $('tab1').classList.remove('active'); refreshEditor();};
  $('tab1').onclick=()=>{activeIdx=1; $('tab1').classList.add('active'); $('tab0').classList.remove('active'); refreshEditor();};

  $('addManualBtn').onclick=()=>{
    steps.push({ id:null, description:'', isManual:true, imgIdx:-1, px:null, py:null });
    updateAndRender();
  };

  $('addWarningBtn').onclick=()=>{ warnings.push({text:''}); renderWarnings(); };

  const getPayload = () => ({
    mainTitle: $('sopTitleInput').value,
    subTitle: $('sopSubtitleInput').value,
    image1: imagesBase64[0],
    image2: imagesBase64[1],
    videoUrl,
    markers1: steps.filter((s) => !s.isManual && s.px != null && s.py != null),
    markers2,
    steps,
    warnings,
    updated_at: new Date().toISOString()
  });

  const applySop = (s) => {
    currentSopId = s.id || null;
    $('sopTitleInput').value = s.mainTitle || '';
    $('sopSubtitleInput').value = s.subTitle || '';

    const incomingSteps = Array.isArray(s.steps) ? s.steps : [];
    if (incomingSteps.length) {
      steps = incomingSteps;
    } else if (Array.isArray(s.markers1)) {
      steps = s.markers1.map((m) => ({
        id: m.id || null,
        px: m.px,
        py: m.py,
        description: m.description || '',
        isManual: false,
        imgIdx: m.imgIdx ?? 0
      }));
    } else {
      steps = [];
    }

    markers2 = Array.isArray(s.markers2) ? s.markers2 : [];
    warnings = Array.isArray(s.warnings) ? s.warnings : [];
    imagesBase64 = [s.image1 || null, s.image2 || null];
    videoUrl = s.videoUrl || s.video1 || null;

    $('videoInfo').textContent = videoUrl ? 'Video yüklü' : '';

    [0,1].forEach(i=>{
      images[i]=null;
      if(imagesBase64[i]){
        const im=new Image();
        im.onload=()=>{images[i]=im; if(i===activeIdx) refreshEditor();};
        im.src=imagesBase64[i];
      }
    });

    updateAndRender();
  };

  $('saveSopBtn').onclick = async ()=>{
    $('statusText').textContent='Kaydediliyor...';
    if (!initSupabase()) {
      localStorage.setItem('last_sop', JSON.stringify(getPayload()));
      $('statusText').textContent='Lokal kaydedildi';
      return;
    }

    const payload = getPayload();
    let res;

    if (currentSopId) {
      res = await supabaseClient.from('sops').update(payload).eq('id', currentSopId).select().single();
    } else {
      res = await supabaseClient.from('sops').insert(payload).select().single();
    }

    if (res.error) {
      $('statusText').textContent = `Hata: ${res.error.message}`;
      return;
    }

    currentSopId = res.data.id;
    $('statusText').textContent='Supabase kaydedildi';
  };

  $('newSopBtn').onclick = ()=>{
    currentSopId = null;
    applySop({});
  };

  const openViewer = (sop) => {
    viewerSop = sop;
    viewerSteps = Array.isArray(sop.steps) ? sop.steps : [];
    viewerStepIndex = 0;

    $('viewerScreen').classList.remove('hidden');
    $('viewerTitle').textContent = sop.mainTitle || 'SOP';
    $('viewerSubtitle').textContent = sop.subTitle || '';

    if (sop.videoUrl) {
      $('viewerVideo').src = sop.videoUrl;
      $('viewerVideo').classList.remove('hidden');
    } else {
      $('viewerVideo').classList.add('hidden');
      $('viewerVideo').removeAttribute('src');
    }

    renderViewerStep();
  };

  const renderViewerStep = () => {
    const step = viewerSteps[viewerStepIndex] || {description:'Adım bulunamadı'};
    $('viewerStepText').textContent = `${viewerStepIndex+1}. ${step.description || '...'}`;
    $('viewerStepCounter').textContent = `${viewerStepIndex+1} / ${Math.max(1,viewerSteps.length)}`;

    let img = viewerSop.image1;
    if (step.imgIdx === 1) img = viewerSop.image2;
    $('viewerImage').src = img || '';
  };

  $('nextStepBtn').onclick = ()=>{ if (viewerStepIndex < viewerSteps.length-1) viewerStepIndex++; renderViewerStep(); };
  $('prevStepBtn').onclick = ()=>{ if (viewerStepIndex > 0) viewerStepIndex--; renderViewerStep(); };
  $('closeViewerBtn').onclick = ()=> $('viewerScreen').classList.add('hidden');

  const renderLibrary = async () => {
    $('libraryList').innerHTML = '';

    if (!initSupabase()) {
      $('libraryList').innerHTML = '<div class="text-sm text-slate-500">Supabase bağlantısı girin.</div>';
      return;
    }

    const { data, error } = await supabaseClient.from('sops').select('*').order('updated_at', {ascending:false});
    if (error) {
      $('libraryList').innerHTML = `<div class="text-sm text-red-600">${error.message}</div>`;
      return;
    }

    if (!data.length) {
      $('libraryList').innerHTML = '<div class="text-sm text-slate-500">Kayıt yok.</div>';
      return;
    }

    data.forEach(s => {
      const card = document.createElement('div');
      card.className = 'bg-white border rounded-xl p-3 shadow-sm space-y-2';
      card.innerHTML = `<div class="font-semibold">${s.mainTitle || 'Başlıksız SOP'}</div>
      <div class="text-xs text-slate-500">${(s.subTitle || '')}</div>
      <div class="text-xs text-slate-400">${new Date(s.updated_at).toLocaleString('tr-TR')}</div>
      <div class="flex gap-2"><button class="play px-3 py-1 bg-blue-600 text-white rounded text-sm">▶ Play</button><button class="load px-3 py-1 bg-slate-100 rounded text-sm">Load</button></div>`;
      card.querySelector('.play').onclick = ()=>openViewer(s);
      card.querySelector('.load').onclick = ()=>{ setMode('editor'); applySop(s); };
      $('libraryList').appendChild(card);
    });
  };

  $('modeEditor').onclick = ()=>setMode('editor');
  $('modeLibrary').onclick = async ()=>{ setMode('library'); await renderLibrary(); };
  $('refreshLibraryBtn').onclick = renderLibrary;

  (()=>{
    $('supabaseUrl').value = localStorage.getItem('sb_url') || '';
    $('supabaseKey').value = localStorage.getItem('sb_key') || '';
    const local = localStorage.getItem('last_sop');
    if (local) applySop(JSON.parse(local));
    updateAndRender();
  })();
</script>
</body>
</html>
