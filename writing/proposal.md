
 







Spatial Estimation of Air Quality at Unmonitored Locations Using Machine Learning: Implications for IoT Sensor Network Design in Swedish Cities

Abdalazeez Asaad











 Master programme
MSc Internet of Things 30credits 
Department of Technology and Society Spring 2026
Main academic supervisor: Fisseha Mekuria

Basic information
Student: Abdalazeez Farouq Mohammad Asaad, aziz.f1987@gmail.com 
Course Code: DA647E
Preliminary Title: Spatial Estimation of Air Quality at Unmonitored Locations Using Machine Learning: Implications for IoT Sensor Network Design in Swedish Cities

Main academic supervisor: Fisseha Mekuria








































1.	Introduction and Background
Rapid urbanization and shifting industrial frameworks have made micro-climatic urban air pollution a critical public health and environmental priority across modern European municipalities. Ground-level pollutants, specifically particulate matter PM2.5 and nitrogen dioxide NO2, exhibit extreme spatial heterogeneity, varying dramatically across sub-kilometre margins due to localized vehicular density, street canyons, and topographies. Despite this high volatility, historical environmental monitoring paradigm designs rely on a sparse framework of stationary, regulatory-grade reference nodes managed by national bodies such as the Swedish Meteorological and Hydrological Institute (SMHI) separated by wide geometric margins [1]. While these reference setups provide pristine data quality, their high capital costs leave vast geometric data gaps across urban communities.
To counter this spatial data scarcity, internet-of-things (IoT) architectures utilizing low-cost distributed microsensors have emerged as a viable solution to capture dense street-level environmental diagnostics [2]. However, the physical placement of these IoT configurations is frequently driven by opportunistic real estate availability, convenience, or human intuition rather than objective mathematical variance minimization. Without a structured placement framework, deployments can result in redundant data coverage in certain zones while leaving critical high-risk blind spots entirely unmonitored.
Recent advancements in environmental data science show that machine learning (ML) and deep learning (DL) architectures can accurately model complex, non-linear spatiotemporal pollutant structures to map unmonitored zones from sparse networks [3], [4]. Sweden's SMHI operates a highly reliable national network of reference-quality monitoring stations. This framework provides an ideal training environment to evaluate spatial estimation models, map regional exposure dynamics, and generate data-driven frameworks for future urban IoT sensor topologies.
Ultimately, this thesis directly addresses these baseline infrastructural inefficiencies. By utilizing five years (2020–2024) of multi-source historical open data from SMHI and the European Union's CORINE Land Cover inventory, this research develops a spatial machine learning estimation framework to map unmonitored zones. This project quantifies an empirical accuracy-distance decay relationship to drive an automated, Particle Swarm Optimization (PSO) placement tool for future municipal IoT node topologies in Swedish urban ecosystems.

2. Problem Statement
While spatial interpolation models are widely used for general mapping, translating continuous model performance into actionable layout design rules for physical infrastructure remains a critical challenge. Standard cross-validation techniques frequently fail in spatial settings because spatial autocorrelation causes models to overfit to localized geographic structures, masking true deployment risk.
Furthermore, while dense deployments of micro-sensors have been used to iteratively cluster and enhance traditional inverse distance weighting (IDW) methods globally [5], there is a distinct lack of localized research determining how spatial estimation error scales continuously as a function of Euclidean and contextual distance from active monitoring hubs within Swedish urban layouts. Without quantifying this accuracy-distance decay relationship, IoT system architects cannot determine if a proposed physical sensor is redundant or if an unmonitored blind spot genuinely requires a physical node deployment. This thesis addresses this gap by applying spatial validation methods across the Swedish monitoring landscape and applying the resulting rules to an optimized municipal deployment case study.



3. Related Work
Recent literature surrounding urban environmental monitoring largely bifurcates into three interconnected domains: the deployment of low-cost IoT networks, spatiotemporal machine learning estimation, and heuristic optimization for node placement.
IoT and Low-Cost Monitoring Frameworks: The rapid adoption of low-cost IoT sensor nodes has been widely documented as a primary method to bypass the financial constraints of sparse regulatory stations. Karinthi et al. [1] and Popescu and Ionescu [2] highlight the viability of these micro-sensors for urban data mining. However, while these studies confirm the technological feasibility of IoT networks, they frequently point to a critical gap: deployments often rely on ad-hoc or convenience-based placement strategies rather than mathematically optimized spatial planning.
Spatiotemporal Machine Learning: To mathematically bridge the spatial gaps between physical sensors, researchers are increasingly pivoting from deterministic interpolation (such as IDW) to advanced machine learning architectures. Agbehadji and Obagbuwa [4] establish that tree-based models and deep learning frameworks are highly effective at capturing non-linear pollutant dispersion. Furthermore, Xie et al. [6] demonstrate that hybrid geostatistical models combining machine learning embeddings with Kriging variance structures significantly outperform traditional geographic methods. Chen and Lin [5] validated these smart spatial interpolation concepts by clustering densely deployed microsensors against regulatory baselines, proving that ML can highly accurately predict PM2.5 exposure in unmonitored zones.
Sensor Placement Optimization: Translating accurate ML models into physical deployment maps requires heuristic optimization. For the physical placement of networked sensors, Filios et al. [7] utilized data-driven predictability reductions, while Gupta and Thakur [8] successfully applied Particle Swarm Optimization (PSO) to minimize network-wide uncertainty. However, many of these existing placement frameworks are historically tested in closed indoor environments (IAQ) or highly localized simulated grids.
The Research Gap: This thesis directly builds upon these established mathematical optimization foundations, explicitly scaling them to macro-urban outdoor topologies. By utilizing Sweden's robust, high-fidelity SMHI network as the empirical baseline, this project uniquely quantifies the continuous accuracy-distance decay relationship to drive actionable outdoor IoT placement.

4. Hypothesis
Machine learning-based spatial estimation models utilizing localized land-use and meteorological covariates will predict daily PM2.5 and NO2 concentrations at spatially withheld locations with a significantly lower Root Mean Squared Error (RMSE) than standard geographic baselines. Furthermore, this estimation error degrades non-linearly with distance to the nearest operational reference station, exhibiting a distinct mathematical threshold beyond which spatial estimation becomes unreliable, thereby identifying the optimal boundary for physical IoT node intervention.


5. Research Questions
•	RQ1: How accurately can machine learning models estimate daily PM2.5 and NO2 concentrations at spatially withheld SMHI reference stations using land-use, topography, and meteorological covariates?
•	RQ2: How does spatial estimation accuracy degrade as a function of distance from the nearest active reference station, and what is the maximum reliable prediction distance threshold before physical sensor deployment becomes necessary?
•	RQ3: Based on the accuracy-distance relationship modeled from the national network, how can optimization heuristics be applied to guide the step-by-step placement of an urban IoT sensor network within a selected Swedish metropolitan area case study?

6. Methodology
Data Sources & Experimental Matrix
The data framework spans a five-year historical baseline (2020–2024) compiling environmental, contextual, and geographic layers into a unified spatial matrix:

Source	Content	Access
SMHI Luftwebb	PM2.5 and NO2 daily averages at all available Swedish reference stations + coordinates	Downloadable, free
SMHI metobs API	Meteorological covariates (temperature, wind velocity/direction, relative humidity)	REST API, free
CORINE Land Cover	Land use classification (urban core, suburban, rural, industrial) per station radius	Free, EU open data

Spatial Features per Station
Euclidean distance and bearing matrices to all neighbouring active target stations.
•	Categorical land-use signatures extracted via CORINE buffer geometry.
•	Gridded population density within a 1km spatial radius.
•	Digital Elevation Model (DEM) topographic features.
•	Localized meteorological variables acting as dynamic spatial covariates.

Technical Approach & Spatial Validation
To prevent spatial autocorrelation from artificially inflating model metrics, the framework implements an iterative Spatial Leave-One-Out Cross-Validation (SLOOCV) routine. During each iteration, a target monitoring station is completely withheld from the training data pool. The model is trained on the remaining national stations, and its predictions are evaluated directly against the unseen observations of the withheld target node.

The project evaluates a progression of architectures:
1.	Inverse Distance Weighting (IDW): The deterministic baseline framework.
2.	Spatial Random Forest (RF) & XGBoost: Tree-based ensembles optimized with explicit spatial coordinates, distance matrices, and CORINE land-cover vectors.
3.	Kriging & ML Hybrids: Geostatistical models leveraging spatial covariance structures, serving as an entry point toward state-of-the-art hybrid spatial embedding frameworks [6].





Design Science Research (DSR) Artefact & Case Study Optimization
The final phase translates the distance-accuracy decay function into a concrete spatial design tool for urban planners, implemented as a localized case study within a selected major Swedish municipality.
The algorithm treats the city's geographic layout as a high-resolution uncertainty grid. To solve the combinatorial problem of where to place physical nodes to yield the highest network-wide reduction in error, the system evaluates meta-heuristic search frameworks. Specifically, it adapts data-driven edge predictability reductions [7] and leverages Particle Swarm Optimization (PSO) strategies to isolate global coordinate optima [8].

7. Expected Outcomes

•	Spatial Estimation Accuracy Benchmarks: Evaluated across the Swedish SMHI network to define baseline error bounds for spatial machine learning models.
•	Quantified Accuracy-Distance Decay Curves: Complete with an empirical reliability threshold establishing where modelling must be substituted by physical infrastructure.
•	High-Resolution Coverage Uncertainty Heatmaps: Highlighting unmonitored blind spots within the selected case study city layout.
•	Actionable IoT Sensor Topology Recommendations: A prioritized coordinate deployment scheme designed to minimize maximum network estimation variance.

8. Risk Management & Mitigations

Identified Research Risk	Impact	Proactive Mitigation strategy
Spatial Autocorrelation and Overfitting: Machine learning architectures (RF/XGBoost) can overfit to close geographic clusters, artificially inflating accuracy metrics during standard training iterations.	High	Strict implementation of the Spatial Leave-One-Out Cross-Validation (SLOOCV) routine. Hiding an entire reference station during each training loop simulates true unmonitored deployment risks and forces the model to rely strictly on contextual land-use and meteorological covariates.
Data Incompleteness and API Downtime: Historical records from the SMHI Luftwebb or the metobs REST API might contain missing variables or telemetry gaps during the 2020–2024 baseline window	Medium	Phase 2 (Data Engineering, Weeks 3–4) allocates dedicated time for robust data cleansing and localized spatial imputation. Stations falling below a 90% data completeness threshold will be filtered out to protect matrix integrity.




9. Timeline
 

10. References
[1] K. N. Karinthi et al., "Establishing A Sustainable Low-Cost Air Quality Monitoring Setup: A Survey of the State-of-the-Art," Sensors, vol. 22, no. 1, p. 394, 2022. https://doi.org/10.3390/s22010394
[2] A. Popescu and M. Ionescu, "IoT Devices for Monitoring and Analysing Air Quality in Urban Environments," in Proceedings of the International Symposium on Electronics and Telecommunications (SIITME), 2024, pp. 112–117. doi: 10.1109/SIITME63973.2024.10814899 
[3] X. Wang and L. Zhang, "Urban Ambient Air Quality Data Mining and Visualisation," in Proceedings of the International Conference on AIoT Computing and Security (AIoTCs), 2022, pp. 402–409. doi: 10.1109/AIoTCs58181.2022.00101
[4] I. E. Agbehadji and I. C. Obagbuwa, "Systematic Review of Machine Learning and Deep Learning Techniques for Spatiotemporal Air Quality Prediction," Atmosphere, vol. 15, no. 11, p. 1352, 2024. https://doi.org/10.3390/atmos15111352
[5] P.-C. Chen and Y.-T. Lin, "Exposure assessment of PM2.5 using smart spatial interpolation on regulatory air quality stations with clustering of densely-deployed microsensors," Environmental Pollution, vol. 292, p. 118401, 2022. https://doi.org/10.1016/j.envpol.2021.118401
[6] J. Xie, F. Liu, S. Liu, and X. Jiang, "An approach to spatiotemporal air quality prediction integrating SwinLSTM and kriging methods," Sustainability, vol. 17, no. 7, p. 2918, 2025. https://doi.org/10.3390/su17072918
[7] G. Filios, S. Nikoletseas, and I. Stivaros, "IAQ Monitoring System Optimizing Data-Driven Sensor Placement," in 2024 20th International Conference on Distributed Computing in Smart Systems and the Internet of Things (DCOSS-IoT), 2024, pp. 408–415. doi: 10.1109/DCOSS-IoT61029.2024.00067 
[8] A. Gupta and N. Thakur, "Optimizing Sensor Placement for Air Quality Monitoring System Using Particle Swarm Optimization," in 2023 International Conference on Automation, Computational and Technology Engineering (ICACCTech), 2023, pp. 1–6. doi: 10.1109/ICACCTech61146.2023.00073

