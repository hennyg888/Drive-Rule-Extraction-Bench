
(() => {
  const page = document.querySelector('.page');
  const still = matchMedia('(prefers-reduced-motion: reduce)');
  const behavior = () => (still.matches ? 'auto' : 'smooth');
  const store = (s, k, v) => { try { window[s].setItem(k, v); } catch (e) {} };
  const langButtons = page.querySelectorAll('[data-lang-btn]');
  function setLang(l) {
    page.dataset.lang = l;
    langButtons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.langBtn === l)));
    store('localStorage', 'passing-rules:lang', l);
    page.querySelectorAll('[data-tip-zh]').forEach(el => { el.title = l === 'zh' ? el.dataset.tipZh : el.dataset.tipEn; });
    requestAnimationFrame(draw);
  }
  langButtons.forEach(b => b.addEventListener('click', () => setLang(b.dataset.langBtn)));

  // ---------------------------------------------------------------- pages: one at a time; the navigation panel marks it
  const nav = document.getElementById('nav');
  const navBody = nav.querySelector('.nav-body');
  const main = document.getElementById('main');
  const appbar = page.querySelector('.appbar');
  const abPage = appbar.querySelector('.ab-page');
  const navOpen = appbar.querySelector('.nav-open');
  const wide = matchMedia('(min-width: 1000px)');
  const docked = () => wide.matches && page.dataset.nav !== 'hide';
  const setTabh = () => page.style.setProperty('--tabh', appbar.offsetHeight + 'px');
  new ResizeObserver(setTabh).observe(appbar);
  setTabh();
  // the page being read: a tab, or for the rule language, its part
  const here = () => (page.dataset.tab === 'language' ? page.dataset.part : page.dataset.tab);
  const mem = {};   // where each page was left, so coming back from the panel returns there

  function markNav() {
    const key = here();
    nav.querySelectorAll('.nv-i').forEach(li => {
      const on = li.dataset.for === key, a = li.querySelector('.nv-a');
      li.classList.toggle('on', on);
      if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    const a = nav.querySelector('.nv-i.on > .nv-a'), n = a && a.querySelector('.nv-n');
    if (a) abPage.innerHTML = (n ? '<span class="n">' + n.textContent + '</span>' : '') + a.querySelector('.nv-l').innerHTML;
  }
  // show a page; true if it is another page than before
  function setPage(tab, part) {
    const from = here(), y = scrollY;   // read before the page changes, while the old page still sets the height
    page.dataset.tab = tab;
    store('sessionStorage', 'passing-rules:tab', tab);
    if (part) { page.dataset.part = part; store('sessionStorage', 'passing-rules:part', part); }
    const moved = here() !== from;
    if (moved) mem[from] = y;
    markNav();
    requestAnimationFrame(() => { if (tab === 'doc') draw(); spyKey = null; spy(); });
    return moved;
  }
  // from the panel: another page opens where it was left (or at its top); the open page goes back to its top
  function openPage(tab, part) {
    const moved = setPage(tab, part);
    window.scrollTo(0, moved && mem[here()] != null ? mem[here()] : 0);
  }

  // ---------------------------------------------------------------- the panel: docked on wide screens (and can be hidden), a drawer on narrow ones
  function setNav(v) {
    if (v === 'hide') page.dataset.nav = 'hide'; else delete page.dataset.nav;
    store('localStorage', 'passing-rules:nav', v);
    setTabh();
    requestAnimationFrame(() => { draw(); spyKey = null; spy(); });
  }
  function keepInView(a, force) {
    // the panel scrolls on its own: keep the current entry in sight
    if (!a || !(force || docked() || page.dataset.drawer === 'open')) return;
    const tr = navBody.getBoundingClientRect(), ar = a.getBoundingClientRect();
    if (ar.top < tr.top + 24 || ar.bottom > tr.bottom - 24) navBody.scrollTop += ar.top - tr.top - tr.height / 3;
  }
  const current = () => nav.querySelector('.nv-i.on .nv-sub [aria-current="true"]') || nav.querySelector('.nv-i.on > .nv-a');
  function openDrawer() {
    page.dataset.drawer = 'open';
    navOpen.setAttribute('aria-expanded', 'true');
    main.inert = true;
    const cur = current();
    keepInView(cur, true);
    (cur || nav).focus({ preventScroll: true });
  }
  function closeDrawer(refocus) {
    if (page.dataset.drawer !== 'open') return;
    delete page.dataset.drawer;
    navOpen.setAttribute('aria-expanded', 'false');
    main.inert = false;
    if (refocus) navOpen.focus({ preventScroll: true });
  }
  navOpen.addEventListener('click', () => {
    if (!wide.matches) { openDrawer(); return; }
    setNav('dock');
    (current() || nav).focus({ preventScroll: true });
  });
  nav.querySelector('.nav-x').addEventListener('click', () => {
    if (!wide.matches) { closeDrawer(true); return; }
    setNav('hide');
    navOpen.focus({ preventScroll: true });
  });
  page.querySelector('.scrim').addEventListener('click', () => closeDrawer(true));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && page.dataset.drawer === 'open') closeDrawer(true); });
  wide.addEventListener('change', () => { closeDrawer(false); setTabh(); requestAnimationFrame(() => { draw(); spyKey = null; spy(); }); });

  // ---------------------------------------------------------------- the rules: view, details, wires
  const doc = document.getElementById('doc');
  const viewButtons = doc.querySelectorAll('.toolbar [data-view]');
  const annot = document.getElementById('annot');
  function setView(v) {
    doc.dataset.view = v;
    viewButtons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.view === v)));
    if (v === 'rules' && !annot.checked) { annot.checked = true; doc.classList.add('annotated'); }
    requestAnimationFrame(() => { draw(); spyKey = null; spy(); });
  }
  viewButtons.forEach(b => b.addEventListener('click', () => setView(b.dataset.view)));
  annot.addEventListener('change', () => { doc.classList.toggle('annotated', annot.checked); requestAnimationFrame(draw); });

  const align = document.getElementById('align');
  const wires = align.querySelector('.wires');
  const colL = align.querySelector('.col-orig');
  const colR = align.querySelector('.col-rules');
  function draw() {
    if (!align.offsetWidth || doc.dataset.view !== 'side') { wires.innerHTML = ''; return; }
    const box = align.getBoundingClientRect();
    const xL = colL.getBoundingClientRect().right - box.left + 6;
    const xR = colR.getBoundingClientRect().left - box.left - 6;
    const xm = (xL + xR) / 2;
    wires.setAttribute('viewBox', '0 0 ' + box.width + ' ' + box.height);
    wires.setAttribute('width', box.width);
    wires.setAttribute('height', box.height);
    let s = '';
    colL.querySelectorAll('[data-m]').forEach(el => {
      const m = el.dataset.m;
      const a = el.getClientRects()[0] || el.getBoundingClientRect();
      const y0 = ((a.top + a.bottom) / 2 - box.top).toFixed(1);
      colR.querySelectorAll('.tgt[data-ms~="' + m + '"]').forEach(t => {
        const b = t.getBoundingClientRect();
        const y1 = (b.top + Math.min(b.height / 2, 11) - box.top).toFixed(1);
        const f = t.dataset.f || 'desc';
        s += '<path class="wire" data-f="' + f + '" data-m="' + m + '" d="M' + xL + ',' + y0 + ' C' + xm + ',' + y0 + ' ' + xm + ',' + y1 + ' ' + xR + ',' + y1 + '" stroke-width="1.8"/>' +
             '<circle class="end" data-f="' + f + '" data-m="' + m + '" cx="' + xL + '" cy="' + y0 + '" r="2.5"/>' +
             '<circle class="end" data-f="' + f + '" data-m="' + m + '" cx="' + xR + '" cy="' + y1 + '" r="2.5"/>';
      });
    });
    wires.innerHTML = s;
  }
  new ResizeObserver(() => requestAnimationFrame(draw)).observe(align);
  // the handbook's typeface loads only when its text is first shown, and the text then wraps differently; so can a picture
  if (document.fonts) { document.fonts.ready.then(draw); document.fonts.addEventListener('loadingdone', () => requestAnimationFrame(draw)); }
  align.addEventListener('load', () => requestAnimationFrame(draw), true);
  window.addEventListener('load', draw);

  // where am I: the section under the toolbar, shown in the toolbar and under the open page in the panel
  const toolbar = doc.querySelector('.toolbar');
  const crumb = doc.querySelector('.crumb');
  const toc = nav.querySelector('.nv-doc');
  const setTb = () => doc.style.setProperty('--tb', toolbar.offsetHeight + 'px');
  new ResizeObserver(setTb).observe(toolbar);
  setTb();
  const heads = [...colR.querySelectorAll('[data-sec]')];
  let spyKey = null;
  // a place reached by a link or from the panel stays marked while it is in sight, even before the reading line gets there:
  // a rule shown mid-screen, a section near the end, or one of two sections side by side in the vague wording
  let pin = null;
  function pinned(links) {
    if (!pin || !links.includes(pin.a)) return null;
    const top = (page.dataset.tab === 'doc' ? toolbar : appbar).getBoundingClientRect().bottom;
    const r = pin.el.getBoundingClientRect();
    const seen = r.bottom > Math.max(top, 0) + 8 && r.top < innerHeight - 8;
    if (seen) pin.reached = true;
    if (seen || (!pin.reached && performance.now() - pin.t0 < 1500)) return pin.a;
    pin = null;
    return null;
  }
  function spy() {
    if (page.dataset.tab === 'register' || page.dataset.tab === 'census') { spyList(page.dataset.tab); return; }
    if (page.dataset.tab !== 'doc') return;
    const lim = toolbar.getBoundingClientRect().bottom + 28;
    const p = pinned([...toc.querySelectorAll('a')]);
    const upTo = p && pin.head;
    const cur = [null, null, null];
    for (const h of heads) {
      if (!upTo && h.getBoundingClientRect().top > lim) break;
      const lv = +h.dataset.lv;
      cur[lv - 1] = h;
      for (let i = lv; i < 3; i++) cur[i] = null;
      if (h === upTo) break;
    }
    const chain = cur.filter(Boolean);
    const key = chain.map(h => h.dataset.sec).join('|');
    if (key === spyKey) return;
    spyKey = key;
    // on a phone the part is dropped when a group and situation are both shown (.c-top)
    crumb.innerHTML = chain.map((h, i) => {
      const t = h.querySelector('.ttl');
      const num = h.dataset.sec === 'x' ? '×' : h.dataset.sec;
      const top = chain.length === 3 && i < 2 ? ' c-top' : '';
      return (i ? '<span class="sep' + (i === 1 ? top : '') + '" aria-hidden="true">›</span>' : '') +
        '<a class="ci' + (i === 0 ? top : '') + '" href="#sec-' + h.dataset.sec + '"><span class="num">' + num + '</span><span class="t">' + (t ? t.innerHTML : '') + '</span></a>';
    }).join('');
    toc.querySelectorAll('[aria-current]').forEach(a => a.removeAttribute('aria-current'));
    const a = chain.map(h => tocLink(h.dataset.sec)).filter(Boolean).pop();
    if (!a) return;
    a.setAttribute('aria-current', 'true');
    keepInView(a);
  }
  // the vague wording and the census: the last section whose heading has passed the top (at the very end, the last one in sight)
  function spyList(tab) {
    const links = [...nav.querySelectorAll('.nv-i[data-for="' + tab + '"] .nv-sub a')];
    const lim = Math.max(appbar.getBoundingClientRect().bottom, 0) + 96;
    const end = innerHeight + scrollY >= document.documentElement.scrollHeight - 4;
    let cur = pinned(links), best = -Infinity;
    if (!cur) links.forEach(a => {
      const t = document.getElementById(a.getAttribute('href').slice(1));
      const top = t ? t.getBoundingClientRect().top : Infinity;
      if ((top <= lim || (end && top < innerHeight)) && top > best) { best = top; cur = a; }
    });
    const key = tab + (cur ? cur.getAttribute('href') : '');
    if (key === spyKey) return;
    spyKey = key;
    links.forEach(a => { if (a === cur) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    keepInView(cur);
  }
  let spyQueued = false;
  window.addEventListener('scroll', () => {
    if (spyQueued) return;
    spyQueued = true;
    requestAnimationFrame(() => { spyQueued = false; spy(); });
  }, { passive: true });

  function highlight(mids) {
    align.classList.add('focus');
    align.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
    mids.forEach(m => {
      align.querySelectorAll('[data-m="' + m + '"]').forEach(x => x.classList.add('hl'));
      align.querySelectorAll('.tgt[data-ms~="' + m + '"]').forEach(x => x.classList.add('hl'));
    });
  }
  function clearHl() {
    align.classList.remove('focus');
    align.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
  }
  // after a jump the page moves under a pointer that has not moved: the jump stays lit until the pointer itself moves
  let px = NaN, py = NaN, hold = null;
  const held = e => hold && Math.abs(e.clientX - hold.x) + Math.abs(e.clientY - hold.y) < 6;
  addEventListener('pointermove', e => { px = e.clientX; py = e.clientY; }, { passive: true });
  addEventListener('pointerdown', e => { px = e.clientX; py = e.clientY; }, { passive: true });
  function onHover(e) {
    if (doc.dataset.view !== 'side') return;
    if (e.type !== 'focusin') { if (held(e)) return; hold = null; }
    const tgt = e.target.closest('.tgt');
    if (tgt && colR.contains(tgt)) { highlight(tgt.dataset.ms.split(' ')); return; }
    const st = e.target.closest('[data-all]');
    if (st && colR.contains(st)) { highlight(st.dataset.all.split(' ')); return; }
    const el = e.target.closest('[data-m]');
    if (el && colL.contains(el)) { highlight([el.dataset.m]); return; }
    clearHl();
  }
  align.addEventListener('pointerover', onHover);
  align.addEventListener('focusin', onHover);
  align.addEventListener('pointerleave', e => { if (held(e)) return; hold = null; clearHl(); });

  // side by side: a click on a passage brings its rules to the same height on screen, a click on a rule its passages
  const alignScroll = align.parentElement;
  function across(el) {
    let from, set, targets;
    if (colL.contains(el)) {
      from = el.closest('[data-m]');
      if (!from) return false;
      set = [from.dataset.m];
      targets = [...colR.querySelectorAll('.tgt[data-ms~="' + from.dataset.m + '"]')];
    } else {
      // the passages behind the line or step clicked, else behind the whole statement
      from = el.closest('.tgt') || el.closest('.stmt');
      if (!from || !colR.contains(from)) return false;
      const st = from.closest('.stmt');
      set = (from.dataset.ms || '').split(' ').filter(Boolean);
      if (!set.length && st) set = (st.dataset.all || '').split(' ').filter(Boolean);
      targets = set.map(m => colL.querySelector('[data-m="' + m + '"]')).filter(Boolean)
        .sort((x, y) => (x.compareDocumentPosition(y) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1));
    }
    if (!targets.length) return false;
    const top = toolbar.getBoundingClientRect().bottom + 12, bottom = innerHeight - 16;
    const first = targets[0].getBoundingClientRect(), last = targets[targets.length - 1].getBoundingClientRect();
    if (first.top < top || last.bottom > bottom) {
      // the first one lands where the click was; the rest come along while they fit
      let dy = first.top - Math.max(from.getBoundingClientRect().top, top);
      const over = last.bottom - dy - bottom;
      if (over > 0) dy = Math.min(dy + over, first.top - top);
      window.scrollBy({ top: dy, behavior: behavior() });
    }
    // and sideways, when the two columns are wider than the screen
    const sr = alignScroll.getBoundingClientRect();
    if (first.left < sr.left || first.right > sr.right) alignScroll.scrollTo({ left: alignScroll.scrollLeft + first.left - sr.left - 16, behavior: behavior() });
    flash(targets);
    hold = { x: px, y: py };
    focusOn(targets[0]);
    highlight(set);
    if (colR.contains(targets[0])) pinTo(targets[0]);
    return true;
  }
  align.addEventListener('keydown', e => {
    if (e.key !== 'Enter' || doc.dataset.view !== 'side' || e.target.closest('a, button, input, label, summary, .ann')) return;
    if (across(e.target)) e.preventDefault();
  });

  // ---------------------------------------------------------------- links: open the page that holds the target
  // one place lit at a time (with reduced motion the mark stays until the next one)
  function flash(els) {
    page.querySelectorAll('.flash').forEach(x => x.classList.remove('flash'));
    void page.offsetWidth;
    els.forEach(x => x.classList.add('flash'));
  }
  function reveal(el, instant) {
    el.scrollIntoView({ behavior: instant ? 'auto' : behavior(), block: 'center' });
    flash([el]);
  }
  function focusOn(t) {
    if (!t.matches('a, button, [tabindex]')) t.setAttribute('tabindex', '-1');
    t.focus({ preventScroll: true });
  }
  function place(t, instant, flash) {
    if (t.matches('.panel, .lx')) window.scrollTo(0, 0);
    else if (t.classList.contains('stmt') && flash) reveal(t, instant);
    else t.scrollIntoView({ behavior: instant ? 'auto' : behavior(), block: t.classList.contains('stmt') ? 'center' : 'start' });
  }
  // refocus: the link that was clicked is hidden now (the closed drawer); instant: a jump from the panel or a link into the page
  function go(t, refocus, instant) {
    const panel = t.closest('.panel'), part = t.closest('.lx');
    const moved = panel ? setPage(panel.id, part && part.id) : false;
    place(t, moved || instant, true);
    // a link on another page is hidden now too: move focus to where it led
    if (moved || refocus) focusOn(t);
    pinTo(t);
  }
  // the panel's entry for a heading of the rules, or for the group or part around it (the panel lists parts and groups)
  function tocLink(sec) {
    for (let s = sec; s; s = s.split('.').slice(0, -1).join('.')) {
      const a = toc.querySelector('a[data-sec="' + s + '"]');
      if (a) return a;
    }
    return null;
  }
  // mark it in the panel: the section itself, or for a rule, the group it sits in
  function pinTo(t) {
    let a = t.id && nav.querySelector('.nv-sub a[href="#' + t.id + '"]'), head = null;
    if (colR.contains(t)) {
      head = t.dataset.sec ? t : heads.filter(x => x.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_FOLLOWING).pop();
      if (!a && head) a = tocLink(head.dataset.sec);
    }
    pin = a ? { a, el: t, head, reached: false, t0: performance.now() } : null;
    requestAnimationFrame(() => { spyKey = null; spy(); });
  }
  document.addEventListener('click', e => {
    const jump = e.target.closest('[data-jump]');
    if (jump) {
      const m = jump.dataset.jump;
      setView('side');
      requestAnimationFrame(() => {
        const t = colL.querySelector('[data-m="' + m + '"]');
        if (t) { reveal(t); hold = { x: px, y: py }; highlight([m]); }
      });
      return;
    }
    const drawer = page.dataset.drawer === 'open';
    // a page in the panel
    const op = e.target.closest('[data-open-tab], [data-open-part]');
    if (op) {
      e.preventDefault();
      closeDrawer(false);
      const part = op.dataset.openPart, tab = part ? 'language' : op.dataset.openTab;
      if (here() === (part || tab)) window.scrollTo(0, 0); else openPage(tab, part);
      if (drawer) focusOn(document.getElementById(part || tab));
      return;
    }
    // in-page links never touch the address bar, which keeps the language link (#en, #zh) intact
    const a = e.target.closest('a[href^="#"]');
    if (!a) {
      // a passage or a rule, side by side; not while selecting text, and not on the details, links or buttons
      if (doc.dataset.view === 'side' && align.contains(e.target) && !e.defaultPrevented && !(e.metaKey || e.ctrlKey || e.shiftKey || e.altKey)
          && !e.target.closest('a, button, input, label, summary, .ann') && !String(getSelection())) across(e.target);
      return;
    }
    const t = document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
    if (!t) return;
    e.preventDefault();
    closeDrawer(false);
    go(t, drawer && nav.contains(a), nav.contains(a));
  });

  setLang(page.dataset.lang);
  setPage(page.dataset.tab, page.dataset.part);
  // a phone is too narrow for two columns joined by lines, so the rules open on their own, with sources
  if (matchMedia('(max-width: 700px)').matches) setView('rules');
  // a link to a part of the page (#register, #r-3.4.4b, …) opens it, on arrival or when the address changes
  addEventListener('hashchange', () => {
    const k = decodeURIComponent(location.hash.slice(1));
    if (k === 'zh' || k === 'en') { setLang(k); return; }
    const t = k && document.getElementById(k);
    if (t) go(t, false, true);
  });
  const h = decodeURIComponent(location.hash.slice(1));
  const target = h && h !== 'zh' && h !== 'en' && document.getElementById(h);
  if (target) {
    requestAnimationFrame(() => go(target, false, true));
    // web fonts and pictures arriving later shift the page: place it once more after loading, unless the reader has moved on
    let touched = false;
    ['wheel', 'touchstart', 'keydown', 'pointerdown'].forEach(ev => addEventListener(ev, () => { touched = true; }, { once: true, passive: true }));
    addEventListener('load', () => (document.fonts ? document.fonts.ready : Promise.resolve())
      .then(() => requestAnimationFrame(() => { if (!touched) { place(target, true, false); pinTo(target); } })), { once: true });
  }
})();
