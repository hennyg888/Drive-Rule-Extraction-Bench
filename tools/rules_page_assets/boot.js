
/* before the page is drawn: the language from the link (#en, #zh) or the reader's last choice, else English;
   the page last open in this browser tab; whether the navigation panel was hidden */
(() => {
  const p = document.currentScript.parentElement;
  const get = (s, k) => { try { return window[s].getItem(k); } catch (e) { return null; } };
  let l = location.hash.slice(1);
  if (l !== 'zh' && l !== 'en') l = get('localStorage', 'passing-rules:lang');
  p.dataset.lang = l === 'zh' ? 'zh' : 'en';
  const t = get('sessionStorage', 'passing-rules:tab'), s = get('sessionStorage', 'passing-rules:part');
  if (['overview', 'language', 'doc', 'register', 'census'].includes(t)) p.dataset.tab = t;
  if (/^l-(anatomy|types|grammar|modal|wording|flags)$/.test(s || '')) p.dataset.part = s;
  if (get('localStorage', 'passing-rules:nav') === 'hide') p.dataset.nav = 'hide';
})();
