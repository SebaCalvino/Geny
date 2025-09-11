import random, uuid
from pathlib import Path

THEMES = [
  "catedrales bioluminiscentes en selvas nubladas",
  "naves de papel gigantes sobre océanos de tinta",
  "ciudades colgantes al atardecer con neblina",
  "desiertos con fósiles de ballenas y auroras"
]

def make_images(outdir: Path):
    theme = random.choice(THEMES)
    prompt = f"Epic, cinematic, ultra-detailed concept art of {theme}"
    img_id = str(uuid.uuid4())[:8]
    img_path = outdir / f"img_{img_id}.png"

    # TODO: Integrar con API de imágenes (OpenAI, Replicate, etc.)
    img_path.write_bytes(b"")  # placeholder

    title = f"Imagen épica — {theme}"
    return title, img_path.relative_to(Path.cwd()), 0.02, {"prompt": prompt}
