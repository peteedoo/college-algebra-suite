# **Assignment: Pre-work 4.5 Exponential and Logarithmic Equations**

---

### **Question 1**
* **Problem:** Write the logarithmic equation as an exponential equation: $\ln x = 5$
* **Answer:** **A. $e^5 = x$**
* **The Rule:** Since $\ln x = \log_e x$, the logarithmic equation $\ln x = y$ is equivalent to the exponential equation $e^y = x$.
* **Work:**
  1. Rewrite $\ln x = 5$ with its explicit base $e$: $\log_e x = 5$.
  2. Convert to exponential form ($\text{base}^{\text{exponent}} = \text{argument}$):
     $$e^5 = x \quad \text{(Choice \textbf{A})}$$

---

### **Question 2**
* **Problem:** Write the equation in its equivalent exponential form: $9 = \log_3 M$
* **Answer:** **`3^9 = M`** (or **`M = 3^9`**, written as $3^9 = M$)
* **The Rule:** For $b > 0, b \neq 1$, $y = \log_b x \iff b^y = x$.
* **Work:**
  1. Identify the base ($3$), the exponent ($9$), and the argument ($M$).
  2. Write in exponential form:
     $$3^9 = M$$

---

### **Question 3**
* **Problem:** Write the following equation in its equivalent exponential form: $4 = \log_b 256$
* **Answer:** **`b^4 = 256`** (written as $b^4 = 256$)
* **The Rule:** $y = \log_b x \iff b^y = x$.
* **Work:**
  1. Identify the base ($b$), the exponent ($4$), and the argument ($256$).
  2. Convert to exponential form:
     $$b^4 = 256$$

---

### **Question 4**
* **Problem:** Write the following equation in its equivalent exponential form: $\log_4 256 = y$
* **Answer:** **`4^y = 256`** (written as $4^y = 256$)
* **The Rule:** $\log_b x = y \iff b^y = x$.
* **Work:**
  1. Identify the base ($4$), the exponent ($y$), and the argument ($256$).
  2. Convert to exponential form:
     $$4^y = 256$$

---

### **Question 5**
* **Problem:** Write the equation in its equivalent exponential form. Then solve for $x$: $\log_2(x - 1) = 4$
  * $\log_2(x - 1) = 4$ in its equivalent exponential form is _______. (Do not simplify.)
  * $x =$ _______
* **Answer:**
  * **Exponential form:** **`x - 1 = 2^4`** (or **`2^4 = x - 1`**, written as $x - 1 = 2^4$)
  * **Solution:** $x =$ **`17`**
* **The Rule:** Convert $\log_b(\text{expression}) = y$ to $\text{expression} = b^y$, then solve for $x$.
* **Work:**
  1. Convert $\log_2(x - 1) = 4$ to exponential form without simplifying $2^4$:
     $$x - 1 = 2^4$$
  2. Evaluate $2^4 = 16$ and solve for $x$:
     $$x - 1 = 16 \implies x = 17$$

---

### **Question 6**
* **Problem:** Write the equation in its equivalent exponential form. Then solve for $x$: $\log_4 x = -2$
  * $\log_4 x = -2$ in its equivalent exponential form is _______. (Do not simplify.)
  * $x =$ _______
* **Answer:**
  * **Exponential form:** **`x = 4^(-2)`** (or **`4^(-2) = x`**, written as $x = 4^{-2}$)
  * **Solution:** $x =$ **`1/16`**
* **The Rule:** Convert $\log_b x = y$ to $x = b^y$ and apply the negative exponent rule $b^{-n} = \frac{1}{b^n}$.
* **Work:**
  1. Convert $\log_4 x = -2$ to exponential form:
     $$x = 4^{-2}$$
  2. Evaluate the negative power:
     $$x = \frac{1}{4^2} = \frac{1}{16}$$

---

### **Question 7**
* **Problem:** Evaluate or simplify the expression without using a calculator: $\ln e^{4x}$
* **Answer:** **`4x`**
* **The Rule:** Inverse Property of Natural Logarithms: $\ln(e^u) = u$ for any real expression $u$.
* **Work:**
  1. Since the natural logarithm has base $e$, $\ln(e^{4x})$ simplifies directly to the exponent:
     $$\ln e^{4x} = 4x$$

---

### **Question 8**
* **Problem:** Use properties of logarithms to condense the logarithmic expression. Write the expression as a single logarithm whose coefficient is $1$. Where possible, evaluate logarithmic expressions: $\ln x + \ln 2$
* **Answer:** **`ln(2x)`** (written as $\ln(2x)$)
* **Graph Equation:** `y = ln(2*x)`
* **The Rule:** Product Rule for Logarithms: $\ln M + \ln N = \ln(MN)$.
* **Work:**
  1. Combine the sum of two natural logarithms into the natural logarithm of their product:
     $$\ln x + \ln 2 = \ln(x \cdot 2) = \ln(2x)$$

---

### **Question 9**
* **Problem:** Use properties of logarithms to condense the logarithmic expression. Write the expression as a single logarithm whose coefficient is $1$. Where possible, evaluate logarithmic expressions: $\log(5x + 4) - \log(x)$
* **Answer:** **`log((5x + 4)/x)`** (written as $\log\left(\frac{5x + 4}{x}\right)$)
* **Graph Equation:** `y = log10((5*x + 4)/x)`
* **The Rule:** Quotient Rule for Logarithms: $\log M - \log N = \log\left(\frac{M}{N}\right)$.
* **Work:**
  1. Combine the difference of two common logarithms into the common logarithm of their quotient:
     $$\log(5x + 4) - \log(x) = \log\left(\frac{5x + 4}{x}\right)$$

---

### **Question 10**
* **Problem:** Use properties of logarithms to condense the logarithmic expression. Write the expression as a single logarithm whose coefficient is $1$. Where possible, evaluate logarithmic expressions: $\log_2(x - 8) - \log_2(x - 4)$
* **Answer:** **C. $\log_2\left(\frac{x - 8}{x - 4}\right)$**
* **Graph Equation:** `y = ln((x - 8)/(x - 4))/ln(2)`
* **The Rule:** Quotient Rule for Logarithms: $\log_b M - \log_b N = \log_b\left(\frac{M}{N}\right)$.
* **Work:**
  1. Apply the quotient property of base-$2$ logarithms:
     $$\log_2(x - 8) - \log_2(x - 4) = \log_2\left(\frac{x - 8}{x - 4}\right) \quad \text{(Choice \textbf{C})}$$

---

### **Question 11**
* **Problem:** Match each equation in Column I with the best first step for solving it in Column II.
  * $10^x = 190$
  * $e^{7x - 1} = 25$
  * $\log_9(x^2 - 13) = 7$
  * $e^{7x}e^x = 7e$
  * $7e^{2x} - 7e^x = 0$
  * $\log(7x - 1) + \log(x + 9) = 1$
* **Answer:**
  * $10^x = 190 \rightarrow$ **`D`** (Take the common logarithm on each side.)
  * $e^{7x - 1} = 25 \rightarrow$ **`B`** (Take the natural logarithm on each side.)
  * $\log_9(x^2 - 13) = 7 \rightarrow$ **`F`** (Change to exponential form.)
  * $e^{7x}e^x = 7e \rightarrow$ **`E`** (Use the product rule for exponents.)
  * $7e^{2x} - 7e^x = 0 \rightarrow$ **`C`** (Let $u = e^x$ and write the equation in quadratic form.)
  * $\log(7x - 1) + \log(x + 9) = 1 \rightarrow$ **`A`** (Write the sum of logarithms as the logarithm of a product.)
* **The Rule:** Choose the algebraic or logarithmic property that isolates the exponential/logarithmic term or reduces the equation to a simpler form.
* **Work:**
  1. **$10^x = 190$:** Since the base is $10$, taking the common ($\log_{10}$) logarithm on each side immediately isolates $x$ (**D**).
  2. **$e^{7x - 1} = 25$:** Since the base is $e$, taking the natural ($\ln$) logarithm on each side eliminates the base $e$ (**B**).
  3. **$\log_9(x^2 - 13) = 7$:** A single logarithm equal to a constant is solved by converting to exponential form $x^2 - 13 = 9^7$ (**F**).
  4. **$e^{7x}e^x = 7e$:** Multiply the like-base exponentials on the left side using the product rule for exponents ($e^{7x+x} = e^{8x}$) (**E**).
  5. **$7e^{2x} - 7e^x = 0$:** Since $e^{2x} = (e^x)^2$, substituting $u = e^x$ turns the equation into the quadratic $7u^2 - 7u = 0$ (**C**).
  6. **$\log(7x - 1) + \log(x + 9) = 1$:** Condense the sum of two logarithms on the left into a single logarithm of a product, $\log[(7x-1)(x+9)] = 1$ (**A**).
