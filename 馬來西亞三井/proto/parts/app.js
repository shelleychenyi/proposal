/* ================= Interactive app mode ================= */
(function () {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  document.documentElement.classList.add('app');
  const dev = $('#device');
  function fit() {
    if (innerWidth <= 500) { dev.style.transform = 'none'; return; }
    const s = Math.min((innerHeight - 60) / 844, (innerWidth - 60) / 390, 1.15);
    dev.style.transform = `scale(${s})`;
  }
  addEventListener('resize', fit); fit();

  // ---------- state ----------
  let pts = 1884, streak = 5, mall = 'LaLaport BBCC', rtPosts = 0, spun = false;
  const stack = [];
  let cur = null;
  const enter = {};

  function go(id, push = true) {
    const nx = document.getElementById(id); if (!nx) return;
    if (cur && push && cur !== id) stack.push(cur);
    $$('.screen.on').forEach(e => e.classList.remove('on'));
    nx.classList.add('on'); nx.scrollTop = 0; $$('.scroll', nx).forEach(e => e.scrollTop = 0);
    cur = id;
    if (enter[id]) enter[id]();
  }
  function back() { const p = stack.pop(); go(p || 'home', false); }
  let tt;
  function toast(msg) { const t = $('#tst'); t.textContent = msg; t.classList.add('on'); clearTimeout(tt); tt = setTimeout(() => t.classList.remove('on'), 2200); }
  function sheet(html) { $('#ovBody').innerHTML = html; $('#ov').classList.add('open'); }
  function closeSheet() { $('#ov').classList.remove('open'); }
  function setPts(d) {
    pts += d;
    const n = pts.toLocaleString();
    const p = $('#home .tier .pts'); if (p) p.firstChild.textContent = n;
    $$('#me .score').forEach(e => e.textContent = n + ' MSP pts');
    const m = $('#home .tier .meta span'); if (m) m.innerHTML = `${Math.max(0, 2500 - pts)} pts to <b>SENPAI</b> 🔥`;
    const bar = $('#home .tier .bar'); if (bar) bar.style.setProperty('--w', Math.min(100, (pts - 1500) / 1000 * 100 + 37) + '%');
  }
  function qrHTML(n = 25, seed = 7) {
    let h = '', x = seed;
    const finder = (r, c) => { for (const [R, C] of [[0, 0], [0, n - 7], [n - 7, 0]]) { const a = r - R, b = c - C; if (a >= 0 && a < 7 && b >= 0 && b < 7) return (a === 0 || a === 6 || b === 0 || b === 6 || (a > 1 && a < 5 && b > 1 && b < 5)) ? 1 : 0; } return -1; };
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
      let f = finder(r, c); if (f < 0) { x = (x * 9301 + 49297) % 233280; f = x / 233280 > .52 ? 1 : 0; }
      h += `<i style="background:${f ? '#16202E' : '#fff'}"></i>`;
    }
    return h;
  }
  $('#miniqr').innerHTML = qrHTML();

  // ---------- data ----------
  const BR = {
    akiba: {name: 'Akiba Ramen', img: '../assets/app/ramen.jpg', tags: ['📍 L4-FC-14', '🕌 Muslim-friendly', '💸 RM9.90+'], score: 4.8, p: 92, n: 128,
      sum: 'People rave about the creamy chicken broth and the price. Some say it gets busy at lunch.',
      chips: ['🍜 Creamy paitan', '💸 Value for money', '🍤 Mix & match tempura', '✅ No pork, no lard'],
      web: [['IG', '@yuumi_kato', 'Aug 2026 · 629 ❤', '"Found a hidden ramen gem in KL 🍜✨ seriously satisfying, from only RM9.90!"'],
            ['@', 'Threads user', 'Aug 2026', '"Congrats on the opening! No pork, no lard, Muslim friendly 🙌"']],
      rt: [['rookie', 'Aina R.', 'Rookie', 5, 'Sedap gila! Broth very creamy, portion big for the price.', ['🤤 Sedap gila', '💸 Worth it']],
           ['senpai', 'Marcus L.', 'Senpai', 4, 'Came after ACG Base. Queue 10 min at 1pm but moves fast.', ['⏳ Long queue', '✅ Halal-friendly']]]},
    doko: {name: 'Doko Koko Café', img: '../assets/app/collabcafe.jpg', tags: ['📍 L1', '🎌 Collab café', '🛍️ Merch corner'], score: 4.7, p: 90, n: 98,
      sum: 'Fans love the themed menus and the huge merch section. Weekends get packed, so book ahead.',
      chips: ['🎀 Themed menus', '🛍️ Huge merch', '📸 IG-worthy', '⏳ Weekend queue'],
      web: [['IG', '@fayejimeno', 'Aug 2026 · 4,585 ❤', '"The food was so well themed! Don\'t forget the huge merch section 🩵"'],
            ['IG', '@yushirocos', 'Oct 2026', '"The sukiyaki soup is so goooood!!"']],
      rt: [['explorer', 'Hui Min', 'Explorer', 5, 'Collab menu so cute, got the limited coaster. Will come back next collab!', ['📸 IG-worthy', '🤤 Sedap gila']]]},
    animate: {name: 'Animate Café', img: '../assets/app/acg_event.jpg', tags: ['📍 L2 · ACG Base', '🇯🇵 Malaysia\'s first', '🎌 Collab menus'], score: 4.6, p: 89, n: 57,
      sum: 'Malaysia\'s first official Animate Café. Fans enjoy the rotating collabs and the comfort food.',
      chips: ['🎌 Rotating collabs', '🍙 Comfort food', '🎁 Free coasters', '👀 Anime heaven'],
      web: [['IG', '@mijuyq', 'Jul 2026 · 492 ❤', '"This mall is secretly heaven for anime fans 👀"']],
      rt: []},
    ngam: {name: 'Ngam Ngam Neighbourhood', img: null, emoji: '🧸', tags: ['📍 L2-59', '👨‍👩‍👧 Family', '🥗 Healthy bowls'], score: 4.6, p: 94, n: 24,
      sum: 'Parents love that the play area is right next to the tables. Kids meals from RM10.90.',
      chips: ['🛝 Play area', '👶 Kids meals RM10.90', '🥗 Healthy bowls', '📚 Reading corner'],
      web: [['IG', '@mymamapicks', 'Sep 2026 · 165 ❤', '"Loved how the play area is RIGHT by the tables 🤎"']],
      rt: []}
  };
  let brandKey = 'akiba', brandTab = 'web';
  function renderBrand() {
    const b = BR[brandKey];
    const hero = $('#brand .bhero');
    hero.querySelector('img').style.display = b.img ? 'block' : 'none';
    if (b.img) hero.querySelector('img').src = b.img;
    hero.style.background = b.img ? '' : 'linear-gradient(135deg,#E7F8F3,#FFF1DD)';
    let em = hero.querySelector('.bigem'); if (!em) { em = document.createElement('div'); em.className = 'bigem'; em.style.cssText = 'position:absolute;inset:0;display:grid;place-items:center;font-size:110px'; hero.appendChild(em); }
    em.textContent = b.img ? '' : b.emoji;
    const list = brandTab === 'web'
      ? b.web.map(w => `<div class="post"><div class="who"><i style="background:${w[0] === 'IG' ? 'linear-gradient(135deg,#F58529,#DD2A7B)' : '#111'}">${w[0]}</i>${w[1]} <em>${w[2]}</em></div><p>${w[3]}</p><div class="st">Source: public post · curated by Pandora AI</div></div>`).join('')
      : (b.rt.length ? b.rt.map(r => `<div class="rtp"><div class="who"><img src="../assets/app/char_${r[0]}.png">${r[1]} <span class="vb">Verified ✓</span><em>${r[2]}</em></div><div class="lan">${'🏮'.repeat(r[3])}</div><p>${r[4]}</p><div class="tg">${r[5].map(t => `<span>${t}</span>`).join('')}</div></div>`).join('')
        : `<div class="post" style="text-align:center;color:var(--mid)">No Real Talk yet. Be the first! ✍️</div>`);
    $('#brand .bcard').innerHTML = `<h2>${b.name}</h2><div class="tags">${b.tags.map(t => `<span>${t}</span>`).join('')}</div>
      <div class="meter"><div class="ring" style="--p:${b.p}%"><div>${b.score}</div></div><div class="r"><b>${b.p}% love it · ${b.n} posts</b><p>✨ AI summary: ${b.sum}</p></div></div>
      <div class="love-chips">${b.chips.map((c, i) => `<span style="animation-delay:${.3 + i * .15}s">${c}</span>`).join('')}</div>
      <div class="tabs"><span class="${brandTab === 'web' ? 'on' : ''}" data-act="btab" data-t="web">🌐 Web Buzz</span><span class="${brandTab === 'rt' ? 'on' : ''}" data-act="btab" data-t="rt">🗣️ Real Talk (${b.rt.length})</span></div>${list}`;
  }
  function openBrand(k) { brandKey = k; brandTab = 'web'; go('brand'); }
  enter.brand = renderBrand;

  // ---------- wire existing markup ----------
  const navMap = {Home: 'home', Quest: 'quest', Scan: 'scan', Buzz: 'buzz', Me: 'me'};
  $$('.nav > div').forEach(d => { const t = d.textContent.trim().split(/\s+/).pop(); if (navMap[t]) d.dataset.go = navMap[t]; });
  $$('.back').forEach(b => b.dataset.act = 'back');
  $('#home .mall').dataset.act = 'mall';
  $$('#home .icons div')[0].dataset.go = 'notif';
  $$('#home .icons div')[1].dataset.act = 'qr';
  $('#home .tier').dataset.go = 'tiers';
  $('#home .d.today').dataset.act = 'checkin';
  ['scan', 'ask', 'capsule', 'parking'].forEach((g, i) => $$('#home .q')[i].dataset.go = g);
  $$('#home .qc').forEach(e => e.dataset.go = 'quest');
  $$('#home .bz').forEach((e, i) => { e.dataset.act = 'brand'; e.dataset.k = ['akiba', 'doko'][i]; });
  // more home sections
  const homeMore = `<div class="home-more"><div class="sec"><b>Vouchers for you 🎟️</b><a data-go="me">My wallet</a></div>
    <div class="hs">${[['#E84C7A', 'RM20 OFF', 'Sasa · min RM100'], ['#2B67B0', 'RM10 OFF', 'ACG Chapter'], ['#C8102E', '5% OFF', 'Kickers · MSP Special']].map(v =>
      `<div class="vch" style="min-width:250px;margin:0" data-act="collectv" data-v="${v[1]} · ${v[2]}"><div class="l" style="background:${v[0]};width:84px">${v[1].replace(' ', '<br>')}</div><div class="r"><b>${v[2]}</b><span>Tap to collect · free</span></div></div>`).join('')}</div>
    <div class="sec"><b>Happening at LaLaport 🎉</b><a data-go="notif">All</a></div>
    <div class="hs"><div class="ev" data-go="quest"><img src="../assets/app/acg_event.jpg"><div><b>ACG Matsuri · 7–9 Nov</b><span>Stamp Rally · +300 XP</span></div></div>
    <div class="ev" data-act="brand" data-k="doko"><img src="../assets/app/collabcafe.jpg"><div><b>Doko Koko × NIKKE</b><span>Collab café · till 9 Nov</span></div></div>
    <div class="ev" data-go="parking"><img src="../assets/app/ramen.jpg"><div><b>MSP Member Free Parking</b><span>Explorer 4H · till 31 Dec</span></div></div></div></div>`;
  const spacer = $('#homeInner > div:last-child'); spacer.insertAdjacentHTML('beforebegin', homeMore); spacer.style.height = '110px';
  // tiers
  $('#tiers .btn.blue').dataset.go = 'levelup';
  $('#tiers .btn.blue').textContent = 'Preview: what Senpai unlocks →';
  $$('#tiers .tc').forEach(c => c.dataset.act = 'tiercard');
  // quest
  const qis = $$('#quest .qi');
  qis[0].dataset.act = 'brand'; qis[0].dataset.k = 'akiba';
  qis[1].dataset.act = 'stamp';
  qis[2].dataset.act = 'squad';
  $('#quest .banner').dataset.go = 'capsule';
  // capsule
  $$('#capsule .btn')[0].dataset.act = 'spin';
  $$('#capsule .btn')[1].dataset.act = 'spin50';
  $('#capsule .reveal').dataset.act = 'closereveal';
  $('#capsule .sec a').dataset.act = 'toast'; $('#capsule .sec a').dataset.msg = '🔁 Share a trade link with your kawan';
  // scan
  $('#scan .sheet .btn').dataset.act = 'scandone';
  // ask
  $$('#ask .sugg span').forEach(s => s.dataset.act = 'ask');
  $('#ask .input').innerHTML = '<input id="askIn" placeholder="Ask anything, lah…"><div class="mic" data-act="asksend">➤</div>';
  $('#askIn').addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); askSend(); } });
  // buzz
  $$('#buzz .seg span').forEach(s => s.dataset.act = 'seg');
  $('#buzz .hero').dataset.act = 'brand'; $('#buzz .hero').dataset.k = 'animate';
  $$('#buzz .bi').forEach((e, i) => { e.dataset.act = 'brand'; e.dataset.k = ['akiba', 'doko', 'animate', 'ngam'][i]; });
  // brand
  const tb = $$('#brand .topb div'); tb[0].dataset.act = 'back'; tb[1].dataset.act = 'fav';
  $('#brand .cta .btn.ghost').dataset.act = 'route';
  $$('#brand .cta .btn')[1].dataset.go = 'realtalk';
  // real talk
  $$('#rate span').forEach((s, i) => { s.dataset.act = 'rate'; s.dataset.i = i; });
  $$('#stick span').forEach(s => s.dataset.act = 'vibe');
  $('#realtalk .ta').setAttribute('contenteditable', 'true');
  $('#realtalk .btn').dataset.act = 'post';
  // level up
  $('#levelup .unl').insertAdjacentHTML('afterend', '<div class="pad" style="margin-top:22px"><div class="btn" data-act="lvdone">Shiok! Let\'s go 🎉</div></div>');

  // ---------- enter hooks ----------
  enter.capsule = () => { $('#gacha').classList.remove('shake', 'turn'); $('#capsule').classList.remove('go'); spun = false; };
  enter.scan = () => {
    const c = $('#coins'), sc = $('#scan'); c.innerHTML = ''; sc.classList.remove('fly');
    for (let i = 0; i < 10; i++) { const e = document.createElement('div'); e.className = 'coin'; e.textContent = '★'; e.style.left = (150 + Math.random() * 80) + 'px'; e.style.top = (580 + Math.random() * 40) + 'px'; e.style.setProperty('--dx', (-80 - Math.random() * 60) + 'px'); e.style.setProperty('--dy', (-560 - Math.random() * 40) + 'px'); e.style.animationDelay = (3.6 + i * .07) + 's'; c.appendChild(e); }
    void sc.offsetWidth; sc.classList.add('fly');
  };
  enter.realtalk = () => {
    $('#realtalk .hdr h2').textContent = 'Real Talk · ' + BR[brandKey].name.replace(' Neighbourhood', '');
    $$('#rate span').forEach(s => s.classList.remove('on')); $$('#stick span').forEach(s => s.classList.remove('on'));
    const ta = $('#realtalk .ta'); ta.dataset.ph = '1'; ta.innerHTML = '<span id="typed" style="color:#9AA4B2">Tap to write… e.g. "Broth damn creamy, can come back lah!"</span>';
    $('#toast').style.opacity = 0;
  };
  $('#realtalk .ta').addEventListener('focus', e => { const t = e.target; if (t.dataset.ph) { t.innerHTML = ''; delete t.dataset.ph; } });
  enter.levelup = () => {
    const cf = $('#confetti'); cf.innerHTML = '';
    const cs = ['#FFD978', '#FF6FA3', '#22C2A0', '#F39A1E', '#8CC8F5', '#fff'];
    for (let i = 0; i < 70; i++) { const e = document.createElement('div'); e.className = 'conf'; e.style.left = Math.random() * 390 + 'px'; e.style.background = cs[i % 6]; e.style.animationDuration = (2.5 + Math.random() * 2.5) + 's'; e.style.animationDelay = (.8 + Math.random() * 2) + 's'; e.style.borderRadius = i % 3 ? '2px' : '50%'; cf.appendChild(e); }
  };
  enter.me = () => { $('#meMall').textContent = mall; $('#rtCount').textContent = rtPosts + (rtPosts === 1 ? ' post' : ' posts'); };

  // ---------- ask ----------
  const REPLY = {
    plan: `Shiok, here's your Saturday 🗓️<br><b>11:00</b> Animate Café · ACG stamp 🎐<br><b>13:00</b> Akiba Ramen · makan quest 🍜<br><b>15:00</b> Doko Koko collab café 🎀<br><b>17:00</b> Free capsule spin 🎰<br>Want me to add these to your Quest?`,
    kpop: `Ada! 🎤 <b>GSC LaLaport BBCC</b> has a K-pop live viewing tonight at 8pm. Grab the exclusive wristband with your ticket. Senpai & Legend get priority seats 😉`,
    exit: `Nearest exit is <b>P2 · Jalan Hang Tuah</b>, about 3 min walk. Your <b>4H free parking</b> is active, 2h 31m left 🅿️`,
    any: `Got it! Here's what's trending on LaLa Buzz that matches 👇`
  };
  function chatPush(html, cls, delay = 0) {
    const c = $('#chat'); const e = document.createElement('div'); e.className = cls; e.style.animationDelay = delay + 's'; e.innerHTML = html; c.appendChild(e);
    setTimeout(() => c.scrollTo({top: c.scrollHeight, behavior: 'smooth'}), delay * 1000 + 60);
    return e;
  }
  function askSend(text) {
    const inp = $('#askIn'); text = text || inp.value.trim(); if (!text) return; inp.value = '';
    chatPush(text, 'msg me');
    const ty = chatPush('<i></i><i></i><i></i>', 'typing');
    const k = /saturday|plan/i.test(text) ? 'plan' : /k-?pop|event|concert/i.test(text) ? 'kpop' : /exit|park/i.test(text) ? 'exit' : 'any';
    setTimeout(() => { ty.remove(); chatPush(REPLY[k], 'msg ai');
      if (k === 'any') { const p = chatPush(`<img src="../assets/app/ramen.jpg"><div><b>Akiba Ramen</b><span>From RM9.90 · ★4.8 Buzz · 2 min</span></div><div class="go">Go</div>`, 'pick', .3); p.dataset.act = 'brand'; p.dataset.k = 'akiba'; }
      if (k === 'plan') { const p = chatPush(`<div style="font-weight:800;color:var(--blue)">➕ Add 4 stops to Quest</div>`, 'pick', .3); p.dataset.act = 'addplan'; }
    }, 1100);
  }
  $$('#ask .pick').forEach(p => { p.dataset.act = 'brand'; p.dataset.k = 'akiba'; });

  // ---------- capsule ----------
  function spin(cost) {
    if (spun) return;
    if (cost) { if (pts < 50) return toast('Not enough pts lah 😅'); setPts(-50); }
    spun = true;
    const g = $('#gacha'), sc = $('#capsule');
    g.classList.remove('shake', 'turn'); sc.classList.remove('go'); void g.offsetWidth;
    g.classList.add('shake', 'turn'); sc.classList.add('go');
  }

  // ---------- click router ----------
  document.addEventListener('click', e => {
    const g = e.target.closest('[data-go]'), a = e.target.closest('[data-act]');
    const t = a && g ? (a.contains(g) ? g : a) : (a || g);
    if (!t) return;
    if (t === g) return go(g.dataset.go);
    return act(a, e);
  });
  function act(el, e) {
    const k = el.dataset.act;
    switch (k) {
      case 'back': return back();
      case 'close': return closeSheet();
      case 'toast': return toast(el.dataset.msg);
      case 'brand': return openBrand(el.dataset.k);
      case 'btab': brandTab = el.dataset.t; return renderBrand();
      case 'fav': el.textContent = el.textContent === '♡' ? '♥' : '♡'; el.style.color = el.textContent === '♥' ? '#FF6F61' : ''; return toast(el.textContent === '♥' ? '♥ Saved to favourites' : 'Removed from favourites');
      case 'route': return toast('🧭 ' + BR[brandKey].name + ': ' + (BR[brandKey].tags[0].replace('📍 ', '')) + ' · 2 min walk');
      case 'mall': {
        const ms = [['LaLaport BBCC', '#2B67B0', 'Bukit Bintang City Centre'], ['Mitsui Outlet Park BBCC', '#F39A1E', 'Bukit Bintang City Centre'], ['Mitsui Outlet Park KLIA Sepang', '#F39A1E', 'Near KLIA · Tourist Privilege Pass']];
        return sheet(`<h3>Switch mall</h3>${ms.map(m => `<div class="opt ${m[0] === mall ? 'sel' : ''}" data-act="setmall" data-m="${m[0]}" data-c="${m[1]}"><i style="background:${m[1]}"></i><div>${m[0]}<small>${m[2]}</small></div></div>`).join('')}<div class="qrcap">Your level & points work in all 3 malls ✨</div>`);
      }
      case 'setmall': mall = el.dataset.m; $('#home .mall').innerHTML = `<i style="background:${el.dataset.c}"></i>${mall.replace('Mitsui Outlet Park', 'MOP')} ▾`; closeSheet(); return toast('📍 Switched to ' + mall);
      case 'qr': return sheet(`<h3>My Member QR</h3><div class="qrbox">${qrHTML(25, 11)}</div><div class="qrcap">${el.dataset.cap || 'Explorer · 1.2x points · show at counter'}</div><div class="btn" style="margin-top:14px" data-act="close">Done</div>`);
      case 'usev': return sheet(`<h3>${el.dataset.v}</h3><div class="qrbox">${qrHTML(25, 3)}</div><div class="qrcap">Show this to the cashier · valid 10 min</div><div class="btn" style="margin-top:14px" data-act="close">Done</div>`);
      case 'collectv': el.querySelector('.r span').textContent = '✓ Collected to My Vouchers'; return toast('🎟️ ' + el.dataset.v + ' collected');
      case 'collect': return toast('🎟️ 3 more vouchers on the Home page');
      case 'vouchers': return $('#vouchers').scrollIntoView({behavior: 'smooth'});
      case 'checkin': { if (el.dataset.done) return; el.dataset.done = 1; el.querySelector('b').textContent = '✓'; el.classList.remove('today'); el.classList.add('ok'); streak++; $('#home .streak .hd').firstChild.textContent = `🔥 ${streak}-day check-in streak `; setPts(10); return toast('🔥 Checked in! +10 pts'); }
      case 'tiercard': return toast('🏅 ' + el.querySelector('.nm').textContent + ' · ' + (el.querySelector('.ml') ? el.querySelector('.ml').textContent : 'see perks table below'));
      case 'stamp': {
        const st = $$('#quest .stamp')[3]; if (st.classList.contains('got')) return toast('Already stamped ✓');
        st.classList.add('got'); el.classList.add('done'); el.querySelector('.x').textContent = '✓ +30';
        $('#quest .banner b').textContent = '4 / 5 stamps'; return toast('⛩️ Stamp collected! +30 XP');
      }
      case 'squad': return sheet(`<h3>Squad up with a kawan 👯</h3><div class="opt">💬 WhatsApp<small style="margin-left:auto">Most used in MY</small></div><div class="opt">📷 Instagram DM</div><div class="opt">🔗 Copy invite link</div><div class="qrcap">You both get +100 XP when they scan their first receipt</div>`);
      case 'spin': return spin(false);
      case 'spin50': return spin(true);
      case 'closereveal': {
        $('#capsule').classList.remove('go'); $('#gacha').classList.remove('shake', 'turn');
        const empty = $$('#capsule .coll div').find(d => !d.querySelector('img'));
        if (empty && !$('#capsule .coll img[src*=durian]')) { empty.innerHTML = '<img src="../assets/app/fig_durian.jpg">'; $('#capsule .sec b').textContent = 'My collection 7/24'; }
        spun = false; return toast('★ Durian-chan added to your collection');
      }
      case 'scandone': setPts(35); go('home', false); stack.length = 0; return toast('✓ +35 pts added · Makan Quest done');
      case 'ask': return askSend(el.textContent.replace(/^\S+\s/, ''));
      case 'asksend': return askSend();
      case 'addplan': el.innerHTML = '<div style="font-weight:800;color:var(--mint)">✓ Added to Quest</div>'; delete el.dataset.act; return toast('🗺️ 4 stops added to your Quest');
      case 'seg': $$('#buzz .seg span').forEach(s => s.classList.toggle('on', s === el)); return;
      case 'rate': { const i = +el.dataset.i; $$('#rate span').forEach((s, j) => s.classList.toggle('on', j <= i)); return; }
      case 'vibe': return el.classList.toggle('on');
      case 'post': {
        const ta = $('#realtalk .ta'); const txt = ta.dataset.ph ? 'Can come back lah! 👍' : (ta.innerText.trim() || 'Can come back lah! 👍');
        const stars = $$('#rate span.on').length || 5; const tags = $$('#stick span.on').map(s => s.textContent);
        BR[brandKey].rt.unshift(['explorer', 'Shu Hoong (you)', 'Explorer', stars, txt.replace(/</g, '&lt;'), tags.length ? tags : ['💸 Worth it']]);
        rtPosts++; setPts(20); brandTab = 'rt';
        const t = $('#toast'); t.style.transition = 'all .4s cubic-bezier(.3,1.5,.5,1)'; t.style.opacity = 1; t.style.transform = 'translate(-50%,0) scale(1)';
        return setTimeout(() => { t.style.opacity = 0; go('brand', false); }, 1300);
      }
      case 'lvdone': stack.length = 0; return go('home', false);
      case 'lang': $$('.lang span').forEach(s => s.classList.toggle('on', s === el)); return toast(el.textContent === 'BM' ? 'Bahasa Melayu dipilih ✓' : el.textContent === '中文' ? '已切換中文 ✓' : 'English selected ✓');
      case 'myrt': return rtPosts ? openBrand(brandKey) : toast('Scan a receipt, then share your first Real Talk ✍️');
      case 'help': return toast('💬 Ask LaLa can answer most questions 24/7');
      case 'settings': return toast('⚙️ Settings');
    }
  }
  // side jump links (desktop)
  $$('#side [data-j]').forEach(s => s.addEventListener('click', () => { stack.length = 0; const j = s.dataset.j; if (BR[j]) openBrand(j); else go(j); }));

  go('home', false);
})();
