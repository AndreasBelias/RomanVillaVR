# RomanVillaVR

**RomanVillaVR** is a professional virtual reality reconstruction of an ancient Roman *domus*. Developed using the **Vizard** VR toolkit and **3ds Max**, this project integrates historical research with modern 3D asset optimization to create an authentic ancient environment.

## Project Overview
This simulation allows users to explore a historically accurate Roman residence. The project focuses on high-fidelity asset integration, realistic atmospheric lighting, and interactive elements designed for immersive VR exploration.

## Technical Implementation

### 3D Scanning and Artifacts
To enhance the realism of the villa, a 3D scanner was used to digitize two real-world busts:
* **Hippocrates**
* **Marcus Agrippa**

These high-resolution assets were processed and integrated into the villa to provide museum-quality detail that traditional modeling cannot easily replicate.

### Lighting and Environment
* **Atmospheric Lighting:** The interior features a realistic lighting system using torches that cast a specific orange and yellow spectrum to mimic firelight.
* **Custom Sunset Skybox:** Due to specific scene requirements, the native Vizard sky cubemap was manually modified. The color channels were adjusted to simulate a realistic sunset horizon, providing the desired ambient lighting for the exterior without the need for external assets.

### Interactivity
* **Realistic Door Mechanics:** Utilizing the Vizard **Grabber tool**, the villa features interactive doors. This provides users with a tactile method of navigating the space, improving the sense of presence within the VR environment.

### Performance Optimization
To ensure the project is accessible on lower-end hardware and standalone devices, the **ProOptimizer** tool in 3ds Max was utilized. This process involved:
* Reducing the polygon count of complex architectural meshes.
* Maintaining visual fidelity while minimizing the rendering load to ensure high frame rates.

## Historical Research
The villa's layout is based on a study of real-life Roman *domus* architecture. By combining academic research with personal historical knowledge, the final result is a synthesis of structural accuracy and educational value, reflecting the typical social and functional flow of a Roman household.

## Screenshots
The following images demonstrate the villa's lighting, architecture, and scanned artifacts. These images are located in the `/VillaImages` directory of this repository.

| Atrium View | Marcus Agrippa Bust |
| :--- | :--- |
| ![Atrium](./VillaImages/atrium.jpg) | ![Agrippa](./VillaImages/agrippa.jpg) |

| Items | Peristylium |
| :--- | :--- |
| ![Items](./VillaImages/sunset.jpg) | ![Peristylium](./VillaImages/doors.jpg) |

## Built With
* **Vizard VR Toolkit**
* **Autodesk 3ds Max**
* **3D Scanning Technology**
* **Python**

---

**Author:** Andreas Belias  
**Field:** VR Development / 3D Modeling / Historical Reconstruction
