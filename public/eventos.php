<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#11100e">
  <title>Eventos — El Café de los Poetas Muertos</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root{--ink:#11100e;--panel:#191714;--cream:#f5efdf;--muted:#b9b09e;--gold:#d6ad59;--line:#38332b;--serif:'Playfair Display',Georgia,serif;--sans:'DM Sans',Arial,sans-serif}*{box-sizing:border-box}body{margin:0;background:var(--ink);color:var(--cream);font:16px/1.6 var(--sans)}a{color:inherit}.wrap{width:min(1060px,calc(100% - 40px));margin:auto}.nav{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:15px 0;border-bottom:1px solid var(--line)}header{background:#151310}.brand{font:700 1rem var(--serif);text-decoration:none;display:flex;align-items:center;gap:12px}.brand img{width:42px;height:42px;border-radius:50%;object-fit:cover;border:1px solid var(--gold)}.brand span{line-height:1.1}.navlinks{display:flex;align-items:center;gap:22px}.navlinks a{font-size:.85rem;text-decoration:none;color:#e6dfd0}.navlinks a:hover{color:var(--gold)}.hero{padding:70px 0 50px;background:radial-gradient(ellipse at 80% 30%,rgba(111,72,37,.2),transparent 42%)}.eyebrow{color:var(--gold);font-weight:700;letter-spacing:.2em;font-size:.72rem;text-transform:uppercase}.hero h1{font:700 clamp(2.7rem,7vw,4.7rem)/1.05 var(--serif);margin:12px 0}.hero p{color:var(--muted);max-width:650px}.content{padding:25px 0 80px}.event-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:16px}.event-card{background:var(--panel);border:1px solid #353026;display:flex;flex-direction:column;overflow:hidden;transition:transform .28s ease,border-color .28s ease,box-shadow .28s ease} @media(hover:hover){.event-card:hover,.event-card:focus-within{transform:translateY(-5px);border-color:var(--gold);box-shadow:0 16px 36px rgba(0,0,0,.32)}.event-card:hover img{transform:scale(1.035)}} @media(prefers-reduced-motion:reduce){.event-card,.event-card img{transition:none!important}.event-card:hover,.event-card:focus-within{transform:none!important}}.event-card img{width:100%;aspect-ratio:16/7;object-fit:cover;background:#252117;transition:transform .35s ease}.event-body{padding:18px;display:flex;flex:1;flex-direction:column}.event-body h2{font:600 1.38rem/1.2 var(--serif);margin:0 0 8px}.event-meta{color:var(--gold);font-size:.82rem;display:flex;flex-wrap:wrap;gap:7px 16px;margin-bottom:14px}.event-description{white-space:pre-line;color:#c5bdaf;font-size:.91rem;margin:0 0 20px}.event-bottom{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:auto}.spots{color:var(--muted);font-size:.8rem}.button{border:1px solid var(--gold);padding:11px 16px;background:var(--gold);color:var(--ink);font-weight:700;text-decoration:none;cursor:pointer}.button:disabled{opacity:.45;cursor:not-allowed}.registration{scroll-margin-top:20px;margin-top:58px;padding:30px;background:var(--panel);border:1px solid var(--line);max-width:680px}.registration h2{font:600 1.8rem var(--serif);margin:0 0 5px}.registration>p{color:var(--muted);margin:0 0 20px}.field{margin-bottom:15px}.field label{display:block;color:var(--gold);font-size:.8rem;margin-bottom:6px}.field input{width:100%;padding:12px;background:#100f0d;border:1px solid #454036;color:var(--cream)}.consent{display:flex;gap:10px;align-items:flex-start;color:var(--muted);font-size:.78rem;margin:17px 0}.consent input{margin-top:5px;accent-color:var(--gold)}.status{min-height:25px;color:var(--gold);font-size:.86rem;margin-top:12px}.empty{grid-column:1/-1;padding:30px;text-align:center;color:var(--muted);background:var(--panel)}footer{border-top:1px solid var(--line);padding:24px 0;color:var(--muted);font-size:.8rem}.footerrow{display:flex;justify-content:space-between;gap:14px;align-items:center}.footerrow a{color:var(--gold);text-decoration:none}.social-link{display:inline-flex;align-items:center;color:var(--gold)!important}.social-link svg{width:25px;height:25px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;transition:transform .2s}.social-link:hover svg{transform:translateY(-2px) scale(1.08)}.social-link:focus-visible{outline:2px solid var(--gold);outline-offset:4px}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
    @media(max-width:700px){.wrap{width:calc(100% - 30px)}.nav{align-items:flex-start;flex-direction:column}.navlinks{gap:15px;flex-wrap:wrap}.event-grid{grid-template-columns:1fr}.hero{padding-top:48px}.footerrow{flex-direction:column;text-align:center}}
    .registration-dialog{width:min(560px,calc(100% - 28px));max-width:none;max-height:min(90dvh,820px);padding:0;border:1px solid var(--line);background:var(--panel);color:var(--cream);box-shadow:0 24px 80px #000b;overflow:auto}.registration-dialog::backdrop{background:#080706c9;backdrop-filter:blur(4px)}.registration{margin:0;padding:clamp(20px,5vw,34px);max-width:none;border:0}.dialog-head{display:flex;justify-content:space-between;align-items:flex-start;gap:14px}.dialog-close{flex:none;border:1px solid var(--line);background:#100f0d;color:var(--cream);width:38px;height:38px;font-size:1.3rem;cursor:pointer}.registration h2{font:600 clamp(1.5rem,5vw,1.9rem) var(--serif);margin:0 0 5px}.registration>p{color:var(--muted);margin:8px 0 22px}.field{margin-bottom:16px}.field label{display:block;color:var(--gold);font-size:.82rem;margin-bottom:7px}.field input{display:block;width:100%;min-height:46px;padding:12px;background:#100f0d;border:1px solid #454036;color:var(--cream);border-radius:3px;font:inherit}.field input:focus{outline:2px solid var(--gold);outline-offset:1px}.registration .button{width:100%;min-height:48px}.status:empty{display:none}.status{padding-top:5px}.choose-event{min-height:44px}.event-meta{align-items:center}.spots{color:var(--gold);font-size:.82rem}
  </style>
  <link rel="stylesheet" href="design.css">
</head>
<body class="events-page">
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
  <header><nav class="nav wrap"><a class="brand" href="index.php"><img src="images/images%20(1).jfif" alt=""><span>El Café de los<br>Poetas Muertos</span></a><div class="navlinks"><a href="index.php">Inicio</a><a href="menu.php">Menú</a><a href="index.php#visitanos">Visítanos</a></div></nav></header>
  <section class="hero"><div class="wrap"><span class="eyebrow">Encuentros en la casa</span><h1>Eventos con café<br>y buena compañía.</h1><p>Lecturas, talleres y encuentros para compartir lo que nos mueve. Consulta las próximas actividades de la casa.</p></div></section>
  <main class="content wrap" id="contenido"><div class="event-grid" id="event-grid" aria-live="polite"><p class="agenda-loading" role="status">Preparando la agenda…</p></div></main>
  <dialog class="registration-dialog" id="registration-dialog" aria-labelledby="registration-title">
    <form class="registration" id="registration-form"><div class="dialog-head"><h2 id="registration-title">Inscripción</h2><button class="dialog-close" type="button" id="close-registration" aria-label="Cerrar ventana">×</button></div><p id="selected-event">Selecciona primero un evento para registrarte.</p><input type="hidden" id="event-id" name="eventId">
      <div class="field"><label for="name">Nombre completo</label><input id="name" name="name" autocomplete="name" maxlength="100" required></div>
      <div class="field"><label for="phone">Teléfono</label><input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="30" placeholder="Ej. 477 123 4567" required></div>
      <div class="field"><label for="email">Correo electrónico (opcional)</label><input id="email" name="email" type="email" autocomplete="email" maxlength="160"></div>
      <label class="consent"><input id="consent" type="checkbox" required><span>Autorizo el uso de mis datos para gestionar mi inscripción a este evento.</span></label>
      <button class="button" type="submit" id="register-button" disabled>Confirmar inscripción</button><div class="status" id="form-status" role="status" aria-live="polite"></div>
    </form>
  </dialog>
  <footer><div class="wrap footerrow"><span>© <?= date('Y') ?> El Café de los Poetas Muertos</span><a class="social-link" href="https://www.instagram.com/elcafedelospoetasmuertos?obrf=MXh5bGdsYnRxZXl2NQ==" target="_blank" rel="noopener noreferrer" aria-label="Instagram de El Café de los Poetas Muertos (abre en pestaña nueva)" title="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="18" cy="6" r=".8" fill="currentColor" stroke="none"/></svg></a><a class="social-link" href="https://www.facebook.com/profile.php?id=61551230459953&amp;sk=directory_category" target="_blank" rel="noopener noreferrer" aria-label="Facebook de El Café de los Poetas Muertos (abre en pestaña nueva)" title="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.4 21v-8h2.7l.4-3h-3.1V8.1c0-.9.3-1.5 1.6-1.5h1.7V3.9c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.2V10H7.3v3H10v8h3.4z"/></svg></a><a href="index.php">Página principal</a></div></footer>
  <script>
    const grid = document.getElementById('event-grid');
    const form = document.getElementById('registration-form');
    const registrationDialog = document.getElementById('registration-dialog');
    const eventId = document.getElementById('event-id');
    const button = document.getElementById('register-button');
    const statusBox = document.getElementById('form-status');
    const apiBase = ['localhost','127.0.0.1'].includes(location.hostname) ? 'http://127.0.0.1:8000' : '';
    const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
    const dateText = value => new Intl.DateTimeFormat('es-MX',{dateStyle:'long',timeStyle:'short'}).format(new Date(value));
    async function loadEvents() {
      if (location.hostname.endsWith('github.io')) {
        grid.innerHTML = '<div class="agenda-state"><span class="state-mark" aria-hidden="true">&amp;</span><div><h3>La próxima historia está por escribirse.</h3><p>Lecturas, talleres y encuentros alrededor del café. Consulta las próximas fechas y disponibilidad en nuestras redes.</p></div><a class="text-link" href="https://www.instagram.com/elcafedelospoetasmuertos/" target="_blank" rel="noopener noreferrer">Ver agenda en Instagram ↗</a></div>';
        return;
      }
      try {
        const response = await fetch(`${apiBase}/api/events`);
        if (!response.ok) throw new Error('No se pudieron cargar los eventos.');
        const {events} = await response.json();
        const visible = events.filter(event => event.status === 'active');
        grid.innerHTML = visible.length ? visible.map(event => `<article class="event-card">${event.image ? `<img src="${apiBase}${escapeHtml(event.image)}" alt="Imagen del evento ${escapeHtml(event.name)}">` : ''}<div class="event-body"><h2>${escapeHtml(event.name)}</h2><div class="event-meta"><span>${escapeHtml(dateText(event.startsAt))}</span><span>${event.available} lugares disponibles</span></div><p class="event-description">${escapeHtml(event.description)}</p><div class="event-bottom"><span class="spots">Registrados: ${event.registered} / ${event.capacity}</span><button class="button choose-event" type="button" data-id="${event.id}" data-name="${escapeHtml(event.name)}" ${event.available < 1 ? 'disabled' : ''}>${event.available < 1 ? 'Cupo lleno' : 'Registrarme'}</button></div></div></article>`).join('') : '<div class="agenda-state"><span class="state-mark" aria-hidden="true">&amp;</span><div><h3>La próxima historia está por escribirse.</h3><p>Lecturas, talleres y encuentros alrededor del café. Consulta las próximas fechas y disponibilidad en nuestras redes.</p></div><a class="text-link" href="https://www.instagram.com/elcafedelospoetasmuertos/" target="_blank" rel="noopener noreferrer">Ver agenda en Instagram ↗</a></div>';
        grid.querySelectorAll('.choose-event').forEach(item => item.addEventListener('click', () => {
          eventId.value = item.dataset.id;
          document.getElementById('selected-event').textContent = `Vas a inscribirte en: ${item.dataset.name}`;
          button.disabled = false;
          statusBox.textContent = '';
          registrationDialog.showModal();
          document.getElementById('name').focus();
        }));
      } catch (error) { grid.innerHTML = '<div class="agenda-state"><span class="state-mark" aria-hidden="true">&amp;</span><div><h3>No pudimos cargar la agenda.</h3><p>Vuelve a intentarlo o consulta las actividades en nuestras redes.</p></div><div class="state-actions"><button type="button" onclick="loadEvents()">Reintentar</button><a class="text-link" href="https://www.instagram.com/elcafedelospoetasmuertos/">Instagram ↗</a></div></div>'; }
    }
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      button.disabled = true;
      statusBox.textContent = 'Enviando inscripción…';
      const body = {eventId:Number(eventId.value),name:document.getElementById('name').value,phone:document.getElementById('phone').value,email:document.getElementById('email').value};
      try {
        const response = await fetch(`${apiBase}/api/events/register`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'No se pudo completar el registro.');
        statusBox.textContent = result.message;
        form.reset();eventId.value='';button.disabled=true;
        document.getElementById('selected-event').textContent='Tu lugar quedó confirmado.';
        await loadEvents();
      } catch (error) {statusBox.textContent=error.message;button.disabled=!eventId.value;}
    });
    document.getElementById('close-registration').addEventListener('click', () => registrationDialog.close());
    registrationDialog.addEventListener('click', event => { if (event.target === registrationDialog) registrationDialog.close(); });
    loadEvents();
  </script>
</body>
</html>
