#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image Factory para Tektra - Genera prompts épicos para imágenes
"""

import random
import datetime as dt
from pathlib import Path
import json
import logging

log = logging.getLogger("tektra.image_factory")

# Estilos artísticos épicos
ART_STYLES = [
    "cyberpunk neon aesthetic",
    "ethereal fantasy art",
    "cosmic space art",
    "dark gothic atmosphere",
    "vibrant synthwave",
    "minimalist geometric",
    "organic biomechanical",
    "surreal dreamscape",
    "apocalyptic wasteland",
    "crystal formations",
    "flowing liquid metal",
    "glowing plasma energy",
    "fractal mathematics",
    "ancient mystical symbols",
    "futuristic holographic"
]

# Subjects/Temas principales
SUBJECTS = [
    "majestic dragon soaring through storm clouds",
    "lone warrior standing at cliff edge",
    "mystical forest with glowing mushrooms",
    "cybernetic city skyline at midnight",
    "ethereal being made of pure light",
    "ancient temple hidden in jungle",
    "mechanical phoenix rising from ashes",
    "crystalline cavern with floating gems",
    "interdimensional portal crackling with energy",
    "ghostly ship sailing through nebula",
    "biomechanical tree with metal roots",
    "floating islands connected by light bridges",
    "cosmic whale swimming through stars",
    "ruined cathedral overgrown with vines",
    "quantum particles forming geometric patterns",
    "elemental guardian of fire and ice",
    "steampunk airship in cloudy sky",
    "alien landscape with multiple moons",
    "digital consciousness manifesting as light",
    "ancient wizard's tower reaching into clouds"
]

# Ambientes/Settings
ENVIRONMENTS = [
    "in a realm beyond time and space",
    "during a spectacular aurora storm",
    "in the depths of an alien ocean",
    "atop a mountain of crystallized lightning",
    "within a collapsing dimensional rift",
    "surrounded by floating geometric shapes",
    "in a city where gravity flows upward",
    "during the birth of a new star",
    "in a forest where trees are made of light",
    "on a planet with rings of pure energy",
    "inside a massive geode cathedral",
    "during an eclipse of three suns",
    "in a realm where colors have physical form",
    "surrounded by cascading waterfalls of light",
    "in a library containing infinite knowledge"
]

# Elementos técnicos para calidad
TECHNICAL_SPECS = [
    "8K ultra detailed",
    "photorealistic rendering",
    "volumetric lighting",
    "ray-traced reflections",
    "particle effects",
    "depth of field blur",
    "cinematic composition",
    "dramatic lighting",
    "high dynamic range",
    "subsurface scattering",
    "atmospheric haze",
    "lens flares",
    "motion blur effects",
    "macro photography detail",
    "professional color grading"
]

# Mood/Atmosphere
MOODS = [
    "epic and awe-inspiring",
    "mysteriously beautiful",
    "hauntingly atmospheric",
    "vibrantly energetic",
    "serenely peaceful",
    "dramatically intense",
    "magically enchanting",
    "ominously powerful",
    "ethereally dreamy",
    "dynamically explosive"
]

def generate_image() -> str:
    """Genera un prompt épico para imagen y guarda los metadatos"""
    try:
        # Seleccionar elementos aleatorios
        style = random.choice(ART_STYLES)
        subject = random.choice(SUBJECTS)
        environment = random.choice(ENVIRONMENTS)
        tech_spec = random.choice(TECHNICAL_SPECS)
        mood = random.choice(MOODS)
        
        # Agregar elementos adicionales aleatorios
        additional_specs = random.sample(TECHNICAL_SPECS, random.randint(2, 4))
        
        # Construir el prompt
        prompt = f"{subject} {environment}, {style}, {mood}, {tech_spec}, {', '.join(additional_specs)}, masterpiece quality, trending on ArtStation"
        
        # Crear nombre de archivo único
        today = dt.datetime.now().strftime("%Y-%m-%d")
        timestamp = dt.datetime.now().strftime("%H%M%S")
        subject_slug = subject.split()[0:2]  # Primeras 2 palabras del subject
        subject_slug = "_".join(word.lower().replace(',', '') for word in subject_slug)
        
        filename = f"img_{subject_slug}_{timestamp}.txt"
        
        # Crear carpeta de salida
        output_dir = Path(__file__).parent.parent / "output" / today
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar el prompt en un archivo de texto
        prompt_file = output_dir / filename
        prompt_file.write_text(prompt, encoding="utf-8")
        
        # Generar metadata detallada
        metadata = {
            "type": "image_prompt",
            "filename": filename,
            "prompt": prompt,
            "components": {
                "style": style,
                "subject": subject,
                "environment": environment,
                "mood": mood,
                "technical_specs": [tech_spec] + additional_specs
            },
            "created_at": dt.datetime.utcnow().isoformat() + "Z",
            "prompt_length": len(prompt),
            "estimated_tokens": len(prompt.split())
        }
        
        # Guardar metadata
        metadata_file = output_dir / f"{filename.replace('.txt', '_metadata.json')}"
        metadata_file.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        
        # Generar README con instrucciones
        readme_content = f"""# Image Prompt: {subject_slug.replace('_', ' ').title()}

**Generated**: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Prompt
```
{prompt}
```

## Components
- **Style**: {style}
- **Subject**: {subject}
- **Environment**: {environment}  
- **Mood**: {mood}
- **Technical**: {', '.join([tech_spec] + additional_specs)}

## Usage Instructions
1. Copy the prompt from `{filename}`
2. Use with any AI image generator (DALL-E, Midjourney, Stable Diffusion, etc.)
3. Adjust technical specifications based on your preferred platform
4. The prompt is optimized for high-quality, detailed outputs

## Tips
- For Midjourney: Add `--ar 16:9 --v 6` for cinematic aspect ratio
- For DALL-E: The prompt works as-is
- For Stable Diffusion: Consider adding negative prompts like "low quality, blurry, distorted"

Generated by **Tektra** - The autonomous digital craftsman ⚡
"""
        
        readme_file = output_dir / f"{filename.replace('.txt', '_README.md')}"
        readme_file.write_text(readme_content, encoding="utf-8")
        
        log.info(f"Prompt de imagen generado: {subject_slug}")
        return f"Prompt '{subject_slug}' generado en {filename}"
        
    except Exception as e:
        log.error(f"Error generando prompt de imagen: {e}")
        raise

def generate_batch_prompts(count: int = 5) -> list:
    """Genera múltiples prompts de imagen"""
    results = []
    for i in range(count):
        try:
            result = generate_image()
            results.append(result)
        except Exception as e:
            log.error(f"Error generando prompt {i+1}/{count}: {e}")
            results.append(f"Error en prompt {i+1}: {str(e)}")
    return results

def get_prompt_stats() -> dict:
    """Retorna estadísticas sobre los prompts disponibles"""
    return {
        "total_styles": len(ART_STYLES),
        "total_subjects": len(SUBJECTS),
        "total_environments": len(ENVIRONMENTS),
        "total_technical_specs": len(TECHNICAL_SPECS),
        "total_moods": len(MOODS),
        "possible_combinations": len(ART_STYLES) * len(SUBJECTS) * len(ENVIRONMENTS) * len(MOODS),
        "estimated_unique_prompts": "Millions+"
    }

# Función adicional para generar prompts temáticos
def generate_themed_image(theme: str) -> str:
    """Genera un prompt basado en un tema específico"""
    theme_mappings = {
        "cosmic": {
            "styles": ["cosmic space art", "ethereal fantasy art", "vibrant synthwave"],
            "subjects": ["cosmic whale swimming through stars", "interdimensional portal crackling with energy", "ghostly ship sailing through nebula"],
            "environments": ["during the birth of a new star", "on a planet with rings of pure energy", "in a realm beyond time and space"]
        },
        "cyberpunk": {
            "styles": ["cyberpunk neon aesthetic", "futuristic holographic", "flowing liquid metal"],
            "subjects": ["cybernetic city skyline at midnight", "mechanical phoenix rising from ashes", "digital consciousness manifesting as light"],
            "environments": ["in a city where gravity flows upward", "surrounded by floating geometric shapes", "within a collapsing dimensional rift"]
        },
        "fantasy": {
            "styles": ["ethereal fantasy art", "ancient mystical symbols", "organic biomechanical"],
            "subjects": ["majestic dragon soaring through storm clouds", "ancient temple hidden in jungle", "mystical forest with glowing mushrooms"],
            "environments": ["in a forest where trees are made of light", "inside a massive geode cathedral", "during an eclipse of three suns"]
        }
    }
    
    if theme.lower() in theme_mappings:
        theme_data = theme_mappings[theme.lower()]
        style = random.choice(theme_data["styles"])
        subject = random.choice(theme_data["subjects"])
        environment = random.choice(theme_data["environments"])
    else:
        # Fallback a generación normal si el tema no existe
        return generate_image()
    
    # Continuar con la generación normal usando los elementos seleccionados
    tech_spec = random.choice(TECHNICAL_SPECS)
    mood = random.choice(MOODS)
    additional_specs = random.sample(TECHNICAL_SPECS, random.randint(2, 4))
    
    prompt = f"{subject} {environment}, {style}, {mood}, {tech_spec}, {', '.join(additional_specs)}, masterpiece quality, trending on ArtStation"
    
    # Guardar igual que en generate_image() pero con prefijo temático
    today = dt.datetime.now().strftime("%Y-%m-%d")
    timestamp = dt.datetime.now().strftime("%H%M%S")
    filename = f"img_{theme}_{timestamp}.txt"
    
    output_dir = Path(__file__).parent.parent / "output" / today
    output_dir.mkdir(parents=True, exist_ok=True)
    
    prompt_file = output_dir / filename
    prompt_file.write_text(prompt, encoding="utf-8")
    
    log.info(f"Prompt temático '{theme}' generado")
    return f"Prompt temático '{theme}' generado en {filename}"
