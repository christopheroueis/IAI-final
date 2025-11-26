# Exploratory Data Analysis Report

## 1. Data Structure
*   **Rows**: 2865
*   **Columns**: 248
*   **Years**: [2022, 2024]

## 2. Univariate Analysis
### Facility Types
TYPE_CNTRL
Investor Owned    2379
Not-for-Profit     211
Church Related      45
State               18
District             6

### Financial Overview (Averages)
         TOT_HC_REV    TOT_HC_EXP    NET_INCOME
count  2.640000e+03  2.636000e+03  2.627000e+03
mean   1.206253e+07  1.198846e+07  5.272637e+05
std    8.156013e+06  8.171086e+06  5.404397e+06
min   -2.986800e+04 -1.092720e+06 -1.866436e+08
25%    6.206206e+06  6.647083e+06 -3.822780e+05
50%    1.137064e+07  1.129011e+07  3.042890e+05
75%    1.645138e+07  1.572118e+07  1.339406e+06
max    5.563904e+07  8.277134e+07  1.058158e+08

## 3. Bivariate Analysis
### Net Income by Ownership Type
TYPE_CNTRL
Investor Owned    6.125753e+05
Not-for-Profit   -1.501674e+05
District         -2.654353e+05
Church Related   -2.909901e+05
State            -1.639520e+06

## 4. Temporal Analysis (2022 vs 2024)
        TOT_HC_REV    TOT_HC_EXP     NET_INCOME       OCCUP
Year                                                       
2022  1.081074e+07  1.093164e+07  241247.747212  124.992761
2024  1.337254e+07  1.309956e+07  827335.120125  169.309889

## 5. Geographic Analysis (Top 10 Counties)
                  NET_INCOME       OCCUP
COUNTY_x                                
Santa Clara     1.360054e+06  158.126635
Orange          7.919114e+05  154.899178
San Bernardino  7.141085e+05  149.006033
Sacramento      5.202901e+05  149.738434
Ventura         4.813758e+05  125.666769
San Diego       4.792578e+05  155.674432
Los Angeles     3.819422e+05  146.325113
Fresno          2.154810e+05  148.089028
Alameda         1.975593e+05  133.601104
Riverside       1.572828e+05  138.372302

