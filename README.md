# ✨ StudySpark AI

**StudySpark AI** is an AI-powered study workspace that turns lecture materials into clean notes, summaries, flashcards, quizzes, exports, analytics, and a searchable lecture assistant.

Upload a PDF, PowerPoint, text file, or pasted lecture content, then let the app generate study materials you can review, test, export, and ask questions about.

---

## 🚀 Key Features

### 📥 Lecture Upload & Text Extraction

- Upload **PDF**, **PPTX**, or **TXT** lecture files.
- Paste raw lecture notes, transcripts, or article text directly into the app.
- Automatically extracts readable text from supported files.
- Saves lecture metadata such as title, page count, word count, upload date, and file hash.
- Detects duplicate uploads to avoid repeated study sets.

### 🧠 AI Notes Generator

- Generates structured lecture summaries using **Google FLAN-T5 Base**.
- Splits long lecture content into sentence-aware chunks for better summaries.
- Produces clean, bullet-style study notes.
- Extracts important keywords and key concepts with **KeyBERT**.
- Builds a searchable vector knowledge base for each lecture.

### 📖 Notes Viewer

- View generated executive summaries for every lecture.
- Browse extracted key concepts as visual keyword pills.
- Uses relevance-scored keywords when source text is available.
- Shows when notes were last generated.
- Provides a copyable summary view for quick reuse.

### 📄 PDF & DOCX Export

- Export generated lecture notes as a polished **PDF** file.
- Export notes as an editable **DOCX** document.
- Includes title, generation date, summary, and key concepts.
- Generated files are stored locally inside the `generated/` folder.

### 🃏 Smart Flashcards

- Generate AI flashcards from lecture content.
- Choose the number of cards to create.
- Practice active recall with question and answer cards.
- Flip cards to reveal answers.
- Mark cards as **known** or **review again**.
- Track session progress visually.
- Shuffle cards for a fresh review order.
- Regenerate flashcards whenever needed.

### ✅ MCQ Quiz Generator

- Generate multiple-choice questions from lecture content.
- Uses AI-generated questions and concise distractor answers.
- Choose the number of quiz questions.
- Answer all questions inside a Streamlit form.
- Get instant scoring after submission.
- Review correct and incorrect answers.
- Saves quiz results for dashboard analytics.
- Regenerate questions for additional practice.

### 💬 AI Study Assistant

- Ask natural-language questions about a selected lecture.
- Uses a local RAG pipeline:
  - chunks lecture content,
  - embeds text with `all-MiniLM-L6-v2`,
  - stores vectors with FAISS,
  - retrieves relevant lecture passages,
  - generates grounded answers with FLAN-T5.
- Shows relevance confidence for answers.
- Includes lecture source excerpts with similarity scores.
- Provides starter question chips such as:
  - “Summarize the main topics.”
  - “What are the key definitions?”
  - “What should I focus on for an exam?”
- Keeps chat history per lecture during the session.
- Includes a clear chat button.

### 📊 Learning Dashboard

- View total uploaded lectures.
- Track generated note sets, flashcards, and MCQs.
- Estimate total reading time saved.
- Visualize generated resources with Plotly charts.
- Track quiz performance over time.
- Review quiz history with grades.
- View uploaded lectures with page count, word count, and upload date.
- Delete lectures and related study data.

### 🎨 Modern Streamlit UI

- Custom responsive styling.
- Clean sidebar branding.
- Dashboard metrics and visual cards.
- Styled tabs, buttons, uploaders, flashcards, quizzes, and progress bars.
- Mobile-friendly layout improvements.

---

## 🧭 Study Workflow

1. **📥 Upload**
   Add a PDF, PPTX, TXT file, or paste lecture text.

2. **🧠 Generate**
   Create summaries, keywords, and a searchable FAISS knowledge base.

3. **📚 Study**
   Review notes, practice flashcards, and take MCQ quizzes.

4. **💬 Ask AI**
   Use the study assistant to ask lecture-specific questions.

5. **📊 Track**
   Monitor content, quiz history, and learning progress from the dashboard.

---

## 🛠️ Tech Stack

| Area | Tools |
| --- | --- |
| App Framework | Streamlit |
| Data & Charts | Pandas, NumPy, Plotly |
| PDF Processing | pdfplumber |
| PPTX Processing | python-pptx |
| AI Models | Transformers, Torch, Google FLAN-T5 Base |
| Embeddings | sentence-transformers, all-MiniLM-L6-v2 |
| Keyword Extraction | KeyBERT |
| Vector Search | FAISS |
| Exports | python-docx, fpdf2 |
| NLP Utilities | NLTK |
| Database | SQLite |

---

## 📁 Project Structure

```text
StudySpark AI/
├── app.py                         # Main Streamlit landing page
├── requirements.txt               # Python dependencies
├── database/
│   ├── database.py                # SQLite helpers and migrations
│   ├── schema.sql                 # Database schema
│   └── studyspark.db              # Local app database, ignored by Git
├── models/
│   ├── summarizer.py              # AI summary generation
│   ├── keyword_extractor.py       # KeyBERT keyword extraction
│   ├── mcq_generator.py           # MCQ and flashcard generation
│   ├── flashcard_generator.py     # Flashcard wrapper
│   └── rag_engine.py              # FAISS + RAG study assistant
├── pages/
│   ├── 1_Dashboard.py             # Analytics dashboard
│   ├── 2_Upload_Lecture.py        # Upload and text extraction
│   ├── 3_Notes_Generator.py       # Notes and index generation
│   ├── 4_Notes_Viewer.py          # Notes review and export
│   ├── 5_Flashcards.py            # Flashcard practice
│   ├── 6_MCQ_Quiz.py              # Quiz generation and scoring
│   └── 8_AI_Study_Assistant.py    # Lecture-grounded chat assistant
├── services/
│   ├── pdf_processor.py           # PDF text extraction
│   ├── ppt_processor.py           # PowerPoint text extraction
│   ├── export_pdf.py              # PDF export
│   ├── export_docx.py             # DOCX export
│   └── text_cleaner.py            # Text utilities
├── utils/
│   └── styles.py                  # Shared custom UI styles
├── uploads/                       # Uploaded and extracted text files
├── generated/                     # Exported PDF/DOCX notes
└── vectorstore/                   # FAISS indexes and metadata
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/studyspark-ai.git
cd studyspark-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the app

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## 🧪 How To Use

### 📥 Upload a lecture

1. Open **Upload Lecture**.
2. Upload a `PDF`, `PPTX`, or `TXT` file, or paste lecture text.
3. Add or edit the lecture title.
4. Click **Process Lecture**.

### 🧠 Generate notes

1. Open **Notes Generator**.
2. Select a lecture.
3. Click **Generate Notes and Index**.
4. The app creates:
   - AI summary,
   - key concepts,
   - searchable vector index.

### 📖 Review and export notes

1. Open **Notes Viewer**.
2. Select a lecture.
3. Review the summary and keywords.
4. Export as **PDF** or **DOCX**.

### 🃏 Practice flashcards

1. Open **Flashcards**.
2. Select a lecture.
3. Generate flashcards if none exist.
4. Reveal answers and mark each card as known or review again.

### ✅ Take a quiz

1. Open **MCQ Quiz**.
2. Select a lecture.
3. Generate MCQs if none exist.
4. Answer every question.
5. Submit and review your score.

### 💬 Ask the study assistant

1. Open **AI Study Assistant**.
2. Select a lecture context.
3. Ask a question about the lecture.
4. Review the answer, confidence score, and source excerpts.

---

## 🧠 AI Pipeline

StudySpark AI uses a local study pipeline designed for lecture content:

1. **Text extraction** from uploaded files.
2. **Sentence-aware chunking** to preserve readable context.
3. **Summary generation** with FLAN-T5.
4. **Keyword extraction** with KeyBERT and MMR diversity.
5. **Vector embedding** with `all-MiniLM-L6-v2`.
6. **FAISS indexing** for fast lecture search.
7. **RAG answering** with retrieved lecture chunks and source excerpts.
8. **Flashcard and MCQ generation** from lecture sentences.

---

## 💾 Local Data

The app stores runtime data locally:

| Folder/File | Purpose |
| --- | --- |
| `database/studyspark.db` | SQLite database |
| `uploads/` | Uploaded files and extracted lecture text |
| `generated/` | Exported PDF and DOCX files |
| `vectorstore/` | FAISS indexes and metadata |
| `*.log` | Streamlit/runtime logs |

These files are ignored by Git so private study content does not get committed accidentally.

---

## 🔐 Privacy Notes

- Study materials are stored locally in this project folder.
- SQLite, uploads, generated notes, and vector indexes are excluded from Git.
- The app uses local Python model execution through installed AI libraries.
- First model use may download model files through Hugging Face dependencies.

---

## 🧯 Troubleshooting

### Model loading is slow

The first run can take time because transformer and embedding models may need to download and initialize.

### NLTK data is missing

The app attempts to download required NLTK tokenizer data automatically when needed.

### Study assistant says knowledge base not found

Open **Notes Generator** and run **Generate Notes and Index** for that lecture first.

### PDF or PPTX text is empty

Some scanned PDFs or image-only slides may not contain extractable text. Try OCR externally or paste the lecture text manually.

### Port 8501 is already in use

Run Streamlit on another port:

```bash
streamlit run app.py --server.port 8502
```

---

## 🌟 Best Use Cases

- University lecture revision
- Exam preparation
- Research paper note extraction
- Training material review
- Self-study knowledge checks
- Turning long transcripts into study resources

---

## 🧩 Future Improvement Ideas

- User accounts and authentication
- OCR support for scanned PDFs
- Spaced repetition scheduling
- Topic-based lecture grouping
- Better citation formatting
- Cloud sync or optional backup
- Dark mode toggle
- More export formats

---

## 📜 License

Add your preferred license here, such as MIT, Apache-2.0, or a private-use notice.

---

## 🙌 About

**StudySpark AI** helps students turn raw lecture content into practical study tools: summaries, flashcards, quizzes, exports, analytics, and lecture-grounded AI answers.

Learn faster. Review smarter. Study with focus. ✨
