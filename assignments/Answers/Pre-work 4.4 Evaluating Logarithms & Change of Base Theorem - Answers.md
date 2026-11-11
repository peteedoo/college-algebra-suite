# **Assignment: Pre-work 4.4 Evaluating Logarithms & Change of Base Theorem**

---

### **Question 1**
* **Problem:** For the exponential function $f(x) = a^x$, where $a > 1$, is the function increasing or decreasing over its entire domain?
* **Answer:** **A. increasing**
* **Graph Equation:** `f(x) = 2^x`
* **The Rule:** An exponential function $f(x) = a^x$ with base $a > 1$ is strictly increasing over its entire domain $(-\infty, \infty)$, whereas for $0 < a < 1$ it is strictly decreasing.
* **Work:**
  1. Given $f(x) = a^x$ with base $a > 1$.
  2. As $x$ increases from left to right, $a^x$ grows larger without bound.
  3. Therefore, the function is **increasing** over its entire domain (Choice **A**).

---

### **Question 2**
* **Problem:** For the logarithmic function $g(x) = \log_a x$, where $a > 1$, is the function increasing or decreasing over its entire domain?
* **Answer:** **D. Increasing, because $a > 1$.**
* **Graph Equation:** `g(x) = ln(x)/ln(2)`
* **The Rule:** Since $g(x) = \log_a x$ is the inverse of the exponential function $f(x) = a^x$, it is increasing over its entire domain $(0, \infty)$ when $a > 1$ and decreasing when $0 < a < 1$.
* **Work:**
  1. Note that a logarithmic function does not always increase or always decrease; its behavior depends on whether the base $a$ satisfies $a > 1$ or $0 < a < 1$.
  2. Because the base satisfies $a > 1$, $g(x) = \log_a x$ is **increasing, because $a > 1$** (Choice **D**).

---

### **Question 3**
* **Problem:** If $f(x) = 15^x$, what is $f^{-1}(x)$?
* **Answer:** $f^{-1}(x) =$ **`log_15(x)`** (written as $\log_{15} x$)
* **Graph Equation:** `f(x) = ln(x)/ln(15)`
* **The Rule:** The inverse of the exponential function $f(x) = a^x$ is the logarithmic function with the same base, $f^{-1}(x) = \log_a x$.
* **Work:**
  1. Replace $f(x)$ with $y$: $y = 15^x$.
  2. Interchange $x$ and $y$: $x = 15^y$.
  3. Solve for $y$ by converting from exponential form to logarithmic form: $y = \log_{15} x$.
  4. Replace $y$ with $f^{-1}(x)$: $f^{-1}(x) = \log_{15} x$.

---

### **Question 4**
* **Problem:** What is the name given to the exponent to which $2$ must be raised to obtain $17$?
* **Answer:** The expression **`log_2(17)`** ($\log_2 17$) represents the exponent to which $2$ must be raised in order to obtain $17$.
* **The Rule:** By definition of a logarithm, $\log_a x$ is the exponent to which the base $a$ must be raised to obtain $x$ ($a^{\log_a x} = x$).
* **Work:**
  1. Let $y$ be the exponent to which base $2$ is raised to yield $17$: $2^y = 17$.
  2. Rewriting in logarithmic form gives $y = \log_2 17$.

---

### **Question 5**
* **Problem:** Answer the following: A base $e$ logarithm is called a (1) _______ logarithm, and a base $10$ logarithm is called a (2) _______ logarithm.
* **Answer:** (1) **`natural`**, (2) **`common`**
* **The Rule:** A logarithm with base $e$ ($\log_e x = \ln x$) is called a **natural** logarithm, and a logarithm with base $10$ ($\log_{10} x = \log x$) is called a **common** logarithm.
* **Work:**
  1. Base $e$ logarithm $\rightarrow$ **natural** logarithm.
  2. Base $10$ logarithm $\rightarrow$ **common** logarithm.

---

### **Question 6**
* **Problem:** Write $\log_4 36$ in terms of natural logarithms using the change-of-base theorem. (Do not evaluate. Do not simplify.)
* **Answer:** **`ln(36)/ln(4)`** (written as $\frac{\ln 36}{\ln 4}$)
* **The Rule:** Change-of-Base Theorem (for natural logarithms): For any positive real numbers $x, a$ with $a \neq 1$, $\log_a x = \frac{\ln x}{\ln a}$.
* **Work:**
  1. Identify the base $a = 4$ and the argument $x = 36$.
  2. Apply the change-of-base formula using base $e$ ($\ln$):
     $$\log_4 36 = \frac{\ln 36}{\ln 4}$$

---

### **Question 7**
* **Problem:** Why is $\log_2 0$ undefined?
* **Answer:** **B. There is no power of $2$ that yields a result of $0$.**
* **The Rule:** For any base $a > 0$ ($a \neq 1$), $a^y > 0$ for all real numbers $y$. Therefore, $a^y = 0$ has no solution, and $\log_a 0$ is undefined.
* **Work:**
  1. Suppose $\log_2 0 = y$.
  2. In equivalent exponential form, this means $2^y = 0$.
  3. Since $2^y > 0$ for every real number $y$, there is no power of $2$ that yields a result of $0$ (Choice **B**).

---

### **Question 8**
* **Problem:** Between what two consecutive integers must $\log_4 15$ lie? (Use ascending order.)
* **Answer:** The expression $\log_4 15$ must lie between **`1`** and **`2`**.
* **The Rule:** Since $f(x) = \log_4 x$ is strictly increasing, if $4^n < 15 < 4^{n+1}$, then $n < \log_4 15 < n + 1$.
* **Work:**
  1. Find consecutive integer powers of $4$ that bound $15$:
     $$4^1 = 4 \quad \text{and} \quad 4^2 = 16$$
  2. Since $4 < 15 < 16$, taking $\log_4$ of all parts gives:
     $$\log_4(4^1) < \log_4 15 < \log_4(4^2)$$
     $$1 < \log_4 15 < 2$$
  3. Thus, $\log_4 15$ lies between **`1`** and **`2`**.

---

### **Question 9**
* **Problem:** The graph of $y = \log x$ shows a point on the graph at $(2, 0.30103)$. Write the logarithmic equation associated with that point.
* **Answer:** **A. $\log 2 = 0.30103$**
* **Graph Equation:** `y = log10(x)`
* **The Rule:** A point $(x_0, y_0)$ lies on the graph of $y = \log x$ if and only if $y_0 = \log x_0$.
* **Work:**
  1. From the given point $(2, 0.30103)$, substitute $x = 2$ and $y = 0.30103$ into $y = \log x$.
  2. We obtain $0.30103 = \log 2$, or equivalently $\log 2 = 0.30103$ (Choice **A**).

---

### **Question 10**
* **Problem:** The graph of $y = \ln x$ shows a point on the graph at $(2.5, 0.91629073)$. Write the logarithmic equation associated with that point.
* **Answer:** **`0.91629073 = ln 2.5`** (4th option: $0.91629073 = \ln 2.5.$)
* **Graph Equation:** `y = ln(x)`
* **The Rule:** A point $(x_0, y_0)$ lies on the graph of $y = \ln x$ if and only if $y_0 = \ln x_0$.
* **Work:**
  1. Substitute the coordinates $x = 2.5$ and $y = 0.91629073$ into the equation $y = \ln x$.
  2. This gives **`0.91629073 = ln 2.5`**.
