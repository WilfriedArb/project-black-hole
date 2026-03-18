---

# 🕳️ Gravitational Lens Simulation

This project simulates the light deflection caused by massive objects (like black holes) using **Fermat** principles and **Eikonal** equation. It leverages **Taichi Lang** for high-performance physical computing and **Streamlit** for a live, interactive web interface.

## 🚀 Live Demo

CPU computing : https://project-black-hole-nvssmzbs5jh6eryw2ozeqj.streamlit.app/
GPU computing : https://wilfriedarb.github.io/project-black-hole/

## 🌟 Features

This project is split into three specialized branches to balance performance and accessibility:

### 1. `main` Branch: High-Fidelity (Local GPU)

* **Backend:** Taichi with **Vulkan** (GPU).
* **Resolution:** Full HD (1920x1080).
* **Performance:** Real-time or near-real-time rendering using thousands of GPU cores.
* **Accuracy:** High-precision ray marching with 600+ steps per pixel.

### 2. `website` Branch: Web-Optimized (Streamlit Cloud)

* **Backend:** Taichi with **CPU** (Portable).
* **Resolution:** Optimized low-res (e.g., 480p) for fluidity on web servers.
* **Interface:** Interactive sliders to adjust mass, distance, and resolution in real-time.
* **Hosting:** Deployed live on Streamlit Cloud.

### 3. `webgpu` Branch: Local GPU on web page

* **Backend:** Taichi with **GPU**.
* **Resolution:** Optimized low-res (e.g., 480p) for fluidity on web servers.
* **Interface:** Interactive sliders to adjust Schwarzschild radius in real-time.
* **Developpment:** AI convertion of the main python program into html.

---

## 🔬 Physics Background

It is physically impossible to create a standard optical lens that perfectly mimics a black hole because the refractive index would need to be infinite at the event horizon.

To solve this, the simulation uses an **effective refractive index** approach derived from the **Schwarzschild metric**. If a ray passes within the Schwarzschild radius, it is "captured," and the corresponding pixel is rendered black, forming the shadow of the black hole.

---

## 🚀 Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/wilfriedarb/gravitational-lens.git
cd gravitational-lens

```


2. Install dependencies:
```bash
pip install -r requirements.txt

```



### Running the App

* **To run the interactive web version:**
```bash
streamlit run app.py

```


* **To run the high-res GPU simulation (requires Vulkan):**
Ensure you are on the `main` branch and run your executable script.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Parallel Computing:** [Taichi Lang](https://www.taichi-lang.org/)
* **Web Interface:** [Streamlit](https://streamlit.io/)
* **Numerics:** NumPy

---

## 📈 Roadmap

* [x] 2D deflection simulation.
* [x] 3D Ray-Tracing (Ray Marching) implementation.
* [x] GPU acceleration via Vulkan.
* [x] Streamlit Cloud deployment (CPU version).
* [ ] **Next Step:** Compute de real geodesic equations of photons nearby a Schwarzschild Black Hole.

---
