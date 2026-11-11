# Build Understanding 4.6 Applications of Exponential Growth and Decay — Answers

### **Question 1**
* **Problem:** The exponential model $A = 879.4e^{0.015t}$ describes the population, $A$, of a country in millions, $t$ years after 2003. Use the model to determine the population of the country in 2003.
* **Answer:** **`879.4` million**
* **Graph Equation:** `f(x) = 879.4 * e^(0.015*x)`
* **The Rule:** The year 2003 corresponds to $t = 0$, where $A(0) = A_0 e^0 = A_0$.
* **Work:**
  1. Substitute $t = 0$ (for the year 2003) into the model:
     $$A = 879.4e^{0.015(0)} = 879.4e^0 = 879.4(1) = 879.4\text{ million}$$

---

### **Question 2**
* **Problem:** The exponential models describe the population of the indicated country, $A$, in millions, $t$ years after 2006. Which country has the greatest growth rate? By what percentage is the population of that country increasing each year?
  - Country 1: $A = 147.8e^{-0.002t}$
  - Country 2: $A = 27.4e^{0.023t}$
  - Country 3: $A = 134.6e^{0.006t}$
  - Country 4: $A = 1098.7e^{0.013t}$
* **Answer:** **Country `2` has the greatest growth rate; increasing by `2.3`% each year.**
* **Graph Equation:** `f(x) = 27.4 * e^(0.023*x)`
* **The Rule:** In $A = A_0 e^{kt}$, the relative annual growth rate is $k$ (expressed as a percentage by multiplying $k$ by $100\%$).
* **Work:**
  1. Compare the growth constants $k$ for each country:
     - Country 1: $k = -0.002$ ($-0.2\%$, decreasing)
     - Country 2: $k = 0.023$ ($2.3\%$)
     - Country 3: $k = 0.006$ ($0.6\%$)
     - Country 4: $k = 0.013$ ($1.3\%$)
  2. The largest positive value of $k$ is $0.023$ (Country 2).
  3. Convert $0.023$ to a percentage: $0.023 \times 100\% = 2.3\%$.

---

### **Question 3**
* **Problem:** The exponential models describe the population of the indicated country, $A$, in millions, $t$ years after 2010. Which countries have a decreasing population? By what percentage is the population of these countries decreasing each year?
  - Country B: $A = 1183.1e^{0.004t}$
  - Country C: $A = 32.5e^{0.013t}$
  - Country D: $A = 121.7e^{-0.003t}$
  - Country E: $A = 143.7e^{-0.002t}$
* **Answer:** **Choice A: Country D and Country E have the decreasing populations. The population of Country D is decreasing by `0.3`% and the population of Country E is decreasing by `0.2`% each year.**
* **Graph Equation:** `f(x) = 121.7 * e^(-0.003*x)`
* **The Rule:** A negative constant $k < 0$ in $A = A_0 e^{kt}$ indicates a decreasing population at a rate of $|k| \times 100\%$ per year.
* **Work:**
  1. Identify the models with $k < 0$:
     - Country D has $k = -0.003 < 0$, which corresponds to a decrease of $0.003 \times 100\% = 0.3\%$ per year.
     - Country E has $k = -0.002 < 0$, which corresponds to a decrease of $0.002 \times 100\% = 0.2\%$ per year.
  2. This matches Choice A with `0.3`% and `0.2`%.

---

### **Question 4**
* **Problem:** A sample of $400\text{ g}$ of radioactive lead-210 decays to polonium-210 according to the function $A(t) = 400e^{-0.032t}$, where $t$ is time in years. Find the amount of radioactive lead remaining after (a) $4\text{ yr}$, (b) $8\text{ yr}$, (c) $15\text{ yr}$. (d) Find the half-life.
* **Answer:**
  - **(a) `352` g**
  - **(b) `310` g**
  - **(c) `248` g**
  - **(d) `21.66` yr**
* **Graph Equation:** `f(x) = 400 * e^(-0.032*x)`
* **The Rule:** Evaluate $A(t)$ at each given $t$, and find the half-life by solving $\frac{1}{2}A_0 = A_0 e^{kt} \implies t = \frac{\ln 2}{|k|}$.
* **Work:**
  1. **(a) After $4\text{ yr}$:**
     $$A(4) = 400e^{-0.032(4)} = 400e^{-0.128} \approx 400(0.879853) \approx 351.94\text{ g} \approx 352\text{ g}$$
  2. **(b) After $8\text{ yr}$:**
     $$A(8) = 400e^{-0.032(8)} = 400e^{-0.256} \approx 400(0.774142) \approx 309.66\text{ g} \approx 310\text{ g}$$
  3. **(c) After $15\text{ yr}$:**
     $$A(15) = 400e^{-0.032(15)} = 400e^{-0.48} \approx 400(0.618783) \approx 247.51\text{ g} \approx 248\text{ g}$$
  4. **(d) Half-life:**
     $$200 = 400e^{-0.032t} \implies 0.5 = e^{-0.032t} \implies t = \frac{\ln(0.5)}{-0.032} = \frac{\ln 2}{0.032} \approx 21.6608\text{ yr} \approx 21.66\text{ yr}$$

---

### **Question 5**
* **Problem:** Find the half-life of a radioactive element, which decays according to the function $A(t) = A_0 e^{-0.0125t}$, where $t$ is the time in years. (Round to the nearest tenth.)
* **Answer:** **`55.5` years**
* **Graph Equation:** `f(x) = e^(-0.0125*x) - 0.5`
* **The Rule:** The half-life of a substance decaying according to $A(t) = A_0 e^{kt}$ ($k < 0$) is $t = \frac{\ln(0.5)}{k} = \frac{\ln 2}{|k|}$.
* **Work:**
  1. Set $A(t) = 0.5 A_0$:
     $$0.5 A_0 = A_0 e^{-0.0125t} \implies 0.5 = e^{-0.0125t}$$
  2. Take the natural logarithm of both sides:
     $$\ln(0.5) = -0.0125t \implies t = \frac{\ln(0.5)}{-0.0125} = \frac{\ln 2}{0.0125} \approx \frac{0.69314718}{0.0125} \approx 55.4518 \approx 55.5\text{ years}$$

---

### **Question 6**
* **Problem:** Find the doubling time of an investment earning $5\%$ interest if interest is compounded continuously. (Round to the nearest tenth of a year.)
* **Answer:** **`13.9` years**
* **Graph Equation:** `f(x) = e^(0.05*x) - 2`
* **The Rule:** For continuous compounding $A = P e^{rt}$, the doubling time ($A = 2P$) is $t = \frac{\ln 2}{r}$.
* **Work:**
  1. Set $A = 2P$ with $r = 0.05$:
     $$2P = P e^{0.05t} \implies 2 = e^{0.05t}$$
  2. Take the natural logarithm of both sides:
     $$\ln 2 = 0.05t \implies t = \frac{\ln 2}{0.05} \approx \frac{0.69314718}{0.05} \approx 13.8629 \approx 13.9\text{ years}$$

---

### **Question 7**
* **Problem:** How long will it take for an investment to triple, if interest is compounded continuously at $4\%$? (Round to the nearest tenth of a year.)
* **Answer:** **`27.5` years**
* **Graph Equation:** `f(x) = e^(0.04*x) - 3`
* **The Rule:** For continuous compounding $A = P e^{rt}$, the tripling time ($A = 3P$) is $t = \frac{\ln 3}{r}$.
* **Work:**
  1. Set $A = 3P$ with $r = 0.04$:
     $$3P = P e^{0.04t} \implies 3 = e^{0.04t}$$
  2. Take the natural logarithm of both sides:
     $$\ln 3 = 0.04t \implies t = \frac{\ln 3}{0.04} \approx \frac{1.09861229}{0.04} \approx 27.4653 \approx 27.5\text{ years}$$

---

### **Question 8**
* **Problem:** An initial amount of a radioactive substance, $y_0$, is given, along with information about the amount remaining after a given time $t$. For an equation of the form $y = y_0 e^{kt}$ that models the situation, give the exact value of $k$ in terms of natural logarithms: $y_0 = 60\text{ g}$; After $2\text{ hr}$, $30\text{ g}$ remain.
* **Answer:** **`-(ln 2)/2` (or `(1/2)ln(1/2)` or `-1/2 ln 2`)**
* **Graph Equation:** `f(x) = 60 * e^(-0.5*ln(2)*x)`
* **The Rule:** Substitute $y_0$, $t$, and $y$ into $y = y_0 e^{kt}$, divide by $y_0$, and take the natural logarithm to solve for $k$.
* **Work:**
  1. Substitute $y_0 = 60$, $t = 2$, and $y = 30$:
     $$30 = 60e^{2k}$$
  2. Divide both sides by $60$:
     $$\frac{30}{60} = e^{2k} \implies \frac{1}{2} = e^{2k}$$
  3. Take the natural logarithm of both sides and solve for $k$:
     $$2k = \ln\left(\frac{1}{2}\right) = -\ln 2 \implies k = -\frac{\ln 2}{2} = \frac{1}{2}\ln\left(\frac{1}{2}\right)$$

---

### **Question 9**
* **Problem:** How long, to the nearest day, will it take any quantity of a radioactive element to decay to $25\%$ of its initial amount, knowing that it decays according to the exponential function $A(t) = A_0 e^{-0.085t}$, where $t$ is the time in days?
* **Answer:** **`16` days**
* **Graph Equation:** `f(x) = e^(-0.085*x) - 0.25`
* **The Rule:** Set $A(t) = 0.25 A_0$, cancel $A_0$, and take the natural logarithm of both sides to solve for $t$.
* **Work:**
  1. Set $A(t) = 0.25 A_0$:
     $$0.25 A_0 = A_0 e^{-0.085t} \implies 0.25 = e^{-0.085t}$$
  2. Take the natural logarithm of both sides:
     $$\ln(0.25) = -0.085t$$
  3. Divide by $-0.085$:
     $$t = \frac{\ln(0.25)}{-0.085} \approx \frac{-1.38629436}{-0.085} \approx 16.3093\text{ days} \approx 16\text{ days}$$

---

### **Question 10**
* **Problem:** Suppose an Egyptian mummy is discovered in which the amount of carbon-14 present is only about one-sixth the amount found in living human beings. The amount of carbon-14 present in animal bones after $t$ years is given by $y = y_0 e^{-0.0001216t}$, where $y_0$ is the amount of carbon-14 present in living human beings. About how long ago did the Egyptian die? (Round to the nearest integer as needed.)
* **Answer:** **`14735` yr (or `14,735` yr)**
* **Graph Equation:** `f(x) = e^(-0.0001216*x) - 1/6`
* **The Rule:** Substitute $y = \frac{1}{6}y_0$ into the carbon-14 decay formula and solve for $t$ using natural logarithms.
* **Work:**
  1. Substitute $y = \frac{1}{6}y_0$:
     $$\frac{1}{6}y_0 = y_0 e^{-0.0001216t} \implies \frac{1}{6} = e^{-0.0001216t}$$
  2. Take the natural logarithm of both sides:
     $$\ln\left(\frac{1}{6}\right) = -0.0001216t$$
  3. Solve for $t$:
     $$t = \frac{\ln(1/6)}{-0.0001216} = \frac{\ln 6}{0.0001216} \approx \frac{1.79175947}{0.0001216} \approx 14734.864\text{ yr} \approx 14,735\text{ yr}$$

---

### **Question 11**
* **Problem:** During an epidemic, the number of people who have never had the disease and who are not immune (they are susceptible) decreases exponentially according to the function $f(t) = 19,000e^{-0.08t}$, where $t$ is time in days. Find the number of susceptible people at each time (round to the nearest whole number as needed):
  - (a) at the beginning of the epidemic
  - (b) after $8\text{ days}$
  - (c) after $3\text{ weeks}$
* **Answer:**
  - **(a) `19,000` (or `19000`)**
  - **(b) `10,019` (or `10019`)**
  - **(c) `3,541` (or `3541`)**
* **Graph Equation:** `f(x) = 19000 * e^(-0.08*x)`
* **The Rule:** Evaluate $f(t)$ at $t = 0$, $t = 8$, and $t = 3 \times 7 = 21\text{ days}$.
* **Work:**
  1. **(a) At the beginning ($t = 0$):**
     $$f(0) = 19,000e^{-0.08(0)} = 19,000(1) = 19,000$$
  2. **(b) After $8\text{ days}$ ($t = 8$):**
     $$f(8) = 19,000e^{-0.08(8)} = 19,000e^{-0.64} \approx 19,000(0.5272924) \approx 10,018.56 \approx 10,019$$
  3. **(c) After $3\text{ weeks}$ ($t = 3 \times 7 = 21\text{ days}$):**
     $$f(21) = 19,000e^{-0.08(21)} = 19,000e^{-1.68} \approx 19,000(0.186374) \approx 3,541.11 \approx 3,541$$

---

### **Question 12**
* **Problem:** If $12\text{ g}$ of a radioactive substance are present initially and $4\text{ yr}$ later only $6.0\text{ g}$ remain, how much of the substance, to the nearest tenth of a gram, will be present after $5\text{ yr}$?
* **Answer:** **`5.0` g**
* **Graph Equation:** `f(x) = 12 * e^((ln(0.5)/4)*x)`
* **The Rule:** First find the decay constant $k$ using the given condition at $t = 4$, then evaluate $y(t) = y_0 e^{kt}$ at $t = 5$ without rounding intermediate values.
* **Work:**
  1. Use $y_0 = 12$ and $y(4) = 6.0$ to find $k$:
     $$6.0 = 12e^{4k} \implies 0.5 = e^{4k} \implies k = \frac{\ln(0.5)}{4}$$
  2. Substitute $t = 5$ into $y(t) = 12e^{kt}$:
     $$y(5) = 12e^{5\ln(0.5)/4} = 12(0.5)^{5/4} \approx 12(0.4204482) \approx 5.0454\text{ g} \approx 5.0\text{ g}$$
