# Answer Sheet: Build Understanding 4.3 Logarithmic Functions

**Course:** MAT1340003 College Algebra: MA1 (Steven Yamiolkoski) FA26  
**Assignment:** Build Understanding 4.3 Logarithmic Functions  

---

### **Question 1**
* **Problem:** Match the logarithm in Column I with its value in Column II:
  * (a) $\log_2 16$
  * (b) $\log_3 1$
  * (c) $\log_{10} 0.1$
  * (d) $\log_2 \sqrt{2}$
  * (e) $\log_e \left(\frac{1}{e^2}\right)$
  * (f) $\log_{1/2} 8$
* **Answer:**
  * **(1) [for a]: `4`**
  * **(2) [for b]: `0`**
  * **(3) [for c]: `-1`**
  * **(4) [for d]: `1/2`**
  * **(5) [for e]: `-2`**
  * **(6) [for f]: `-3`**
* **The Rule:** $\log_a x = y \iff a^y = x$.
* **Work:**
  * (a) $2^4 = 16 \implies \log_2 16 = 4$.
  * (b) $3^0 = 1 \implies \log_3 1 = 0$.
  * (c) $10^{-1} = 0.1 \implies \log_{10} 0.1 = -1$.
  * (d) $2^{1/2} = \sqrt{2} \implies \log_2 \sqrt{2} = \frac{1}{2}$.
  * (e) $e^{-2} = \frac{1}{e^2} \implies \log_e(e^{-2}) = -2$.
  * (f) $\left(\frac{1}{2}\right)^{-3} = 2^3 = 8 \implies \log_{1/2} 8 = -3$.

---

### **Question 2**
* **Problem:** Match the logarithm in Column I with its value in Column II:
  * (a) $\log_3 81$
  * (b) $\log_3 \frac{1}{3}$
  * (c) $\log_{10} 0.01$
  * (d) $\log_6 \sqrt{6}$
  * (e) $\log_e 1$
  * (f) $\log_3 27^{3/2}$
* **Answer:**
  * **(1) [for a]: `4`**
  * **(2) [for b]: `-1`**
  * **(3) [for c]: `-2`**
  * **(4) [for d]: `1/2`**
  * **(5) [for e]: `0`**
  * **(6) [for f]: `9/2`**
* **The Rule:** Rewrite each argument as a power of the base $a$, then use $\log_a(a^k) = k$.
* **Work:**
  * (a) $3^4 = 81 \implies \log_3 81 = 4$.
  * (b) $3^{-1} = \frac{1}{3} \implies \log_3 \frac{1}{3} = -1$.
  * (c) $10^{-2} = 0.01 \implies \log_{10} 0.01 = -2$.
  * (d) $6^{1/2} = \sqrt{6} \implies \log_6 \sqrt{6} = \frac{1}{2}$.
  * (e) $e^0 = 1 \implies \log_e 1 = 0$.
  * (f) $27^{3/2} = (3^3)^{3/2} = 3^{9/2} \implies \log_3 27^{3/2} = \frac{9}{2}$.

---

### **Question 3**
* **Problem:** Write in exponential form: $\log_3 81 = 4$.
* **Answer:** **`3^4 = 81`**
* **The Rule:** $\log_b x = y \iff b^y = x$.
* **Work:**
  * Base $= 3$, exponent $= 4$, result $= 81 \implies 3^4 = 81$.

---

### **Question 4**
* **Problem:** Write in logarithmic form: $6^3 = 216$. What is the equivalent logarithmic form? $\log_6 \text{[Box 1]} = \text{[Box 2]}$.
* **Answer:** **Box 1: `216`, Box 2: `3`** ($\log_6 216 = 3$)
* **The Rule:** $b^y = x \iff \log_b x = y$.
* **Work:**
  * Base $6$ raised to exponent $3$ equals $216 \implies \log_6(216) = 3$.

---

### **Question 5**
* **Problem:** Solve the given logarithmic equation: $\log_{121} \sqrt[5]{11} = x$.
* **Answer:** **`1/10`** (or `\frac{1}{10}`)
* **The Rule:** Convert to exponential form $121^x = \sqrt[5]{11}$ and express both sides with base $11$.
* **Work:**
  * $121^x = 11^{1/5} \implies (11^2)^x = 11^{1/5} \implies 11^{2x} = 11^{1/5}$.
  * $2x = \frac{1}{5} \implies x = \frac{1}{10}$.

---

### **Question 6**
* **Problem:** Sketch the graph of the function $f(x) = \log_2 x$. Give the domain and range.
* **Answer:**
  * **Graph:** **`Choice A`**
  * **Domain:** `(0, \infty)`
  * **Range:** `(-\infty, \infty)`
* **Graph Equation:** `f(x) = ln(x) / ln(2)`
* **The Rule:** For $b > 1$, $f(x) = \log_b x$ lies to the right of the $y$-axis, passes through $(1, 0)$, and rises slowly from left to right.
* **Work:**
  * At $x = 1, y = 0$; at $x = 2, y = 1$; at $x = 32, y = 5$.
  * **Choice A** passes through $(1, 0)$ and increases through $(32, 5)$ with vertical asymptote $x = 0$.
  * Domain: $(0, \infty)$, Range: $(-\infty, \infty)$.

---

### **Question 7**
* **Problem:** Graph the following function $f(x) = \log_{1/6} x$. Label the vertical asymptote. State the domain and range.
* **Answer:**
  * **Graph:** **`Choice D`**
  * **Domain:** `(0, \infty)`
  * **Range:** `(-\infty, \infty)`
* **Graph Equation:** `f(x) = -ln(x) / ln(6)`
* **The Rule:** For $0 < b < 1$, $f(x) = \log_b x$ lies to the right of the vertical asymptote $x = 0$, passes through $(1, 0)$, and decreases from left to right.
* **Work:**
  * Since base $\frac{1}{6} < 1$, as $x$ increases, $f(x)$ decreases (from $+\infty$ near $x = 0^+$ down through $(1, 0)$ and $(6, -1)$).
  * **Choice D** shows the curve decreasing through $(1, 0)$ with vertical asymptote $x = 0$.
  * Domain: $(0, \infty)$, Range: $(-\infty, \infty)$.

---

### **Question 8**
* **Problem:** Use the properties of logarithms to rewrite the following expression: $\log_{10} \frac{6x}{13}$.
* **Answer:** **`\log_{10} 6 + \log_{10} x - \log_{10} 13`**
* **The Rule:** Quotient and Product Rules of Logarithms: $\log_b\left(\frac{u \cdot v}{w}\right) = \log_b u + \log_b v - \log_b w$.
* **Work:**
  * $\log_{10}\left(\frac{6x}{13}\right) = \log_{10}(6x) - \log_{10} 13 = \log_{10} 6 + \log_{10} x - \log_{10} 13$.

---

### **Question 9**
* **Problem:** Use the properties of logarithms to rewrite the following expression: $5\log_4 x - 6\log_4 y$.
* **Answer:** **`\log_4\left(\frac{x^5}{y^6}\right)`**
* **The Rule:** Power Rule ($k\log_b u = \log_b(u^k)$) followed by Quotient Rule ($\log_b u - \log_b v = \log_b\left(\frac{u}{v}\right)$).
* **Work:**
  * $5\log_4 x - 6\log_4 y = \log_4(x^5) - \log_4(y^6) = \log_4\left(\frac{x^5}{y^6}\right)$.

---

### **Question 10**
* **Problem:** Write in logarithmic form: $5^2 = 25$. What is the equivalent logarithmic form? $\log_5 \text{[Box 1]} = \text{[Box 2]}$.
* **Answer:** **Box 1: `25`, Box 2: `2`** ($\log_5 25 = 2$)
* **The Rule:** $b^y = x \iff \log_b x = y$.
* **Work:**
  * $5^2 = 25 \iff \log_5 25 = 2$.

---

### **Question 11**
* **Problem:** Write the given statement in an equivalent logarithmic form: $\left(\frac{2}{5}\right)^{-3} = \frac{125}{8}$.
* **Answer:** **`Choice D:` $\log_{2/5} \frac{125}{8} = -3$**
* **The Rule:** Base $= \frac{2}{5}$, argument $= \frac{125}{8}$, exponent $= -3 \implies \log_{2/5}\left(\frac{125}{8}\right) = -3$.
* **Work:**
  * Applying $b^y = x \iff \log_b x = y$ gives $\log_{2/5} \frac{125}{8} = -3$ (**Choice D**).

---

### **Question 12**
* **Problem:** Write in exponential form: $\log_7 343 = 3$.
* **Answer:** **`7^3 = 343`**
* **The Rule:** $\log_b x = y \iff b^y = x$.
* **Work:**
  * Base $= 7$, exponent $= 3$, result $= 343 \implies 7^3 = 343$.

---

### **Question 13**
* **Problem:** Write the given statement in an equivalent exponential form: $\log_{\sqrt{5}} 625 = 8$.
* **Answer:** **`(\sqrt{5})^8 = 625`**
* **The Rule:** $\log_b x = y \iff b^y = x$. Do not simplify.
* **Work:**
  * Base $= \sqrt{5}$, exponent $= 8$, result $= 625 \implies (\sqrt{5})^8 = 625$.

---

### **Question 15**
* **Problem:** Solve the logarithmic equation: $x = \log_3 \frac{1}{9}$.
* **Answer:** **`-2`**
* **The Rule:** $\log_b(b^k) = k$.
* **Work:**
  * $\frac{1}{9} = \frac{1}{3^2} = 3^{-2} \implies x = \log_3(3^{-2}) = -2$.

---

### **Question 16**
* **Problem:** Solve the logarithmic equation: $x = \log_4 \sqrt[3]{4}$.
* **Answer:** **`1/3`** (or `\frac{1}{3}`)
* **The Rule:** Rewrite the radical as a fractional exponent: $\sqrt[3]{4} = 4^{1/3}$.
* **Work:**
  * $x = \log_4(4^{1/3}) = \frac{1}{3}$.

---

### **Question 17**
* **Problem:** Solve the logarithmic equation: $x = 10^{\log(12)}$.
* **Answer:** **`12`**
* **The Rule:** Inverse property of logarithms: $b^{\log_b(u)} = u$. Since $\log(12)$ is base $10$, $10^{\log_{10}(12)} = 12$.
* **Work:**
  * $x = 10^{\log_{10}(12)} = 12$.

---

### **Question 18**
* **Problem:** Solve the logarithmic equation: $x = 10^{\log(1)}$.
* **Answer:** **`1`**
* **The Rule:** $10^{\log_{10}(u)} = u$ (or $\log(1) = 0 \implies 10^0 = 1$).
* **Work:**
  * $x = 10^{\log(1)} = 10^0 = 1$.

---

### **Question 19**
* **Problem:** Solve the given logarithmic equation: $\log_5 x = 2$.
* **Answer:** **`25`**
* **The Rule:** Convert $\log_b x = y$ to exponential form $x = b^y$.
* **Work:**
  * $x = 5^2 = 25$.

---

### **Question 20**
* **Problem:** Solve the given logarithmic equation: $x = \log_5 \sqrt[3]{25}$.
* **Answer:** **`2/3`** (or `\frac{2}{3}`)
* **The Rule:** Express $\sqrt[3]{25}$ as a power of $5$: $\sqrt[3]{5^2} = 5^{2/3}$.
* **Work:**
  * $x = \log_5(5^{2/3}) = \frac{2}{3}$.

---

### **Question 21**
* **Problem:** Solve the given logarithmic equation: $\log_{36} x = \frac{3}{2}$.
* **Answer:** **`216`**
* **The Rule:** Convert to exponential form: $x = 36^{3/2}$.
* **Work:**
  * $x = 36^{3/2} = (\sqrt{36})^3 = 6^3 = 216$.

---

### **Question 22**
* **Problem:** Solve the given logarithmic equation: $\log_{1/4}(x + 2) = -3$.
* **Answer:** **`62`**
* **The Rule:** Convert to exponential form: $x + 2 = \left(\frac{1}{4}\right)^{-3}$.
* **Work:**
  * $x + 2 = \left(\frac{1}{4}\right)^{-3} = 4^3 = 64 \implies x = 64 - 2 = 62$.

---

### **Question 23**
* **Problem:** Solve the given logarithmic equation: $\log_{(x + 7)} 13 = 1$.
* **Answer:** **`6`**
* **The Rule:** Convert to exponential form: $(x + 7)^1 = 13$.
* **Work:**
  * $x + 7 = 13 \implies x = 6$. (Check base: $6 + 7 = 13 > 0$ and $\neq 1$).

---

### **Question 25**
* **Problem:** Graph the equation on paper, then choose the correct graph: $y = \log_6 x$.
* **Answer:** **`Choice C`**
* **Graph Equation:** `y = ln(x) / ln(6)`
* **The Rule:** Since base $6 > 1$, the graph is in Quadrants I and IV ($x > 0$), passes through $(1, 0)$, and increases as $x$ increases.
* **Work:**
  * Choice A is exponential growth; Choice B is exponential decay; Choice D is logarithmic decay ($\log_{1/6} x$).
  * **Choice C** passes through $(1, 0)$, has vertical asymptote $x = 0$, and rises from left to right.

---

### **Question 26**
* **Problem:** Graph the function: $f(x) = \log_2(x + 3)$.
* **Answer:** **Plot the vertical asymptote at $x = -3$ and the logarithmic curve shifted $3$ units left, passing through $(-2, 0)$ and $(-1, 1)$.**
* **Graph Equation:** `f(x) = ln(x + 3) / ln(2)`
* **The Rule:** Replacing $x$ with $x + 3$ shifts the graph of $\log_2 x$ and its vertical asymptote $3$ units to the left.
* **Work:**
  * Vertical asymptote: $x = -3$.
  * Key points: $(-2, 0)$, $(-1, 1)$, $(1, 2)$, $(5, 3)$.

---

### **Question 27**
* **Problem:** Graph the function $f(x) = \log_{1/2}(x + 1) - 4$.
* **Answer:** **Plot the vertical asymptote at $x = -1$ and the decreasing logarithmic curve shifted $1$ unit left and $4$ units down, passing through $(0, -4)$ and $(1, -5)$.**
* **Graph Equation:** `f(x) = -ln(x + 1) / ln(2) - 4`
* **The Rule:** $x + 1$ shifts left $1$ unit; $- 4$ shifts down $4$ units.
* **Work:**
  * Vertical asymptote: $x = -1$.
  * Key points: at $x = 0$, $f(0) = \log_{1/2}(1) - 4 = -4$; at $x = 1$, $f(1) = \log_{1/2}(2) - 4 = -1 - 4 = -5$.

---

### **Question 28**
* **Problem:** Graph the function $f(x) = (\log_2 x) + 5$. Give the domain and range.
* **Answer:**
  * **Transformation:** **`Choice A: The graph of f(x) = log_2 x should be translated 5 units up.`**
  * **Domain:** `(0, \infty)`
  * **Range:** `(-\infty, \infty)`
* **Graph Equation:** `f(x) = ln(x) / ln(2) + 5`
* **The Rule:** Adding $5$ outside the logarithm shifts the graph $5$ units up without changing the vertical asymptote $x = 0$ or the domain $(0, \infty)$.
* **Work:**
  * Shift $5$ units up (**Choice A**).
  * Domain: $(0, \infty)$; Range: $(-\infty, \infty)$.

---

### **Question 29**
* **Problem:** Graph the function $f(x) = \log_{1/2}(x - 5)$. Give the domain and range.
* **Answer:**
  * **Domain:** `(5, \infty)`
  * **Range:** `(-\infty, \infty)`
* **Graph Equation:** `f(x) = -ln(x - 5) / ln(2)`
* **The Rule:** The argument of a logarithm must be strictly positive: $x - 5 > 0 \implies x > 5$.
* **Work:**
  * Vertical asymptote is $x = 5$.
  * Domain: $(5, \infty)$; Range: $(-\infty, \infty)$.

---

### **Question 30**
* **Problem:** Write an equation for the given graph (vertical asymptote $x = -4$, passing through $(-3, -2)$ and $(0, 0)$).
* **Answer:** **`Choice A:` $f(x) = \log_2(x + 4) - 2$**
* **Graph Equation:** `f(x) = ln(x + 4) / ln(2) - 2`
* **The Rule:** Vertical asymptote $x = -4$ requires $(x + 4)$ inside the logarithm; plug in $(0, 0)$ to determine whether the base is $2$ or $3$.
* **Work:**
  * Since the vertical asymptote is $x = -4$, the argument is $x + 4$ (eliminating Choices C and D).
  * The graph clearly passes through the origin $(0, 0)$ and $(-2, -1)$.
  * Test $(0, 0)$ in Choice A: $f(0) = \log_2(0 + 4) - 2 = \log_2(4) - 2 = 2 - 2 = 0$.
  * (In Choice B, $f(0) = \log_3(4) - 2 \neq 0$). Thus, **Choice A** is correct.

---

### **Question 31**
* **Problem:** Use the properties of logarithms to rewrite the expression: $\log_3\left(\frac{4y}{z}\right)$.
* **Answer:** **`Choice D:` $\log_3 4 + \log_3 y - \log_3 z$**
* **The Rule:** $\log_b\left(\frac{u \cdot v}{w}\right) = \log_b u + \log_b v - \log_b w$.
* **Work:**
  * $\log_3\left(\frac{4y}{z}\right) = \log_3(4y) - \log_3 z = \log_3 4 + \log_3 y - \log_3 z$ (**Choice D**).

---

### **Question 32**
* **Problem:** Use the properties of logarithms to rewrite the expression: $\log_4\left(\frac{3\sqrt{6}}{5}\right)$.
* **Answer:** **`Choice D:` $\log_4 3 + \frac{1}{2}\log_4 6 - \log_4 5$**
* **The Rule:** Expand products, quotients, and radicals ($\sqrt{6} = 6^{1/2}$).
* **Work:**
  * $\log_4\left(\frac{3 \cdot 6^{1/2}}{5}\right) = \log_4 3 + \log_4(6^{1/2}) - \log_4 5 = \log_4 3 + \frac{1}{2}\log_4 6 - \log_4 5$ (**Choice D**).

---

### **Question 33**
* **Problem:** Use the properties of logarithms to rewrite the following expression: $\log_2(6x + 7y)$.
* **Answer:** **`Choice B: The expression cannot be simplified.`**
* **The Rule:** There is no logarithm property for the logarithm of a sum $\log_b(u + v)$.
* **Work:**
  * Because the argument $6x + 7y$ is a sum that cannot be factored, **the expression cannot be simplified** (**Choice B**).

---

### **Question 34**
* **Problem:** Use the properties of logarithms to rewrite the expression: $\log_2 \sqrt{\frac{3r^7}{z^5}}$.
* **Answer:** **`Choice A:` `\frac{1}{2}\log_2 3 + \frac{7}{2}\log_2 r - \frac{5}{2}\log_2 z`** (or `\frac{1}{2}(\log_2 3 + 7\log_2 r - 5\log_2 z)`)
* **The Rule:** Rewrite the square root as an exponent of $\frac{1}{2}$, then apply the Quotient and Product Rules.
* **Work:**
  * $\log_2 \left(\frac{3r^7}{z^5}\right)^{1/2} = \frac{1}{2}\left(\log_2 3 + \log_2(r^7) - \log_2(z^5)\right) = \frac{1}{2}\log_2 3 + \frac{7}{2}\log_2 r - \frac{5}{2}\log_2 z$.

---

### **Question 35**
* **Problem:** Use the properties of logarithms to rewrite the following expression: $\log_2\left(\frac{xy}{zt}\right)$.
* **Answer:** **`Choice A:` `\log_2 x + \log_2 y - \log_2 z - \log_2 t`**
* **The Rule:** Factors in the numerator have positive logs; factors in the denominator have negative logs.
* **Work:**
  * $\log_2\left(\frac{xy}{zt}\right) = \log_2(xy) - \log_2(zt) = \log_2 x + \log_2 y - (\log_2 z + \log_2 t) = \log_2 x + \log_2 y - \log_2 z - \log_2 t$.

---

### **Question 36**
* **Problem:** Use the properties of logarithms to rewrite the expression: $\log_3 \frac{\sqrt{x}\sqrt[7]{y}}{w^5\sqrt{z}}$.
* **Answer:** **`Choice B:` $\frac{1}{2}\log_3 x + \frac{1}{7}\log_3 y - 5\log_3 w - \frac{1}{2}\log_3 z$**
* **The Rule:** Convert radicals to fractional exponents ($\sqrt{x} = x^{1/2}, \sqrt[7]{y} = y^{1/7}, \sqrt{z} = z^{1/2}$) and expand.
* **Work:**
  * $\log_3\left(\frac{x^{1/2} y^{1/7}}{w^5 z^{1/2}}\right) = \frac{1}{2}\log_3 x + \frac{1}{7}\log_3 y - 5\log_3 w - \frac{1}{2}\log_3 z$ (**Choice B**).

---

### **Question 37**
* **Problem:** Write the expression as a single logarithm with coefficient $1$: $\log_d x + \log_d y - \log_d f$.
* **Answer:** **`Choice B:` $\log_d \frac{xy}{f}$**
* **The Rule:** Combine sums into products in the numerator and differences into the denominator.
* **Work:**
  * $\log_d x + \log_d y - \log_d f = \log_d(xy) - \log_d f = \log_d\left(\frac{xy}{f}\right)$ (**Choice B**).

---

### **Question 38**
* **Problem:** Write the expression as a single logarithm with coefficient $1$: $\log_c m - \log_c n - \log_c k$.
* **Answer:** **`Choice B:` $\log_c \frac{m}{nk}$**
* **The Rule:** Both subtracted logarithms go into the denominator: $\log_c m - (\log_c n + \log_c k) = \log_c\left(\frac{m}{nk}\right)$.
* **Work:**
  * $\log_c m - \log_c n - \log_c k = \log_c\left(\frac{m}{nk}\right)$ (**Choice B**).

---

### **Question 39**
* **Problem:** Write the expression as a single logarithm with coefficient $1$: $2\log_b(z + 2) + \log_b(3z + 3)$.
* **Answer:** **`Choice A:` $\log_b (z + 2)^2(3z + 3)$**
* **The Rule:** Apply the Power Rule first ($2\log_b(z+2) = \log_b(z+2)^2$), then the Product Rule.
* **Work:**
  * $2\log_b(z + 2) + \log_b(3z + 3) = \log_b(z + 2)^2 + \log_b(3z + 3) = \log_b\left((z + 2)^2(3z + 3)\right)$ (**Choice A**).
