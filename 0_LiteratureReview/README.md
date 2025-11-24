# Literature Review

Approaches or solutions that have been tried before on similar projects.

**Summary of Each Work**:

- **Source 1**: [Title of Source 1]

  - **[Link]()**
  - **Objective**:
  - **Methods**:
  - **Outcomes**:
  - **Relation to the Project**:

- **Source 2**: [Title of Source 2]

  - **[Link]()**
  - **Objective**:
  - **Methods**:
  - **Outcomes**:
  - **Relation to the Project**:

- **Source 3**: [Title of Source 3]

  - **[Link]()**
  - **Objective**:
  - **Methods**:
  - **Outcomes**:
  - **Relation to the Project**:

## Literature Review

- **EPEX SPOT market analyses [EPEX2022].**  
  Industry reports and market analyses for Germany show ARIMA/SARIMA and volatility models (GARCH) remain useful baselines for day‑ahead pricing, but modern practice combines exogenous features (renewable feed‑in, cross‑border flows, fuel prices) with ML ensembles (XGBoost/LightGBM) or sequence models (LSTM/GRU) to reduce short‑term point forecast errors. Operationally, short‑horizon ensembles and careful calendar/lag features improve intraday stability.

- **Fraunhofer ISE — renewable forecasting & integration [Fraunhofer2021].**  
  Fraunhofer work demonstrates that combining NWP with ML post‑processing and high‑resolution irradiance nowcasting improves PV/wind forecast skill, especially at very short horizons. They highlight the operational value of probabilistic forecasts (quantiles) for reserve sizing and show that ensemble approaches reduce tail risk during ramp events.

- **ENTSO‑E / TSO operational studies [ENTSOE2019].**  
  Transmission‑level forecasting and adequacy studies use regressions and ML with exogenous drivers (temperature, holidays, economic indicators). TSOs emphasize data quality, consistent timestamping, and robust imputation: reliable historical series are a prerequisite for any operational forecasting pipeline.

- **Academic surveys & hybrid/deep models [Weron2014; Hybrid2020].**  
  Academic comparisons find hybrid pipelines (statistical pre‑processing + ML residual modelling) and attention‑based sequence models often outperform single‑method baselines for short‑term price/load forecasting. Best practices include probabilistic training (quantile/pinball loss), rolling‑window cross‑validation, and ensembles to handle non‑stationarity introduced by market or policy shifts.

**Comparison to related domains**  
Electricity forecasting shares some methods with meteorological or air‑quality forecasting (NWP + ML), but differs in emphasizing market drivers (calendar effects, bidding behaviour, cross‑border flows) and operational metrics (price formation, reserve sizing). Compared with pan‑European market studies, our Germany‑focused work leverages higher‑resolution national feed‑in data (PV/wind) and TSO/market indicators to better model national net‑load ramps and price impacts.

**Key challenges (summary)**  
- Renewable‑driven variability and fast ramps that are hard to capture at coarse time resolution.  
- Heterogeneous public data with misaligned timestamps and missing values requiring robust cleaning.  
- Market non‑stationarity (policy/regulation changes) that reduces model transferability and requires rolling revalidation and retraining.  
- Operational need for probabilistic forecasts (quantiles, prediction intervals), not just point estimates.

**References (placeholders — replace with full citations / BibTeX)**  
- [EPEX2022] EPEX SPOT — Market analyses and reports (2022). https://www.epexspot.com  
- [Fraunhofer2021] Fraunhofer ISE — Renewable forecasting & integration (2021). https://www.ise.fraunhofer.de  
- [ENTSOE2019] ENTSO‑E Transparency Platform and TSO studies (2019). https://transparency.entsoe.eu  
- [Weron2014] Weron, R., “Electricity price forecasting: A review of the state‑of‑the‑art” (2014).  
- [Hybrid2020] Survey / comparison of hybrid ML/time‑series models (2020).

