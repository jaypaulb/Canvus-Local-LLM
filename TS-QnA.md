# TechStack QnA.md
## Technical Stack Questions & Answers

**Date:** July 2025  
**Project:** Canvus-Local-LLM  

---

## Questions for Clarification

### 1. Ollama Integration & Model Selection

**Q1.1: Ollama Python Client Library**
- **Question**: Should we use the existing `ollama-python` library in `lib/ollama-python/` or create our own client?
- **Context**: The library exists but may need updates for vision model support
- **Options**: 
  - Use existing library

**Q1.2: Vision Model Compatibility**
- **Question**: Which specific Ollama vision models should we support/test?
- **Context**: Need to ensure models support both text and image processing
- **Options**: 
  - Gemma3 (default)
  - Llama3.1-8B-vision
  - Qwen2.5-7B-vision
  - Other models from https://ollama.com/search?c=vision

**Q1.3: Model Download & Management**
- **Question**: Should the application automatically download models or require manual installation?
- **Context**: Large models (2-8GB) may take significant time to download
- **Options**:
  - Hybrid approach with user choice at installation

---

### 2. System Tray Implementation

**Q2.1: System Tray Library Choice**
- **Question**: Should we use `pystray` or `infi.systray` for Windows system tray integration?
- **Context**: Need reliable Windows system tray support with custom icons
- **Options**:
    - `infi.systray` (Windows-specific, potentially more stable)

**Q2.2: Configuration UI**
- **Question**: Should configuration be handled through system tray menu or separate settings window?
- **Context**: Need to balance simplicity with functionality
- **Options**:
  - System tray menu only (simpler)
---

### 3. PDF Processing Strategy

**Q3.1: PDF Text Extraction**
- **Question**: Should we use PDFium or PyPDF2 for PDF text extraction?
- **Context**: Need reliable text extraction for large PDFs
- **Options**:
  - PyPDF2 (pure Python, easier installation)

**Q3.2: Text Chunking Strategy**
- **Question**: What chunking strategy should we use for large PDFs?
- **Context**: Need to balance token limits with context preservation
- **Options**:
  - [text](Docs/Summarizing_long_documents.ipynb)

---

### 4. Error Handling & Recovery

**Q4.1: Retry Strategy**
- **Question**: What retry strategy should we implement for failed processing?
- **Context**: Need to handle network issues, model errors, and API failures
- **Options**:
  - Exponential backoff (current plan)

**Q4.2: State Persistence**
- **Question**: Should we persist processing state across application restarts?
- **Context**: Need to handle application crashes and restarts gracefully
- **Options**:
  - In-memory only (simpler)

---

### 5. Performance & Resource Management

**Q5.1: Concurrent Processing Limits**
- **Question**: How many concurrent processing tasks should we allow?
- **Context**: Need to balance performance with resource usage
- **Options**:
  - Fixed limit (e.g., 5 concurrent tasks)

**Q5.2: Memory Management**
- **Question**: How should we handle large file processing (PDFs, images)?
- **Context**: Large files can consume significant memory
- **Options**:
  - Temporary file storage

---

### 6. Security & Privacy

**Q6.1: Credential Storage**
- **Question**: How should we securely store Canvus API credentials?
- **Context**: Need secure storage for API keys and passwords
- **Options**:
  - whichever option is the easiest to implement and test.

**Q6.2: Temporary File Security**
- **Question**: How should we handle temporary files created during processing?
- **Context**: Need to ensure sensitive data is properly cleaned up
- **Options**:
  - Immediate deletion after use

---

### 7. Development & Testing

**Q7.1: Testing Strategy**
- **Question**: How should we test the integration with Canvus and Ollama?
- **Context**: Need comprehensive testing without external dependencies
- **Options**:
  - I'm not sure.  Ideally I would like to just test on a live test server bit by bit - so I guess this would be unit testing?  I basically want to test each workflow by using an api call to create the triggering widget, then see it if process follows through to completion.

**Q7.2: Development Environment**
- **Question**: Should we use Poetry or pip for dependency management?
- **Context**: Need reliable dependency management for development
- **Options**:
  - Poetry (modern, better dependency resolution)

---

### 8. Deployment & Distribution

**Q8.1: Distribution Method**
- **Question**: How should we distribute the application to end users?
- **Context**: Need easy installation for non-technical users
- **Options**:
  - I don't mind so long as it is easy and simple to install without being flags as potentially a virus.

**Q8.2: Auto-Update Strategy**
- **Question**: Should the application support automatic updates?
- **Context**: Need to balance convenience with security
- **Options**:
  - Manual updates only

---

## User Answers

### 1. Ollama Integration & Model Selection
- **Q1.1**: Use existing `ollama-python` library
- **Q1.2**: Support multiple vision models (Gemma3 default)
- **Q1.3**: Hybrid approach with user choice at installation

### 2. System Tray Implementation
- **Q2.1**: Use `infi.systray` (Windows-specific, more stable)
- **Q2.2**: System tray menu only for configuration

### 3. PDF Processing Strategy
- **Q3.1**: Use PyPDF2 (pure Python, easier installation)
- **Q3.2**: Reference existing chunking strategy from `Summarizing_long_documents.ipynb`

### 4. Error Handling & Recovery
- **Q4.1**: Exponential backoff retry strategy
- **Q4.2**: In-memory only state persistence

### 5. Performance & Resource Management
- **Q5.1**: Fixed limit of 5 concurrent processing tasks
- **Q5.2**: Temporary file storage for large files

### 6. Security & Privacy
- **Q6.1**: Easiest to implement credential storage method
- **Q6.2**: Immediate deletion of temporary files after use

### 7. Development & Testing
- **Q7.1**: Live test server with API-driven workflow testing
- **Q7.2**: Poetry for dependency management

### 8. Deployment & Distribution
- **Q8.1**: Easy and simple installation without virus flags
- **Q8.2**: Manual updates only

---

## Additional Questions

*[Space for any additional questions you may have]*

---

## Technical Decisions

### Final Architecture Decisions

1. **Ollama Integration**: Use existing `ollama-python` library with hybrid model download approach
2. **System Tray**: `infi.systray` for Windows-specific integration with system tray menu only
3. **PDF Processing**: PyPDF2 with reference to existing chunking strategy
4. **Error Handling**: Exponential backoff with in-memory state persistence
5. **Performance**: Fixed 5 concurrent tasks with temporary file storage
6. **Security**: Easiest credential storage implementation with immediate file deletion
7. **Testing**: Live test server with API-driven workflow testing
8. **Development**: Poetry for dependency management
9. **Deployment**: Simple installation without virus flags, manual updates only

### Implementation Priority

1. **Phase 1**: Core system tray application with basic configuration
2. **Phase 2**: Canvus API integration with subscription streams
3. **Phase 3**: Ollama integration with vision model support
4. **Phase 4**: PDF processing with PyPDF2 and chunking strategy
5. **Phase 5**: Testing on live server with API-driven workflows 