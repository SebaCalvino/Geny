# factories/factory_images.py
import os
import base64
import random
from pathlib import Path
from datetime import datetime

try:
    from openai import OpenAI
except Exception:
    raise RuntimeError("Falta instalar 'openai'. Agregalo en requirements.txt")

# ---------- Prompt scaffolding para fotorrealismo ----------
CAMERAS = [
    "Sony A7R IV con lente 85mm f/1.4",
    "Canon R5 con lente 50mm f/1.2",
    "Nikon Z9 con 35mm f/1.4",
    "Fujifilm GFX100 con 110mm f/2",
    "ARRI Alexa LF, anamórfico 40mm (fotograma cinematográfico)"
]

LIGHTING = [
    "luz dorada de atardecer (golden hour)",
    "luz suave rebotada por ventana grande",
    "luz dura cenital estilo editorial",
    "neón cian-magenta con rim light",
    "día nublado con contraste suave"
]

POST = [
    "detalle de piel realista y poros visibles",
    "bokeh cremoso con viñeteo ligero",
    "grano fotográfico ISO 400",
    "color grading cinematográfico",
    "HDR sutil con sombras detalladas"
]

SUBJECTS = [
    "retrato close-up de una persona pensando",
    "un café humeante sobre una mesa de madera antigua",
    "auto clásico estacionado en calle mojada de noche",
    "chef emplatando en una cocina profesional",
    "montaña nevada con un caminante en primer plano",
    "perro corriendo en la playa, gotas de agua congeladas",
    "ciudad futurista bajo lluvia con letreros de neón"
]

def build_prompt(topic: str | None = None) -> str:
    subject = topic or random.choice(SUBJECTS)
    cam = random.choice(CAMERAS)
    light = random.choice(LIGHTING)
    post = ", ".join(random.sample(POST, 2))
    return (
        f"{subject}. Fotografía hiper-realista, {cam}. "
        f"Iluminación: {light}. Profundidad de campo corta, enfoque nítido en el sujeto. "
        f"{post}. Evitar estilo ilustración o 3D. Sin texto, sin marcas de agua."
    )

# ---------- Generador ----------
def make_images(base_dir: Path, how_many: int = 3, topic: str | None = None):
    """
    Genera 'how_many' imágenes realistas en base_dir usando OpenAI Images (gpt-image-1).
    Devuelve: (titulo, relative_path, costo_estimado, meta_dict)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("No se encontró OPENAI_API_KEY en el entorno del workflow.")

    client = OpenAI(api_key=api_key)
    outdir = Path(base_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    created = []
    for i in range(how_many):
        prompt = build_prompt(topic)
        resp = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            quality="high",
            n=1
        )

        b64 = resp.data[0].b64_json
        img_bytes = base64.b64decode(b64)
        fname = f"img_{datetime.utcnow().strftime('%H%M%S')}_{i:02d}.png"
        fpath = outdir / fname
        with open(fpath, "wb") as f:
            f.write(img_bytes)

        est_cost = 0.04  # USD aprox por imagen 1024x1024

        created.append((
            "Foto fotorrealista — " + (topic or "random"),
            fpath,
            est_cost,
            {"prompt": prompt, "provider": "openai:gpt-image-1"}
        ))

    title, path, cost, meta = created[-1]
    relpath = path.relative_to(Path.cwd())
    return title, relpath, cost, meta
