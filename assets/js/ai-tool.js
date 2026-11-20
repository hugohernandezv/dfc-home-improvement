/* ------------------------------------------------------------------
   AI Kitchen Inspiration (ai-kitchen-inspiration.html)

   Ported from the Fox Remodeling / McManus tool. Same wizard, same prompt,
   same before/after slider. On DFC:
   - the image model is reached through /api/ai-preview (dfc-api on Railway,
     the key never reaches the browser);
   - the lead goes out through FormSubmit, the same path as the price
     estimator, so it lands in the same inbox (hugo@, cc admin@);
   - the design is parked on the server only when the visitor sends it, so
     the email can link to it.
   ------------------------------------------------------------------ */
(function () {
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  if (!$('#aipDrop')) return;

  const LEAD_ENDPOINT = 'https://formsubmit.co/ajax/hugo@dfchomeimprovement.com';
  const LEAD_CC = 'admin@dfchomeimprovement.com';
  const PHONE = '(703) 596-8375';

  const OPTIONS = {
    "Design style":   ["Transitional", "Modern Farmhouse", "Classic Traditional", "Contemporary", "Warm Minimal", "Coastal"],
    "Cabinets":       ["Shaker", "Flat Panel", "Raised Panel", "Glass Front", "Open Shelving", "Two Tone"],
    "Countertops":    ["Quartz", "Quartzite", "Granite", "Marble", "Butcher Block", "Solid Surface"],
    "Backsplash":     ["Subway Tile", "Full Slab", "Herringbone Tile", "Zellige Tile", "Mosaic Accent", "Natural Stone"],
    "Color palette":  ["Warm Neutrals", "Crisp White", "Cool Grays", "Deep and Moody", "Earthy and Natural", "Two Tone Contrast"],
    "Budget range":   ["Under $50k", "$50k to $75k", "$75k to $100k", "$100k to $150k", "$150k+", "Not sure yet"]
  };
  const ORDER = ["Design style", "Cabinets", "Countertops", "Backsplash", "Color palette", "Budget range"];
  // Budget stays a list even in Advanced: a free-text budget is not useful to anyone.
  const FREE_TEXT = ["Design style", "Cabinets", "Countertops", "Backsplash", "Color palette"];
  const HINT = {
    "Design style":  "e.g. warm transitional with brass accents",
    "Cabinets":      "e.g. inset shaker, painted sage",
    "Countertops":   "e.g. honed white quartzite, thick edge",
    "Backsplash":    "e.g. zellige tile up to the ceiling",
    "Color palette": "e.g. creamy whites with black accents"
  };

  const track = (name, params, fb) => { if (typeof window.dfcTrack === 'function') window.dfcTrack(name, params || {}, fb); };
  const answers = {};
  let advanced = false, b64 = null, mime = null, objURL = null, savedURL = '', lastImage = null;

  /* ---- steps ---- */
  function goStep(n) {
    $('.aip-main').dataset.step = n;
    $$('.aip-panel').forEach(p => p.classList.toggle('show', +p.dataset.panel === n));
    $$('.aip-step').forEach(s => {
      const i = +s.dataset.step;
      s.classList.toggle('active', i === n);
      s.classList.toggle('done', i < n);
    });
    $$('.aip-line').forEach(l => l.classList.toggle('fill', +l.dataset.line < n));
    const top = $('.aip-card').getBoundingClientRect().top + window.scrollY - 110;
    window.scrollTo({ top, behavior: 'smooth' });
  }

  /* ---- 1. the photo: downscaled in the browser before it is sent ---- */
  const drop = $('#aipDrop'), file = $('#aipFile');
  drop.addEventListener('click', () => file.click());
  drop.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); file.click(); } });
  $('#aipChange').addEventListener('click', e => { e.stopPropagation(); file.click(); });
  ['dragenter', 'dragover'].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.add('drag'); }));
  ['dragleave', 'drop'].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove('drag'); }));
  drop.addEventListener('drop', e => { if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]); });
  file.addEventListener('change', e => { if (e.target.files[0]) handleFile(e.target.files[0]); });

  function handleFile(f) {
    if (!f.type.startsWith('image/')) return;
    objURL = URL.createObjectURL(f);
    $('#aipPreviewImg').src = objURL;
    $('#aipPreview').classList.add('show');
    drop.style.display = 'none';
    $('#aipToStyle').disabled = true;
    const img = new Image();
    img.onload = () => {
      const max = 1600, scale = Math.min(1, max / Math.max(img.width, img.height));   // same as the iCreate kit
      const c = document.createElement('canvas');
      c.width = Math.round(img.width * scale);
      c.height = Math.round(img.height * scale);
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      b64 = c.toDataURL('image/jpeg', 0.86).split(',')[1];
      mime = 'image/jpeg';
      $('#aipToStyle').disabled = false;
    };
    // A format the canvas cannot decode (some HEICs) still has to work.
    img.onerror = () => {
      const r = new FileReader();
      r.onload = () => { b64 = r.result.split(',')[1]; mime = f.type; $('#aipToStyle').disabled = false; };
      r.readAsDataURL(f);
    };
    img.src = objURL;
    track('ai_photo_added', { tool: 'ai kitchen inspiration' });
  }
  $('#aipToStyle').addEventListener('click', () => goStep(2));
  $('#aipBack').addEventListener('click', () => goStep(1));

  /* ---- 2. the finishes ---- */
  const grid = $('#aipGrid');
  function renderFields() {
    grid.innerHTML = '';
    ORDER.forEach(key => {
      const asText = advanced && FREE_TEXT.includes(key);
      const field = document.createElement('div');
      field.className = 'aip-field' + (answers[key] ? ' answered' : '');
      const label = document.createElement('label');
      label.textContent = key;
      field.appendChild(label);

      if (asText) {
        const inp = document.createElement('input');
        inp.type = 'text'; inp.className = 'aip-txt';
        inp.placeholder = HINT[key] || ''; inp.value = answers[key] || '';
        inp.setAttribute('aria-label', key);
        inp.addEventListener('input', () => {
          const v = inp.value.trim();
          if (v) { answers[key] = v; field.classList.add('answered'); }
          else { delete answers[key]; field.classList.remove('answered'); }
          updateProgress();
        });
        field.appendChild(inp);
      } else {
        const btn = document.createElement('button');
        btn.type = 'button'; btn.className = 'aip-dd';
        btn.setAttribute('aria-haspopup', 'listbox');
        const val = document.createElement('span');
        val.textContent = answers[key] || 'Select';
        btn.append(val, Object.assign(document.createElement('i'), { className: 'aip-caret' }));
        const list = document.createElement('div');
        list.className = 'aip-list';
        OPTIONS[key].forEach(opt => {
          const o = document.createElement('button');
          o.type = 'button';
          o.className = 'aip-opt' + (answers[key] === opt ? ' sel' : '');
          o.innerHTML = '<span></span><svg class="ck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
          o.querySelector('span').textContent = opt;
          o.addEventListener('click', () => {
            answers[key] = opt;
            val.textContent = opt;
            field.classList.add('answered');
            list.querySelectorAll('.aip-opt').forEach(x => x.classList.remove('sel'));
            o.classList.add('sel');
            field.classList.remove('open');
            updateProgress();
          });
          list.appendChild(o);
        });
        btn.addEventListener('click', e => {
          e.stopPropagation();
          const wasOpen = field.classList.contains('open');
          $$('.aip-field').forEach(f => f.classList.remove('open'));
          if (!wasOpen) field.classList.add('open');
        });
        field.append(btn, list);
      }
      grid.appendChild(field);
    });
  }
  document.addEventListener('click', () => $$('.aip-field').forEach(f => f.classList.remove('open')));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') $$('.aip-field').forEach(f => f.classList.remove('open')); });

  $('#aipAdv').addEventListener('change', e => {
    advanced = e.target.checked;
    $('#aipNotesWrap').hidden = !advanced;
    renderFields();
    updateProgress();
  });

  function updateProgress() {
    const n = ORDER.filter(k => answers[k] && String(answers[k]).trim()).length;
    $('#aipCount').textContent = n + ' of 6 chosen';
    $('#aipPct').textContent = Math.round(n / 6 * 100) + '%';
    $('#aipFill').style.width = (n / 6 * 100) + '%';
    const g = $('#aipGo');
    g.disabled = n < 6;
    g.textContent = n < 6 ? 'Choose ' + (6 - n) + ' more' : 'Show me my kitchen';
  }

  /*PROMPT:START  Prompt from the iCreate AI Remodel Visualizer kit (2026-11-13, same as the McManus tool): a real gut
    remodel, never a repaint or a reface. DETAIL says what each choice means to the AI; the names stay DFC's own,
    so they still match the style guide at the bottom of the page. */
  const DETAIL = {
    "Design style": {
      "Transitional": 'transitional, the best of classic and modern: Shaker cabinetry in soft neutral colors, simple clean molding, a mix of polished nickel and brass, and timeless lighting such as linen drum or simple glass pendants',
      "Modern Farmhouse": 'modern farmhouse: warm and relaxed, white cabinetry with matte black accents, an apron-front sink, a bridge or gooseneck faucet, wood accents such as floating shelves, and simple black metal pendant lights',
      "Classic Traditional": 'classic traditional: rich, detailed cabinetry with crown molding, furniture-style details, granite or marble, polished nickel or brass hardware and elegant lantern or chandelier lighting',
      "Contemporary": 'contemporary: sleek flat-panel cabinetry with little or no visible hardware, bold contrast, large-format surfaces, integrated lighting and clean, uncluttered lines',
      "Warm Minimal": 'warm minimal: light white oak and soft white, smooth plaster or matte finishes, honed stone, minimal hardware, natural textures and almost nothing on display, calm and serene',
      "Coastal": 'coastal: bright whites and soft sea blues, light wood tones, woven rattan or natural fiber accents, brushed nickel, and an airy, relaxed, light-filled feel'
    },
    "Cabinets": {
      "Shaker": 'classic five-piece shaker doors: a square frame of narrow, flat stiles and rails around a recessed flat center panel, full-overlay',
      "Flat Panel": 'sleek flat slab doors and drawer fronts with slim or integrated pulls',
      "Raised Panel": 'refined raised-panel doors with a classic profile',
      "Glass Front": 'solid lower cabinets with glass-front upper cabinets, slim mullions and lit interiors',
      "Open Shelving": 'new lower cabinets with open floating wood shelves in place of some upper cabinets',
      "Two Tone": 'two-tone cabinetry, the lower cabinets (and the island, only if the room already has one) in one color and the uppers in a lighter one'
    },
    "Countertops": {
      "Quartz": 'quartz countertops with a clean, consistent finish and a subtle marble-look vein',
      "Quartzite": 'natural quartzite countertops with soft, organic veining',
      "Granite": 'polished granite countertops with natural speckle and movement',
      "Marble": 'honed marble countertops with classic soft gray veining',
      "Butcher Block": 'warm oiled butcher-block wood countertops',
      "Solid Surface": 'seamless matte solid-surface countertops'
    },
    "Backsplash": {
      "Subway Tile": 'handmade-look subway tile in a tight running bond',
      "Full Slab": 'a full-height stone slab backsplash with soft veining that matches the countertops',
      "Herringbone Tile": 'tile in a herringbone pattern',
      "Zellige Tile": 'glossy handmade zellige tile with natural variation in tone',
      "Mosaic Accent": 'a refined small hexagon or penny-round mosaic tile',
      "Natural Stone": 'natural stone tile with an organic texture'
    },
    "Color palette": {
      "Warm Neutrals": 'creamy warm whites, soft beige and taupe, light natural wood and soft brass accents',
      "Crisp White": 'bright white cabinetry, white stone, a few dark accents and an airy, light-filled feel',
      "Cool Grays": 'soft cool grays, white stone and brushed nickel',
      "Deep and Moody": 'deep green, navy or charcoal cabinetry with warm brass accents, rich and moody',
      "Earthy and Natural": 'natural wood tones, sage green, warm stone and terracotta accents',
      "Two Tone Contrast": 'a crisp contrast of light upper cabinets with darker lower cabinets (and island, only if the room already has one)'
    },
    "Budget range": {
      "Under $50k": 'good-quality new cabinetry, quartz or granite countertops and new stainless appliances',
      "$50k to $75k": 'semi-custom cabinetry, quartz or natural stone countertops, upgraded lighting and new appliances',
      "$75k to $100k": 'custom cabinetry to the ceiling, natural stone, a professional range and layered lighting',
      "$100k to $150k": 'fully custom cabinetry, premium natural stone, integrated panel-ready appliances and designer lighting',
      "$150k+": 'bespoke custom cabinetry, luxury stone, integrated panel-ready appliances, a professional range and designer lighting and hardware',
      "Not sure yet": 'tasteful upper-mid-range materials and new appliances'
    }
  };
  const HARDWARE = {
    "Transitional": 'polished nickel or brushed brass cup pulls on drawers and bar pulls on doors',
    "Modern Farmhouse": 'matte black or aged brass cup pulls on drawers and bar pulls on doors',
    "Classic Traditional": 'polished nickel or unlacquered brass bin pulls on drawers and knobs on doors',
    "Contemporary": 'integrated finger pulls or slim edge pulls, almost invisible',
    "Warm Minimal": 'minimal slim pulls in matte black or light oak',
    "Coastal": 'brushed nickel or soft brass knobs and cup pulls'
  };
  const said = f => (DETAIL[f] && DETAIL[f][answers[f]]) || answers[f];
  const hardware = () => HARDWARE[answers['Design style']] || 'new hardware that suits the design style';
  function buildPrompt() {
    let p = 'You are a senior designer at a high-end design-build remodeling company. Show this kitchen or bathroom after a complete professional remodel: a full gut renovation, NOT a paint job, NOT cabinet refacing and NOT a light refresh.'
      + ' KEEP the architecture exactly as it is: the same walls, ceiling height, windows, doorways, camera angle, lens and perspective, and the same layout. Every appliance and fixture stays exactly where it is now: the range or cooktop, the sink, the dishwasher, the refrigerator, the microwave or hood all keep their current positions. Do not add, remove or move any of them, and do not add an island that is not already there.'
      + ' REPLACE everything else with brand new work: all cabinet boxes and doors, countertops, backsplash, sink and faucet, lighting, hardware, flooring and appliances. Do not reuse, repaint or copy the existing cabinet doors, their panel profiles, their seams, their gaps, their knobs or pulls, or their hardware positions: lay out the doors fresh.'
      + ' Show real craftsmanship: doors and drawer fronts aligned in clean rows with tight, even 1/8 inch gaps (full-overlay or inset), drawer stacks where they make sense, upper cabinets taken to the ceiling or finished with crown molding, finished end panels, recessed toe kicks and under-cabinet lighting. Throw away all existing knobs and pulls and use completely new ' + hardware() + ', placed consistently on every drawer and door at the same height. Swap every dated appliance for a new modern one in a matching finish (stainless steel unless the style calls for panel-ready), in the same spot. Clear countertops with only a few tasteful styling pieces.'
      + ' If it is a bathroom, apply the same standard to the vanity, mirror, lighting, shower or tub, tile and plumbing fixtures.'
      + ' Design direction: ' + said('Design style') + '. Cabinetry: ' + said('Cabinets') + '. Countertops: ' + said('Countertops') + '. Backsplash: ' + said('Backsplash') + '. Color palette: ' + said('Color palette') + '. Flooring: new flooring that suits the design. Materials level: ' + said('Budget range') + '.';
    const notes = $('#aipNotes') ? $('#aipNotes').value.trim() : '';
    if (advanced && notes) p += ' Additional notes from the homeowner to honor: ' + notes + '.';
    p += ' Make it photorealistic and magazine quality with natural daylight. Do not add any text, labels, people or watermarks.';
    return p;
  }
  /*PROMPT:END*/

  /* ---- 3. generate ---- */
  $('#aipGo').addEventListener('click', generate);
  async function generate() {
    goStep(3);
    $('#aipLoading').style.display = 'block';
    $('#aipResult').style.display = 'none';
    $('#aipErr').classList.remove('show');
    try {
      const res = await fetch('/api/ai-preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: buildPrompt(), image: b64, mimeType: mime || 'image/jpeg' })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error((data.error && (data.error.message || data.error)) || 'the design service is busy.');
      const part = ((data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts) || []).find(p => p.inlineData);
      if (!part) throw new Error('no image came back.');
      showResult(part.inlineData.data, part.inlineData.mimeType || 'image/png');
      track('ai_design_generated', { tool: 'ai kitchen inspiration', style: answers['Design style'], budget: answers['Budget range'] }, 'AIDesignGenerated');
    } catch (err) {
      $('#aipErr').textContent = 'Sorry, ' + String(err.message || err).replace(/\.?$/, '.') + ' Please go back and try once more, or call us at ' + PHONE + '.';
      $('#aipErr').classList.add('show');
    }
  }

  function showResult(data, type) {
    const url = 'data:' + type + ';base64,' + data;
    $('#aipLoading').style.display = 'none';
    $('#aipResult').style.display = 'block';
    $('#aipAfter').src = url;
    $('#aipBefore').src = objURL;
    $('#aipOpen').href = url;
    requestAnimationFrame(initSlider);
    // Held in memory only; parked on the server only if the visitor sends it.
    lastImage = data;
    savedURL = '';
  }

  let sliderReady = false;
  function initSlider() {
    const ba = $('#aipBa'), before = ba.querySelector('.aip-before'), div = $('#aipDiv'), beforeImg = $('#aipBefore');
    const size = () => { beforeImg.style.width = ba.clientWidth + 'px'; };
    const setPct = p => { p = Math.max(0, Math.min(100, p)); before.style.width = p + '%'; div.style.left = p + '%'; };
    size();
    setPct(50);
    if (sliderReady) return;
    sliderReady = true;
    window.addEventListener('resize', size);
    let dragging = false;
    const move = x => { const r = ba.getBoundingClientRect(); setPct((x - r.left) / r.width * 100); };
    ba.addEventListener('pointerdown', e => { dragging = true; ba.setPointerCapture(e.pointerId); move(e.clientX); });
    ba.addEventListener('pointermove', e => { if (dragging) move(e.clientX); });
    ba.addEventListener('pointerup', () => { dragging = false; });
    ba.addEventListener('pointercancel', () => { dragging = false; });
  }

  $('#aipRestart').addEventListener('click', () => {
    b64 = null; objURL = null; savedURL = ''; lastImage = null;
    drop.style.display = 'block';
    $('#aipPreview').classList.remove('show');
    $('#aipToStyle').disabled = true;
    $('#aipSend').classList.remove('show');
    file.value = '';
    Object.keys(answers).forEach(k => delete answers[k]);
    if ($('#aipNotes')) $('#aipNotes').value = '';
    renderFields(); updateProgress(); goStep(1);
  });

  /* ---- 4. send it to DFC ---- */
  $('#aipSendOpen').addEventListener('click', () => {
    $('#aipSend').classList.add('show');
    $('#aipSend').scrollIntoView({ behavior: 'smooth', block: 'center' });
    setTimeout(() => $('#aipName').focus(), 400);
  });

  $('#aipForm').addEventListener('submit', async e => {
    e.preventDefault();
    const form = e.target, btn = $('#aipSubmit'), status = $('#aipStatus');
    const val = id => (($(id) || {}).value || '').trim();
    status.className = 'aip-status';
    if (!form.checkValidity()) {
      status.textContent = 'Please complete every field above.';
      status.classList.add('is-error');
      form.reportValidity();
      return;
    }
    if (val('#aipHoney')) return;   // honeypot: a bot filled the hidden field
    btn.disabled = true;
    const label = btn.textContent;
    btn.textContent = 'Sending...';
    status.textContent = '';

    // Park the design so the email can link to it. Best effort: the lead
    // still goes if this fails, it just arrives without the picture.
    if (lastImage && !savedURL) {
      try {
        const r = await fetch('/api/ai-save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ image: lastImage }) });
        const j = await r.json();
        if (j && j.url) savedURL = location.origin + j.url;
      } catch (err) { /* carry on without it */ }
    }

    const fd = new FormData();
    fd.append('name', val('#aipName'));
    fd.append('phone', val('#aipPhone'));
    fd.append('email', val('#aipEmail'));
    fd.append('project_address', val('#aipAddress'));
    ORDER.forEach(k => fd.append(k, answers[k] || 'not given'));
    const notes = $('#aipNotes') ? $('#aipNotes').value.trim() : '';
    if (notes) fd.append('Their notes', notes);
    fd.append('design_image', savedURL || 'Could not be saved, ask them for a screenshot');
    fd.append('_subject', 'Kitchen design from the AI Kitchen Inspiration tool');
    fd.append('_template', 'table');
    fd.append('_captcha', 'false');
    fd.append('_cc', LEAD_CC);
    fd.append('source', 'AI Kitchen Inspiration tool');
    fd.append('page_url', location.href);
    fd.append('submitted_at', new Date().toISOString());

    try {
      const r = await fetch(LEAD_ENDPOINT, { method: 'POST', headers: { Accept: 'application/json' }, body: fd });
      const j = await r.json().catch(() => ({}));
      if (!r.ok || (j && j.success === 'false')) throw new Error('send failed');
      track('generate_lead', { form_source: 'ai kitchen inspiration' }, 'AIDesignLead');
      form.reset();
      status.textContent = 'Thank you, your design is on its way. We will call you within 24 hours to talk it through.';
      status.classList.add('is-ok');
    } catch (err) {
      status.textContent = 'Sorry, that did not send. Please call or text us at ' + PHONE + '.';
      status.classList.add('is-error');
    } finally {
      btn.disabled = false;
      btn.textContent = label;
    }
  });

  /* Style guide: tap an example for a closer look. Same lightbox look as the
     portfolio; opens on the cached card photo, then swaps in the 1600px one. */
  const lb = $('#aipLb');
  if (lb) {
    const cards = $$('.aip-ex-card');
    const lbImg = $('#aipLbImg');
    const lbCap = $('#aipLbCap');
    let current = 0;
    let lastFocus = null;
    const show = i => {
      current = (i + cards.length) % cards.length;
      const card = cards[current];
      const thumb = card.querySelector('img');
      const full = card.querySelector('.aip-ex-img').dataset.full;
      lbImg.src = thumb.currentSrc || thumb.src;
      lbImg.alt = thumb.alt;
      lbCap.textContent = card.querySelector('.aip-ex-name').textContent.trim() + ' · ' + card.querySelector('p').textContent;
      const hi = new Image();
      const want = current;
      hi.onload = () => { if (current === want) lbImg.src = full; };
      hi.src = full;
    };
    const open = i => {
      lastFocus = document.activeElement;
      show(i);
      lb.classList.add('open');
      lb.setAttribute('aria-hidden', 'false');
      document.body.classList.add('menu-open');
      $('#aipLbClose').focus();
    };
    const close = () => {
      lb.classList.remove('open');
      lb.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('menu-open');
      if (lastFocus) lastFocus.focus();
    };
    cards.forEach((card, i) => card.querySelector('.aip-ex-img').addEventListener('click', () => open(i)));
    $('#aipLbClose').addEventListener('click', close);
    $('#aipLbNext').addEventListener('click', () => show(current + 1));
    $('#aipLbPrev').addEventListener('click', () => show(current - 1));
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    document.addEventListener('keydown', e => {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') show(current + 1);
      else if (e.key === 'ArrowLeft') show(current - 1);
    });
    let touchX = null;
    lb.addEventListener('touchstart', e => { touchX = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', e => {
      if (touchX === null) return;
      const dx = e.changedTouches[0].clientX - touchX;
      touchX = null;
      if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
    });
  }

  renderFields();
  updateProgress();
})();
