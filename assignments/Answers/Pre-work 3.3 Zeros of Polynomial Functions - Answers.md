# **Pre-work 3.3 Zeros of Polynomial Functions — Answers**

### **Question 1**
* **Problem:** Select the correct choice that completes the sentence below. A number is divisible by 2 if (1) ________.
* **Answer:** **`it has an even ones digit.`**
* **The Rule:** A whole number is divisible by $2$ if and only if its last (ones) digit is even ($0, 2, 4, 6,$ or $8$).
* **Work:** Among the given choices, divisibility by $2$ is determined solely by having an even ones digit.

---

### **Question 2**
* **Problem:** Select the correct choice that completes the sentence below. A number is divisible by 5 if (1) ________.
* **Answer:** **`its ones digit is 0 or 5.`**
* **The Rule:** A whole number is divisible by $5$ if and only if its ones digit is $0$ or $5$.
* **Work:** Multiples of $5$ ($5, 10, 15, 20, \dots$) always end in $0$ or $5$.

---

### **Question 3**
* **Problem:** Select the correct choice that completes the sentence below. A number is divisible by 6 if (1) ________.
* **Answer:** **`it has an even ones digit and the sum of its digits is divisible by 3.`**
* **The Rule:** A number is divisible by $6$ if it is divisible by both $2$ (even ones digit) and $3$ (sum of digits is divisible by $3$).
* **Work:** Since $6 = 2 \times 3$ and $\gcd(2,3) = 1$, both the divisibility test for $2$ and the divisibility test for $3$ must hold simultaneously.

---

### **Question 4**
* **Problem:** Select the correct choice that completes the sentence below. A number is divisible by 9 if (1) ________.
* **Answer:** **`the sum of its digits is divisible by 9.`**
* **The Rule:** A whole number is divisible by $9$ if and only if the sum of its digits is a multiple of $9$.
* **Work:** Because $10^k \equiv 1 \pmod 9$, a number has the same remainder modulo $9$ as the sum of its digits.

---

### **Question 5**
* **Problem:** Find all the factors of $147$.
* **Answer:** **`1, 3, 7, 21, 49, 147`**
* **The Rule:** Test divisibility by integers up to $\sqrt{n}$ and pair each divisor $d$ with $n/d$.
* **Work:**
  1. $147 = 1 \times 147$
  2. Sum of digits is $1 + 4 + 7 = 12$ (divisible by $3$): $147 = 3 \times 49$
  3. Since $49 = 7^2$, $147 = 7 \times 21$
  4. Listing all positive factors in ascending order: `1, 3, 7, 21, 49, 147`.

---

### **Question 6**
* **Problem:** Find all the factors of $121$.
* **Answer:** **`1, 11, 121`**
* **The Rule:** Test prime numbers up to $\sqrt{121} = 11$.
* **Work:**
  1. $121 = 1 \times 121$
  2. $121 = 11 \times 11$
  3. Listing each distinct factor once: `1, 11, 121`.

---

### **Question 7**
* **Problem:** Find all the factors of $71$.
* **Answer:** **`1, 71`**
* **The Rule:** A prime number has only $1$ and itself as positive factors.
* **Work:** Testing primes up to $\sqrt{71} \approx 8.4$ ($2, 3, 5, 7$): none divide $71$. Thus $71$ is prime, and its only factors are `1, 71`.

---

### **Question 8**
* **Problem:** Find all the factors of $50$.
* **Answer:** **`1, 2, 5, 10, 25, 50`**
* **The Rule:** Pair each divisor $d \le \sqrt{50}$ with $50/d$.
* **Work:**
  1. $50 = 1 \times 50$
  2. $50 = 2 \times 25$
  3. $50 = 5 \times 10$
  4. All factors: `1, 2, 5, 10, 25, 50`.

---

### **Question 9**
* **Problem:** Decide whether the following statement is true or false. If false, tell why. Since $x - 1$ is a factor of $f(x) = x^6 - x^4 + 2x^2 - 2$, we can conclude that $f(1) = 0$.
* **Answer:** **Choice A** (`The statement is true.`)
* **Graph Equation:** `f(x) = x^6 - x^4 + 2*x^2 - 2`
* **The Rule:** By the Factor Theorem, $x - k$ is a factor of a polynomial $f(x)$ if and only if $f(k) = 0$.
* **Work:** Here $x - k = x - 1$, so $k = 1$. Since $x - 1$ is a factor of $f(x)$, we immediately conclude $f(1) = 1^6 - 1^4 + 2(1)^2 - 2 = 0$.

---

### **Question 10**
* **Problem:** Determine whether the following statement is true or false. If false, explain why. Because $f(2) = 0$ for $f(x) = x^6 - x^4 + 6x^2 - 72$, we can conclude that $x - 2$ is a factor of $f(x)$.
* **Answer:** **Choice D** (`The statement is true.`)
* **Graph Equation:** `f(x) = x^6 - x^4 + 6*x^2 - 72`
* **The Rule:** By the Factor Theorem, if $f(k) = 0$, then $x - k$ is a factor of $f(x)$.
* **Work:** Since $f(2) = 0$, $k = 2$, which means $x - 2$ is a factor of $f(x)$.

---

### **Question 11**
* **Problem:** Decide whether the following statement is true or false. If false, tell why. For $f(x) = (x + 2)^5 \cdot (x - 4)$, $2$ is a zero of multiplicity $5$.
* **Answer:** **Choice A** (`The statement is false because 2 is not a zero of f(x).`)
* **Graph Equation:** `f(x) = (x + 2)^5 * (x - 4)`
* **The Rule:** A factor $(x - k)^m$ corresponds to a zero $x = k$ of multiplicity $m$.
* **Work:** Setting $(x + 2)^5(x - 4) = 0$ gives $x = -2$ (multiplicity $5$) and $x = 4$ (multiplicity $1$). Since $f(2) = (4)^5(-2) \neq 0$, $2$ is not a zero of $f(x)$.

---

### **Question 12**
* **Problem:** Determine whether the following statement is true or false. If false, explain why. Because $4 + 5i$ is a zero of $f(x) = x^2 - 8x + 41$, we can conclude that $4 - 5i$ is also a zero.
* **Answer:** **Choice A** (`The statement is true.`)
* **Graph Equation:** `f(x) = x^2 - 8*x + 41`
* **The Rule:** Conjugate Zeros Theorem: If a polynomial has real coefficients and $a + bi$ is a zero, then its complex conjugate $a - bi$ is also a zero.
* **Work:** Since $f(x) = x^2 - 8x + 41$ has real coefficients ($1, -8, 41$) and $4 + 5i$ is a zero, its conjugate $4 - 5i$ is also a zero.

---

### **Question 13**
* **Problem:** Determine whether the following statement is true or false. If false, explain why. If $z = 2 - 3i$, then $\bar{z} = -2 + 3i$.
* **Answer:** **Choice B** (`The statement is false. If z = 2 - 3i, then z̄ =` **`2 + 3i`**)
* **The Rule:** The complex conjugate of $z = a + bi$ is $\bar{z} = a - bi$ (only the sign of the imaginary part changes).
* **Work:** For $z = 2 - 3i$, keep the real part $2$ and negate the imaginary part $-3i$ to get $\bar{z} = 2 + 3i$.

---

### **Question 14**
* **Problem:** Determine whether each statement is true or false. If false, explain why. The product of a complex number and its conjugate is always a real number.
* **Answer:** **Choice C** (`The statement is true.`)
* **The Rule:** For any complex number $a + bi$ (with $a, b \in \mathbb{R}$), $(a + bi)(a - bi) = a^2 + b^2 \in \mathbb{R}$.
* **Work:** $(a + bi)(a - bi) = a^2 - abi + abi - b^2i^2 = a^2 + b^2$, which has no imaginary part and is always a real number.

---

### **Question 15**
* **Problem:** Select the correct choice that completes the sentence below. If three positive numbers, five negative numbers, and zero are multiplied, the product is (1) ________.
* **Answer:** **`0.`**
* **The Rule:** Zero Property of Multiplication: The product of any set of numbers containing $0$ is $0$.
* **Work:** Multiplying any real number by $0$ yields $0$.
