# **Assignment: Build Understanding 4.4 Evaluating Logarithms and Change of Base Formula**

---

### **Question 1**
* **Problem:** Find the exact value: $\log 10^{-7}$
* **Answer:** **`-7`**
* **The Rule:** For any real number $r$, $\log_{10}(10^r) = r$.
* **Work:**
  1. Recall that $\log x$ denotes the common logarithm $\log_{10} x$.
  2. Using the inverse property $\log_{10}(10^r) = r$:
     $$\log 10^{-7} = \log_{10}(10^{-7}) = -7$$

---

### **Question 2**
* **Problem:** Find the exact value: $\log 0.1$
* **Answer:** **`-1`**
* **The Rule:** Express the decimal as a power of $10$ and apply $\log_{10}(10^r) = r$.
* **Work:**
  1. Rewrite $0.1$ as a fraction and power of $10$:
     $$0.1 = \frac{1}{10} = 10^{-1}$$
  2. Evaluate the common logarithm:
     $$\log 0.1 = \log_{10}(10^{-1}) = -1$$

---

### **Question 3**
* **Problem:** Use a calculator to find the common logarithm: $\log(17)$ (Round to four decimal places as needed.)
* **Answer:** **`1.2304`**
* **The Rule:** Evaluate the base-$10$ logarithm on a scientific calculator and round to four decimal places.
* **Work:**
  1. Compute $\log_{10}(17) \approx 1.23044892$.
  2. Rounding to four decimal places gives **`1.2304`**.

---

### **Question 4**
* **Problem:** Find the common logarithm of $0.0775$: $\log 0.0775$ (Round to four decimal places as needed.)
* **Answer:** **`-1.1107`**
* **The Rule:** Evaluate the base-$10$ logarithm on a calculator and round to four decimal places. Note that since $0 < 0.0775 < 1$, its common logarithm is negative.
* **Work:**
  1. Compute $\log_{10}(0.0775) \approx -1.110698297$.
  2. Rounding to four decimal places gives **`-1.1107`**.

---

### **Question 5**
* **Problem:** Find the value: $\log\left(\frac{527}{327}\right)$ (Round to four decimal places as needed.)
* **Answer:** **`0.2073`**
* **The Rule:** Evaluate the common logarithm of the quotient and round to four decimal places.
* **Work:**
  1. Compute $\frac{527}{327} \approx 1.611620795$.
  2. Take the base-$10$ logarithm:
     $$\log\left(\frac{527}{327}\right) \approx 0.20726285 \approx 0.2073$$

---

### **Question 6**
* **Problem:** Find the value: $\log 335 + \log 35$ (Round to four decimal places as needed.)
* **Answer:** **`4.0691`**
* **The Rule:** By the product property of logarithms, $\log A + \log B = \log(AB)$.
* **Work:**
  1. Combine or evaluate directly:
     $$\log 335 + \log 35 = \log(335 \times 35) = \log(11725)$$
  2. Using a calculator:
     $$\log_{10}(11725) \approx 4.0691128 \approx 4.0691$$

---

### **Question 7**
* **Problem:** Find the value: $\log 508 - \log 361$ (Round to four decimal places as needed.)
* **Answer:** **`0.1484`**
* **The Rule:** By the quotient property of logarithms, $\log A - \log B = \log\left(\frac{A}{B}\right)$.
* **Work:**
  1. Combine or evaluate directly:
     $$\log 508 - \log 361 = \log\left(\frac{508}{361}\right)$$
  2. Using a calculator:
     $$\log_{10}\left(\frac{508}{361}\right) \approx 0.14835859 \approx 0.1484$$

---

### **Question 8**
* **Problem:** Why is the value of $\log(349 \times 29)$ the same as that of $\log 349 + \log 29$?
* **Answer:** **C. The logarithm of a product of two numbers is the equal to the sum of logarithms of the numbers.**
* **The Rule:** Product Property of Logarithms: For any positive real numbers $x, y$ and base $a > 0, a \neq 1$, $\log_a(xy) = \log_a x + \log_a y$.
* **Work:**
  1. The expression $\log(349 \times 29)$ is the logarithm of a product.
  2. By the Product Property of Logarithms, $\log(349 \times 29) = \log 349 + \log 29$, which states that the logarithm of a product of two numbers equals the sum of the logarithms of the numbers (Choice **C**).

---

### **Question 9**
* **Problem:** Use a calculator to find approximations of the common logarithms (Round to four decimal places as needed):
  (a) $\log(455.2)$
  (b) $\log(45.52)$
  (c) $\log(4.552)$
* **Answer:**
  * **(a)** **`2.6582`**
  * **(b)** **`1.6582`**
  * **(c)** **`0.6582`**
* **The Rule:** Moving the decimal point of $x$ by one place divides $x$ by $10$, which decreases $\log_{10}(x)$ by $\log_{10}(10) = 1$ while keeping the fractional part (mantissa) the same.
* **Work:**
  1. **(a)** $\log(455.2) = \log(10^2 \times 4.552) = 2 + \log(4.552) \approx 2 + 0.658202 = \mathbf{2.6582}$.
  2. **(b)** $\log(45.52) = \log(10^1 \times 4.552) = 1 + \log(4.552) \approx 1 + 0.658202 = \mathbf{1.6582}$.
  3. **(c)** $\log(4.552) \approx 0.658202 = \mathbf{0.6582}$.

---

### **Question 10**
* **Problem:** Evaluate the following expression. Do not use a calculator: $\ln e^{\frac{9}{5}}$ (Type an integer or a fraction.)
* **Answer:** **`9/5`**
* **The Rule:** Inverse Property of Natural Logarithms: $\ln(e^x) = x$ for any real number $x$.
* **Work:**
  1. Since $\ln$ has base $e$, $\ln\left(e^{9/5}\right) = \frac{9}{5}$.

---

### **Question 11**
* **Problem:** Find the value: $\ln\left(\frac{1}{e^{11}}\right)$
* **Answer:** **`-11`**
* **The Rule:** Rewrite $\frac{1}{e^n}$ as $e^{-n}$ using negative exponents, then apply $\ln(e^x) = x$.
* **Work:**
  1. Rewrite the argument with a negative exponent:
     $$\frac{1}{e^{11}} = e^{-11}$$
  2. Apply the inverse property of natural logarithms:
     $$\ln(e^{-11}) = -11$$

---

### **Question 12**
* **Problem:** Find the value: $\ln \sqrt[14]{e}$ (Simplify your answer. Type an integer or a fraction.)
* **Answer:** **`1/14`**
* **The Rule:** Rewrite $\sqrt[n]{e}$ as $e^{1/n}$ using rational exponents, then apply $\ln(e^x) = x$.
* **Work:**
  1. Rewrite the radical as a fractional exponent:
     $$\sqrt[14]{e} = e^{1/14}$$
  2. Apply $\ln(e^x) = x$:
     $$\ln\left(e^{1/14}\right) = \frac{1}{14}$$

---

### **Question 13**
* **Problem:** Use a calculator to find the natural logarithm, base $e$: $\ln 78$ (Round to four decimal places as needed.)
* **Answer:** **`4.3567`**
* **The Rule:** Evaluate the natural logarithm $\ln(78) = \log_e(78)$ on a calculator and round to four decimal places.
* **Work:**
  1. Compute $\ln(78) \approx 4.3567088$.
  2. Rounding to four decimal places gives **`4.3567`**.

---

### **Question 14**
* **Problem:** Use a calculator to find the natural logarithm, base $e$: $\ln 0.0918$ (Round to four decimal places as needed.)
* **Answer:** **`-2.3881`**
* **The Rule:** Evaluate the natural logarithm on a calculator and round to four decimal places.
* **Work:**
  1. Compute $\ln(0.0918) \approx -2.38814258$.
  2. Rounding to four decimal places gives **`-2.3881`**.

---

### **Question 15**
* **Problem:** Find the value: $\ln\left(\frac{86}{11}\right)$ (Round the final answer to four decimal places as needed. Round all intermediate values to four decimal places as needed.)
* **Answer:** **`2.0565`**
* **The Rule:** Divide the numerator by the denominator and take the natural logarithm, rounding to four decimal places.
* **Work:**
  1. Compute $\frac{86}{11} \approx 7.8182$.
  2. Take the natural logarithm:
     $$\ln\left(\frac{86}{11}\right) \approx 2.056452 \approx 2.0565$$

---

### **Question 16**
* **Problem:** Find the value: $\ln 26 + \ln 904$ (Round the final answer to four decimal places as needed. Round all intermediate values to four decimal places as needed.)
* **Answer:** **`10.0649`**
* **The Rule:** Evaluate each natural logarithm and add (or multiply arguments inside a single natural logarithm).
* **Work:**
  1. Evaluate each term to four decimal places:
     $$\ln 26 \approx 3.2581, \quad \ln 904 \approx 6.8068$$
  2. Sum the values:
     $$3.2581 + 6.8068 = 10.0649$$

---

### **Question 17**
* **Problem:** Find the value: $\ln 82 - \ln 20$ (Round the final answer to four decimal places as needed. Round all intermediate values to four decimal places as needed.)
* **Answer:** **`1.4110`**
* **The Rule:** Evaluate each natural logarithm and subtract (or divide arguments inside a single natural logarithm).
* **Work:**
  1. Evaluate each term to four decimal places:
     $$\ln 82 \approx 4.4067, \quad \ln 20 \approx 2.9957$$
  2. Subtract the values:
     $$4.4067 - 2.9957 = 1.4110$$

---

### **Question 18**
* **Problem:** Use the change-of-base theorem to find the logarithm: $\log_2 9$ (Simplify your answer. Do not round until the final answer. Then round to four decimal places as needed.)
* **Answer:** **`3.1699`**
* **The Rule:** Change-of-Base Theorem: $\log_a x = \frac{\ln x}{\ln a} = \frac{\log x}{\log a}$.
* **Work:**
  1. Apply the change-of-base formula:
     $$\log_2 9 = \frac{\ln 9}{\ln 2}$$
  2. Evaluate using a calculator without intermediate rounding:
     $$\frac{\ln 9}{\ln 2} \approx \frac{2.19722458}{0.69314718} \approx 3.169925 \approx \mathbf{3.1699}$$

---

### **Question 19**
* **Problem:** Use the change-of-base theorem to find the logarithm: $\log_9 0.65$ (Simplify your answer. Do not round until the final answer. Then round to four decimal places as needed.)
* **Answer:** **`-0.1961`**
* **The Rule:** Change-of-Base Theorem: $\log_a x = \frac{\ln x}{\ln a}$.
* **Work:**
  1. Apply the change-of-base formula:
     $$\log_9 0.65 = \frac{\ln 0.65}{\ln 9}$$
  2. Evaluate using a calculator:
     $$\frac{\ln 0.65}{\ln 9} \approx \frac{-0.4307829}{2.1972246} \approx -0.1960577 \approx \mathbf{-0.1961}$$

---

### **Question 20**
* **Problem:** Use the change-of-base theorem to find the logarithm: $\log_{1/4} 8$ (Simplify your answer. Do not round until the final answer. Then round to four decimal places as needed.)
* **Answer:** **`-1.5`** (or **`-3/2`**)
* **The Rule:** Change-of-Base Theorem: $\log_a x = \frac{\ln x}{\ln a}$.
* **Work:**
  1. Apply the change-of-base formula with base $2$ or base $e$:
     $$\log_{1/4} 8 = \frac{\ln 8}{\ln(1/4)} = \frac{\ln(2^3)}{\ln(2^{-2})} = \frac{3\ln 2}{-2\ln 2} = -\frac{3}{2} = -1.5$$

---

### **Question 21**
* **Problem:** Use the change-of-base theorem to find the logarithm: $\log_{1/2} 9$
  * Part 1: Use the change-of-base theorem to rewrite the given expression in terms of natural logarithms or common logarithms. (Do not evaluate. Do not simplify.)
  * Part 2: Evaluate the expression. (Simplify your answer. Do not round until the final answer. Then round to four decimal places as needed.)
* **Answer:**
  * **Part 1 (Rewrite):** **`ln(9)/ln(1/2)`** (or **`log(9)/log(1/2)`**, written as $\frac{\ln 9}{\ln(1/2)}$ or $\frac{\log 9}{\log(1/2)}$)
  * **Part 2 (Evaluate):** **`-3.1699`**
* **The Rule:** Change-of-Base Theorem: $\log_a x = \frac{\ln x}{\ln a} = \frac{\log x}{\log a}$.
* **Work:**
  1. Rewrite using natural logarithms:
     $$\log_{1/2} 9 = \frac{\ln 9}{\ln\left(\frac{1}{2}\right)}$$
  2. Evaluate using a calculator:
     $$\frac{\ln 9}{\ln(0.5)} \approx \frac{2.19722458}{-0.69314718} \approx -3.169925 \approx \mathbf{-3.1699}$$

---

### **Question 22**
* **Problem:** Use the change-of-base theorem to find the logarithm: $\log_\pi 48$
  * Part 1: Use the change-of-base theorem to rewrite the given expression in terms of natural logarithms or common logarithms. (Do not evaluate. Do not simplify.)
  * Part 2: Evaluate the expression. (Simplify your answer. Do not round until the final answer. Then round to four decimal places as needed.)
* **Answer:**
  * **Part 1 (Rewrite):** **`ln(48)/ln(pi)`** (or **`log(48)/log(pi)`**, written as $\frac{\ln 48}{\ln \pi}$ or $\frac{\log 48}{\log \pi}$)
  * **Part 2 (Evaluate):** **`3.3818`**
* **The Rule:** Change-of-Base Theorem: $\log_a x = \frac{\ln x}{\ln a}$.
* **Work:**
  1. Rewrite using natural logarithms:
     $$\log_\pi 48 = \frac{\ln 48}{\ln \pi}$$
  2. Evaluate using a calculator:
     $$\frac{\ln 48}{\ln \pi} \approx \frac{3.87120101}{1.14472989} \approx 3.3817593 \approx \mathbf{3.3818}$$

---

### **Question 23**
* **Problem:** Given $g(x) = e^x$, evaluate each of the following:
  (a) $g(\ln 3)$
  (b) $g[\ln(7^2)]$
  (c) $g\left[\ln\left(\frac{1}{e^4}\right)\right]$
* **Answer:**
  * **(a)** **`3`**
  * **(b)** **`49`**
  * **(c)** **`1/e^4`** (or $e^{-4}$)
* **Graph Equation:** `g(x) = e^x`
* **The Rule:** Since $g(x) = e^x$ and $\ln x = \log_e x$ are inverse functions, $e^{\ln u} = u$ for any $u > 0$.
* **Work:**
  1. **(a)** $g(\ln 3) = e^{\ln 3} = \mathbf{3}$.
  2. **(b)** $g[\ln(7^2)] = e^{\ln(49)} = \mathbf{49}$.
  3. **(c)** $g\left[\ln\left(\frac{1}{e^4}\right)\right] = e^{\ln(1/e^4)} = \mathbf{\frac{1}{e^4}}$.

---

### **Question 24**
* **Problem:** Given $f(x) = \ln x$, evaluate:
  a) $f(e^2)$
  b) $f(e^{\ln 5})$
  c) $f(e^{6\ln 5})$
* **Answer:**
  * **a)** **`2`**
  * **b)** **`ln 5`**
  * **c)** **`6 ln 5`** (or **`ln(15625)`**)
* **Graph Equation:** `f(x) = ln(x)`
* **The Rule:** For any real number $u$, $f(e^u) = \ln(e^u) = u$.
* **Work:**
  1. **a)** $f(e^2) = \ln(e^2) = \mathbf{2}$.
  2. **b)** $f(e^{\ln 5}) = \ln(e^{\ln 5}) = \mathbf{\ln 5}$ (since $e^{\ln 5} = 5$, $f(5) = \ln 5$).
  3. **c)** $f(e^{6\ln 5}) = \ln(e^{6\ln 5}) = \mathbf{6\ln 5}$ (or $\ln(5^6) = \ln 15625$).

---

### **Question 25**
* **Problem:** Which of the following is equivalent to $4\ln(3x)$ for $x > 0$?
  * $\ln 81 + \ln x$
  * $\ln(12x)$
  * $\ln(81x^4)$
  * $\ln 12 + \ln x$
* **Answer:** **`ln(81x^4)`** (3rd option: $\ln(81x^4)$)
* **Graph Equation:** `y = 4*ln(3*x)`
* **The Rule:** By the Power Property of Logarithms, $r\ln u = \ln(u^r)$, and by the Product Rule for Exponents, $(ab)^r = a^r b^r$.
* **Work:**
  1. Apply the power property of logarithms to move the coefficient $4$ into the exponent of the argument $(3x)$:
     $$4\ln(3x) = \ln\left((3x)^4\right)$$
  2. Raise both factors inside the parentheses to the $4$th power:
     $$\ln(3^4 x^4) = \ln(81x^4)$$

---

### **Question 26**
* **Problem:**
  (a) Find the decibel rating of a sound, $d = 10\log\frac{I}{I_0}$, having intensity $100,000,000,000I_0$, where $I_0$ is the initial intensity.
  (b) If the intensity of a sound is tripled, by how much is the decibel rating increased? (Round to the nearest integer as needed.)
* **Answer:**
  * **(a)** The decibel rating of this sound is **`110`**.
  * **(b)** The decibel rating of the sound increases by about **`5`** decibels.
* **The Rule:** Substitute $I$ into $d = 10\log_{10}\left(\frac{I}{I_0}\right)$ and simplify using logarithm properties.
* **Work:**
  1. **(a)** Note that $100,000,000,000 = 10^{11}$. Substitute $I = 10^{11}I_0$ into the formula:
     $$d = 10\log\left(\frac{10^{11}I_0}{I_0}\right) = 10\log(10^{11}) = 10(11) = \mathbf{110}$$
  2. **(b)** If an intensity $I$ is tripled to $3I$, the new decibel rating $d_{\text{new}}$ is:
     $$d_{\text{new}} = 10\log\left(\frac{3I}{I_0}\right) = 10\left(\log 3 + \log\frac{I}{I_0}\right) = 10\log 3 + 10\log\frac{I}{I_0}$$
     The increase in decibels is:
     $$\Delta d = 10\log 3 \approx 10(0.47712) \approx 4.7712 \approx \mathbf{5}\text{ decibels}$$

---

### **Question 27**
* **Problem:** The magnitude of an earthquake, measured on the Richter scale, is $\log_{10}\frac{I}{I_0}$, where $I$ is the amplitude registered on a seismograph $100\text{ km}$ from the epicenter of the earthquake, and $I_0$ is the amplitude of a certain (small) size. Find the Richter scale rating for an amplitude of $100,000,000I_0$.
* **Answer:** The magnitude, $R$ (measured on the Richter scale) is **`8`**.
* **The Rule:** Substitute $I = 10^8 I_0$ into $R = \log_{10}\left(\frac{I}{I_0}\right)$ and apply $\log_{10}(10^k) = k$.
* **Work:**
  1. Count the zeros in $100,000,000$: $100,000,000 = 10^8$.
  2. Substitute $I = 10^8 I_0$ into the Richter scale formula:
     $$R = \log_{10}\left(\frac{10^8 I_0}{I_0}\right) = \log_{10}(10^8) = \mathbf{8}$$

---

### **Question 28**
* **Problem:** Fill in the blank: The expression $\log_a x$ represents the (1) _______ to which the base $a$ must be raised to obtain $x$.
* **Answer:** (1) **`exponent`**
* **The Rule:** A logarithm is an **exponent**: $y = \log_a x \iff a^y = x$.
* **Work:**
  1. In the equation $a^y = x$, $a$ is the base and $y = \log_a x$ is the **exponent** to which $a$ must be raised to obtain $x$.
