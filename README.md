
# 🏭 MechanicAI | Text-to-CAD Agent

**MechanicAI** is an AI-powered CAD generation tool that transforms natural language descriptions into professional-grade 3D mechanical components. Built on the **build123d** ecosystem, it leverages specialized libraries to ensure industrial accuracy for gears, fasteners, and bearings.

## 🚀 Features

* **Natural Language to 3D**: Generate complex geometry like gears, bolts, and flanges using simple English prompts.
* **Interactive Parameter Tuning**: Fine-tune your designs in real-time using sidebar sliders generated automatically from the AI's code.
* **Professional Libraries**:
* **Gears**: High-fidelity Spur, Helical, Bevel, and Cycloidal gears via `gggears`.
* **Standard Parts**: ISO-standard bolts, nuts, washers, and bearings via `bd-warehouse`.


* **Multi-Format Export**: Download your creations as **STL** (for 3D printing/web viewing) or **STEP** (for professional CAD software like Fusion 360 or Ansys).

---

## 🛠️ Technical Stack

| Component | Technology |
| --- | --- |
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **CAD Engine** | [build123d](https://github.com/gumyr/build123d) |
| **AI Orchestration** | `smolagents` & `litellm` |
| **LLM Support** | Groq (Llama 3.3) & Google (Gemini 2.0 Flash) |
| **3D Rendering** | `streamlit-stl` & `trimesh` |

---

## 📦 Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/MechanicAI.git
cd MechanicAI

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Configure Secrets:**
Create a `.env` or use Streamlit's `secrets.toml` to add your API keys:
* `GEMINI_API_KEY`
* `GROQ_API_KEY`


4. **Run the App:**
```bash
streamlit run app.py

```



---

## 🧩 Usage Examples

Try entering these prompts into the chat interface:

* *"Create an M8 hex bolt with 45mm length"*
* *"Generate a 24-tooth spur gear with module 2 and a 10mm bore"*
* *"Design a ball bearing size M20-40-8"*
* *"Create a 2-inch steel pipe section with a slip-on flange"*

---

## ❤️ Credits & Acknowledgments

This project stands on the shoulders of incredible open-source mechanical engineering libraries:

* **[bd-warehouse](https://github.com/gumyr/bd_warehouse)**: Created by **gumyr**. This library provides the professional-grade fasteners, bearings, and piping components used in MechanicAI.
* **[gggears](https://www.google.com/search?q=https://github.com/clalancette/gggears)**: Created by **clalancette**. This library is responsible for the precise involute and cycloidal gear geometries.
* **[build123d](https://github.com/gumyr/build123d)**: The core functional CAD framework that makes script-based 3D modeling possible.

---

## 👨‍💻 About the Author

Developed by a Mechanical Engineering student at **Zakir Husain College of Engineering and Technology (ZHCET)**, AMU. This project is part of an ongoing exploration into **Generative AI for Mechanical Design**.

---

