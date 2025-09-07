# Deloitte Preparation

https://www.linkedin.com/posts/pinaki-singha-roy-263627138_deloitte-interview-questions-for-data-science-activity-7232371546365779968-IDpB/  
https://nodeflair.com/companies/deloitte/interviews/senior-data-scientist  
https://www.interviewquery.com/interview-guides/deloitte-data-scientist  

_I CAN GET THE JOB and I WILL  
BUILD STRONG RELATIONSHIP with INTERVIEWER_


# How I am going to prepare
1. What I know from JD, prepare strong for what I know
2. What I don't know from JD, prepare for what I can
3. Prepare for Why Deloitte, Why Consulting, Why this department
4. Prepare for Domain Knowledge Audit/Assurance
5. Prepare for Behavioural Questions
6. Prepare for Business Case Study Questions

# 1. WHAT I KNOW FROM JD
- problem-solving skills
- capable of generating original solutions to real-world problems.
- coaching junior data scientists/analysts
- reviewing code and documentation to a high standard.
- Python (pandas, numpy, scikit-learn).
- End-to-end experience of 
	- managing 
	- multiple data science and analytics projects in 
	- different industries and 
	- with different types of data (text, numerical, categorical).
- Experience in project management 
- Experience in a DevOps environment
- cloud environment - Azure, AWS
- Git
- Excel, SQL
- Docker 
- Range of machine learning techniques (Supervised and unsupervised).
- Strong communication and data presentation skill
	- With the ability to build convincing recommendations 
	- Sell these to a non-technical audience.
- Self-driven, able to work independently yet acts as a team player
- Able to apply data science principles through a business lens.
- Experience delivery data science for financial industry or large/complex organisations.

# 2. WHAT I HAVE TO PREPARE
## 2.1 Azure
## 2.2 Mathematics, Pprobability, and Statistics.

#### 📌 Mathematics (10 Q\&A)

**Q1. Why do we use linear algebra in machine learning?**  
👉 Linear algebra helps us organize and process data in tables (matrices). Think of it as Excel on steroids. In audit, matrices let us handle thousands of transactions at once for fraud detection.

**Q2. What is an eigenvalue/eigenvector, and why do we care?**  
👉 Imagine you’re stretching a rubber band. Eigenvectors are the directions that don’t twist, just stretch; eigenvalues tell us how much. In audit, this helps reduce dimensions (PCA) to find hidden patterns in financial data.

**Q3. What is the difference between convex and non-convex functions?**  
👉 Convex = a bowl shape, always one lowest point. Non-convex = hills and valleys, many traps. In ML, convex loss is easier to optimize (like minimizing audit error).

**Q4. Why is gradient descent important?**  
👉 It’s like rolling a ball down a hill until it finds the lowest valley. In audit ML, it helps models learn from discrepancies in financial data.

**Q5. What’s the difference between L1 and L2 regularization?**  
👉 L1 = makes some weights exactly zero (feature selection, like ignoring irrelevant audit factors).
L2 = makes weights small but not zero (smooths model, avoids overfitting).

**Q6. What is the difference between continuous and discrete variables?**  
👉 Continuous = flowing water (revenue amount). Discrete = marbles (number of invoices). In assurance, you track both.

**Q7. Explain vectors vs scalars in simple terms.**  
👉 Scalar = one number (profit this year). Vector = a list of numbers (profit for each month). Auditors often work with vectors.

**Q8. What’s a dot product?**  
👉 Multiply matching parts of two lists and add them. Like scoring transactions by multiplying “risk factor” × “weight.”

**Q9. Why do we normalize data?**  
👉 Imagine comparing salaries in dollars and cents vs age in years. Without scaling, the big numbers dominate. In audit ML, normalization ensures fair comparisons.

**Q10. What is the difference between supervised and unsupervised learning mathematically?**  
👉 Supervised = equation with both input (X) and output (Y). Unsupervised = only input (X), no answer key. In audit, supervised detects known fraud, unsupervised finds unknown anomalies.

---

#### 🎲 Probability (10 Q\&A)

**Q1. What is probability in simplest terms?**  
👉 Probability = chance of something happening. Like flipping a coin = 50/50. In audit, it’s chance a transaction is fraudulent.

**Q2. What is conditional probability?**  
👉 It’s the chance of an event given another event. Example: “If the company is in healthcare, what’s the chance of revenue manipulation?”

**Q3. What’s Bayes’ Theorem and why do we care in audit?**  
👉 Bayes updates beliefs when new evidence arrives. In audit, you may think fraud risk = 5%, but after seeing suspicious journal entries, update risk = 60%.

**Q4. Explain independence in probability.**  
👉 Two events are independent if one doesn’t affect the other. Like rolling two dice. In audit, two transactions are independent if one doesn’t influence the other.

**Q5. What is expectation in probability?**  
👉 Expectation = average outcome if repeated many times. Example: Expected value of claims per policy. Auditors use it to estimate financial risk.

**Q6. What’s the difference between variance and standard deviation?**  
👉 Variance = how spread out numbers are. Standard deviation = square root of variance (easier to understand scale). In audit, used to measure risk spread.

**Q7. What’s the Law of Large Numbers?**  
👉 The more samples you take, the closer the average gets to the truth. In audit, sampling 1,000 invoices gives better accuracy than just 10.

**Q8. What is the Central Limit Theorem?**  
👉 No matter the distribution, if you take large samples, the averages form a bell curve. Auditors use this for hypothesis testing.

**Q9. What’s the difference between permutation and combination?**  
👉 Permutation = order matters (arranging audit reports). Combination = order doesn’t matter (choosing 5 invoices from 100).

**Q10. What’s overfitting in probability terms?**  
👉 When a model learns noise as if it’s signal. In audit, that’s like concluding fraud just because of random coincidences in small samples.

---

#### 📊 Statistics (10 Q\&A)

**Q1. What’s the difference between descriptive and inferential statistics?**  
👉 Descriptive = summarize what happened (average revenue). Inferential = predict/explain (likelihood next year’s revenue changes).

**Q2. What’s correlation vs causation?**  
👉 Correlation = two things move together (ice cream sales ↑, pool accidents ↑). Causation = one causes the other (ice cream doesn’t cause drowning). Auditors must avoid false assumptions.

**Q3. What is p-value in simple terms?**  
👉 P-value = probability results happened by chance. Low p-value (<0.05) = unlikely random. In audit, it tests if anomalies are real.

**Q4. What is hypothesis testing?**  
👉 It’s a way to test ideas with data. Example: “Is expense reporting fraud more likely in Q4?”

**Q5. What’s the difference between Type I and Type II error?**  
👉 Type I = false alarm (flagging normal transaction as fraud).
Type II = missed alarm (ignoring fraud). In audit, Type II is riskier.

**Q6. Explain confidence interval in simple terms.**  
👉 It’s like saying, “I’m 95% sure company profit is between £5M–£7M.”

**Q7. What is regression analysis?**  
👉 Regression shows how one variable affects another. In audit, predicting expense growth from revenue growth.

**Q8. What is multicollinearity and why is it bad?**  
👉 When predictors are highly related (e.g., revenue & sales count). Model gets confused. In audit ML, can overstate risk.

**Q9. What is an outlier, and why does it matter?**  
👉 Outlier = unusual data point. Example: one invoice of £10M when all others are £10K. Auditors investigate outliers for fraud risk.

**Q10. What’s the difference between population and sample?**  
👉 Population = all transactions. Sample = subset checked by auditor. Good sampling ensures conclusions apply to the whole population.

---

## 2.3 LLM 
#### Large Language Models, 
#### Generative AI frameworks, 
#### prompt engineering
#### fine tuning
#### resource augmentation.

---

## 2.4 Deep Learning (e.g. RNNs, CNNs)

### **2.4.1. Basics of Neural Network (NN)**  

#### 🧠 Layman’s Explanation:

* Imagine your brain is full of light switches (neurons). Each switch decides if it should turn ON (1) or stay OFF (0) depending on signals from other switches.
* A Neural Network is just a giant web of these switches, where layers of them learn patterns in data.

#### 📖 Example:

* You show the network many pictures of cats and dogs.
* At first it guesses randomly, but over time it learns “pointy ears” = cat, “floppy ears” = dog.
* Finally, it becomes good at telling cats from dogs.

#### ❓ Why NN if ML already exists?

* Traditional ML (like Logistic Regression, Decision Trees) is like a calculator — good at simple patterns.
* But Neural Networks are like super-brains — they can see **very complex patterns** (images, speech, text, fraud patterns in finance).

#### ✅ Use Case in Audit/Assurance:

* **Anomaly detection in transactions**: NN can find unusual patterns in millions of entries (e.g., hidden fraud, duplicate billing, or manipulation of revenue figures).

---

### **2.4.2. Basics of CNN & RNN**  

#### 📸 CNN (Convolutional Neural Network):

* Imagine scanning a picture with a small magnifying glass — you look for edges, shapes, then bigger patterns.
* CNNs are **specialized for images and spatial data**.

**Why needed?**  

* Normal NNs struggle with images (too many pixels).
* CNNs compress this information smartly while keeping important features.

**Use Case in Audit:**  

* Detecting **forged signatures or altered invoices** from scanned documents.

**Pseudo Code (Python-like):**  

```python
# Pseudo CNN model
model = CNN()
model.add(ConvLayer(filters=32, kernel=3))  # looks for edges
model.add(ReLU())                           # adds non-linearity
model.add(MaxPool())                        # reduces size
model.add(Dense(10, softmax))               # final classification
model.train(images, labels)
```

---

#### ⏳ RNN (Recurrent Neural Network):

* Imagine reading a story — you don’t forget the earlier part when you read the next sentence.
* RNNs remember previous steps → good for sequences.

**Why needed?**  

* NNs and CNNs can’t remember order. RNNs keep context.

**Use Case in Audit:**  

* **Detecting fraud across time** (e.g., unusual sequence of journal entries, payroll manipulation).

**Pseudo Code:**  

```python
# Pseudo RNN model
model = RNN()
model.add(LSTM(units=64))          # memory cells
model.add(Dense(1, sigmoid))       # fraud (yes/no)
model.train(transaction_sequences, labels)
```

---

### **2.4.3. 10 Interview Questions & Answers (Audit/Assurance Focus)**  

#### **Q1. Explain Neural Networks in simple terms.**  

**A:** A neural network is a system of connected “neurons” that learn patterns from data. Unlike traditional ML, it can capture complex, non-linear relationships — e.g., unusual financial entries indicating fraud.

---

#### **Q2. Why use Deep Learning in Audit when simpler ML works?**  

**A:** Traditional ML works for small, structured problems. Deep Learning is needed when patterns are complex, like unstructured invoice text, audio records, or millions of ledger entries with hidden anomalies.

---

#### **Q3. What is a CNN and how could it help in Deloitte’s Assurance services?**  

**A:** CNNs analyze visual data. In audit, they can check scanned receipts, detect forged documents, or identify inconsistencies in handwritten signatures.

---

#### **Q4. What is an RNN and its role in audit analytics?**  

**A:** RNNs learn from sequences. In audit, they can detect suspicious sequences of transactions over time (e.g., month-end revenue spikes that don’t align with business operations).

---

#### **Q5. How would you explain “overfitting” to a client?**  

**A:** Overfitting means the model memorizes training data instead of learning general rules. In audit, that would mean flagging only past fraud cases, but missing new patterns.

---

#### **Q6. How can Deep Learning improve regulatory compliance checks?**  

**A:** By automatically scanning large volumes of contracts, policies, or transactions for non-compliance, deep learning reduces manual review time while increasing accuracy.

---

#### **Q7. Give an example where Deloitte could use CNNs in Audit.**  

**A:** Deloitte could use CNNs to scan thousands of invoices for signs of tampering, such as font inconsistencies, modified numbers, or forged seals.

---

#### **Q8. How can RNNs help with fraud detection in banking audits?**  

**A:** RNNs can model the sequence of customer transactions, detecting suspicious behavior patterns (e.g., sudden cash withdrawals followed by transfers to multiple accounts).

---

#### **Q9. What challenges do you see in applying Deep Learning in Assurance?**  

**A:**  

1. Data availability (labeled fraud data is rare).
2. Explainability (black-box models).
3. Regulatory concerns (e.g., GDPR).
   Deloitte must balance accuracy with interpretability and compliance.

---

#### **Q10. How would you explain Deep Learning value to a non-technical client?**  

**A:** “Deep Learning is like giving the computer an experienced auditor’s brain — it learns patterns from millions of records to highlight risks that humans may overlook, faster and at scale.”

---


Excellent — now let’s go a bit **more technical** (still simple, but more precise) so you’re clear on the building blocks.

---

###  **2.4.4. Neuron, Weights, Edges**  

* **Neuron (Node):**  
  A small math unit. It takes inputs, multiplies by some numbers (weights), adds a bias, passes through an activation (e.g., ReLU, Sigmoid), and outputs a value.

  Formula:

  $$
  y = f(w_1x_1 + w_2x_2 + … + b)
  $$

* **Weights:**  
  The importance of each input. If $w_1$ is large, input $x_1$ matters a lot.

* **Edges:**  
  Connections between neurons. Each edge carries a weight (like a pipe with thickness controlling flow).

---

###  **2.4.5. Layers & Why Multiple**  

* **Layers:** Groups of neurons stacked together.

  * **Input Layer:** Just takes raw data (pixels, features).
  * **Hidden Layers:** Transform and learn deeper patterns.
  * **Output Layer:** Gives prediction (class, number, etc.).

* **Why multiple?**  
  Each layer extracts progressively **abstract features**:

  * 1st layer in CNN: edges
  * 2nd: shapes
  * 3rd: objects

* **How many layers needed?**  

  * Small data/simple problem → few layers (2–3).
  * Complex problem (image, NLP) → deep networks (10+).
    Rule of thumb: **start small, add depth until validation accuracy stops improving.**  

---

###  **2.4.6. Types of Layers**  

* **Dense (Fully Connected):** Every neuron connects to every neuron in the next layer. Used at the end for combining features.

* **Convolutional (ConvLayer):** Uses a sliding filter (kernel) to detect local features (edges, corners). Efficient for images.

* **Pooling (MaxPool / AvgPool):** Shrinks the image by picking important values (e.g., max in a region). Reduces computation and noise.

* **Dropout:** Randomly turns off some neurons during training → prevents overfitting.

* **Recurrent (RNN/LSTM/GRU):** Layers that remember previous steps (sequential data).

---

###  **2.4.7. Output Layer: Regression vs Classification**  

* **Regression (predict numbers):**  

  * Output layer has **1 neuron** (or more if multiple values).
  * Activation: **None** or **linear**.
  * Loss: **MSE (Mean Squared Error)**.
    Example: Predicting revenue next quarter.

* **Classification (predict categories):**  

  * Binary: 1 neuron + **Sigmoid** activation (0–1 probability).
  * Multi-class: Multiple neurons + **Softmax** (probabilities sum to 1).
  * Loss: **Cross-Entropy**.
    Example: Fraud (yes/no), document type (invoice/receipt/contract).

---

###  **2.4.8. RNN vs LSTM**  

* **RNN (Vanilla):** Remembers past sequence via hidden state.
  Problem: **Vanishing/Exploding Gradients** → forgets long sequences.

* **Is LSTM a must?**  
  No — simple RNNs work for short sequences.
  But for most practical tasks (text, transactions, speech), **LSTMs or GRUs** are preferred because they handle long-term memory better.

---

###  **2.4.9. LSTM (Long Short-Term Memory)**  

* Think of LSTM as RNN with a **memory cell + gates**:

  * **Forget Gate:** Decides what info to drop.
  * **Input Gate:** Decides what new info to store.
  * **Output Gate:** Decides what to pass forward.

This architecture solves the “forgetting problem” of standard RNNs.

**Example:**  

* Vanilla RNN may forget the start of a sentence like
  “The company that audited Deloitte’s books **was fraudulent**.”
* LSTM can keep memory of “company” → “was fraudulent” across long gaps.

---

###  **Summary Cheat Points (Interview-Safe)**  

* **Neuron = mini calculator (weighted sum + activation).**  
* **Weights/edges = importance of connections.**  
* **Layers = abstraction levels; depth decided by validation performance.**  
* **ConvLayer = feature extraction, MaxPool = size reduction, Dense = decision making.**  
* **Output differs for regression (linear, MSE) vs classification (softmax/sigmoid, Cross-Entropy).**  
* **RNN remembers sequences, but LSTM adds gates to fix forgetting → standard in real use.**  

---

## 2.5 NLP techniques (e.g. TF-IDF, word-embedding)

### 2.5.1. Background – Why NLP techniques are needed?

Imagine you’re asked to review **millions of audit documents, contracts, or financial statements**.
The computer sees them as just strings of letters. To analyse them, we need to **turn words into numbers** so models can understand patterns.

* **Why needed?**  
  Humans understand meaning. Machines don’t. NLP techniques give structure to messy text.
* **Purpose?**  

  * Spot fraud in audit reports
  * Find unusual language in compliance docs
  * Summarise thousands of client contracts
  * Detect sentiment in customer complaints

So NLP = **bridge from text → useful numbers for analysis.**  

---

### 2.5.2. Techniques Explained

####  TF-IDF (Term Frequency – Inverse Document Frequency)

* Think of it like **highlighting important words** in a set of documents.
* **TF** = how often a word appears in a document (e.g., “revenue” in one report).
* **IDF** = how rare that word is across all documents. Rare = more weight, common = less weight.
* **Outcome**: Words like *“revenue recognition”* may get high importance, while *“the”, “and”* get almost zero.
* **Use in audit**: Helps identify which terms are unusually frequent in suspicious contracts.

---

####  Word Embeddings (Word2Vec, GloVe, BERT embeddings)

* Imagine every word gets an **address in a 3D map**.
* Words with similar meaning (“profit”, “income”) live **close together**.
* Unlike TF-IDF, embeddings **understand context & similarity**.
* **Outcome**: Machine sees relationships (e.g., *“fraud” \~ “misstatement”*).
* **Use in audit**: Automatically cluster risky phrases in financial statements, or find related terms auditors should check.

---

📊 **Simple Comparison:**  

| Feature         | TF-IDF                        | Word Embedding                                  |
| --------------- | ----------------------------- | ----------------------------------------------- |
| Focus           | Frequency & rarity of words   | Meaning & context of words                      |
| Output          | Sparse vector (lots of zeros) | Dense vector (compact numbers)                  |
| Example Insight | “Which words are unusual?”    | “Which words mean similar things?”              |
| Audit Example   | Flag rare terms in reports    | Group “fraud”, “theft”, “embezzlement” together |

---

### 2.5.3. 10 Interview Questions (Deloitte Manager DS/ML – Audit context)
#### 🎯 Mini Model Answers

**1. Explain TF-IDF in simple terms. How does it help in detecting anomalies in audit text data?**  
TF-IDF scores words by how frequent they are in a document versus how rare across all documents. In audit, if one contract overuses a rare word like “side-agreement,” it signals unusual language worth review.

---

**2. How do word embeddings improve over TF-IDF when analysing financial documents?**  
Embeddings capture meaning, not just counts. For example, “fraud” and “misstatement” may not appear in the same form, but embeddings show they’re similar. This helps auditors detect risk phrases even if the wording changes.

---

**3. If you had 10,000 client contracts, how would you use TF-IDF to flag unusual clauses for audit review?**  
I’d convert each contract into TF-IDF vectors, then rank terms with the highest rarity. Clauses with these high-weight terms would be flagged as “non-standard” for further audit inspection.

---

**4. How can embeddings be used to detect synonyms like “underreporting” vs “misstatement” in compliance reports?**  
Because embeddings place similar words close in vector space, clustering techniques can group terms like “underreporting,” “misstatement,” and “error,” helping auditors detect risk even when language varies.

---

**5. How would you combine TF-IDF with embeddings in a hybrid model for fraud detection?**  
I’d use TF-IDF for transparency (which words are rare) and embeddings for semantic similarity. Together, they create a richer representation—highlighting both unusual and meaning-related risks in financial text.

---

**6. What challenges occur when using TF-IDF on very large corpora (e.g., millions of audit logs)?**  
Scalability and sparsity are major issues. The feature space can be huge, leading to high memory costs. Also, TF-IDF ignores word order and meaning, which limits insights in nuanced audit language.

---

**7. How do you deal with domain-specific vocabulary (e.g., IFRS terms) when training embeddings?**  
I’d use pre-trained embeddings as a base and fine-tune them on domain-specific corpora—such as IFRS, GAAP, or audit reports—so the model learns technical terms like “goodwill impairment” accurately.

---

**8. How would you explain to a non-technical audit partner why embeddings are better than keyword search?**  
Keyword search is literal. If you type “fraud,” it won’t find “embezzlement.” Embeddings understand meaning, so they can surface all related risks. It’s like moving from word-matching to concept-matching.

---

**9. How would you ensure NLP outputs comply with GDPR or audit transparency requirements?**  
By anonymising sensitive data before training, keeping audit trails of model decisions, and using explainable methods like TF-IDF alongside embeddings. Transparency and traceability are key in regulatory environments.

---

**10. Suppose your junior team proposed using TF-IDF for an NLP fraud detection project. How would you guide them towards a more advanced but explainable approach?**  
I’d acknowledge TF-IDF’s strengths in explainability, but suggest combining it with embeddings for semantic coverage. I’d guide them to prototype both, compare results, and present trade-offs to stakeholders for an informed choice.

---

### 2.5.4. NLP Math Summary

---

#### **1. Vector Norm (Magnitude / Length)**

For vector $A = [a_1, a_2, \dots, a_n]$:

$$
||A|| = \sqrt{\sum_{i=1}^n a_i^2}
$$

👉 Measures the **length of a vector** in n-dimensional space.
Example: $A=[3,4]$ → $||A||=\sqrt{3^2+4^2}=5$.

---

#### **2. Cosine Similarity**

$$
\text{cosine\_similarity}(A,B) = \frac{A \cdot B}{||A|| \, ||B||}
$$

* Dot product in numerator.
* Norms in denominator.
* Range = $[-1,1]$.

👉 Measures the **angle between two vectors** (closeness in direction, not magnitude).

---

#### **3. Euclidean Distance (L2)**

$$
d(A,B) = \sqrt{\sum_{i=1}^n (a_i - b_i)^2}
$$

👉 Straight-line distance between two vectors.

* Sensitive to scale.
* Good for dense embeddings.

---

#### **4. Manhattan Distance (L1)**

$$
d(A,B) = \sum_{i=1}^n |a_i - b_i|
$$

👉 “City-block” distance — adds up absolute differences.

* Robust in sparse spaces (like TF-IDF).

---

#### **5. Jaccard Similarity**

For two sets $A, B$:

$$
J(A,B) = \frac{|A \cap B|}{|A \cup B|}
$$

👉 Measures **overlap** between sets.

* 1 = identical sets.
* 0 = no overlap.
* Often used with **bag-of-words models**.

---

#### **6. TF-IDF (Term Frequency – Inverse Document Frequency)**

$$
TF(t, d) = \frac{\text{count of term } t \text{ in document } d}{\text{total terms in document } d}
$$

$$
IDF(t) = \log \Bigg(\frac{N}{1 + n_t}\Bigg)
$$

$$
TF\text{-}IDF(t,d) = TF(t,d) \times IDF(t)
$$

* $N$ = total documents
* $n_t$ = docs containing term $t$

👉 Highlights words that are **important in a document but rare across corpus**.

---

#### ✅ Deloitte Audit Example Connections

* **Norms** → required for cosine similarity in document comparison.
* **Cosine similarity** → measure closeness of two audit reports.
* **Euclidean/Manhattan** → compare embedding distances (e.g., fraud vs error).
* **Jaccard** → compare clause overlap between contracts.
* **TF-IDF** → flag unusual terms in financial reports.
* 
---

## 2.6 Experience developing Generative AI projects.

---

## 2.7 Exercising software engineering best practices. E.g. 
	- test-driven development, 
	- smart data structure
	- algorithm selection.

---

## 2.8 Azure Databricks

---

## 2.9 Azure MLflow

---

## 2.10 Azure ML services and/or other ML services.

---

## 2.11 PowerBI

---

## 2.12 Tableau.

---

## 2.13 Agile development team.

---


# 3. Prepare for Why Deloitte, Why Consulting, Why this department
### QUESTIONS 
	https://www.youtube.com/watch?v=XGGpnVBWSDw&ab_channel=MyConsultingOffer  
	https://nodeflair.com/companies/deloitte/interviews/data-scientist  
	https://www.interviewquery.com/interview-guides/deloitte-data-scientist  
	
	Not What you Achieved rather HOW you DID it  

### Q2 Tell me About yourself
	-> Why you fit for your job
	-> Key Roles that showcase your skills and accomplishment
	-> Link your roles together.
	-> Align your Journey

### WHY DELOITTE
	-> Why Does Deloitte Stands out for you ? Innovation AI Data ? 
		-> Research on Latest ACtivity

### WHY THE DEPARTMENT

### Q3 WHY CONSULTING
	-> Challenges, Everyday is different
	-> Love Fast-paced
	-> Creative Solutions
	-> Different Stakeholder
	-> Different Industries
	-> Data oR Strategy Or What is your Kick ? Aha Feeling  What Excite you the most

	LONG TERM ROLES
		-> Strategic thinking
		-> Leadership roles
		-> Problem Solving
		-> Communication
		-> 5 to 10 Years


### Q4 TELL ME SOMETHING THAT IS NOT ON YOUR RESUME?
	-> 

### Q5 TELL ME ABOUT A TIME YOU FAILED
	-> Ability to Fight setbacks
	-> Learn from Them
	-> GROW
	FOCUS ON WHAT YOU LEARNT -> Resilence and Proactive

### DELOITTE Evaluation
  - Relevance
  - Role
  - Impact

### TECHNO-MANGERIAL ROLES
#### Questions
    - Can you discuss your experience with cloud platforms?
    - What is your familiarity with MLOps?
    - Have you encountered any data challenges in your previous work?
    - How did you deploy the solution?
    - Which algorithm did you use and why?
    - Can you explain the basics of machine learning and decision trees?

# 4. Understanding the Domain - Audit and Assurance

**Audit & Assurance = Deloitte is like a trusted referee who checks that companies are telling the truth, managing risks, and following the rules — so that leaders, investors, and the public can trust them.** 

**Public Interest = the wellbeing of everyone outside the company who can be harmed if the company lies, cheats, or hides the truth. Deloitte’s role is to make sure businesses are transparent so the whole system stays fair and trusted.**  

**Deloitte gives independent assurance by acting like a trusted referee. They check whether companies are honestly reporting risks, profits, or processes. This builds trust for everyone involved — from boards (governance) to stakeholders (employees, investors, customers) to regulators (FCA, HMRC, etc.).**  

**Deloitte connects assurance → governance → stakeholders → regulators**  
**Company → Risks → Regulation → Deloitte Assurance Action,**  

**Deloitte’s Analytics & Data Science team makes sure data is used responsibly, transparently, and compliantly, so businesses can be trusted by regulators and the public.**  

**Yes — GDPR, IP conflicts, obfuscation of sensitive data, anonymisation, and audit trails ALL fall under Deloitte’s “data compliance + public trust” mandate.**  

**Deloitte makes sure data is legal, safe, unbiased, and well-documented → this protects clients from regulators and restores confidence with the public.**  

**“Assurance to those charged with governance”**  
- People in charge of running or overseeing the company → board of directors, regulators, or even shareholders.  
- Example: Board of Tesco wants to know if their financial reporting is accurate. Deloitte provides assurance.  

**“Responding to emerging issues and protecting the public interest”**  
- Emerging issues = new risks like fraud, cyberattacks, climate reporting, or AI misuse.  
- Public interest = ordinary people (customers, employees, investors).  
- Example: If a company fakes its carbon emissions report, Deloitte detects it → this protects the public who care about climate change.  

**“Providing assurance to help businesses”**  
- Means Deloitte checks and confirms that a business is transparent, resilient, and compliant.  
- Example: A startup wants to go public on the London Stock Exchange. Deloitte audits them to assure investors that their finances and risks are in order.  


**“Public interest” means things that affect society as a whole, not just the company or its shareholders.**  
It includes:
- Investors → so they don’t get tricked into investing in fake numbers.  
- Customers → so products are safe, ethical, and companies aren’t cheating.  
- Employees → so jobs are secure, salaries are fair, pensions are protected.  
- Governments/Regulators → so tax is paid properly, laws are followed.  
- Society at large → so businesses don’t cause crises (financial crash, pollution, fraud).  

**"Assurance in Business"**  
- A company says: “Our accounts are correct, we made £500M profit.”
- Deloitte audits and confirms if this is true.
- Investors, banks, and regulators now trust the company’s report → that’s assurance in action.

**"Independent Assurance"**  
👉 “Independent” means Deloitte is like a referee, not part of either team.
If Tesco says, “We don’t use child labour,” Deloitte can independently verify supply chains. Their independence gives the public confidence — because Deloitte has no reason to lie for Tesco.

**"Risk Assessment / Managed / Mitigated**"
Example (Bank):
- Risk = fake loan applications.
- Deloitte checks if the bank has:
    Processes to verify IDs (managed risk).
    Extra fraud-detection ML model (mitigated risk).
- Deloitte then reports: “Risk of fraud is being managed at acceptable levels.”


**"Charged with Governance"**  
- The people in charge of running and overseeing the business.
- Examples: board of directors, audit committee, senior executives.
- Deloitte’s job = give these leaders clear, reliable info so they can make smart, safe decisions.

**Board = Charged with Governance**  
- board of directors
- audit committee
- senior executives.

**Stakeholders = anyone who cares about the business**  
- Shareholders: people who invested money.
- Employees: want job security, fair pay.
- Customers: want safe products.
- Suppliers: want timely payments.
- Banks: want loans repaid.

**Regulators = referees of the whole industr**y
- Financial Conduct Authority (FCA) → checks banks aren’t cheating.
- HMRC → checks taxes are paid.
- Environment Agency → checks pollution rules are followed.
- Ofcom → checks telecom companies follow rules.


**"High quality and transparent reporting on data use"**  
When Deloitte uses or analyses data, they must show where it came from, how it was processed, and whether it’s reliable.   
Example:
- A bank uses ML to detect fraud.
- Deloitte checks the data pipeline → no missing fields, no bias, no tampering.
- They create a transparent report showing exactly how data was used → regulators and stakeholders trust the outcome.

**“Compliance of data handling is critical”**  
Acronyms / Frameworks That Apply:
- GDPR (General Data Protection Regulation – Europe/UK) → privacy law protecting personal data.
- HIPAA (Health Insurance Portability and Accountability Act – US, healthcare data).
- SOX (Sarbanes-Oxley Act – US, financial data integrity).
- PCI-DSS (Payment Card Industry Data Security Standard – protects credit card data).
- ISO 27001 (International standard for information security).
- FCA - Financial Conduct Authority (UK regulator)

**Examples of Risks & How Deloitte Help**s
- GDPR violation → A company stores customer data without consent → Deloitte checks compliance, anonymises personal data, and reports gaps.
- IP conflict → Two companies fight over ownership of an AI model trained on proprietary datasets → Deloitte verifies data provenance.
- Sensitive data obfuscation → Deloitte ensures names/addresses are masked or tokenized before analysis → protects privacy.
- Bias in ML models → If hiring models discriminate by gender/ethnicity, Deloitte audits the data & features → ensures fairness.
- Regulatory compliance → FCA (UK), HMRC (UK tax), SEC (US) all require clean, auditable data → Deloitte ensures pipelines are compliant.

**“Rebuilding trust of the public”**  
👉 If companies misuse or lose data, public trust collapses. Deloitte’s role = fix and rebuild trust.

# 5. BEHAVIOURAL QUESTIONS
### From the book Notes

# 6. BUSINESS CASE STUDY QUESTIONS
### Preparation


# 7. MISCELLANEOUS

#### 7.1 Regression Metrics: From Covariance to Adjusted R²

1. **Covariance**

$$
Cov(X, Y) = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{n-1}
$$

---

2. **Correlation (r)**

$$
r = \frac{Cov(X,Y)}{\sigma_X \sigma_Y}
$$

---

3. **Coefficient of Determination (R²)**

- *Simple regression*:

$$
R^2 = r^2
$$

- *General regression*:

$$
R^2 = 1 - \frac{SS_{res}}{SS_{tot}}
$$

Where:

$$
SS_{tot} = \sum (y_i - \bar{y})^2
$$

$$
SS_{res} = \sum (y_i - \hat{y}_i)^2
$$

---

4. **Adjusted R²**

$$
AdjR^2 = 1 - \Bigg( \frac{(1 - R^2)(n - 1)}{n - k - 1} \Bigg)
$$
