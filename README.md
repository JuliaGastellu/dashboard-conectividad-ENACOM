# Internet Penetration and Quality in Argentina: A Data-Driven Study

This study analyzes internet connectivity in Argentina using public data. It quantifies service penetration, characterizes technologies used, evaluates connection quality, and identifies digital gaps across regions. The findings help understand the current landscape and propose strategies for improved access and service quality.

## Installation & Requirements

1. Clone the repository:
   ```bash
   git clone https://github.com/JuliaGastellu/dashboard-conectividad-ENACOM.git
   ```
2. Create a virtual environment:
   ```bash
   python -m venv env
   ```
3. Activate the environment:
   ```bash
   # Windows:
   env\Scripts\activate
   # macOS/Linux:
   source env/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- **Data:** Processed CSV files.
- **Notebooks:** Scripts for data cleaning, transformation, and analysis.
- **ETL_PIDA:** Code and results for raw data processing.
- **EDA_PIDA:** Exploratory analysis, including KPI development.
- **Visualizations:** Interactive dashboard files.
- **Documentation:** Project details and methodologies.

## Methodology

1. **Data Acquisition:** Public data from [ENACOM Open Data](https://www.enacom.gob.ar/datosabiertos).
2. **Data Cleaning & Preparation:** Removing duplicates, correcting errors, and handling missing values.
3. **Exploratory Analysis:** Statistical techniques and visualizations to identify patterns and anomalies.
4. **In-Depth Analysis:** Trends in internet technologies, regional differences, and connection speed vs. household income.
5. **KPI Development:** Key performance indicators to assess internet access and evolution.
6. **Visualization:** Results are presented through an interactive dashboard.

## Key Findings

### Technology Trends & Digital Transition

Fiber optic dominates urban areas due to high-speed demand and provider investments. In contrast, wireless technologies (4G/5G) are growing in rural regions, albeit with lower speeds.

![Access by Technology & Province](images/1.png)

### Regional Disparities & Growth Patterns

- **Fiber optic is expanding rapidly** in cities, while older technologies (ADSL, dial-up) decline.
- **Growth rate varies across provinces,** influenced by economic factors, infrastructure investments, and public policies.
- **Public policies play a crucial role**—provinces with proactive telecom investments see faster growth.

![Download Speed Evolution by Province & Year](images/2.png)

### Factors Influencing Connectivity

- **Economic Cycles:** Infrastructure investment fluctuates with economic conditions.
- **Regulatory Policies:** Competition-driven regulations accelerate connectivity growth.
- **External Events:** Pandemics, natural disasters, and geopolitical factors impact service availability.
- **Radio Spectrum Allocation:** Efficient spectrum management is crucial for mobile network expansion.

![Internet Access by Province & Year](images/5.png)

### Urban vs. Rural Connectivity Gaps

Urban areas benefit from faster technology adoption, while rural regions lag due to lower infrastructure density and provider competition.

![Technology Distribution by Province](images/7.png)

## KPIs for Measuring Progress

- **KPI 1: Internet Access Growth** – Increase household internet penetration by 2% per province in the next quarter.
- **KPI 2: Fiber Optic Expansion** – Raise fiber optic adoption by 2% per province.
- **KPI 3: High-Speed Connectivity** – Boost connections over 20 Mbps by 5% in provinces with low speeds.

These KPIs align with strategic goals to expand infrastructure, enhance service quality, and reduce the digital divide.

## Author

- [@JuliaGastellu](https://github.com/JuliaGastellu)


