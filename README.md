# 🧙‍♂️ Geny

**Maker Bot** es un duende digital que nunca se queda quieto:  
mientras vos hacés tus cosas, va creando **arte random**, **mini-páginas web** y **juegos simples** por su cuenta.  
Cuando le preguntás “¿novedades?”, te cuenta todo lo que fabricó hasta el momento.

---

## 🚀 Qué hace
- Genera **imágenes épicas** a partir de prompts aleatorios.
- Crea **landing pages** con HTML/CSS/JS en estilos variados.
- Construye **juegos clásicos simples** como Snake.
- Guarda todo en la carpeta `output/<fecha>/`.
- Mantiene un registro en SQLite (`log/status.db`).
- Expone una API minimal con Flask:
  - `GET /quehaces` → qué fue lo último que generó.
  - `GET /novedades` → lista de los últimos ítems creados.

---

## 📂 Estructura
🤖 Ejecución automática con GitHub Actions

El bot también puede correr en la nube con GitHub Actions:
	•	Workflow en .github/workflows/maker-bot.yml:
	•	Se ejecuta cada 20 minutos (cron).
	•	También en cada push o manualmente desde la pestaña Actions.
	•	Cada run:
	1.	Corre orchestrator.py una vez.
	2.	Guarda lo generado en output/.
	3.	Hace commit automático al repo.

⸻

🔧 Configuración

Archivo config.yaml:
	•	interval_minutes: intervalo de creación (local).
	•	daily_budget_usd: límite de costo por día (para APIs de imágenes).
	•	max_items_per_day: cantidad máxima de imágenes, webs y juegos.
	•	random_weights: probabilidad relativa de cada tipo de creación.
	•	paths: rutas para salidas y DB.
	•	telegram: (opcional) para integrarlo con un bot de Telegram.

⸻

🖼️ Generación de imágenes

Actualmente factory_images.py guarda un placeholder.
Para imágenes reales podés conectar:
	•	OpenAI Images (gpt-image-1)
	•	Replicate (ej. stability-ai/sdxl)
	•	O tu propio backend local.

Solo reemplazá el TODO en factory_images.py y usá tu clave de API desde variables de entorno.

⸻

📜 Licencia

Este proyecto es experimental y abierto. Usalo, hackealo y mejoralo.

⸻

🌟 Futuras mejoras
	•	Integrar Telegram Bot para preguntar desde el celu /quehaces y /novedades.
	•	Publicar automáticamente webs en GitHub Pages.
	•	Más fábricas: música generativa, relatos, datasets raros
