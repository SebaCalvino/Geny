#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web Factory para Tektra - Genera sitios web completos y creativos
"""

import random
import datetime as dt
from pathlib import Path
import json
import logging

log = logging.getLogger("tektra.web_factory")

# Paletas de colores épicas
COLOR_PALETTES = [
    {
        "name": "Cyber Neon",
        "primary": "#00ff88",
        "secondary": "#ff0080",
        "accent": "#8800ff",
        "bg": "#0a0a0a",
        "text": "#ffffff"
    },
    {
        "name": "Ocean Deep",
        "primary": "#0077be",
        "secondary": "#00a8cc",
        "accent": "#ffd23f",
        "bg": "#001122",
        "text": "#e8f4f8"
    },
    {
        "name": "Sunset Fire",
        "primary": "#ff6b35",
        "secondary": "#f7931e",
        "accent": "#ffcd3c",
        "bg": "#2d1b1b",
        "text": "#fff8f0"
    },
    {
        "name": "Forest Mystic",
        "primary": "#2d5016",
        "secondary": "#3a6b35",
        "accent": "#8fbc8f",
        "bg": "#1a1a0d",
        "text": "#f0f8e8"
    },
    {
        "name": "Purple Galaxy",
        "primary": "#663399",
        "secondary": "#9933cc",
        "accent": "#cc99ff",
        "bg": "#1a0d1a",
        "text": "#f8f0ff"
    }
]

# Conceptos de sitios web creativos
SITE_CONCEPTS = [
    {"name": "Astral Photography", "theme": "photography", "desc": "Capturing cosmic moments"},
    {"name": "Neon Fitness Lab", "theme": "fitness", "desc": "High-tech workout experiences"},
    {"name": "Digital Zen Garden", "theme": "meditation", "desc": "Virtual mindfulness space"},
    {"name": "Cyber Coffee Co.", "theme": "coffee", "desc": "Futuristic café experience"},
    {"name": "Quantum Art Studio", "theme": "art", "desc": "Next-gen creative collective"},
    {"name": "Nova Tech Solutions", "theme": "tech", "desc": "Innovative software development"},
    {"name": "Ethereal Music Lab", "theme": "music", "desc": "Electronic sound experiments"},
    {"name": "Crystal Wellness Hub", "theme": "wellness", "desc": "Holistic health sanctuary"},
    {"name": "Pixel Perfect Agency", "theme": "design", "desc": "Creative digital solutions"},
    {"name": "Urban Explorer Co.", "theme": "travel", "desc": "City adventure guides"}
]

def generate_site() -> str:
    """Genera un sitio web completo y creativo"""
    try:
        # Seleccionar concepto y paleta aleatoria
        concept = random.choice(SITE_CONCEPTS)
        palette = random.choice(COLOR_PALETTES)
        
        # Crear carpeta para el sitio
        today = dt.datetime.now().strftime("%Y-%m-%d")
        site_name = concept["name"].lower().replace(" ", "_")
        
        output_dir = Path(__file__).parent.parent / "output" / today
        output_dir.mkdir(parents=True, exist_ok=True)
        
        site_dir = output_dir / f"web_{site_name}"
        site_dir.mkdir(exist_ok=True)
        
        # Generar archivos del sitio
        html_content = generate_html(concept, palette)
        css_content = generate_css(palette)
        js_content = generate_js(concept)
        
        # Escribir archivos
        (site_dir / "index.html").write_text(html_content, encoding="utf-8")
        (site_dir / "styles.css").write_text(css_content, encoding="utf-8")
        (site_dir / "script.js").write_text(js_content, encoding="utf-8")
        
        # Generar metadata
        metadata = {
            "type": "website",
            "concept": concept,
            "palette": palette,
            "created_at": dt.datetime.utcnow().isoformat() + "Z",
            "files": ["index.html", "styles.css", "script.js"]
        }
        
        (site_dir / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), 
            encoding="utf-8"
        )
        
        # Generar README
        readme_content = f"""# {concept['name']}

{concept['desc']}

## Detalles
- **Tema**: {concept['theme']}
- **Paleta**: {palette['name']}
- **Creado**: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Archivos
- `index.html` - Página principal
- `styles.css` - Estilos personalizados
- `script.js` - Interactividad
- `metadata.json` - Metadatos de generación

Abre `index.html` en tu navegador para ver el sitio.
"""
        
        (site_dir / "README.md").write_text(readme_content, encoding="utf-8")
        
        log.info(f"Sitio web generado: {concept['name']} con paleta {palette['name']}")
        return f"Sitio '{concept['name']}' generado en {site_dir.relative_to(output_dir.parent)}"
        
    except Exception as e:
        log.error(f"Error generando sitio web: {e}")
        raise

def generate_html(concept: dict, palette: dict) -> str:
    """Genera el HTML del sitio"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{concept['name']}</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <header class="hero-section">
        <nav class="navbar">
            <div class="nav-brand">{concept['name']}</div>
            <div class="nav-menu">
                <a href="#about">About</a>
                <a href="#services">Services</a>
                <a href="#contact">Contact</a>
            </div>
        </nav>
        
        <div class="hero-content">
            <h1 class="hero-title">{concept['name']}</h1>
            <p class="hero-subtitle">{concept['desc']}</p>
            <button class="cta-button" id="ctaBtn">Explore Now</button>
        </div>
        
        <div class="hero-visual">
            <div class="floating-elements">
                <div class="element element-1"></div>
                <div class="element element-2"></div>
                <div class="element element-3"></div>
            </div>
        </div>
    </header>

    <main>
        <section id="about" class="section about-section">
            <div class="container">
                <h2 class="section-title">About Us</h2>
                <div class="about-grid">
                    <div class="about-card">
                        <div class="card-icon">✨</div>
                        <h3>Innovation</h3>
                        <p>Pushing boundaries in {concept['theme']} with cutting-edge approaches.</p>
                    </div>
                    <div class="about-card">
                        <div class="card-icon">🚀</div>
                        <h3>Excellence</h3>
                        <p>Delivering premium experiences that exceed expectations.</p>
                    </div>
                    <div class="about-card">
                        <div class="card-icon">💎</div>
                        <h3>Quality</h3>
                        <p>Crafted with attention to detail and passion for perfection.</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="services" class="section services-section">
            <div class="container">
                <h2 class="section-title">Our Services</h2>
                <div class="services-grid">
                    <div class="service-card">
                        <h3>Premium {concept['theme'].title()}</h3>
                        <p>Experience the future of {concept['theme']} with our innovative solutions.</p>
                        <div class="service-price">Starting at $299</div>
                    </div>
                    <div class="service-card featured">
                        <h3>Elite Package</h3>
                        <p>Complete {concept['theme']} transformation with personal consultation.</p>
                        <div class="service-price">Starting at $599</div>
                    </div>
                    <div class="service-card">
                        <h3>Custom Solutions</h3>
                        <p>Tailored {concept['theme']} experiences designed just for you.</p>
                        <div class="service-price">Contact Us</div>
                    </div>
                </div>
            </div>
        </section>

        <section id="contact" class="section contact-section">
            <div class="container">
                <h2 class="section-title">Get In Touch</h2>
                <div class="contact-grid">
                    <div class="contact-info">
                        <h3>Ready to start your journey?</h3>
                        <p>Contact us today and let's create something amazing together.</p>
                        <div class="contact-details">
                            <div class="contact-item">
                                <span class="contact-icon">📧</span>
                                <span>hello@{concept['name'].lower().replace(' ', '')}.com</span>
                            </div>
                            <div class="contact-item">
                                <span class="contact-icon">📱</span>
                                <span>+1 (555) 123-4567</span>
                            </div>
                            <div class="contact-item">
                                <span class="contact-icon">📍</span>
                                <span>San Francisco, CA</span>
                            </div>
                        </div>
                    </div>
                    <div class="contact-form">
                        <form id="contactForm">
                            <input type="text" placeholder="Your Name" required>
                            <input type="email" placeholder="Your Email" required>
                            <textarea placeholder="Your Message" rows="4" required></textarea>
                            <button type="submit" class="submit-btn">Send Message</button>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <h3>{concept['name']}</h3>
                    <p>{concept['desc']}</p>
                </div>
                <div class="footer-links">
                    <div class="link-group">
                        <h4>Services</h4>
                        <a href="#">Premium {concept['theme'].title()}</a>
                        <a href="#">Consultations</a>
                        <a href="#">Custom Solutions</a>
                    </div>
                    <div class="link-group">
                        <h4>Company</h4>
                        <a href="#">About</a>
                        <a href="#">Team</a>
                        <a href="#">Careers</a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 {concept['name']}. Crafted with passion by Tektra.</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>"""

def generate_css(palette: dict) -> str:
    """Genera el CSS del sitio"""
    return f"""/* {palette['name']} Theme - Generated by Tektra */
:root {{
    --primary: {palette['primary']};
    --secondary: {palette['secondary']};
    --accent: {palette['accent']};
    --bg: {palette['bg']};
    --text: {palette['text']};
    --card-bg: {palette['bg']}dd;
    --shadow: 0 10px 30px rgba(0,0,0,0.3);
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    overflow-x: hidden;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}}

/* Header & Hero */
.hero-section {{
    min-height: 100vh;
    background: linear-gradient(135deg, var(--bg) 0%, var(--primary)20 100%);
    position: relative;
    display: flex;
    flex-direction: column;
}}

.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: var(--bg)95;
    backdrop-filter: blur(10px);
    z-index: 1000;
    transition: all 0.3s ease;
}}

.nav-brand {{
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}}

.nav-menu {{
    display: flex;
    gap: 2rem;
}}

.nav-menu a {{
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}}

.nav-menu a:hover {{
    color: var(--primary);
}}

.hero-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 8rem 2rem 2rem;
    position: relative;
    z-index: 2;
}}

.hero-title {{
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 700;
    background: linear-gradient(45deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
    animation: fadeInUp 1s ease-out;
}}

.hero-subtitle {{
    font-size: 1.5rem;
    margin-bottom: 2rem;
    opacity: 0.9;
    animation: fadeInUp 1s ease-out 0.2s both;
}}

.cta-button {{
    background: linear-gradient(45deg, var(--primary), var(--secondary));
    color: white;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    animation: fadeInUp 1s ease-out 0.4s both;
    box-shadow: var(--shadow);
}}

.cta-button:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.4);
}}

/* Floating Elements */
.hero-visual {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: hidden;
    z-index: 1;
}}

.floating-elements {{
    position: relative;
    width: 100%;
    height: 100%;
}}

.element {{
    position: absolute;
    border-radius: 50%;
    background: linear-gradient(45deg, var(--primary)40, var(--secondary)40);
    animation: float 6s ease-in-out infinite;
}}

.element-1 {{
    width: 100px;
    height: 100px;
    top: 20%;
    left: 10%;
    animation-delay: 0s;
}}

.element-2 {{
    width: 150px;
    height: 150px;
    top: 60%;
    right: 10%;
    animation-delay: 2s;
}}

.element-3 {{
    width: 80px;
    height: 80px;
    top: 40%;
    left: 80%;
    animation-delay: 4s;
}}

/* Sections */
.section {{
    padding: 6rem 0;
}}

.section-title {{
    font-size: 3rem;
    text-align: center;
    margin-bottom: 3rem;
    color: var(--primary);
}}

/* About Section */
.about-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}}

.about-card {{
    background: var(--card-bg);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    transition: transform 0.3s ease;
    border: 1px solid var(--primary)30;
    backdrop-filter: blur(10px);
}}

.about-card:hover {{
    transform: translateY(-10px);
}}

.card-icon {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.about-card h3 {{
    color: var(--primary);
    margin-bottom: 1rem;
    font-size: 1.5rem;
}}

/* Services Section */
.services-section {{
    background: linear-gradient(45deg, var(--bg) 0%, var(--secondary)10 100%);
}}

.services-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}}

.service-card {{
    background: var(--card-bg);
    padding: 2rem;
    border-radius: 20px;
    transition: all 0.3s ease;
    border: 1px solid var(--primary)30;
    position: relative;
}}

.service-card.featured {{
    border: 2px solid var(--primary);
    transform: scale(1.05);
}}

.service-card:hover {{
    transform: translateY(-10px);
    box-shadow: var(--shadow);
}}

.service-card h3 {{
    color: var(--primary);
    margin-bottom: 1rem;
    font-size: 1.5rem;
}}

.service-price {{
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--secondary);
    margin-top: 1rem;
}}

/* Contact Section */
.contact-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    margin-top: 2rem;
}}

.contact-details {{
    margin-top: 2rem;
}}

.contact-item {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}}

.contact-icon {{
    font-size: 1.2rem;
}}

.contact-form {{
    background: var(--card-bg);
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid var(--primary)30;
}}

.contact-form input,
.contact-form textarea {{
    width: 100%;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid var(--primary)30;
    border-radius: 10px;
    background: var(--bg)80;
    color: var(--text);
    font-family: inherit;
}}

.submit-btn {{
    background: linear-gradient(45deg, var(--primary), var(--secondary));
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    width: 100%;
}}

.submit-btn:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}}

/* Footer */
.footer {{
    background: var(--bg)95;
    padding: 3rem 0 1rem;
    border-top: 1px solid var(--primary)30;
}}

.footer-content {{
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 3rem;
    margin-bottom: 2rem;
}}

.footer-brand h3 {{
    color: var(--primary);
    margin-bottom: 1rem;
}}

.footer-links {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 2rem;
}}

.link-group h4 {{
    color: var(--secondary);
    margin-bottom: 1rem;
}}

.link-group a {{
    display: block;
    color: var(--text)80;
    text-decoration: none;
    margin-bottom: 0.5rem;
    transition: color 0.3s ease;
}}

.link-group a:hover {{
    color: var(--primary);
}}

.footer-bottom {{
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--primary)20;
    color: var(--text)70;
}}

/* Animations */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes float {{
    0%, 100% {{
        transform: translateY(0) rotate(0deg);
    }}
    33% {{
        transform: translateY(-20px) rotate(120deg);
    }}
    66% {{
        transform: translateY(10px) rotate(240deg);
    }}
}}

/* Responsive */
@media (max-width: 768px) {{
    .nav-menu {{
        display: none;
    }}
    
    .contact-grid {{
        grid-template-columns: 1fr;
    }}
    
    .footer-content {{
        grid-template-columns: 1fr;
    }}
    
    .hero-title {{
        font-size: 3rem;
    }}
    
    .section {{
        padding: 3rem 0;
    }}
}}

/* Smooth scrolling */
html {{
    scroll-behavior: smooth;
}}

/* Custom scrollbar */
::-webkit-scrollbar {{
    width: 8px;
}}

::-webkit-scrollbar-track {{
    background: var(--bg);
}}

::-webkit-scrollbar-thumb {{
    background: var(--primary);
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: var(--secondary);
}}"""

def generate_js(concept: dict) -> str:
    """Genera el JavaScript del sitio"""
    return f"""// {concept['name']} - Interactive Experience by Tektra
document.addEventListener('DOMContentLoaded', function() {{
    
    // Smooth navbar background transition on scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {{
        if (window.scrollY > 100) {{
            navbar.style.background = 'var(--bg)';
            navbar.style.boxShadow = 'var(--shadow)';
        }} else {{
            navbar.style.background = 'var(--bg)95';
            navbar.style.boxShadow = 'none';
        }}
    }});

    // CTA Button interaction
    const ctaBtn = document.getElementById('ctaBtn');
    ctaBtn.addEventListener('click', function() {{
        // Scroll to services section
        document.getElementById('services').scrollIntoView({{
            behavior: 'smooth'
        }});
        
        // Add pulse animation
        this.style.animation = 'pulse 0.6s ease-out';
        setTimeout(() => {{
            this.style.animation = '';
        }}, 600);
    }});

    // Contact form handling
    const contactForm = document.getElementById('contactForm');
    contactForm.addEventListener('submit', function(e) {{
        e.preventDefault();
        
        const submitBtn = this.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        
        // Show loading state
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        // Simulate form submission
        setTimeout(() => {{
            submitBtn.textContent = 'Message Sent! ✨';
            submitBtn.style.background = 'linear-gradient(45deg, #00ff88, #00cc66)';
            
            setTimeout(() => {{
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                submitBtn.style.background = '';
                this.reset();
            }}, 2000);
        }}, 1500);
    }});

    // Parallax effect for floating elements
    window.addEventListener('scroll', () => {{
        const scrolled = window.pageYOffset;
        const parallax = document.querySelectorAll('.element');
        const speed = 0.5;

        parallax.forEach(element => {{
            const yPos = -(scrolled * speed);
            element.style.transform = `translate3d(0, ${{yPos}}px, 0)`;
        }});
    }});

    // Card hover effects with random colors
    const cards = document.querySelectorAll('.about-card, .service-card');
    cards.forEach(card => {{
        card.addEventListener('mouseenter', function() {{
            const colors = ['var(--primary)', 'var(--secondary)', 'var(--accent)'];
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            this.style.borderColor = randomColor + '80';
            this.style.boxShadow = `0 15px 40px ${{randomColor}}30`;
        }});
        
        card.addEventListener('mouseleave', function() {{
            this.style.borderColor = '';
            this.style.boxShadow = '';
        }});
    }});

    // Intersection Observer for animations
    const observerOptions = {{
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    }};

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
            }}
        }});
    }}, observerOptions);

    // Observe all sections and cards
    document.querySelectorAll('.section, .about-card, .service-card').forEach(el => {{
        el.style.opacity = '0';
        observer.observe(el);
    }});

    // Dynamic background particles
    function createParticle() {{
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            width: 4px;
            height: 4px;
            background: var(--primary);
            border-radius: 50%;
            pointer-events: none;
            z-index: -1;
            animation: particle-float 8s linear forwards;
        `;
        
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.top = '100vh';
        
        document.body.appendChild(particle);
        
        setTimeout(() => {{
            particle.remove();
        }}, 8000);
    }}

    // Create particles periodically
    setInterval(
