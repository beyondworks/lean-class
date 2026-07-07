// AI 에이전트 입문 — 16:9 캐러셀 + 발표자/청중 동기화
// 동기화: BroadcastChannel('deck-sync') + localStorage('deck-current') 폴백
// 임베드(?embed): 발표자 미리보기용 — 스스로 조작/방송 안 함, 수신만(offset 적용)
(() => {
  const track = document.getElementById('track');
  const slides = [...track.children];
  const dotsWrap = document.getElementById('dots');
  const prog = document.getElementById('prog');
  const cnow = document.getElementById('cnow');
  const ctot = document.getElementById('ctot');
  const n = slides.length;

  const params = new URLSearchParams(location.search);
  const EMBED = params.has('embed');
  const OFFSET = parseInt(params.get('offset') || '0', 10);
  if (EMBED) document.body.classList.add('embed');

  const bc = ('BroadcastChannel' in window) ? new BroadcastChannel('deck-sync') : null;
  const LS_CUR = 'deck-current';
  const clamp = k => Math.max(0, Math.min(n - 1, k));

  ctot.textContent = String(n).padStart(2, '0');

  // 점
  slides.forEach((_, k) => {
    const b = document.createElement('button');
    b.setAttribute('aria-label', `${k + 1}번 슬라이드`);
    b.addEventListener('click', () => setMaster(k));
    dotsWrap.appendChild(b);
  });
  const dots = [...dotsWrap.children];

  let master = 0; // 동기화된 청중 현재 위치

  function renderTo(disp) {
    track.style.transform = `translateX(-${disp * 100}%)`;
    dots.forEach((d, j) => d.classList.toggle('on', j === disp));
    prog.style.width = `${((disp + 1) / n) * 100}%`;
    cnow.textContent = String(disp + 1).padStart(2, '0');
  }

  // master 변경. fromSync=true 이면 수신/초기화(재방송 안 함)
  function setMaster(m, fromSync) {
    master = clamp(m);
    renderTo(EMBED ? clamp(master + OFFSET) : master);
    if (fromSync || EMBED) return;
    try { localStorage.setItem(LS_CUR, String(master)); } catch (e) {}
    bc && bc.postMessage({ type: 'goto', i: master });
    if (history.replaceState) history.replaceState(null, '', '#' + (master + 1));
  }

  // 수신
  if (bc) bc.onmessage = e => { if (e.data && e.data.type === 'goto') setMaster(e.data.i, true); };
  window.addEventListener('storage', e => {
    if (e.key === LS_CUR && e.newValue != null) setMaster(parseInt(e.newValue, 10), true);
  });

  function fsEl() { return document.fullscreenElement || document.webkitFullscreenElement || null; }
  function toggleFs() {
    const el = document.documentElement;
    if (!fsEl()) {
      const req = el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen;
      if (req) { try { const p = req.call(el); if (p && p.catch) p.catch(() => {}); } catch (e) {} }
    } else {
      const ex = document.exitFullscreen || document.webkitExitFullscreen || document.msExitFullscreen;
      if (ex) { try { ex.call(document); } catch (e) {} }
    }
  }
  function openPresenter() { window.open('presenter.html', 'presenter', 'width=1280,height=820'); }

  // 청중/메인만 조작
  if (!EMBED) {
    window.addEventListener('keydown', e => {
      if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); setMaster(master + 1); }
      else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); setMaster(master - 1); }
      else if (e.key === 'Home') setMaster(0);
      else if (e.key === 'End') setMaster(n - 1);
      else if (e.key === 'f' || e.key === 'F') toggleFs();
      else if (e.key === 's' || e.key === 'S') openPresenter();
    });
    let x0 = null;
    const down = x => x0 = x;
    const up = x => { if (x0 == null) return; const dx = x - x0; if (Math.abs(dx) > 50) setMaster(master + (dx < 0 ? 1 : -1)); x0 = null; };
    track.addEventListener('touchstart', e => down(e.touches[0].clientX), { passive: true });
    track.addEventListener('touchend', e => up(e.changedTouches[0].clientX), { passive: true });
    track.addEventListener('mousedown', e => down(e.clientX));
    window.addEventListener('mouseup', e => up(e.clientX));
    const fsBtn = document.getElementById('fsBtn');
    const prBtn = document.getElementById('prBtn');
    if (fsBtn) fsBtn.addEventListener('click', toggleFs);
    if (prBtn) prBtn.addEventListener('click', openPresenter);
  }

  // 초기 위치: 해시 > 저장 > 0
  let init = 0;
  const h = parseInt(location.hash.replace('#', ''), 10);
  if (h >= 1 && h <= n) init = h - 1;
  else { const s = parseInt(localStorage.getItem(LS_CUR) || '', 10); if (s >= 0 && s < n) init = s; }
  setMaster(init, true);
})();
