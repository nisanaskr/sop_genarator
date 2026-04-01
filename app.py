<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual SOP Creator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- PDF & Word Libraries -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/docx@7.1.0/build/index.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
        .canvas-container { position: relative; display: inline-block; cursor: crosshair; width: 100%; }
        canvas { display: block; max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
        
        .marker {
            position: absolute; width: 28px; height: 28px;
            background: rgba(239, 68, 68, 0.95); color: white;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-size: 14px; font-weight: bold; transform: translate(-50%, -50%);
            border: 2px solid white; pointer-events: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3); z-index: 10;
        }

        .blue-marker {
            position: absolute; width: 28px; height: 28px;
            background: rgba(59, 130, 246, 0.95); color: white;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-size: 14px; font-weight: bold; transform: translate(-50%, -50%);
            border: 2px solid white; pointer-events: auto; cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3); z-index: 9;
        }
        .blue-marker:hover { transform: translate(-50%, -50%) scale(1.1); background: rgba(37, 99, 235, 1); }

        @media print { .no-print { display: none; } }
        .loading-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255,255,255,0.9); display: flex; align-items: center;
            justify-content: center; z-index: 100;
        }
        .status-pill { transition: all 0.3s ease; }
        .modal-backdrop { background: rgba(0,0,0,0.5); backdrop-filter: blur(2px); }
        
        .tool-btn.active { background-color: #000080; color: white; border-color: #000080; }
        .tab-btn.active { border-bottom: 2px solid #000080; color: #000080; font-weight: 700; }
    </style>
</head>
<body class="p-4 md:p-8">

    <div id="loading" class="loading-overlay hidden">
        <div class="flex flex-col items-center gap-2">
            <div class="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <p class="text-sm font-semibold text-slate-700" id="loadingText">İşlem Yapılıyor...</p>
        </div>
    </div>

    <!-- Confirmation Modal -->
    <div id="confirmModal" class="fixed inset-0 z-[200] hidden flex items-center justify-center p-4 modal-backdrop">
        <div class="bg-white rounded-xl shadow-xl max-w-sm w-full p-6 space-y-4 border border-slate-200">
            <h3 class="text-lg font-bold text-slate-800" id="modalTitle">Emin misiniz?</h3>
            <p class="text-slate-600 text-sm" id="modalMessage">Veriler kalıcı olarak silinecek.</p>
            <div class="flex justify-end gap-3 pt-2">
                <button id="modalCancelBtn" class="px-4 py-2 text-sm font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">Vazgeç</button>
                <button id="modalConfirmBtn" class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg shadow-md transition-all">Evet</button>
            </div>
        </div>
    </div>

    <div class="max-w-5xl mx-auto space-y-6">
        <!-- Header -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-xl shadow-sm border border-slate-200 no-print">
            <div class="flex items-center gap-4 flex-grow">
                <div id="logoUploadArea" class="w-16 h-16 shrink-0 border-2 border-dashed border-slate-300 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-[#000080] hover:bg-slate-50 transition-all overflow-hidden relative group">
                    <div id="logoPlaceholder" class="text-slate-400 flex flex-col items-center">
                        <i data-lucide="image" class="w-4 h-4"></i>
                        <span class="text-[8px] font-bold mt-1 uppercase">Logo</span>
                    </div>
                    <img id="logoPreview" class="hidden w-full h-full object-contain p-1" src="">
                    <input type="file" id="logoInput" class="hidden" accept="image/*">
                </div>

                <div class="flex-grow space-y-2">
                    <div class="flex items-center justify-between">
                        <h1 class="text-xl font-bold text-[#000080] leading-none text-nowrap">Visual SOP Creator</h1>
                        <div id="saveStatus" class="status-pill text-[10px] font-bold px-2 py-1 rounded-full bg-slate-100 text-slate-400">Bağlantı Hazır</div>
                    </div>
                    <input type="text" id="sopTitleInput" class="w-full p-1 text-lg font-bold border-b border-slate-200 focus:border-[#000080] focus:outline-none transition-colors text-slate-800 bg-transparent" placeholder="Ana Başlık (Örn: Paketleme Süreci)">
                    <input type="text" id="sopSubtitleInput" class="w-full p-1 text-sm font-medium border-b border-slate-100 focus:border-[#000080] focus:outline-none transition-colors text-slate-500 bg-transparent" placeholder="Alt Başlık (Örn: Departman, Tarih veya Versiyon)">
                </div>
            </div>
            
            <div class="flex flex-wrap gap-2 shrink-0">
                <button id="resetImageBtn" class="px-4 py-2 text-sm font-medium text-orange-600 bg-orange-50 hover:bg-orange-100 rounded-lg transition-colors flex items-center gap-2 border border-orange-200">
                    <i data-lucide="image-minus" class="w-4 h-4"></i> Reset Photo
                </button>
                <button id="resetBtn" class="px-4 py-2 text-sm font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors flex items-center gap-2">
                    <i data-lucide="rotate-ccw" class="w-4 h-4"></i> Reset All
                </button>
                <div class="flex bg-[#000080] rounded-lg shadow-md overflow-hidden">
                    <button id="exportBtn" class="px-3 py-2 text-[10px] font-bold text-white hover:bg-[#000066] border-r border-[#000066]/50">JPG</button>
                    <button id="exportPdfBtn" class="px-3 py-2 text-[10px] font-bold text-white hover:bg-[#000066] border-r border-[#000066]/50">PDF</button>
                    <button id="exportWordBtn" class="px-3 py-2 text-[10px] font-bold text-white hover:bg-[#000066] flex items-center gap-1">WORD</button>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Left Editor -->
            <div class="lg:col-span-2 space-y-4">
                <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden p-4">
                    <!-- Tab Bar -->
                    <div class="flex border-b border-slate-100 mb-4">
                        <button id="tab0" class="tab-btn active px-4 py-2 text-sm transition-all flex items-center gap-2">
                            <i data-lucide="image" class="w-4 h-4"></i> Görsel 1
                        </button>
                        <button id="tab1" class="tab-btn px-4 py-2 text-sm transition-all flex items-center gap-2">
                            <i data-lucide="image" class="w-4 h-4"></i> Görsel 2
                        </button>
                    </div>

                    <div id="uploadArea" class="bg-slate-50 p-12 rounded-xl border-2 border-dashed border-slate-200 flex flex-col items-center justify-center gap-4 text-slate-500 hover:border-[#000080] transition-colors cursor-pointer">
                        <i data-lucide="image-plus" class="w-12 h-12 text-slate-300"></i>
                        <div class="text-center">
                            <p class="font-semibold text-slate-700">Bu Sekme İçin Görsel Yükle</p>
                            <p class="text-xs">PNG, JPG veya JPEG</p>
                        </div>
                        <input type="file" id="fileInput" class="hidden" accept="image/*">
                    </div>

                    <div id="editorArea" class="hidden space-y-4">
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                            <span class="text-sm font-semibold text-slate-700 flex items-center gap-2">
                                <i data-lucide="mouse-pointer-2" class="w-4 h-4"></i> Görsel Üzerine Tıklayın
                            </span>
                            <div class="flex bg-slate-100 p-1 rounded-lg border border-slate-200 overflow-hidden">
                                <button id="toolInstruction" class="tool-btn active px-3 py-1.5 text-xs font-bold rounded-md flex items-center gap-2 transition-all">
                                    <i data-lucide="list-ordered" class="w-3 h-3 text-red-500"></i> Talimat (Kırmızı)
                                </button>
                                <button id="toolMarker" class="tool-btn px-3 py-1.5 text-xs font-bold rounded-md flex items-center gap-2 transition-all">
                                    <i data-lucide="circle-dot" class="w-3 h-3 text-blue-500"></i> İşaretleyici (Mavi)
                                </button>
                            </div>
                        </div>
                        <div class="canvas-container" id="canvasContainer">
                            <canvas id="mainCanvas"></canvas>
                            <div id="markersOverlay"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Tables -->
            <div class="space-y-4">
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col h-fit">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-lg font-bold text-[#000080] flex items-center gap-2">
                            <i data-lucide="list-checks" class="w-5 h-5"></i> Instructions
                        </h2>
                        <button id="addManualBtn" class="px-3 py-1 text-xs font-semibold text-white bg-blue-500 hover:bg-blue-600 rounded-md shadow-sm flex items-center gap-1 transition-all">
                            <i data-lucide="plus" class="w-3 h-3"></i> Add Manual Step
                        </button>
                    </div>
                    <div class="overflow-auto max-h-[350px]">
                        <table class="w-full text-sm text-left">
                            <thead class="text-xs text-slate-500 uppercase bg-slate-50 sticky top-0">
                                <tr>
                                    <th class="px-2 py-3 w-8 text-center">No</th>
                                    <th class="px-2 py-3">Instruction</th>
                                    <th class="px-2 py-3 w-8"></th>
                                </tr>
                            </thead>
                            <tbody id="tableBody" class="divide-y divide-slate-100"></tbody>
                        </table>
                        <div id="emptyTableState" class="py-8 text-center text-slate-400">
                            <p class="text-xs italic">Talimat modunda görsel üzerine tıklayın</p>
                        </div>
                    </div>
                </div>

                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-lg font-bold text-[#b91c1c] flex items-center gap-2">
                            <i data-lucide="alert-triangle" class="w-5 h-5"></i> Warnings
                        </h2>
                        <button id="addWarningBtn" class="px-3 py-1 text-xs font-semibold text-white bg-red-500 hover:bg-red-600 rounded-md shadow-sm flex items-center gap-1 transition-all">
                            <i data-lucide="plus" class="w-3 h-3"></i> Add Warning
                        </button>
                    </div>
                    <div id="warningsContainer" class="space-y-2 max-h-[250px] overflow-auto"></div>
                </div>
            </div>
        </div>
    </div>

    <canvas id="exportCanvas" class="hidden"></canvas>

    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, onAuthStateChanged, signInWithCustomToken } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore, doc, setDoc, getDoc, deleteDoc } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

        // --- GITHUB İÇİN BURAYI DÜZENLE ---
        const firebaseConfig = {
          apiKey: "BURAYA_API_KEY_GELECEK",
          authDomain: "PROJE_ID.firebaseapp.com",
          projectId: "PROJE_ID",
          storageBucket: "PROJE_ID.firebasestorage.app",
          messagingSenderId: "SENDER_ID",
          appId: "APP_ID"
        };
        
        const appId = 'visual-sop-v1';
        let app, auth, db;
        
        try {
            if(firebaseConfig.apiKey !== "BURAYA_API_KEY_GELECEK") {
                app = initializeApp(firebaseConfig);
                auth = getAuth(app);
                db = getFirestore(app);
            }
        } catch(e) { console.error("Firebase başlatılamadı."); }

        const elements = {
            fileInput: document.getElementById('fileInput'),
            logoInput: document.getElementById('logoInput'),
            uploadArea: document.getElementById('uploadArea'),
            logoUploadArea: document.getElementById('logoUploadArea'),
            editorArea: document.getElementById('editorArea'),
            mainCanvas: document.getElementById('mainCanvas'),
            markersOverlay: document.getElementById('markersOverlay'),
            tableBody: document.getElementById('tableBody'),
            emptyTableState: document.getElementById('emptyTableState'),
            warningsContainer: document.getElementById('warningsContainer'),
            resetBtn: document.getElementById('resetBtn'),
            resetImageBtn: document.getElementById('resetImageBtn'),
            exportBtn: document.getElementById('exportBtn'),
            exportPdfBtn: document.getElementById('exportPdfBtn'),
            exportWordBtn: document.getElementById('exportWordBtn'),
            addManualBtn: document.getElementById('addManualBtn'),
            addWarningBtn: document.getElementById('addWarningBtn'),
            sopTitleInput: document.getElementById('sopTitleInput'),
            sopSubtitleInput: document.getElementById('sopSubtitleInput'),
            logoPreview: document.getElementById('logoPreview'),
            logoPlaceholder: document.getElementById('logoPlaceholder'),
            loadingOverlay: document.getElementById('loading'),
            loadingText: document.getElementById('loadingText'),
            saveStatus: document.getElementById('saveStatus'),
            confirmModal: document.getElementById('confirmModal'),
            modalConfirmBtn: document.getElementById('modalConfirmBtn'),
            modalCancelBtn: document.getElementById('modalCancelBtn'),
            modalTitle: document.getElementById('modalTitle'),
            modalMessage: document.getElementById('modalMessage'),
            toolInstruction: document.getElementById('toolInstruction'),
            toolMarker: document.getElementById('toolMarker'),
            tabBtns: [document.getElementById('tab0'), document.getElementById('tab1')]
        };
        
        const ctx = elements.mainCanvas.getContext('2d');

        let activeIdx = 0;
        let images = [null, null];
        let imagesBase64 = [null, null];
        let companyLogo = null;
        let companyLogoBase64 = null;
        let points = []; 
        let warnings = [];
        let user = null;
        let saveTimeout;
        let isResetting = false;
        let currentMode = 'instruction'; 

        lucide.createIcons();

        // --- Fonksiyon Tanımlamaları (Hoisting hatalarını önlemek için en üstte) ---

        const setupCanvas = () => {
            const img = images[activeIdx];
            if (!img) return;
            const dw = 1200; const scale = dw / img.width;
            elements.mainCanvas.width = dw; elements.mainCanvas.height = img.height * scale;
            ctx.drawImage(img, 0, 0, dw, elements.mainCanvas.height);
        };

        const renderMarkers = () => {
            elements.markersOverlay.innerHTML = '';
            points.forEach((p, idx) => {
                if (p.imgIdx !== activeIdx || p.isManual) return;
                const marker = document.createElement('div');
                marker.className = p.isSilent ? 'blue-marker' : 'marker';
                marker.innerText = p.id;
                marker.style.left = `${p.px}%`; marker.style.top = `${p.py}%`;
                if (p.isSilent) marker.oncontextmenu = (e) => { e.preventDefault(); points.splice(idx, 1); updateAndRender(); saveData(); };
                elements.markersOverlay.appendChild(marker);
            });
        };

        const refreshEditor = () => {
            if (images[activeIdx]) {
                elements.uploadArea.classList.add('hidden');
                elements.editorArea.classList.remove('hidden');
                setupCanvas();
                renderMarkers();
            } else {
                elements.uploadArea.classList.remove('hidden');
                elements.editorArea.classList.add('hidden');
            }
        };

        const setStatus = (status) => {
            const labels = { saving: 'Kaydediliyor...', saved: 'Kaydedildi', error: 'Hata', connected: 'Hazır' };
            elements.saveStatus.innerText = labels[status] || 'Hazır';
        };

        const renderTable = () => {
            const tablePoints = points.filter(p => !p.isSilent);
            elements.emptyTableState.classList.toggle('hidden', tablePoints.length > 0);
            elements.tableBody.innerHTML = '';
            points.forEach((p, idx) => {
                if (p.isSilent) return;
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="px-2 py-3 font-bold text-center ${p.isManual ? 'text-blue-500' : 'text-red-500'}">${p.id}</td>
                    <td class="px-2 py-3"><textarea class="w-full p-2 border border-slate-200 rounded-md text-[10px]" oninput="updateDesc(${idx}, this.value)">${p.description}</textarea></td>
                    <td class="px-2 py-3"><button onclick="removePoint(${idx})" class="text-slate-300 hover:text-red-500"><i data-lucide="trash-2" class="w-3 h-3"></i></button></td>
                `;
                elements.tableBody.appendChild(tr);
            });
            lucide.createIcons();
        };

        const renderWarnings = () => {
            elements.warningsContainer.innerHTML = '';
            warnings.forEach((w, idx) => {
                const div = document.createElement('div');
                div.className = 'flex items-center gap-2';
                div.innerHTML = `<input type="text" value="${w.text}" class="flex-grow p-2 text-[10px] border rounded" oninput="updateWarn(${idx}, this.value)"><button onclick="removeWarn(${idx})" class="text-red-500">×</button>`;
                elements.warningsContainer.appendChild(div);
            });
        };

        const updateAndRender = () => {
            let instrCount = 0; let markerCount = 0;
            points.forEach((p) => {
                if (p.isSilent) { markerCount++; p.id = markerCount; }
                else { instrCount++; p.id = instrCount; }
            });
            renderMarkers(); renderTable(); lucide.createIcons();
        };

        const applyData = (data) => {
            elements.sopTitleInput.value = data.title || '';
            elements.sopSubtitleInput.value = data.subtitle || '';
            points = data.points || [];
            warnings = data.warnings || [];
            imagesBase64 = data.imagesBase64 || [null, null];
            companyLogoBase64 = data.logoImage || null;

            if (companyLogoBase64) {
                const img = new Image();
                img.onload = () => { companyLogo = img; elements.logoPreview.src = companyLogoBase64; elements.logoPreview.classList.remove('hidden'); elements.logoPlaceholder.classList.add('hidden'); };
                img.src = companyLogoBase64;
            }

            const loadImg = (idx) => {
                if (!imagesBase64[idx]) return;
                const img = new Image();
                img.onload = () => { images[idx] = img; if (idx === activeIdx) refreshEditor(); };
                img.src = imagesBase64[idx];
            };
            loadImg(0); loadImg(1);
            updateAndRender();
            setStatus('saved');
        };

        const loadFromLocalStorage = () => {
            const raw = localStorage.getItem('sop_local_data');
            if (raw) applyData(JSON.parse(raw));
        };

        const getDocRef = () => (db && user) ? doc(db, 'sop_data', user.uid) : null;

        const loadData = async () => {
            const docRef = getDocRef();
            if (!docRef) return;
            elements.loadingOverlay.classList.remove('hidden');
            try {
                const docSnap = await getDoc(docRef);
                if (docSnap.exists()) applyData(docSnap.data());
            } catch (e) { console.error(e); }
            finally { elements.loadingOverlay.classList.add('hidden'); }
        };

        const saveData = async () => {
            if (isResetting) return;
            const data = {
                title: elements.sopTitleInput.value,
                subtitle: elements.sopSubtitleInput.value,
                points, warnings, imagesBase64,
                logoImage: companyLogoBase64,
                lastUpdated: new Date().toISOString()
            };

            localStorage.setItem('sop_local_data', JSON.stringify(data));
            
            const docRef = getDocRef();
            if (!docRef) { setStatus('saved'); return; }
            
            setStatus('saving');
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(async () => {
                try {
                    await setDoc(docRef, data);
                    setStatus('saved');
                } catch (e) { setStatus('error'); }
            }, 1500);
        };

        const initAuth = async () => {
            if (!auth) return;
            try {
                await signInAnonymously(auth);
            } catch(e) { console.error("Auth hatası."); }
        };

        // --- Event Listenerlar ve Başlatma ---

        elements.tabBtns.forEach((btn, idx) => {
            btn.onclick = () => {
                activeIdx = idx;
                elements.tabBtns.forEach((b, i) => b.classList.toggle('active', i === idx));
                refreshEditor();
            };
        });

        elements.toolInstruction.onclick = () => {
            currentMode = 'instruction';
            elements.toolInstruction.classList.add('active');
            elements.toolMarker.classList.remove('active');
        };
        elements.toolMarker.onclick = () => {
            currentMode = 'marker';
            elements.toolMarker.classList.add('active');
            elements.toolInstruction.classList.remove('active');
        };

        elements.uploadArea.onclick = () => elements.fileInput.click();
        elements.logoUploadArea.onclick = () => elements.logoInput.click();
        
        elements.fileInput.onchange = (e) => handleImageUpload(e, 'main');
        elements.logoInput.onchange = (e) => handleImageUpload(e, 'logo');
        elements.sopTitleInput.oninput = saveData;
        elements.sopSubtitleInput.oninput = saveData;

        function handleImageUpload(e, type) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (event) => {
                const img = new Image();
                img.onload = () => {
                    const canvasResize = document.createElement('canvas');
                    let w = img.width, h = img.height;
                    const maxW = type === 'logo' ? 200 : 1000;
                    if (w > maxW) { h *= maxW / w; w = maxW; }
                    canvasResize.width = w; canvasResize.height = h;
                    canvasResize.getContext('2d').drawImage(img, 0, 0, w, h);
                    const comp = canvasResize.toDataURL('image/jpeg', 0.5);

                    if (type === 'main') { images[activeIdx] = img; imagesBase64[activeIdx] = comp; refreshEditor(); }
                    else { companyLogo = img; companyLogoBase64 = comp; elements.logoPreview.src = comp; elements.logoPreview.classList.remove('hidden'); elements.logoPlaceholder.classList.add('hidden'); }
                    saveData();
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);
        }

        elements.mainCanvas.addEventListener('click', (e) => {
            if (!images[activeIdx]) return;
            const rect = elements.mainCanvas.getBoundingClientRect();
            const px = ((e.clientX - rect.left) / rect.width) * 100;
            const py = ((e.clientY - rect.top) / rect.height) * 100;
            points.push({ id: null, px, py, description: '', isManual: false, isSilent: currentMode === 'marker', imgIdx: activeIdx });
            updateAndRender(); saveData();
        });

        elements.addManualBtn.onclick = () => {
            points.push({ id: null, px: null, py: null, description: '', isManual: true, isSilent: false, imgIdx: -1 });
            updateAndRender(); saveData();
        };

        elements.addWarningBtn.onclick = () => {
            warnings.push({ text: '' }); renderWarnings(); saveData();
        };

        window.updateDesc = (idx, val) => { points[idx].description = val; saveData(); };
        window.removePoint = (idx) => { points.splice(idx, 1); updateAndRender(); saveData(); };
        window.updateWarn = (idx, val) => { warnings[idx].text = val; saveData(); };
        window.removeWarn = (idx) => { warnings.splice(idx, 1); renderWarnings(); saveData(); };

        // Export logic
        const getMergedImage = (img, pointsForImg) => {
            const tempCanvas = document.createElement('canvas');
            const tCtx = tempCanvas.getContext('2d');
            const dw = 1200;
            const scale = dw / img.width;
            tempCanvas.width = dw;
            tempCanvas.height = img.height * scale;
            tCtx.drawImage(img, 0, 0, dw, tempCanvas.height);
            
            pointsForImg.forEach(p => {
                if (p.isManual) return;
                tCtx.beginPath(); tCtx.arc((p.px/100)*dw, (p.py/100)*tempCanvas.height, 18, 0, 2*Math.PI);
                tCtx.fillStyle = p.isSilent ? '#3b82f6' : '#ef4444';
                tCtx.fill(); tCtx.strokeStyle = 'white'; tCtx.lineWidth = 3; tCtx.stroke();
                tCtx.fillStyle = 'white'; tCtx.font = 'bold 18px Arial'; tCtx.textAlign = 'center'; tCtx.textBaseline = 'middle';
                tCtx.fillText(p.id, (p.px/100)*dw, (p.py/100)*tempCanvas.height);
            });
            return tempCanvas.toDataURL('image/jpeg', 0.85);
        };

        const wrapText = (context, text, x, y, maxWidth, lineHeight, draw = true) => {
            const words = text.split(' '); let line = '', count = 1;
            for(let n=0; n<words.length; n++) {
                let test = line + words[n] + ' ';
                if (context.measureText(test).width > maxWidth && n > 0) {
                    if(draw) context.fillText(line, x, y); 
                    line = words[n] + ' '; y += lineHeight; count++;
                } else line = test;
            }
            if(draw) context.fillText(line, x, y); return count;
        };

        const renderExport = async () => {
            const canv = document.getElementById('exportCanvas');
            const exCtx = canv.getContext('2d');
            canv.width = 1240; canv.height = 1754;
            exCtx.fillStyle = 'white'; exCtx.fillRect(0, 0, 1240, 1754);

            const title = elements.sopTitleInput.value.trim().toUpperCase() || 'STANDARD OPERATING PROCEDURE';
            const subtitle = elements.sopSubtitleInput.value.trim();
            let headY = 80, tStartX = 60;

            if (companyLogo) {
                const lScale = Math.min(80 / companyLogo.width, 80 / companyLogo.height);
                const lw = companyLogo.width * lScale, lh = companyLogo.height * lScale;
                exCtx.drawImage(companyLogo, 60, headY - (lh/2), lw, lh);
                tStartX = 60 + lw + 25;
            }

            exCtx.fillStyle = '#000080'; exCtx.font = 'bold 36px Arial'; exCtx.textBaseline = 'middle';
            exCtx.fillText(title, tStartX, subtitle ? headY - 15 : headY);
            if (subtitle) { exCtx.fillStyle = '#64748b'; exCtx.font = '500 24px Arial'; exCtx.fillText(subtitle, tStartX, headY + 20); }

            exCtx.strokeStyle = '#000080'; exCtx.lineWidth = 3;
            exCtx.beginPath(); exCtx.moveTo(60, 135); exCtx.lineTo(1180, 135); exCtx.stroke();

            let imgY = 175;
            const activeImages = images.filter(img => img !== null);
            let imgHeightUsed = 0;

            if (activeImages.length === 1) {
                const img = activeImages[0];
                const imgW = 1120; const scale = imgW / img.width;
                const imgH = Math.min(img.height * scale, 750);
                const actualIdx = images.indexOf(img);
                const merged = getMergedImage(img, points.filter(p => p.imgIdx === actualIdx));
                const imgEl = new Image(); imgEl.src = merged; 
                await new Promise(r => imgEl.onload = r);
                exCtx.drawImage(imgEl, 60, imgY, imgW, imgH);
                imgHeightUsed = imgH;
            } else if (activeImages.length === 2) {
                const imgW = 550;
                for (let i = 0; i < 2; i++) {
                    if (!images[i]) continue;
                    const scale = imgW / images[i].width;
                    const imgH = Math.min(images[i].height * scale, 600);
                    const merged = getMergedImage(images[i], points.filter(p => p.imgIdx === i));
                    const imgEl = new Image(); imgEl.src = merged;
                    await new Promise(r => imgEl.onload = r);
                    exCtx.drawImage(imgEl, 60 + i * 570, imgY, imgW, imgH);
                    imgHeightUsed = Math.max(imgHeightUsed, imgH);
                }
            }

            const instrPoints = points.filter(p => !p.isSilent);
            let curY = imgY + imgHeightUsed + 60;
            exCtx.fillStyle = '#f1f5f9'; exCtx.fillRect(60, curY, 1120, 50);
            exCtx.fillStyle = '#000080'; exCtx.font = 'bold 18px Arial';
            exCtx.fillText('NO', 80, curY + 25); exCtx.fillText('INSTRUCTIONS', 160, curY + 25);
            
            curY += 50; exCtx.strokeStyle = '#e2e8f0'; exCtx.lineWidth = 1;
            instrPoints.forEach(p => {
                exCtx.fillStyle = p.isManual ? '#3b82f6' : '#ef4444';
                exCtx.font = 'bold 20px Arial'; exCtx.fillText(p.id, 85, curY + 40);
                exCtx.fillStyle = '#334155'; exCtx.font = '18px Arial';
                const lines = wrapText(exCtx, (p.description || '...'), 160, curY + 40, 900, 25);
                exCtx.beginPath(); exCtx.moveTo(60, curY + 70 + (lines-1)*25); exCtx.lineTo(1180, curY + 70 + (lines-1)*25); exCtx.stroke();
                curY += 80 + (lines-1)*25;
            });

            const actWarns = warnings.filter(w => w.text.trim() !== '');
            if (actWarns.length > 0) {
                curY += 40; exCtx.fillStyle = '#b91c1c'; exCtx.font = 'bold 20px Arial';
                exCtx.fillText('WARNINGS', 80, curY + 35); curY += 70;
                actWarns.forEach(w => {
                    exCtx.fillStyle = '#b91c1c'; exCtx.fillText('•', 80, curY);
                    exCtx.fillStyle = '#1e293b'; exCtx.font = '16px Arial';
                    curY += 22 * wrapText(exCtx, w.text, 105, curY, 900, 22) + 5;
                });
            }
            return canv;
        };

        elements.exportBtn.onclick = async () => {
            elements.loadingOverlay.classList.remove('hidden');
            const canv = await renderExport();
            const link = document.createElement('a');
            link.download = `${elements.sopTitleInput.value || 'SOP'}.jpg`;
            link.href = canv.toDataURL('image/jpeg', 0.95); link.click();
            elements.loadingOverlay.classList.add('hidden');
        };

        elements.exportPdfBtn.onclick = async () => {
            elements.loadingOverlay.classList.remove('hidden');
            const canv = await renderExport();
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF('p', 'mm', 'a4');
            pdf.addImage(canv.toDataURL('image/jpeg', 0.95), 'JPEG', 0, 0, 210, 297);
            pdf.save(`${elements.sopTitleInput.value || 'SOP'}.pdf`);
            elements.loadingOverlay.classList.add('hidden');
        };

        elements.exportWordBtn.onclick = async () => {
            const docxLib = window.docx;
            if (!docxLib) { alert("Word kütüphanesi yüklenemedi."); return; }
            elements.loadingText.innerText = "Word Dosyası Hazırlanıyor...";
            elements.loadingOverlay.classList.remove('hidden');
            const { Document, Packer, Paragraph, Table, TableCell, TableRow, ImageRun, WidthType, AlignmentType, TextRun, BorderStyle, HeadingLevel } = docxLib;
            const dataUriToUint8Array = (uri) => {
                const base64 = uri.split(',')[1];
                const binary = atob(base64);
                const bytes = new Uint8Array(binary.length);
                for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
                return bytes;
            };
            try {
                const children = [];
                const docTitle = elements.sopTitleInput.value || 'SOP';
                const headerCells = [];
                if (companyLogoBase64) {
                    headerCells.push(new TableCell({
                        children: [new Paragraph({ children: [new ImageRun({ data: dataUriToUint8Array(companyLogoBase64), transformation: { width: 60, height: 60 } })] })],
                        borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }
                    }));
                }
                headerCells.push(new TableCell({
                    children: [
                        new Paragraph({ children: [new TextRun({ text: docTitle.toUpperCase(), bold: true, size: 36, color: "000080" })] }),
                        new Paragraph({ children: [new TextRun({ text: elements.sopSubtitleInput.value, size: 24, color: "666666" })] })
                    ],
                    borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }
                }));
                children.push(new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, rows: [new TableRow({ children: headerCells })] }));
                children.push(new Paragraph({ text: "", spacing: { after: 200 } }));
                if (images.some(i => i)) {
                    const imgCells = [];
                    for (let i = 0; i < images.length; i++) {
                        if (!images[i]) continue;
                        const mergedData = getMergedImage(images[i], points.filter(p => p.imgIdx === i));
                        const ratio = images[i].height / images[i].width;
                        imgCells.push(new TableCell({
                            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({ data: dataUriToUint8Array(mergedData), transformation: { width: 280, height: 280 * ratio } })] })],
                            borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } }
                        }));
                    }
                    children.push(new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, rows: [new TableRow({ children: imgCells })] }));
                }
                children.push(new Paragraph({ text: "TALİMATLAR", heading: HeadingLevel.HEADING_2, spacing: { before: 400, after: 200 } }));
                const instrRows = [new TableRow({ children: [
                    new TableCell({ children: [new Paragraph({ text: "NO", bold: true })], shading: { fill: "F1F5F9" } }),
                    new TableCell({ children: [new Paragraph({ text: "TALİMAT", bold: true })], shading: { fill: "F1F5F9" } })
                ]})];
                points.filter(p => !p.isSilent).forEach(p => {
                    instrRows.push(new TableRow({ children: [
                        new TableCell({ children: [new Paragraph({ text: String(p.id), bold: true })] }),
                        new TableCell({ children: [new Paragraph({ text: p.description || "..." })] })
                    ]}));
                });
                children.push(new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, rows: instrRows }));
                const actWarns = warnings.filter(w => w.text.trim() !== '');
                if (actWarns.length > 0) {
                    children.push(new Paragraph({ text: "UYARILAR", heading: HeadingLevel.HEADING_2, spacing: { before: 400, after: 200 }, color: "B91C1C" }));
                    actWarns.forEach(w => children.push(new Paragraph({ text: `• ${w.text}`, color: "B91C1C" })));
                }
                const docGenerated = new Document({ sections: [{ children }] });
                const blob = await Packer.toBlob(docGenerated);
                window.saveAs(blob, `${docTitle.replace(/\s+/g,'_')}.docx`);
            } catch (err) { console.error(err); alert("Word dosyası oluşturulamadı."); }
            finally { elements.loadingOverlay.classList.add('hidden'); }
        };

        const showConfirm = (title, msg, callback) => {
            elements.modalTitle.innerText = title; elements.modalMessage.innerText = msg;
            elements.confirmModal.classList.remove('hidden');
            elements.modalConfirmBtn.onclick = () => { elements.confirmModal.classList.add('hidden'); callback(); };
            elements.modalCancelBtn.onclick = () => elements.confirmModal.classList.add('hidden');
        };

        elements.resetImageBtn.onclick = () => {
            showConfirm("Görseli Sıfırla", `Görsel ${activeIdx + 1} ve üzerindeki noktalar silinecek.`, async () => {
                images[activeIdx] = null; imagesBase64[activeIdx] = null;
                points = points.filter(p => p.imgIdx !== activeIdx);
                refreshEditor(); updateAndRender(); await saveData();
            });
        };

        elements.resetBtn.onclick = () => {
            showConfirm("Her Şeyi Sıfırla", "Tüm veriler temizlenecek.", async () => {
                isResetting = true; points = []; warnings = []; images = [null, null]; imagesBase64 = [null, null];
                companyLogo = null; companyLogoBase64 = null;
                elements.sopTitleInput.value = ''; elements.sopSubtitleInput.value = '';
                elements.logoPreview.classList.add('hidden'); elements.logoPlaceholder.classList.remove('hidden');
                refreshEditor(); updateAndRender(); renderWarnings();
                const docRef = getDocRef(); if (docRef) await deleteDoc(docRef);
                localStorage.removeItem('sop_local_data');
                isResetting = false; setStatus('connected');
            });
        };

        // --- Uygulama Başlatma (Hataları önlemek için tüm tanımlardan sonra) ---
        if(auth) {
            onAuthStateChanged(auth, (u) => { user = u; if (user) loadData(); });
            initAuth();
        } else {
            loadFromLocalStorage();
        }

    </script>
</body>
</html>
