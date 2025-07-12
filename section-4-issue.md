## 4. AI Processing Workflows

This section implements the core AI processing workflows that handle different types of content and triggers. Each workflow will process specific content types through the local Ollama instance and create appropriate responses in the Canvus workspace. The workflows must handle text analysis, PDF processing, canvas analysis, and snapshot OCR with proper error handling and user feedback.

### 4.1 Text Analysis Workflow
- [ ] **Trigger Detection**
  - Implement `{{ }}` trigger detection in note content
  - Create trigger validation and duplicate prevention
  - Set up trigger context extraction
  - Implement trigger timeout handling

- [ ] **Text Processing**
  - Create text extraction and cleaning
  - Implement system prompt generation
  - Set up Ollama text generation requests
  - Create response formatting and validation

- [ ] **Response Creation**
  - Implement response note creation with 66% alpha
  - Create dynamic note sizing based on character count
  - Set up response placement and styling
  - Implement response error handling and retry logic

### 4.2 PDF Analysis Workflow
- [ ] **PDF Trigger Detection**
  - Implement "AI_Icon_PDF_Precis" image trigger detection
  - Create PDF widget parent validation
  - Set up PDF download and storage
  - Implement PDF metadata extraction

- [ ] **PDF Text Extraction**
  - Integrate PyPDF2 for text extraction
  - Implement text cleaning and formatting
  - Create text chunking based on token limits
  - Set up chunk processing and summarization

- [ ] **PDF Processing**
  - Implement chunk-based processing through Ollama
  - Create precis generation with structured output
  - Set up processing progress tracking
  - Implement large PDF handling and memory management

### 4.3 Canvas Analysis Workflow
- [ ] **Canvas Trigger Detection**
  - Implement "AI_Icon_Canvus_Precis" image trigger
  - Create BackgroundID parent validation
  - Set up canvas data gathering
  - Implement canvas state snapshot

- [ ] **Canvas Data Collection**
  - Implement all widget retrieval with annotations
  - Create connector relationship mapping
  - Set up anchor widget classification
  - Implement canvas structure analysis

- [ ] **Canvas Processing**
  - Create comprehensive canvas analysis prompts
  - Implement relationship analysis and insights
  - Set up canvas overview generation
  - Create structured analysis output

### 4.4 Snapshot Analysis Workflow
- [ ] **Snapshot Trigger Detection**
  - Implement "Snapshot at ..." image trigger detection
  - Create snapshot image download and processing
  - Set up OCR preparation and validation
  - Implement snapshot metadata extraction

- [ ] **OCR Processing**
  - Implement vision model OCR using Ollama
  - Create image preprocessing for OCR
  - Set up OCR text extraction and formatting
  - Implement OCR accuracy validation

- [ ] **Snapshot Response**
  - Create feedback note during processing
  - Implement extracted text note creation
  - Set up original snapshot cleanup
  - Create OCR error handling and retry logic 