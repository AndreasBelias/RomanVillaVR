# RomanVillaVR

**RomanVillaVR** is an immersive virtual reality reconstruction of an ancient Roman *domus*. Developed using the **Vizard VR Toolkit**, **Python**, and **Autodesk 3ds Max**, the project combines historical research, 3D scanning, interactive VR elements, lighting design, and 3D asset optimization to create a historically informed ancient environment.

## Project Overview

The simulation allows users to explore a reconstructed Roman residence in an immersive virtual environment.

The project focuses on:

- Detailed 3D asset integration
- Atmospheric lighting
- Interactive elements
- Historical architectural research
- Performance-aware scene optimization
- Integration of 3D-scanned artifacts

## Technical Implementation

### 3D Scanning and Artifacts

A 3D scanner was used to digitize two real-world busts:

- **Hippocrates**
- **Marcus Agrippa**

The scanned models were processed, optimized, and integrated into the virtual villa as high-detail digital artifacts.

This part of the project involved:

- 3D scanning
- Mesh processing
- Texture integration
- Scene placement
- Performance optimization

### Lighting and Environment

The environment includes a custom lighting setup designed to create an immersive atmosphere.

#### Atmospheric Lighting

The interior uses torch-inspired lighting with warm orange and yellow tones to simulate firelight inside the villa.

#### Custom Sunset Skybox

The native Vizard sky cubemap was manually modified to create a sunset environment.

The image color channels were adjusted to produce a warmer horizon and provide suitable ambient lighting for the exterior areas of the villa.

### Interactivity

#### Interactive Door Mechanics

The villa includes interactive doors implemented using the Vizard **Grabber** tool.

This allows users to interact with doors while navigating the environment, improving immersion and the sense of presence inside the virtual space.

### Performance Optimization

The **ProOptimizer** tool in Autodesk 3ds Max was used to reduce the complexity of selected architectural meshes.

The optimization process focused on:

- Reducing polygon counts
- Preserving the visual appearance of the scene
- Lowering rendering requirements
- Improving performance on lower-end hardware

## Historical Research

The villa layout was designed based on research into Roman *domus* architecture.

The reconstruction includes spaces commonly associated with Roman domestic buildings, such as:

- The atrium
- The peristylium
- Interior living areas
- Decorative spaces
- Household and architectural objects

The project combines historical research with virtual reality and 3D development to create an educational and explorable representation of a Roman residence.

## Repository Structure

```text
RomanVillaVR/
├── src/
│   ├── Roman Villa Final.py
│   ├── headset_config.py
│   └── vizconnect_config.py
├── exported/
│   └── Legacy runtime files from an earlier project version
├── media/
│   ├── Atrium.png
│   ├── Agrippa.png
│   ├── Items.png
│   └── Peristylium.png
├── docs/
│   └── ATTRIBUTION.md
├── .gitignore
├── LICENSE
└── README.md
```

- `src/` — latest Python and Vizard source code
- `exported/` — legacy runtime files from an earlier project version
- `media/` — selected screenshots of the completed environment
- `docs/ATTRIBUTION.md` — credits and licensing information for third-party assets

## Project Assets

The complete Autodesk 3ds Max project, raw 3D scans, high-resolution textures, and the latest full runtime export are not included in this repository because of their large file size.

This repository focuses on:

- Source code
- Technical documentation
- Selected screenshots
- The development approach
- The main VR and 3D implementation details

Some decorative objects and textures used in the environment were obtained from third-party sources.

Available attribution and licensing information is documented in:

`docs/ATTRIBUTION.md`

The repository license applies only to the original work created for this project. Third-party assets remain subject to their respective licenses.

## Screenshots

The following images demonstrate the villa's architecture, lighting, interior objects, and scanned artifacts.

| Atrium View | Marcus Agrippa Bust |
| :---: | :---: |
| ![Atrium](./media/Atrium.png) | ![Agrippa](./media/Agrippa.png) |

| Interior Objects | Peristylium |
| :---: | :---: |
| ![Items](./media/Items.png) | ![Peristylium](./media/Peristylium.png) |

## Built With

- **Python**
- **Vizard VR Toolkit**
- **Autodesk 3ds Max**
- **3D Scanning Technology**
- **ProOptimizer**
- **GLTF and 3D asset workflows**

## Main Contributions

- Designed and assembled the Roman villa environment
- Implemented the Vizard VR scene
- Integrated interactive door mechanics
- Processed and integrated 3D-scanned busts
- Configured the lighting and sunset skybox
- Optimized complex meshes for improved rendering performance
- Conducted historical research for the villa layout
- Organized and integrated architectural, decorative, and interactive elements

## Limitations

- The latest complete runtime export is not included because of its large size
- The original 3ds Max project is not included
- Some third-party decorative assets cannot be redistributed independently
- The repository is intended primarily as a source-code and portfolio presentation of the completed project

## Author

**Andreas Belias**

Informatics and Telecommunications Student

**Fields:** Virtual Reality, Visual Computing, 3D Modeling, Historical Reconstruction