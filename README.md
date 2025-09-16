# ⚡ Tektra

**Tektra** is an autonomous bot that randomly generates **epic images**, **complete websites**, and **simple games**.  
All creations are automatically stored in `output/<date>/` with a clear index of progress and metadata.  

Tektra can run via **GitHub Actions** (cron jobs) or on a **Flask server**, and provides endpoints to check the latest outputs.  
Its mission: keep creating while you’re away — a digital forge that never sleeps.  

The name **Tektra** comes from the Greek word *téktōn* (τέκτων), meaning “craftsman” or “builder.”  
It captures the project’s essence: an endless digital artisan forging creations with autonomy, diversity, and imagination.  

**Creativity never sleeps, neither does Tektra.**

---

## ✨ Features

- 🎨 **Epic image generation**  
  Detailed prompts create unique and impressive visuals.  
  Each image is saved with metadata for reproducibility.

- 🌐 **Mini-websites**  
  Responsive HTML/CSS/JS pages with coherent design, palettes, and narratives.  
  Each site includes a landing page, navigation, footer, and functional links.

- 🎮 **Simple games**  
  Beyond Snake: Tektra generates aesthetic, minimal games with clear mechanics and victory conditions.

- 📂 **Organized outputs**  
  Creations are saved in `output/YYYY-MM-DD/` with an index for easy exploration.

- ⚙️ **Automation**  
  Runs automatically on a schedule via GitHub Actions, or locally with Flask.

- 📡 **API endpoints**  
  Check the latest creation with `/quehaces` and recent activity with `/novedades`.

---

## 🚀 Objectives

- Provide **autonomous creation** so new content appears without user input.  
- Ensure **variety** across images, sites, and games.  
- Deliver **accessible outputs** that anyone can explore directly.  
- Build a foundation for future expansion: more generators, better visuals, richer games.  

---

## 🌱 Values

- **Autonomy** → Tektra creates continuously without intervention.  
- **Diversity** → Outputs span multiple formats for richness and surprise.  
- **Accessibility** → Clear file structures and easy-to-explore outputs.  
- **Endless creativity** → Like a modern *téktōn*, Tektra never stops forging.  

---

## 🛠️ Installation

### Clone the repository
```bash
git clone https://github.com/<your-username>/Tektra.git
cd Tektra
Create a virtual environment
bash
Copiar código
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
Install dependencies
bash
Copiar código
pip install -r requirements.txt
⚙️ Usage
Local run with Flask
bash
Copiar código
python app.py
Then open http://localhost:5000 to check endpoints.

With GitHub Actions
A workflow file (.github/workflows/maker-bot.yml) triggers orchestrator.py periodically.
Outputs are committed automatically to the repo under output/.

📂 Output Structure
pgsql
Copiar código
output/
  2025-09-15/
    img_galaxy_1234.png
    metadata.json
    /web_mythica/
       index.html
       styles.css
       script.js
    /game_orbital/
       index.html
    index.md
Images → named with prompt slug and timestamp.

Websites → self-contained folders with README.

Games → playable in browser.

Index → summary of daily creations.

📡 API Endpoints (Flask)
/quehaces → Returns the latest creation.

/novedades → Returns recent creations.

These can be integrated with Telegram bots or other clients.

🤖 Roadmap
Expand game library beyond 300 random concepts.

Smarter prompt generation for more detailed images.

Mobile-friendly interface with Telegram bot.

Publish outputs via GitHub Pages.

Add cost control & daily limits with config.yaml.

🧑‍💻 Contributing
Pull requests are welcome!
Ideas for new generators (games, image styles, website templates) are especially appreciated.

📄 License
This project is licensed under the MIT License.
See the LICENSE file for details.
