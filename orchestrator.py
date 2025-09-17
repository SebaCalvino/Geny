# -*- coding: utf-8 -*-
"""
Factory de mini-webs — OVERHAUL (paletas + historia + 4 páginas + metadata)
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
import json, random, re, datetime as dt

PALETTES = [
    {"bg":"#0f0f12","fg":"#e8e8ec","acc1":"#7c3aed","acc2":"#22d3ee"},
    {"bg":"#0b132b","fg":"#eaeaea","acc1":"#6fffe9","acc2":"#ffd166"},
    {"bg":"#111827","fg":"#f3f4f6","acc1":"#f59e0b","acc2":"#10b981"},
    {"bg":"#121212","fg":"#fafafa","acc1":"#9b5de5","acc2":"#f15bb5"},
]

def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s, flags=re.U)
    s = re.sub(r"[\s_-]+", "-", s.strip().lower(), flags=re.U)
    return s

def pick_palette(index_hint: int | None, seed: int) -> tuple[dict, int]:
    if index_hint is not None:
        i = int(index_hint) % len(PALETTES)
        return PALETTES[i], i
    random.seed(seed); i = random.randint(0, len(PALETTES)-1)
    return PALETTES[i], i

def now_iso() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()

@dataclass
class CompanyData:
    name: str
    address: str
    phone: str
    email: str
    hours: str
    social: dict

def fake_company(brand: str, city: str = "CABA", country: str = "Argentina") -> CompanyData:
    slug = slugify(brand)
    return CompanyData(
        name=f"{brand} S.A.S.",
        address=f"Av. Corrientes 2345, {city}, {country}",
        phone="+54 9 11 2345-6789",
        email=f"hola@{slug}.com",
        hours="Lun–Vie 9:00–18:00",
        social={
            "instagram": f"https://instagram.com/{slug}",
            "twitter": f"https://x.com/{slug}",
            "linkedin": f"https://linkedin.com/company/{slug}"
        }
    )

def tpl_styles(palette: dict) -> str:
    return dedent(f"""\
    :root {{
      --bg:{palette['bg']}; --fg:{palette['fg']};
      --acc1:{palette['acc1']}; --acc2:{palette['acc2']};
      --muted:#9aa0a6; --card:color-mix(in oklab, var(--bg), white 6%);
      --border:color-mix(in oklab, var(--bg), white 14%); --radius:14px;
      --shadow:0 10px 30px rgba(0,0,0,.35);
    }}
    *{{box-sizing:border-box}} html,body{{height:100%}}
    body{{
      margin:0;color:var(--fg);
      background:
        radial-gradient(1200px 600px at 10% -10%, color-mix(in oklab, var(--acc1), transparent 82%), transparent 60%),
        radial-gradient(800px 400px at 100% 0%, color-mix(in oklab, var(--acc2), transparent 88%), transparent 55%),
        linear-gradient(180deg, var(--bg) 0%, color-mix(in oklab, var(--bg), black 8%) 100%);
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Inter, Helvetica, Arial; line-height:1.6;
    }}
    a{color:var(--acc2);text-decoration:none} a:hover{color:var(--acc1)}
    :focus-visible{outline:2px solid var(--acc2);outline-offset:2px}
    .container{width:min(1100px,92%);margin:0 auto}
    .site-header{position:sticky;top:0;z-index:40;backdrop-filter:blur(8px);background:color-mix(in oklab,var(--bg),transparent 40%);border-bottom:1px solid var(--border)}
    .nav-wrap{display:flex;align-items:center;justify-content:space-between;padding:14px 0}
    .brand{display:flex;align-items:center;gap:12px;color:var(--fg);font-weight:700}
    .brandmark{width:28px;height:28px;color:var(--acc2)}
    .main-nav a{margin-left:18px;padding:8px 10px;border-radius:10px;color:var(--fg)}
    .main-nav a.active,.main-nav a:hover{background:var(--card);border:1px solid var(--border)}
    .hero{display:grid;grid-template-columns:1.1fr .9fr;gap:28px;padding:40px 0 28px;align-items:center}
    .hero-text h1{font-size:clamp(28px,4vw,48px);line-height:1.1}
    .hero-text p{max-width:58ch}
    .hero-media img.hero-img{width:100%;height:auto;border-radius:var(--radius);box-shadow:var(--shadow)}
    .cta-row{display:flex;gap:12px;margin-top:14px;flex-wrap:wrap}
    .btn{display:inline-block;padding:10px 16px;border-radius:12px;font-weight:600;border:1px solid var(--border);transition:transform .06s ease}
    .btn:hover{transform:translateY(-1px)}
    .btn-primary{background:var(--acc1);color:#fff;border-color:color-mix(in oklab,var(--acc1),black 10%)}
    .btn-primary:hover{background:color-mix(in oklab,var(--acc1),white 10%)}
    .btn-ghost{background:transparent;color:var(--fg)}
    .btn-secondary{background:var(--card);color:var(--fg)}
    .features{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding:22px 0}
    .card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:16px;box-shadow:var(--shadow)}
    .card .icon svg{width:24px;height:24px;color:var(--acc2)}
    .showcase{display:grid;gap:16px;padding:22px 0}
    .showcase-item{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:center}
    .showcase img{width:100%;height:auto;border-radius:var(--radius)}
    .page h1,.page h2{letter-spacing:-.01em}
    .grid-2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
    .team{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
    .company{line-height:1.8}
    .card-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
    .gallery{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px}
    .form label{display:grid;gap:6px;margin-bottom:10px}
    input,select,textarea{background:#0e0e13;color:var(--fg);border:1px solid var(--border);border-radius:10px;padding:10px}
    input:focus,select:focus,textarea:focus{outline:2px solid var(--acc2)}
    .site-footer{margin-top:40px;border-top:1px solid var(--border);background:color-mix(in oklab,var(--bg),transparent 30%)}
    .footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:16px;padding:16px 0}
    .copyright{padding:14px 0;color:var(--muted)}
    @media (max-width:900px){
      .hero{grid-template-columns:1fr}
      .features{grid-template-columns:1fr}
      .grid-2{grid-template-columns:1fr}
      .card-grid{grid-template-columns:1fr 1fr}
      .footer-grid{grid-template-columns:1fr}
    }
    @media (max-width:520px){.card-grid{grid-template-columns:1fr}}
    """)

def brandmark_svg() -> str:
    return """\
<!-- brandmark.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="currentColor" stop-opacity=".95"/>
      <stop offset="1" stop-color="currentColor" stop-opacity=".55"/>
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="16" fill="url(#g)"/>
  <ellipse cx="32" cy="36" rx="24" ry="10" fill="none" stroke="currentColor" stroke-width="2"/>
</svg>
"""

def tpl_header(brand: str) -> str:
    return dedent(f"""\
    <header class="site-header">
      <div class="container nav-wrap">
        <a class="brand" href="index.html" aria-label="Inicio {brand}">
          <svg class="brandmark" viewBox="0 0 64 64" aria-hidden="true">
            <circle cx="32" cy="32" r="16"/>
            <ellipse cx="32" cy="36" rx="24" ry="10" fill="none" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>{brand}</span>
        </a>
        <nav class="main-nav" aria-label="Primaria">
          <a href="index.html">Inicio</a>
          <a href="about.html">Nosotros</a>
          <a href="services.html">Servicios</a>
          <a href="contact.html">Contacto</a>
        </nav>
      </div>
    </header>
    """)

def tpl_footer(company: CompanyData) -> str:
    return dedent(f"""\
    <footer class="site-footer">
      <div class="container footer-grid">
        <div>
          <h4>{company.name.split()[0]}</h4>
          <p>Clínica digital con base en Buenos Aires, operando para toda LATAM.</p>
        </div>
        <div>
          <h4>Contacto</h4>
          <ul>
            <li><a href="mailto:{company.email}">{company.email}</a></li>
            <li><a href="tel:{company.phone.replace(' ', '')}">{company.phone}</a></li>
            <li><a href="{company.social['instagram']}" target="_blank" rel="noopener">Instagram</a></li>
            <li><a href="{company.social['twitter']}" target="_blank" rel="noopener">X/Twitter</a></li>
            <li><a href="{company.social['linkedin']}" target="_blank" rel="noopener">LinkedIn</a></li>
          </ul>
        </div>
        <div>
          <h4>Navegación</h4>
          <ul>
            <li><a href="about.html">Nosotros</a></li>
            <li><a href="services.html">Servicios</a></li>
            <li><a href="contact.html">Contacto</a></li>
          </ul>
        </div>
      </div>
      <div class="container copyright">© <span id="year"></span> {company.name.split()[0]} — Todos los derechos reservados</div>
    </footer>
    """)

def page_wrap(title: str, head_extra: str, header: str, body: str, footer: str) -> str:
    return dedent(f"""\
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>{title}</title>
      <link rel="stylesheet" href="assets/css/styles.css" />
      {head_extra}
    </head>
    <body>
      {header}
      {body}
      {footer}
      <script src="assets/js/script.js"></script>
    </body>
    </html>
    """)

def tpl_index(brand: str) -> str:
    return dedent(f"""\
    <main>
      <section class="hero container">
        <div class="hero-text">
          <h1>{brand}: clínica digital que <strong>nunca te suelta la mano</strong></h1>
          <p>Teleconsulta, historial clínico y estudios en la nube. Atención segura, humana y accesible — estés donde estés.</p>
          <div class="cta-row">
            <a class="btn btn-primary" href="contact.html">Reservar teleconsulta</a>
            <a class="btn btn-ghost" href="services.html">Ver servicios</a>
          </div>
        </div>
        <div class="hero-media">
          <img class="hero-img" src="https://images.unsplash.com/photo-1586773860418-d37222d8fce3?q=80&w=1600&auto=format&fit=crop" alt="Profesional de salud usando plataforma de telemedicina">
        </div>
      </section>

      <section class="features container">
        <article class="card">
          <div class="icon">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </div>
          <h3>Telemedicina segura</h3>
          <p>Consultas encriptadas, prescripción digital y seguimiento posconsulta.</p>
        </article>
        <article class="card">
          <div class="icon">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 8v8a2 2 0 0 1-2 2H5l-2 2V8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M7 11h10M7 15h7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </div>
          <h3>Atención humana</h3>
          <p>Agenda ágil, recordatorios y múltiples canales de contacto.</p>
        </article>
        <article class="card">
          <div class="icon">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18M3 12h18" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/></svg>
          </div>
          <h3>Datos en la nube</h3>
          <p>Historial clínico centralizado con permisos claros y auditoría.</p>
        </article>
      </section>

      <section class="showcase container">
        <div class="showcase-item">
          <img src="https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?q=80&w=1600&auto=format&fit=crop" alt="Dashboard con resultados de laboratorio digitalizados">
          <div>
            <h3>Resultados inteligentes</h3>
            <p>Graficamos tendencias y marcamos valores fuera de rango.</p>
          </div>
        </div>
        <div class="showcase-item">
          <img src="https://images.unsplash.com/photo-1551190822-a9333d879b1f?q=80&w=1600&auto=format&fit=crop" alt="Paciente en videoconsulta médica">
          <div>
            <h3>Videoconsulta estable</h3>
            <p>Calidad adaptativa y reconexión silenciosa para evitar cortes.</p>
          </div>
        </div>
      </section>

      <section class="cta container">
        <h2>Tu salud, a un clic de distancia</h2>
        <p>Profesionales certificados y foco en privacidad.</p>
        <a class="btn btn-primary" href="contact.html">Empezar ahora</a>
      </section>
    </main>
    """)

def tpl_about(company: CompanyData) -> str:
    return dedent(f"""\
    <main class="container page">
      <h1>Nuestra historia</h1>
      <p>{company.name.split()[0]} nació con una idea simple: que nadie quede fuera del sistema de salud por barreras geográficas o económicas. Empezamos en Buenos Aires y hoy acompañamos a pacientes en toda LATAM.</p>

      <div class="grid-2">
        <img src="https://images.unsplash.com/photo-1580281657527-47a87a0f43d1?q=80&w=1600&auto=format&fit=crop" alt="Equipo médico y de ingeniería planificando mejoras">
        <div>
          <h2>Misión</h2>
          <p>Brindar atención confiable, segura y humana con herramientas digitales accesibles.</p>
          <h2>Visión</h2>
          <p>Conectar pacientes y profesionales con datos claros y decisiones informadas.</p>
        </div>
      </div>

      <h2>Datos de la empresa</h2>
      <ul class="company">
        <li><strong>Nombre:</strong> {company.name}</li>
        <li><strong>Dirección:</strong> {company.address}</li>
        <li><strong>Teléfono:</strong> {company.phone}</li>
        <li><strong>Email:</strong> <a href="mailto:{company.email}">{company.email}</a></li>
        <li><strong>Horario:</strong> {company.hours}</li>
        <li><strong>Redes:</strong>
          <a href="{company.social['instagram']}" target="_blank" rel="noopener">Instagram</a> ·
          <a href="{company.social['twitter']}" target="_blank" rel="noopener">X/Twitter</a> ·
          <a href="{company.social['linkedin']}" target="_blank" rel="noopener">LinkedIn</a>
        </li>
      </ul>
    </main>
    """)

def tpl_services() -> str:
    return dedent("""\
    <main class="container page">
      <h1>Servicios</h1>
      <p>Atención integral y digital. Elegí el plan que mejor se adapte a vos.</p>

      <div class="card-grid">
        <article class="card service">
          <div class="icon"><svg viewBox="0 0 24 24"><path d="M12 2v20M2 12h20" fill="none" stroke="currentColor" stroke-width="2"/></svg></div>
          <h3>Teleconsulta general</h3>
          <p>Consulta de 30 minutos con clínica médica. Recetas digitales y notas de consulta.</p>
          <a class="btn btn-secondary" href="contact.html">Reservar</a>
        </article>

        <article class="card service">
          <div class="icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/></svg></div>
          <h3>Pediatría en línea</h3>
          <p>Control de crecimiento, fiebre y seguimiento con especialistas.</p>
          <a class="btn btn-secondary" href="contact.html">Reservar</a>
        </article>

        <article class="card service">
          <div class="icon"><svg viewBox="0 0 24 24"><path d="M3 6h18v12H3zM7 10h10" fill="none" stroke="currentColor" stroke-width="2"/></svg></div>
          <h3>Laboratorio digital</h3>
          <p>Carga de resultados, gráficos de evolución y alertas de valores fuera de rango.</p>
          <a class="btn btn-secondary" href="contact.html">Reservar</a>
        </article>

        <article class="card service">
          <div class="icon"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h10" fill="none" stroke="currentColor" stroke-width="2"/></svg></div>
          <h3>Plan crónico</h3>
          <p>Seguimiento mensual para hipertensión, diabetes y EPOC.</p>
          <a class="btn btn-secondary" href="contact.html">Reservar</a>
        </article>
      </div>

      <section class="gallery">
        <img src="https://images.unsplash.com/photo-1588515611460-8f5891714f8d?q=80&w=1600&auto=format&fit=crop" alt="Profesional monitoreando parámetros de salud" />
        <img src="https://images.unsplash.com/photo-1584433144859-1fc3ab64a957?q=80&w=1600&auto=format&fit=crop" alt="Sala limpia con equipamiento médico" />
      </section>
    </main>
    """)

def tpl_contact(company: CompanyData) -> str:
    return dedent(f"""\
    <main class="container page">
      <h1>Contacto</h1>
      <p>Respondemos de {company.hours} (UTC-3). También por redes.</p>

      <div class="grid-2">
        <form id="contact-form" class="card form" novalidate>
          <label>Nombre<input type="text" name="name" required minlength="2" placeholder="Tu nombre" /></label>
          <label>Email<input type="email" name="email" required placeholder="tucorreo@ejemplo.com" /></label>
          <label>Motivo
            <select name="topic" required>
              <option value="">Seleccioná una opción</option>
              <option>Teleconsulta</option>
              <option>Resultados</option>
              <option>Soporte</option>
            </select>
          </label>
          <label>Mensaje<textarea name="message" required minlength="10" rows="4" placeholder="Contanos brevemente tu consulta"></textarea></label>
          <button class="btn btn-primary" type="submit">Enviar</button>
          <p id="form-msg" role="status" aria-live="polite"></p>
        </form>

        <aside class="card contact-data">
          <h2>Datos</h2>
          <ul>
            <li><strong>Dirección:</strong> {company.address}</li>
            <li><strong>Teléfono:</strong> <a href="tel:{company.phone.replace(' ', '')}">{company.phone}</a></li>
            <li><strong>Email:</strong> <a href="mailto:{company.email}">{company.email}</a></li>
            <li><strong>Instagram:</strong> <a href="{company.social['instagram']}" target="_blank" rel="noopener">@{company.name.split()[0].lower()}</a></li>
            <li><strong>Twitter:</strong> <a href="{company.social['twitter']}" target="_blank" rel="noopener">@{company.name.split()[0].lower()}</a></li>
            <li><strong>LinkedIn:</strong> <a href="{company.social['linkedin']}" target="_blank" rel="noopener">/company/{company.name.split()[0].lower()}</a></li>
            <li><strong>Horario:</strong> {company.hours}</li>
          </ul>
        </aside>
      </div>
    </main>
    """)

def tpl_script_js() -> str:
    return dedent("""\
    // script.js — utilidades mínimas
    (function(){
      const y = document.getElementById('year');
      if (y) y.textContent = new Date().getFullYear();

      const form = document.getElementById('contact-form');
      const msg = document.getElementById('form-msg');
      if (form && msg) {
        form.addEventListener('submit', (e) => {
          e.preventDefault();
          const ok = form.checkValidity();
          msg.textContent = ok ? '¡Gracias! Te responderemos pronto.' : 'Revisá los campos obligatorios.';
        });
      }
    })();
    """)

def readme_md(brand: str) -> str:
    return dedent(f"""\
    # {brand}
    Mini-sitio generado automáticamente.

    ## Ver localmente
    1. Abrí `index.html` en el navegador.
    2. Navegá con el header/footer (index, about, services, contact).

    ## Publicación (GitHub Pages)
    - Subí esta carpeta a tu branch de páginas (o usá un workflow que copie a `gh-pages`).
    - Paths relativos; sin dependencias externas obligatorias.
    """)

def generate_website(output_dir: str, site_title: str, palette_index: int | None = None) -> dict:
    brand = site_title
    slug = slugify(site_title)
    seed = abs(hash(slug)) % (10**6)
    palette, pidx = pick_palette(palette_index, seed)
    company = fake_company(brand)

    base = Path(output_dir)
    base.mkdir(parents=True, exist_ok=True)

    assets_css = base / "assets" / "css"
    assets_js = base / "assets" / "js"
    assets_images = base / "assets" / "images"
    for p in (assets_css, assets_js, assets_images):
        p.mkdir(parents=True, exist_ok=True)

    (assets_css / "styles.css").write_text(tpl_styles(palette), encoding="utf-8")
    (assets_js / "script.js").write_text(tpl_script_js(), encoding="utf-8")
    (assets_images / "brandmark.svg").write_text(brandmark_svg(), encoding="utf-8")

    header = tpl_header(brand)
    footer = tpl_footer(company)

    index_html = page_wrap(
        f"{brand} — Clínica Digital",
        '<meta name="description" content="Telemedicina, historia clínica y estudios en la nube.">',
        header.replace('href="index.html">Inicio</a>', 'href="index.html" class="active">Inicio</a>'),
        tpl_index(brand),
        footer
    )
    about_html = page_wrap(f"{brand} — Sobre nosotros","", header.replace('>Nosotros<',' class="active">Nosotros<'), tpl_about(company), footer)
    services_html = page_wrap(f"{brand} — Servicios","", header.replace('>Servicios<',' class="active">Servicios<'), tpl_services(), footer)
    contact_html = page_wrap(f"{brand} — Contacto","", header.replace('>Contacto<',' class="active">Contacto<'), tpl_contact(company), footer)

    (base / "index.html").write_text(index_html, encoding="utf-8")
    (base / "about.html").write_text(about_html, encoding="utf-8")
    (base / "services.html").write_text(services_html, encoding="utf-8")
    (base / "contact.html").write_text(contact_html, encoding="utf-8")
    (base / "README.md").write_text(readme_md(brand), encoding="utf-8")

    metadata = {
        "title": brand,
        "slug": slug,
        "palette": palette,
        "theme_story": f"{brand} integra teleconsulta, seguimiento y estudios en la nube con foco en privacidad en LATAM.",
        "company": {
            "name": company.name, "address": company.address, "phone": company.phone,
            "email": company.email, "hours": company.hours, "social": company.social
        },
        "pages": ["index.html","about.html","services.html","contact.html"],
        "images": [
            f"assets/images/hero_{slug}.jpg","assets/images/section_1.jpg",
            "assets/images/section_2.jpg","assets/images/brandmark.svg"
        ],
        "created_at": now_iso()
    }
    (base / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    return {"slug": slug, "palette_index": pidx, "output_dir": str(base), "pages": metadata["pages"]}
