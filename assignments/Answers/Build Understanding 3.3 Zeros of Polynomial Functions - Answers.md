# **Build Understanding 3.3 Zeros of Polynomial Functions — Answers**

### **Question 1**
* **Problem:** Use the factor theorem and synthetic division to decide whether the second polynomial is a factor of the first: $4x^4 + 11x^3 - 13x^2 + 161x + 1$; $x + 5$. Is $x + 5$ a factor of $4x^4 + 11x^3 - 13x^2 + 161x + 1$?
* **Answer:** **`No`**
* **Graph Equation:** `f(x) = 4*x^4 + 11*x^3 - 13*x^2 + 161*x + 1`
* **The Rule:** By the Factor Theorem, $x - k$ is a factor of $f(x)$ if and only if the remainder $f(k) = 0$.
* **Work:**
  Using synthetic division with $k = -5$ and coefficients $4, 11, -13, 161, 1$:
  - Bring down $4$.
  - $4(-5) + 11 = -9$
  - $-9(-5) - 13 = 32$
  - $32(-5) + 161 = 1$
  - $1(-5) + 1 = -4$
  Since $f(-5) = -4 \neq 0$, $x + 5$ is **not** a factor (`No`).

---

### **Question 2**
* **Problem:** Use the factor theorem and synthetic division to decide whether the second polynomial is a factor of the first: $-x^3 + 8x - 3$; $x + 3$. Is $x + 3$ a factor of $-x^3 + 8x - 3$?
* **Answer:** **`Yes`**
* **Graph Equation:** `f(x) = -x^3 + 8*x - 3`
* **The Rule:** $x + 3$ is a factor of $f(x)$ if and only if $f(-3) = 0$.
* **Work:**
  Using synthetic division with $k = -3$ and coefficients $-1, 0, 8, -3$:
  - Bring down $-1$.
  - $(-1)(-3) + 0 = 3$
  - $3(-3) + 8 = -1$
  - $(-1)(-3) - 3 = 0$
  Since the remainder is $0$, $x + 3$ is a factor (`Yes`).

---

### **Question 3**
* **Problem:** Use the factor theorem and synthetic division to decide whether the second polynomial is a factor of the first: $x^3 + 5x^2 + 9$; $x - 3$. Is $x - 3$ a factor of $x^3 + 5x^2 + 9$?
* **Answer:** **`No, because f(3) = 81`** (Enter **`81`** in the box)
* **Graph Equation:** `f(x) = x^3 + 5*x^2 + 9`
* **The Rule:** $x - 3$ is a factor of $f(x)$ if and only if $f(3) = 0$.
* **Work:**
  Using synthetic division with $k = 3$ and coefficients $1, 5, 0, 9$:
  - Bring down $1$.
  - $1(3) + 5 = 8$
  - $8(3) + 0 = 24$
  - $24(3) + 9 = 81$
  Since $f(3) = 81 \neq 0$, $x - 3$ is not a factor.

---

### **Question 4**
* **Problem:** Factor $f(x)$ into linear factors given that $k$ is a zero of $f(x)$: $f(x) = 4x^3 + 15x^2 - 81x + 70$; $k = 2$.
* **Answer:** **`(x - 2)(4x - 5)(x + 7)`**
* **Graph Equation:** `f(x) = 4*x^3 + 15*x^2 - 81*x + 70`
* **The Rule:** Divide $f(x)$ by $x - k$ using synthetic division, then factor the resulting quadratic quotient.
* **Work:**
  1. Synthetic division by $k = 2$ on coefficients $4, 15, -81, 70$:
     - Bring down $4$
     - $4(2) + 15 = 23$
     - $23(2) - 81 = -35$
     - $-35(2) + 70 = 0$
  2. Quotient is $4x^2 + 23x - 35 = (4x - 5)(x + 7)$.
  3. Complete factorization: $f(x) = (x - 2)(4x - 5)(x + 7)$.

---

### **Question 5**
* **Problem:** Factor $f(x) = 4x^3 - 3x^2 - 16x + 12$ into linear factors given that $-2$ is a zero of $f(x)$.
* **Answer:** **`(x + 2)(x - 2)(4x - 3)`**
* **Graph Equation:** `f(x) = 4*x^3 - 3*x^2 - 16*x + 12`
* **The Rule:** Divide $f(x)$ by $x + 2$ and factor the remaining quadratic.
* **Work:**
  1. Synthetic division by $k = -2$ on $4, -3, -16, 12$:
     - Bring down $4$
     - $4(-2) - 3 = -11$
     - $(-11)(-2) - 16 = 6$
     - $6(-2) + 12 = 0$
  2. Factor the quotient $4x^2 - 11x + 6 = (4x - 3)(x - 2)$.
  3. Complete factorization: $f(x) = (x + 2)(x - 2)(4x - 3)$.

---

### **Question 6**
* **Problem:** Factor $f(x)$ into linear factors given that $k$ is a zero of $f(x)$: $f(x) = x^4 + 3x^3 - 12x^2 - 52x - 48$; $k = -2$ (multiplicity 2).
* **Answer:** **`(x + 2)^2(x - 4)(x + 3)`**
* **Graph Equation:** `f(x) = x^4 + 3*x^3 - 12*x^2 - 52*x - 48`
* **The Rule:** Apply synthetic division twice with $k = -2$, then factor the quadratic quotient.
* **Work:**
  1. First synthetic division with $k = -2$ on $1, 3, -12, -52, -48$ gives quotient coefficients $1, 1, -14, -24$ and remainder $0$.
  2. Second synthetic division with $k = -2$ on $1, 1, -14, -24$ gives quotient coefficients $1, -1, -12$ and remainder $0$.
  3. Factor $x^2 - x - 12 = (x - 4)(x + 3)$.
  4. Complete factorization: $f(x) = (x + 2)^2(x - 4)(x + 3)$.

---

### **Question 7**
* **Problem:** Given that $4$ is a zero of the polynomial function $f(x) = x^3 - 6x^2 + 18x - 40$, find the remaining zeros.
* **Answer:** **`1 - 3i, 1 + 3i`**
* **Graph Equation:** `f(x) = x^3 - 6*x^2 + 18*x - 40`
* **The Rule:** Divide $f(x)$ by $x - 4$ and solve the resulting quadratic equation using the quadratic formula.
* **Work:**
  1. Synthetic division with $k = 4$ on $1, -6, 18, -40$:
     - Bring down $1$
     - $1(4) - 6 = -2$
     - $(-2)(4) + 18 = 10$
     - $10(4) - 40 = 0$
  2. Solve $x^2 - 2x + 10 = 0$:
     $$x = \frac{2 \pm \sqrt{(-2)^2 - 4(1)(10)}}{2} = \frac{2 \pm \sqrt{-36}}{2} = 1 \pm 3i$$

---

### **Question 8**
* **Problem:** Use the Rational Zero Theorem to list all possible rational zeros for $f(x) = x^3 + 13x^2 - 14x + 14$.
* **Answer:** **Choice B** (`-1, 1, -2, 2, -7, 7, -14, 14`)
* **Graph Equation:** `f(x) = x^3 + 13*x^2 - 14*x + 14`
* **The Rule:** Every rational zero $p/q$ has $p$ dividing the constant term ($14$) and $q$ dividing the leading coefficient ($1$).
* **Work:**
  - Factors of $14$: $\pm 1, \pm 2, \pm 7, \pm 14$
  - Factors of $1$: $\pm 1$
  - Possible rational zeros: $-1, 1, -2, 2, -7, 7, -14, 14$ (**Choice B**).

---

### **Question 9**
* **Problem:** For $f(x) = x^3 + 7x^2 + 7x - 15$, (a) list all possible rational zeros, (b) find all rational zeros, and (c) factor $f(x)$.
* **Answer:**
  * **(a):** **Choice A** (`±1, ±3, ±5, ±15`)
  * **(b):** **Choice C** (`1, -3, -5`)
  * **(c):** **`(x - 1)(x + 3)(x + 5)`**
* **Graph Equation:** `f(x) = x^3 + 7*x^2 + 7*x - 15`
* **The Rule:** Use the Rational Zero Theorem, test candidates via synthetic division, and factor the quotient.
* **Work:**
  - **(a)** Factors of $-15$ over factors of $1$: $\pm 1, \pm 3, \pm 5, \pm 15$ (**Choice A**).
  - **(b)** Test $x = 1$: $f(1) = 1 + 7 + 7 - 15 = 0$. Synthetic division gives $x^2 + 8x + 15 = (x + 3)(x + 5) = 0 \implies x = 1, -3, -5$ (**Choice C**).
  - **(c)** Factored form: `(x - 1)(x + 3)(x + 5)`.

---

### **Question 10**
* **Problem:** List all possible rational zeros, find all rational zeros, and factor $f(x) = x^3 + 6x^2 + 3x - 10$.
* **Answer:**
  * **Possible rational zeros:** **Choice A** (`±1, ±2, ±5, ±10`)
  * **Rational zeros:** **Choice C** (`1, -2, -5`)
  * **Factored form:** **Choice B** (`(x - 1)(x + 2)(x + 5)`)
* **Graph Equation:** `f(x) = x^3 + 6*x^2 + 3*x - 10`
* **The Rule:** Apply the Rational Zero Theorem and synthetic division.
* **Work:**
  - Factors of $-10$ over factors of $1$: $\pm 1, \pm 2, \pm 5, \pm 10$ (**Choice A**).
  - Test $x = 1$: $f(1) = 1 + 6 + 3 - 10 = 0$. Quotient is $x^2 + 7x + 10 = (x + 2)(x + 5)$, yielding zeros $1, -2, -5$ (**Choice C**) and factored form $(x - 1)(x + 2)(x + 5)$ (**Choice B**).

---

### **Question 11**
* **Problem:** Determine whether the following statement is true or false: $\frac{7}{5}$ is a possible rational zero of $f(x) = 4x^3 + 11x^2 - 9x - 10$.
* **Answer:** **`False`**
* **Graph Equation:** `f(x) = 4*x^3 + 11*x^2 - 9*x - 10`
* **The Rule:** For $p/q$ to be a possible rational zero, $p$ must divide the constant term ($-10$) and $q$ must divide the leading coefficient ($4$).
* **Work:** $7$ does not divide $-10$ and $5$ does not divide $4$. Thus the statement is `False`.

---

### **Question 12**
* **Problem:** Determine whether the following statement is true or false: The value $\frac{1}{5}$ is a possible rational zero of $f(x) = 4x^4 - 4x^3 + x^2 - x + 1$.
* **Answer:** **`False`**
* **Graph Equation:** `f(x) = 4*x^4 - 4*x^3 + x^2 - x + 1`
* **The Rule:** The denominator $q$ of a possible rational zero $p/q$ must divide the leading coefficient ($4$).
* **Work:** Since $5$ is not a factor of $4$, $\frac{1}{5}$ is not a possible rational zero (`False`).

---

### **Question 13**
* **Problem:** Use the Rational Zero Theorem to list all possible rational zeros for $f(x) = 9x^4 - x^3 + 2x^2 - 2x - 6$.
* **Answer:** **Choice C** (`±1, ±3, ±2, ±6, ±1/3, ±2/3, ±1/9, ±2/9`)
* **Graph Equation:** `f(x) = 9*x^4 - x^3 + 2*x^2 - 2*x - 6`
* **The Rule:** Divide all factors of the constant term ($-6$) by all factors of the leading coefficient ($9$), removing duplicates.
* **Work:**
  - $p \in \{\pm 1, \pm 2, \pm 3, \pm 6\}$
  - $q \in \{\pm 1, \pm 3, \pm 9\}$
  - Distinct ratios $p/q$: $\pm 1, \pm 2, \pm 3, \pm 6, \pm \frac{1}{3}, \pm \frac{2}{3}, \pm \frac{1}{9}, \pm \frac{2}{9}$ (**Choice C**).

---

### **Question 14**
* **Problem:** Use the Rational Zero Theorem to list all possible rational zeros for $f(x) = 6x^5 + 11x^4 + 4x^3 - 2x^2 + 20x - 2$.
* **Answer:** **Choice B** (`-1, 1, -2, 2, -1/2, 1/2, -1/3, 1/3, -1/6, 1/6, -2/3, 2/3`)
* **Graph Equation:** `f(x) = 6*x^5 + 11*x^4 + 4*x^3 - 2*x^2 + 20*x - 2`
* **The Rule:** Divide all factors of $-2$ ($\pm 1, \pm 2$) by all factors of $6$ ($\pm 1, \pm 2, \pm 3, \pm 6$).
* **Work:**
  - Ratios with $p = \pm 1$: $\pm 1, \pm \frac{1}{2}, \pm \frac{1}{3}, \pm \frac{1}{6}$
  - Additional ratios with $p = \pm 2$: $\pm 2, \pm \frac{2}{3}$
  - Complete list matches **Choice B**.

---

### **Question 15**
* **Problem:** The function $f(x) = 7x^3 - 5x^2 - 63x + 45$ is given.
  - **a.** List all rational zeros that are possible according to the Rational Zero Theorem.
  - **b.** Use synthetic division to test several possible rational zeros in order to identify one actual zero.
  - **c.** Use the zero from part (b) to find all the zeros of the polynomial function.
* **Answer:**
  * **a.:** **Choice D** (`±1, ±3, ±9, ±5, ±15, ±45, ±1/7, ±3/7, ±9/7, ±5/7, ±15/7, ±45/7`)
  * **b.:** **`3`** (or **`-3`** or **`5/7`**)
  * **c.:** **`-3, 5/7, 3`**
* **Graph Equation:** `f(x) = 7*x^3 - 5*x^2 - 63*x + 45`
* **The Rule:** Factor by grouping or synthetic division after listing $p/q$ where $p \mid 45$ and $q \mid 7$.
* **Work:**
  - **a.** Factors of $45$ are $\pm 1, \pm 3, \pm 5, \pm 9, \pm 15, \pm 45$; dividing by $\pm 1, \pm 7$ gives **Choice D**.
  - **b. & c.** Factoring by grouping:
    $$f(x) = x^2(7x - 5) - 9(7x - 5) = (7x - 5)(x^2 - 9) = (7x - 5)(x - 3)(x + 3)$$
    Thus the zeros are $-3, \frac{5}{7}, 3$.

---

### **Question 16**
* **Problem:** For the polynomial function $f(x) = (x - 5)^4(x^2 - 7)$, find all zeros and their multiplicities.
* **Answer:** **Choice A** (`5 (multiplicity 4), √7, -√7`)
* **Graph Equation:** `f(x) = (x - 5)^4 * (x^2 - 7)`
* **The Rule:** Set each factor equal to zero; the exponent on each irreducible linear factor is its multiplicity.
* **Work:**
  - $(x - 5)^4 = 0 \implies x = 5$ with multiplicity $4$.
  - $x^2 - 7 = 0 \implies x = \pm\sqrt{7}$, each with multiplicity $1$.

---

### **Question 17**
* **Problem:** Find all zeros of the function $f(x) = 7(x - 1)^4(5x + 3)(x^2 - 9)$ and their multiplicities.
* **Answer:** **Choice C** (`1 (multiplicity 4), -3/5, 3, -3`)
* **Graph Equation:** `f(x) = 7*(x - 1)^4*(5*x + 3)*(x^2 - 9)`
* **The Rule:** Factor completely into linear factors and read off each root and its exponent.
* **Work:**
  - $(x - 1)^4 = 0 \implies x = 1$ (multiplicity $4$)
  - $5x + 3 = 0 \implies x = -\frac{3}{5}$ (multiplicity $1$)
  - $x^2 - 9 = (x - 3)(x + 3) = 0 \implies x = 3, -3$ (each multiplicity $1$).

---

### **Question 19**
* **Problem:** Find a polynomial of degree 3 with real coefficients and zeros of $-3, -1,$ and $4$, for which $f(-2) = 24$. (Simplify your answer. Do not factor.)
* **Answer:** **`4x^3 - 52x - 48`**
* **Graph Equation:** `f(x) = 4*x^3 - 52*x - 48`
* **The Rule:** Write $f(x) = a(x - r_1)(x - r_2)(x - r_3)$, solve for $a$ using the given point, and expand.
* **Work:**
  1. $f(x) = a(x + 3)(x + 1)(x - 4)$
  2. Substitute $x = -2$:
     $$f(-2) = a(-2 + 3)(-2 + 1)(-2 - 4) = a(1)(-1)(-6) = 6a = 24 \implies a = 4$$
  3. Expand:
     $$f(x) = 4(x^2 + 4x + 3)(x - 4) = 4(x^3 - 13x - 12) = 4x^3 - 52x - 48$$

---

### **Question 20**
* **Problem:** Find a polynomial of degree 3 with only real coefficients and zeros of $-4, 1,$ and $0$ for which $f(4) = -1$.
* **Answer:** **Choice D** (`f(x) = -1/96 x^3 - 1/32 x^2 + 1/24 x`)
* **Graph Equation:** `f(x) = (-1/96)*x^3 - (1/32)*x^2 + (1/24)*x`
* **The Rule:** Form $f(x) = ax(x + 4)(x - 1)$ and use $f(4) = -1$ to find $a$.
* **Work:**
  1. $f(x) = ax(x + 4)(x - 1) = a(x^3 + 3x^2 - 4x)$
  2. $f(4) = a(4)(8)(3) = 96a = -1 \implies a = -\frac{1}{96}$
  3. $f(x) = -\frac{1}{96}x^3 - \frac{3}{96}x^2 + \frac{4}{96}x = -\frac{1}{96}x^3 - \frac{1}{32}x^2 + \frac{1}{24}x$ (**Choice D**).

---

### **Question 21**
* **Problem:** Find a polynomial function $f(x)$ of least degree having only real coefficients and zeros as given. Assume multiplicity 1 unless otherwise stated: zero of $3$ (multiplicity 2) and zero $3i$.
* **Answer:** **`x^4 - 6x^3 + 18x^2 - 54x + 81`**
* **Graph Equation:** `f(x) = x^4 - 6*x^3 + 18*x^2 - 54*x + 81`
* **The Rule:** By the Conjugate Zeros Theorem, $-3i$ must also be a zero. Multiply $(x - 3)^2(x - 3i)(x + 3i)$.
* **Work:**
  $$f(x) = (x - 3)^2(x^2 + 9) = (x^2 - 6x + 9)(x^2 + 9) = x^4 - 6x^3 + 18x^2 - 54x + 81$$

---

### **Question 22**
* **Problem:** Find all complex zeros of the polynomial function $f(x) = x^3 + 10x^2 + 34x + 45$. Give exact values.
* **Answer:** **Choice C** (`-5, (-5 + i√11)/2, (-5 - i√11)/2`)
* **Graph Equation:** `f(x) = x^3 + 10*x^2 + 34*x + 45`
* **The Rule:** Find a rational zero by synthetic division, then apply the quadratic formula to the depressed quadratic.
* **Work:**
  1. Test $x = -5$: $(-5)^3 + 10(-5)^2 + 34(-5) + 45 = -125 + 250 - 170 + 45 = 0$.
  2. Synthetic division by $k = -5$ gives quotient $x^2 + 5x + 9$.
  3. Solve $x^2 + 5x + 9 = 0$:
     $$x = \frac{-5 \pm \sqrt{25 - 36}}{2} = \frac{-5 \pm i\sqrt{11}}{2}$$

---

### **Question 23**
* **Problem:** Find all complex zeros of the polynomial function $f(x) = x^4 - 8x^3 + 13x^2$. Give exact values. List multiple zeros as necessary.
* **Answer:** **`0, 0, 4 - sqrt(3), 4 + sqrt(3)`** ($0, 0, 4 - \sqrt{3}, 4 + \sqrt{3}$; or if entered once: **`0, 4 - sqrt(3), 4 + sqrt(3)`**)
* **Graph Equation:** `f(x) = x^4 - 8*x^3 + 13*x^2`
* **The Rule:** Factor out the greatest common monomial power $x^2$ and solve the remaining quadratic via the quadratic formula.
* **Work:**
  1. $f(x) = x^2(x^2 - 8x + 13) = 0 \implies x = 0$ (multiplicity $2$).
  2. Solve $x^2 - 8x + 13 = 0$:
     $$x = \frac{8 \pm \sqrt{64 - 52}}{2} = \frac{8 \pm 2\sqrt{3}}{2} = 4 \pm \sqrt{3}$$
