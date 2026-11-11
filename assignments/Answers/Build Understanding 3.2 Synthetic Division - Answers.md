# **Build Understanding 3.2 Synthetic Division — Answers**

### **Question 1**
* **Problem:** Use synthetic division to perform the division: $\frac{x^3 + 3x^2 + 7x + 5}{x + 1}$.
* **Answer:** **`x^2 + 2x + 5`**
* **Graph Equation:** `(x^3 + 3x^2 + 7x + 5) / (x + 1)`
* **The Rule:** To divide $P(x)$ by $(x - c)$, place $c$ in the divisor box. If dividing by $(x + c)$, place $-c$ in the box. Write the coefficients of $P(x)$ in descending order.
* **Work:**
  1. Divisor is $x + 1 = x - (-1)$, so $c = -1$.
  2. Coefficients of $P(x) = x^3 + 3x^2 + 7x + 5$ are $[1, 3, 7, 5]$.
  3. Synthetic division tableau:
     * Bring down $1$.
     * $1(-1) + 3 = 2$
     * $2(-1) + 7 = 5$
     * $5(-1) + 5 = 0$ (Remainder is $0$)
  4. The quotient is $1x^2 + 2x + 5 = x^2 + 2x + 5$.

---

### **Question 2**
* **Problem:** Divide: $\frac{2x^4 - 11x^3 + 13x^2 - 7x + 12}{x - 4}$.
* **Answer:** **`2x^3 - 3x^2 + x - 3`**
* **Graph Equation:** `(2x^4 - 11x^3 + 13x^2 - 7x + 12) / (x - 4)`
* **The Rule:** Set the divisor $x - 4 = 0 \implies c = 4$. Multiply and add coefficients down the tableau.
* **Work:**
  1. Divisor $c = 4$, coefficients are $[2, -11, 13, -7, 12]$.
  2. Synthetic division steps:
     * Bring down $2$.
     * $2(4) - 11 = -3$
     * $-3(4) + 13 = 1$
     * $1(4) - 7 = -3$
     * $-3(4) + 12 = 0$ (Remainder is $0$)
  3. The quotient polynomial is $2x^3 - 3x^2 + x - 3$.

---

### **Question 3**
* **Problem:** Use synthetic division to perform the division: $\frac{x^4 + x^3 + 4x^2 + 8x + 4}{x + 1}$.
* **Answer:** **`x^3 + 4x + 4`**
* **Graph Equation:** `(x^4 + x^3 + 4x^2 + 8x + 4) / (x + 1)`
* **The Rule:** If an intermediate term in the quotient has a coefficient of $0$, that term drops out of the simplified answer.
* **Work:**
  1. Divisor $c = -1$, coefficients are $[1, 1, 4, 8, 4]$.
  2. Synthetic division steps:
     * Bring down $1$.
     * $1(-1) + 1 = 0$ (The $x^2$ term is $0x^2$)
     * $0(-1) + 4 = 4$
     * $4(-1) + 8 = 4$
     * $4(-1) + 4 = 0$ (Remainder is $0$)
  3. The resulting quotient is $1x^3 + 0x^2 + 4x + 4 = x^3 + 4x + 4$.

---

### **Question 4**
* **Problem:** Divide using synthetic division: $\frac{x^5 + 4x^4 + 3x^3 + 3x^2 + 6x - 5}{x + 3}$.
* **Answer:** **`x^4 + x^3 + 3x - 3 + 4/(x + 3)`** (or $x^4 + x^3 + 3x - 3 + \frac{4}{x + 3}$)
* **Graph Equation:** `(x^5 + 4x^4 + 3x^3 + 3x^2 + 6x - 5) / (x + 3)`
* **The Rule:** When there is a non-zero remainder $R$, write the final result as $Q(x) + \frac{R}{D(x)}$.
* **Work:**
  1. Divisor root $c = -3$, coefficients are $[1, 4, 3, 3, 6, -5]$.
  2. Synthetic division steps:
     * Bring down $1$.
     * $1(-3) + 4 = 1$
     * $1(-3) + 3 = 0$ ($x^2$ term is $0$)
     * $0(-3) + 3 = 3$
     * $3(-3) + 6 = -3$
     * $-3(-3) - 5 = 4$ (Remainder $R = 4$)
  3. The quotient is $x^4 + x^3 + 3x - 3$ with remainder $4$, yielding $x^4 + x^3 + 3x - 3 + \frac{4}{x + 3}$.

---

### **Question 5**
* **Problem:** Use synthetic division to perform the division: $\frac{-6x^3 + 9x^2 - 5x + 3}{x - 2}$.
* **Answer:** **`-6x^2 - 3x - 11 - 19/(x - 2)`** (or `-6x^2 - 3x - 11 + (-19)/(x - 2)`)
* **Graph Equation:** `(-6x^3 + 9x^2 - 5x + 3) / (x - 2)`
* **The Rule:** Handle negative leading coefficients and remainders with care when expressing the fractional remainder.
* **Work:**
  1. Divisor root $c = 2$, coefficients are $[-6, 9, -5, 3]$.
  2. Synthetic division steps:
     * Bring down $-6$.
     * $-6(2) + 9 = -3$
     * $-3(2) - 5 = -11$
     * $-11(2) + 3 = -19$ (Remainder $R = -19$)
  3. The quotient is $-6x^2 - 3x - 11$ with remainder $-19$, giving $-6x^2 - 3x - 11 - \frac{19}{x - 2}$.

---

### **Question 6**
* **Problem:** Use synthetic division to perform the following division: $\frac{x^4 - 6x^3 - x^2 + 36x}{x - 4}$.
* **Answer:** **`x^3 - 2x^2 - 9x`**
* **Graph Equation:** `(x^4 - 6x^3 - x^2 + 36x) / (x - 4)`
* **The Rule:** Always insert a placeholder coefficient of $0$ for any missing powers of $x$, including a missing constant term!
* **Work:**
  1. The numerator has no constant term, so write it as $x^4 - 6x^3 - x^2 + 36x + 0$.
  2. Divisor root $c = 4$, coefficients are $[1, -6, -1, 36, 0]$.
  3. Synthetic division steps:
     * Bring down $1$.
     * $1(4) - 6 = -2$
     * $-2(4) - 1 = -9$
     * $-9(4) + 36 = 0$
     * $0(4) + 0 = 0$ (Remainder $R = 0$)
  4. The quotient is $1x^3 - 2x^2 - 9x + 0 = x^3 - 2x^2 - 9x$.

---

### **Question 7**
* **Problem:** Use synthetic division to perform the following division: $\frac{x^3 - 27}{x - 3}$.
* **Answer:** **`x^2 + 3x + 9`**
* **Graph Equation:** `(x^3 - 27) / (x - 3)`
* **The Rule:** Insert $0$ placeholders for both $x^2$ and $x$: $x^3 + 0x^2 + 0x - 27$.
* **Work:**
  1. Divisor root $c = 3$, coefficients are $[1, 0, 0, -27]$.
  2. Synthetic division steps:
     * Bring down $1$.
     * $1(3) + 0 = 3$
     * $3(3) + 0 = 9$
     * $9(3) - 27 = 0$ (Remainder is $0$)
  3. The quotient is $x^2 + 3x + 9$ with remainder $0$. (This also verifies the difference of cubes factorization $a^3 - b^3 = (a - b)(a^2 + ab + b^2)$).

---

### **Question 8**
* **Problem:** Use synthetic division to perform the division: $\frac{x^5 + 32}{x + 2}$.
* **Answer:** **`x^4 - 2x^3 + 4x^2 - 8x + 16`**
* **Graph Equation:** `(x^5 + 32) / (x + 2)`
* **The Rule:** Insert $0$ for each missing power ($x^4, x^3, x^2, x$): $[1, 0, 0, 0, 0, 32]$.
* **Work:**
  1. Divisor root $c = -2$, coefficients are $[1, 0, 0, 0, 0, 32]$.
  2. Synthetic division steps:
     * Bring down $1$.
     * $1(-2) + 0 = -2$
     * $-2(-2) + 0 = 4$
     * $4(-2) + 0 = -8$
     * $-8(-2) + 0 = 16$
     * $16(-2) + 32 = 0$ (Remainder is $0$)
  3. The quotient is $x^4 - 2x^3 + 4x^2 - 8x + 16$.

---

### **Question 9**
* **Problem:** Express $f(x)$ in the form $f(x) = (x - k)q(x) + r$ for the given value of $k$: $f(x) = 4x^3 + x^2 + x - 5, \quad k = -1$.
* **Answer:** **`f(x) = (x + 1)(4x^2 - 3x + 4) - 9`**
* **Graph Equation:** `4x^3 + x^2 + x - 5; k = -1`
* **The Rule:** Division Algorithm: $f(x) = (x - k)q(x) + r$, where $q(x)$ is the quotient polynomial and $r$ is the constant remainder.
* **Work:**
  1. Divisor $k = -1$, coefficients are $[4, 1, 1, -5]$.
  2. Synthetic division steps:
     * Bring down $4$.
     * $4(-1) + 1 = -3$
     * $-3(-1) + 1 = 4$
     * $4(-1) - 5 = -9$ (Remainder $r = -9$)
  3. Quotient is $q(x) = 4x^2 - 3x + 4$ and remainder $r = -9$.
  4. Form: $f(x) = (x - (-1))(4x^2 - 3x + 4) + (-9) = (x + 1)(4x^2 - 3x + 4) - 9$.

---

### **Question 10**
* **Problem:** Express $f(x)$ in the form $f(x) = (x - k)q(x) + r$ for the given value of $k$: $f(x) = x^3 + 4x^2 + 9x + 10, \quad k = -2$.
* **Answer:** **`f(x) = (x + 2)(x^2 + 2x + 5)`**
* **Graph Equation:** `x^3 + 4x^2 + 9x + 10; k = -2`
* **The Rule:** When remainder $r = 0$, $f(x) = (x - k)q(x)$.
* **Work:**
  1. Divisor $k = -2$, coefficients are $[1, 4, 9, 10]$.
  2. Synthetic division steps:
     * Bring down $1$.
     * $1(-2) + 4 = 2$
     * $2(-2) + 9 = 5$
     * $5(-2) + 10 = 0$ (Remainder $r = 0$)
  3. Quotient is $q(x) = x^2 + 2x + 5$ and remainder is $0$.
  4. Form: $f(x) = (x + 2)(x^2 + 2x + 5)$.

---

### **Question 11**
* **Problem:** Express $f(x)$ in the form $f(x) = (x - k)q(x) + r$ for the given value of $k$: $f(x) = 4x^4 - 2x^3 - 14x^2 - x, \quad k = 4$.
* **Answer:** $f(x) = (x -$ **`4`** $)($ **`4x^3 + 14x^2 + 42x + 167`** $) +$ **`668`**
* **Graph Equation:** `4x^4 - 2x^3 - 14x^2 - x; k = 4`
* **The Rule:** Supply the missing constant term $0$: coefficients are $[4, -2, -14, -1, 0]$.
* **Work:**
  1. Divisor $k = 4$, coefficients are $[4, -2, -14, -1, 0]$.
  2. Synthetic division steps:
     * Bring down $4$.
     * $4(4) - 2 = 14$
     * $14(4) - 14 = 42$
     * $42(4) - 1 = 167$
     * $167(4) + 0 = 668$ (Remainder $r = 668$)
  3. Quotient $q(x) = 4x^3 + 14x^2 + 42x + 167$, remainder $r = 668$.
  4. Result: $f(x) = (x - 4)(4x^3 + 14x^2 + 42x + 167) + 668$.

---

### **Question 12**
* **Problem:** Express $f(x)$ in the form $f(x) = (x - k)q(x) + r$ for the given value of $k$: $f(x) = 2x^4 + 6x^3 - 13x^2 + 72, \quad k = -2$.
* **Answer:** **`2x^4 + 6x^3 - 13x^2 + 72 = (x + 2)(2x^3 + 2x^2 - 17x + 34) + 4`**
* **Graph Equation:** `2x^4 + 6x^3 - 13x^2 + 72; k = -2`
* **The Rule:** Insert $0$ for the missing $x$ term: coefficients $[2, 6, -13, 0, 72]$.
* **Work:**
  1. Divisor $k = -2$, coefficients are $[2, 6, -13, 0, 72]$.
  2. Synthetic division steps:
     * Bring down $2$.
     * $2(-2) + 6 = 2$
     * $2(-2) - 13 = -17$
     * $-17(-2) + 0 = 34$
     * $34(-2) + 72 = 4$ (Remainder $r = 4$)
  3. Quotient is $q(x) = 2x^3 + 2x^2 - 17x + 34$, remainder is $r = 4$.
  4. Result: $2x^4 + 6x^3 - 13x^2 + 72 = (x + 2)(2x^3 + 2x^2 - 17x + 34) + 4$.

---

### **Question 13**
* **Problem:** Use the remainder theorem and synthetic division to find $f(k)$: $k = -1; \quad f(x) = x^2 - 3x + 4$.
* **Answer:** $f(k) =$ **`8`** (or $f(-1) = 8$)
* **Graph Equation:** `x^2 - 3x + 4; k = -1`
* **The Rule:** Remainder Theorem: The remainder when a polynomial $f(x)$ is divided by $(x - k)$ is equal to $f(k)$.
* **Work:**
  1. Divisor $k = -1$, coefficients $[1, -3, 4]$.
  2. Synthetic division steps:
     * Bring down $1$.
     * $1(-1) - 3 = -4$
     * $-4(-1) + 4 = 8$ (Remainder $r = 8$)
  3. By the Remainder Theorem, $f(-1) = 8$.

---

### **Question 14**
* **Problem:** For the following polynomial function, use the remainder theorem to find $f(k)$: $f(x) = 2x^2 - 5x - 5; \quad k = 4$.
* **Answer:** $f(4) =$ **`7`**
* **Graph Equation:** `2x^2 - 5x - 5; k = 4`
* **The Rule:** By the Remainder Theorem, synthetic division by $k$ gives the exact value of $f(k)$ in the remainder box.
* **Work:**
  1. Divisor $k = 4$, coefficients $[2, -5, -5]$.
  2. Synthetic division steps:
     * Bring down $2$.
     * $2(4) - 5 = 3$
     * $3(4) - 5 = 7$ (Remainder is $7$)
  3. Therefore, $f(4) = 7$.

---

### **Question 15**
* **Problem:** Use the remainder theorem and synthetic division to find $f(k)$ for the given value of $k$: $f(x) = -x^3 - 9x^2 - 21x - 1; \quad k = -5$.
* **Answer:** $f(-5) =$ **`4`**
* **Graph Equation:** `-x^3 - 9x^2 - 21x - 1; k = -5`
* **The Rule:** Evaluate $f(-5)$ by finding the remainder when dividing by $x - (-5) = x + 5$.
* **Work:**
  1. Divisor $k = -5$, coefficients $[-1, -9, -21, -1]$.
  2. Synthetic division steps:
     * Bring down $-1$.
     * $-1(-5) - 9 = -4$
     * $-4(-5) - 21 = -1$
     * $-1(-5) - 1 = 4$ (Remainder is $4$)
  3. Therefore, $f(-5) = 4$.

---

### **Question 16**
* **Problem:** For the following polynomial function, use the remainder theorem to find $f(k)$: $f(x) = 3x^5 - 10x^3 - 17x^2 - 50; \quad k = 2$.
* **Answer:** $f(2) =$ **`-102`**
* **Graph Equation:** `3x^5 - 10x^3 - 17x^2 - 50; k = 2`
* **The Rule:** Insert $0$ placeholders for missing powers $x^4$ and $x$: coefficients are $[3, 0, -10, -17, 0, -50]$.
* **Work:**
  1. Divisor $k = 2$, coefficients $[3, 0, -10, -17, 0, -50]$.
  2. Synthetic division steps:
     * Bring down $3$.
     * $3(2) + 0 = 6$
     * $6(2) - 10 = 2$
     * $2(2) - 17 = -13$
     * $-13(2) + 0 = -26$
     * $-26(2) - 50 = -102$ (Remainder is $-102$)
  3. Therefore, $f(2) = -102$.

---

### **Question 17**
* **Problem:** Use synthetic division to decide whether the given number $k$ is a zero of the polynomial function. If it is not, give the value of $f(k)$: $f(x) = x^2 - 9x + 20; \quad k = 4$.
* **Answer:** **Choice B: The given $k$ is a zero of the polynomial function.**
* **Graph Equation:** `x^2 - 9x + 20; k = 4`
* **The Rule:** Factor Theorem: A number $k$ is a zero of $f(x)$ if and only if $f(k) = 0$ (the remainder is $0$).
* **Work:**
  1. Divisor $k = 4$, coefficients $[1, -9, 20]$.
  2. Synthetic division steps:
     * Bring down $1$.
     * $1(4) - 9 = -5$
     * $-5(4) + 20 = 0$ (Remainder $r = 0$)
  3. Since the remainder is $0$, $f(4) = 0$.
  4. Therefore, $k = 4$ is a zero of the polynomial function (**Choice B**).

---

### **Question 18**
* **Problem:** Use synthetic division to decide whether the given number $k$ is a zero of the polynomial function. If it is not, give the value of $f(k)$: $f(x) = x^3 + 9x^2 + 8x - 60; \quad k = -6$.
* **Answer:** **Choice B: The given $k$ is a zero of the polynomial function.**
* **Graph Equation:** `x^3 + 9x^2 + 8x - 60; k = -6`
* **The Rule:** By the Factor Theorem, if the remainder is $0$, then $k$ is a zero of $f(x)$.
* **Work:**
  1. Divisor $k = -6$, coefficients $[1, 9, 8, -60]$.
  2. Synthetic division steps:
     * Bring down $1$.
     * $1(-6) + 9 = 3$
     * $3(-6) + 8 = -10$
     * $-10(-6) - 60 = 0$ (Remainder $r = 0$)
  3. Since $f(-6) = 0$, $k = -6$ is a zero of the polynomial function (**Choice B**).

---

### **Question 19**
* **Problem:** Use synthetic division to decide whether the given number $k$ is a zero of the polynomial function. If it is not, give the value of $f(k)$: $f(x) = 2x^3 - 11x^2 - 7x + 70; \quad k = 4$.
* **Answer:** **Choice A: The given $k$ is not a zero of the polynomial function. $f(4) = -6$.**
* **Graph Equation:** `2x^3 - 11x^2 - 7x + 70; k = 4`
* **The Rule:** If the remainder $f(k) \neq 0$, then $k$ is not a zero of the function.
* **Work:**
  1. Divisor $k = 4$, coefficients $[2, -11, -7, 70]$.
  2. Synthetic division steps:
     * Bring down $2$.
     * $2(4) - 11 = -3$
     * $-3(4) - 7 = -19$
     * $-19(4) + 70 = -76 + 70 = -6$ (Remainder $r = -6$)
  3. Since $f(4) = -6 \neq 0$, $k = 4$ is not a zero of the polynomial function (**Choice A**).

---

### **Question 20**
* **Problem:** Use synthetic division to decide whether the given number $k$ is a zero of the given polynomial function. If it is not, give the value of $f(k)$: $f(x) = x^3 + 5x^2 + 8x + 16, \quad k = -4$.
* **Answer:** **Choice B: The given $k$ is a zero of the polynomial function.**
* **Graph Equation:** `x^3 + 5x^2 + 8x + 16; k = -4`
* **The Rule:** Perform synthetic division with $k = -4$; if remainder $f(-4) = 0$, then $k = -4$ is a zero.
* **Work:**
  1. Divisor $k = -4$, coefficients $[1, 5, 8, 16]$.
  2. Synthetic division steps:
     * Bring down $1$.
     * $1(-4) + 5 = 1$
     * $1(-4) + 8 = 4$
     * $4(-4) + 16 = 0$ (Remainder $r = 0$)
  3. Since $f(-4) = 0$, $k = -4$ is a zero of the polynomial function (**Choice B**).
