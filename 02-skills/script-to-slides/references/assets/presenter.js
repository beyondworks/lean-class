// 발표자 모드 컨트롤러
// - 슬라이드 이동을 BroadcastChannel/localStorage로 방송 → 청중 창 + 미리보기 iframe 동기화
// - 발표자 노트: localStorage 자동 저장 / 기본 스크립트(notes.js) 시드 / 글자 크기 조절
(() => {
  const $ = id => document.getElementById(id);
  const N = (window.DEFAULT_NOTES && DEFAULT_NOTES.length) || 32;
  const clamp = k => Math.max(0, Math.min(N - 1, k));

  const bc = ('BroadcastChannel' in window) ? new BroadcastChannel('deck-sync') : null;
  const LS_CUR = 'deck-current', LS_NOTES = 'deck-notes', LS_SIZE = 'deck-notes-size';

  const pnow = $('pnow'), ptot = $('ptot'), notes = $('notes'),
        saveState = $('saveState'), ptimer = $('ptimer');
  ptot.textContent = N;

  let master = clamp(parseInt(localStorage.getItem(LS_CUR) || '0', 10) || 0);

  // ── 슬라이드 이동 ──
  function goto(m, fromSync) {
    master = clamp(m);
    pnow.textContent = master + 1;
    loadNote();
    if (fromSync) return;
    try { localStorage.setItem(LS_CUR, String(master)); } catch (e) {}
    if (bc) bc.postMessage({ type: 'goto', i: master });
  }
  // 청중이 넘기면 수신
  if (bc) bc.onmessage = e => { if (e.data && e.data.type === 'goto') goto(e.data.i, true); };
  window.addEventListener('storage', e => {
    if (e.key === LS_CUR && e.newValue != null) goto(parseInt(e.newValue, 10), true);
  });

  $('pPrev').addEventListener('click', () => goto(master - 1));
  $('pNext').addEventListener('click', () => goto(master + 1));
  document.addEventListener('keydown', e => {
    if (e.target === notes) return; // 노트 입력 중엔 방향키로 슬라이드 안 넘김
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); goto(master + 1); }
    else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); goto(master - 1); }
    else if (e.key === 'Home') goto(0);
    else if (e.key === 'End') goto(N - 1);
  });
  $('audBtn').addEventListener('click', () => window.open('index.html', 'audience'));

  // ── 발표자 노트 ──
  function getNotes() { try { return JSON.parse(localStorage.getItem(LS_NOTES) || '{}'); } catch (e) { return {}; } }
  function loadNote() {
    const edited = getNotes();
    notes.value = (edited[master] != null) ? edited[master]
      : (window.DEFAULT_NOTES ? (DEFAULT_NOTES[master] || '') : '');
    saveState.textContent = '저장됨'; saveState.classList.remove('saving');
  }
  let t = null;
  notes.addEventListener('input', () => {
    saveState.textContent = '저장 중…'; saveState.classList.add('saving');
    clearTimeout(t);
    t = setTimeout(() => {
      const ed = getNotes(); ed[master] = notes.value;
      try { localStorage.setItem(LS_NOTES, JSON.stringify(ed)); } catch (e) {}
      saveState.textContent = '저장됨'; saveState.classList.remove('saving');
    }, 500);
  });
  $('nReset').addEventListener('click', () => {
    const ed = getNotes(); delete ed[master];
    try { localStorage.setItem(LS_NOTES, JSON.stringify(ed)); } catch (e) {}
    loadNote();
  });

  // ── 글자 크기 ──
  let size = parseInt(localStorage.getItem(LS_SIZE) || '18', 10);
  function applySize() { notes.style.fontSize = size + 'px'; try { localStorage.setItem(LS_SIZE, String(size)); } catch (e) {} }
  $('nMinus').addEventListener('click', () => { size = Math.max(12, size - 2); applySize(); });
  $('nPlus').addEventListener('click', () => { size = Math.min(40, size + 2); applySize(); });
  applySize();

  // ── 타이머 ──
  let start = Date.now();
  const fmt = s => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
  setInterval(() => { ptimer.textContent = fmt(Math.floor((Date.now() - start) / 1000)); }, 500);
  $('ptReset').addEventListener('click', () => { start = Date.now(); ptimer.textContent = '00:00'; });

  // 초기 렌더
  goto(master, true);
})();
