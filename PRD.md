# Product Requirements Document (PRD)
## Multitaction Canvus to Local Ollama LLM Interface

**Version:** 1.1  
**Date:** July 2025  
**Project:** Canvus-Local-LLM  

---

## 0. Executive Summary

### Problem Statement
Users need intelligent AI processing capabilities within Canvus collaborative workspaces without external cloud dependencies. Current solutions lack real-time processing, local privacy, and seamless integration with existing workflows.

### Solution Overview
A Windows system tray application that provides real-time AI processing through local Ollama vision models, monitoring Canvus workspaces via subscription streams for intelligent document analysis, canvas summarization, and AI-powered interactions.

### Core Value Proposition
- **Privacy-First**: All processing on local Ollama instance
- **Real-Time**: Subscription-based monitoring with immediate feedback
- **Seamless Integration**: Minimal UI footprint with system tray operation
- **Intelligent Processing**: Multiple workflows for different content types

---

## 1. Core Architecture & Foundation

### 1.1 System Tray Application
**Platform**: Windows system tray (notification area)  
**Interface**: Right-click context menu with hierarchical settings  
**Dependencies**: Python, CanvusPythonAPI, Ollama client, PDFium

**Configuration Menu Structure**:
```
Restart
Settings
├── Canvus Server Address
├── API Key (preferred)
├── Username (optional, hidden if API Key set)
├── Password (optional, hidden if API Key set)
└── Model Selection (default: Gemma3)
```

### 1.2 Real-Time Processing Foundation
**Primary Method**: Canvus API `?subscribe` endpoint  
**Data Format**: ASCII text stream with JSON objects per line  
**Keep-alive**: Blank lines for connection maintenance  

**Staged Subscription Architecture**:
1. Subscribe to `/clients` endpoint
2. On new client: GET `/clients/{client_id}/workspaces`
3. Iterate workspaces to extract CanvasIDs
4. Start separate process per canvas: `/canvases/{canvas_id}?subscribe`

### 1.3 Event Processing Strategy
**Concurrent Processing**: Non-blocking trigger processing  
**Change Detection**: Monitor Title, Text, ParentID changes only  
**Race Condition Prevention**: Avoid processing same widget during movement  
**Duplicate Prevention**: Track processed widget IDs with timestamp validation

---

## 3. Functional Requirements

### 3.1 Core Architecture

#### 3.1.1 System Tray Application
- **Platform:** Windows system tray (notification area)
- **Interface:** Right-click context menu with options:
  - Restart
  - Settings (submenu):
    - Set Canvus Server Address
    - Set API Key
    - Set Username (optional, hidden if API Key set)
    - Set Password (optional, hidden if API Key set)
    - Model Selection (default: Gemma3)

#### 3.1.2 Configuration Management
- **Storage:** Local configuration file
- **Settings:** Editable via system tray right-click menu
- **Persistence:** Maintains settings between application restarts

### 3.2 Real-time Processing System

#### 3.2.1 Subscription Architecture
- **Primary Method:** Canvus API `?subscribe` endpoint
- **Data Format:** ASCII text stream with JSON objects per line
- **Keep-alive:** Blank lines for connection maintenance
- **Staged Processing:**
  1. Subscribe to clients endpoint
  2. On new client: get workspaces
  3. Iterate workspaces to get CanvasIDs
  4. Start separate process per canvas subscription

#### 3.2.2 Event Processing
- **Concurrent Processing:** Non-blocking trigger processing
- **Change Detection:** Monitor Title, Text, ParentID changes only
- **Race Condition Prevention:** Avoid processing same widget multiple times during movement

### 3.3 AI Processing Workflows

#### 3.3.1 Basic AI Interaction
**Trigger:** Note content begins and ends with `{{ }}`
**Process:**
1. Remove `{{ }}` from triggering note
2. Update note to indicate processing status
3. Send text to LLM with system prompt
4. Create new response note with 66% alpha channel
5. Size response note based on character count

**Response Placement:**
- New note with same color and location as original
- Alpha channel: 66% transparency
- Dynamic sizing based on character count
- Scale adjustment to maintain visual consistency

#### 3.3.2 PDF Analysis
**Trigger:** Image with title "AI_Icon_PDF_Precis" with PDF widget as parent
**Process:**
1. Download PDF from Canvus server
2. Extract text using PDFium
3. Chunk text based on token limits
4. Process chunks through LLM for summarization
5. Create precis note with results

**Text Processing:**
- Use PDFium for text extraction
- Implement chunking strategy from `Summarizing_long_documents.ipynb`
- Control detail level through chunk management

#### 3.3.3 Canvas Analysis
**Trigger:** Image with title "AI_Icon_Canvus_Precis" with BackgroundID as parent
**Process:**
1. GET all widgets for canvas with annotations
2. Include connectors for relationship context
3. Use anchor widgets for area classification
4. Process complete dataset through LLM
5. Generate canvas overview and insights

**Analysis Scope:**
- All widget types (notes, images, PDFs, videos, browsers)
- Connectors for relationship mapping
- Anchor widgets for area classification (Brainstorm, Outcomes, etc.)

#### 3.3.4 Snapshot Analysis
**Trigger:** Image with title starting "Snapshot at ..."
**Process:**
1. Download image to local file
2. Create feedback note explaining process
3. Pass image file to LLM for OCR analysis
4. Replace feedback note with extracted text note
5. Delete original snapshot

#### 3.3.5 Image Generation (Future Phase)
**Trigger:** Note content with image generation prompt
**Process:**
1. System prompt to determine response type (Note vs Image)
2. Extract image generation text
3. Pass to external image generation service
4. Create image widget with generated content

### 3.4 Model Management

#### 3.4.1 Vision Model Support
- **Requirement:** Ollama vision models only
- **Default Model:** Gemma3
- **Model Source:** https://ollama.com/search?c=vision
- **Auto-download:** Automatic model installation if not present

#### 3.4.2 Model Configuration
- **User Selection:** Via system tray settings
- **Default:** Gemma3 vision model
- **Validation:** Ensure selected model supports vision capabilities

### 3.5 Error Handling & Retry Logic

#### 3.5.1 Retry Strategy
- **Retry Count:** 3 attempts
- **Intervals:** Immediately, 10s, 30s
- **Feedback:** Update trigger/feedback notes with countdown and error messages

#### 3.5.2 Error Communication
- **Visual Feedback:** Traffic light system in notes
- **Status Updates:** Real-time progress indication
- **Error Details:** Clear error messages in feedback notes

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- **Background Operation:** Optimized for background processing
- **Resource Usage:** Memory and CPU efficient
- **Concurrent Processing:** Non-blocking trigger processing
- **Response Time:** Real-time processing with immediate feedback

### 4.2 Security Requirements
- **Authentication:** API Key preferred, username/password fallback
- **Local Processing:** All AI processing on local Ollama instance
- **No External Dependencies:** No cloud services required
- **Secure Storage:** Local configuration file management

### 4.3 Reliability Requirements
- **Uptime:** Continuous background operation
- **Error Recovery:** Automatic retry with exponential backoff
- **Data Integrity:** Prevent duplicate processing
- **Connection Management:** Handle subscription stream disconnections

### 4.4 Usability Requirements
- **System Tray Integration:** Minimal UI footprint
- **Configuration:** Simple right-click menu interface
- **Feedback:** Traffic light status system
- **Logging:** File-based logging with debug mode option

---

## 5. Technical Architecture

### 5.1 System Components

#### 5.1.1 Core Application
- **Language:** Python
- **Framework:** Windows system tray application
- **Dependencies:** 
  - CanvusPythonAPI library
  - Ollama Python client
  - PDFium for PDF processing
  - Vision model support

#### 5.1.2 API Integration
- **Canvus API:** Using existing CanvusPythonAPI library
- **Ollama API:** Direct HTTP API calls
- **Subscription Streams:** Real-time event processing

#### 5.1.3 Data Processing
- **Text Chunking:** Based on token limits
- **PDF Processing:** PDFium text extraction
- **Image Processing:** Vision model OCR capabilities
- **Response Sizing:** Dynamic note sizing algorithms

### 5.2 Data Flow

#### 5.2.1 Subscription Flow
1. Connect to Canvus server
2. Subscribe to clients endpoint
3. Monitor for new clients/workspaces
4. Subscribe to canvas endpoints
5. Process real-time updates

#### 5.2.2 Processing Flow
1. Detect trigger conditions
2. Validate trigger (prevent duplicates)
3. Create feedback note
4. Process content through LLM
5. Create response note
6. Update status indicators

### 5.3 Configuration Management
- **File Format:** JSON configuration file
- **Settings:** Server address, API key, model selection
- **Persistence:** Local file storage
- **UI:** System tray right-click menu

---

## 6. User Experience

### 6.1 System Tray Interface
- **Icon:** Distinctive application icon
- **Menu:** Right-click context menu
- **Status:** Visual indication of connection status
- **Settings:** Easy access to configuration

### 6.2 Feedback System
- **Traffic Light System:** Color-coded status indicators
- **Progress Updates:** Real-time processing status
- **Error Communication:** Clear error messages
- **Visual Feedback:** Note color and transparency changes

### 6.3 Processing Indicators
- **Trigger Notes:** Immediate status updates
- **Feedback Notes:** Progress indication for long processes
- **Response Notes:** Semi-transparent overlay notes
- **Error Notes:** Clear error communication

---

## 7. Implementation Phases

### 7.1 Phase 1: Core Infrastructure
- System tray application setup
- Canvus API integration
- Basic subscription stream handling
- Configuration management

### 7.2 Phase 2: Basic AI Processing
- Text analysis with `{{ }}` triggers
- Response note creation
- Error handling and retry logic
- Traffic light feedback system

### 7.3 Phase 3: Document Processing
- PDF analysis workflow
- Text extraction and chunking
- Canvas analysis with widget relationships
- Snapshot OCR processing

### 7.4 Phase 4: Advanced Features
- Image generation integration
- Enhanced model management
- Performance optimization
- Advanced error handling

---

## 8. Success Metrics

### 8.1 Performance Metrics
- **Response Time:** < 30 seconds for text processing
- **Uptime:** > 99% availability
- **Error Rate:** < 5% processing failures
- **Resource Usage:** < 500MB memory usage

### 8.2 User Experience Metrics
- **Processing Success:** > 95% successful triggers
- **User Feedback:** Positive status system usage
- **Configuration Ease:** < 2 minutes setup time
- **Error Recovery:** > 90% successful retries

---

## 9. Risk Assessment

### 9.1 Technical Risks
- **Subscription Stream Stability:** Handle connection drops
- **Model Availability:** Ensure vision model compatibility
- **Memory Usage:** Monitor large document processing
- **Race Conditions:** Prevent duplicate processing

### 9.2 Mitigation Strategies
- **Connection Recovery:** Automatic reconnection logic
- **Model Validation:** Check model capabilities on startup
- **Resource Monitoring:** Implement memory usage limits
- **Processing Locks:** Prevent concurrent processing of same widget

---

## 10. Future Enhancements

### 10.1 Planned Features
- **Image Generation:** Stable Diffusion integration
- **Advanced OCR:** Enhanced document processing
- **Multi-server Support:** Multiple Canvus server connections
- **Plugin Architecture:** Extensible processing workflows

### 10.2 Potential Improvements
- **Machine Learning:** Adaptive processing based on usage patterns
- **Advanced Analytics:** Canvas relationship analysis
- **Collaboration Features:** Multi-user processing coordination
- **Integration APIs:** Third-party service connections

---

## 11. Conclusion

The Multitaction Canvus to Local Ollama LLM Interface provides a comprehensive solution for real-time AI processing within Canvus workspaces. The system tray application architecture ensures minimal user interface footprint while providing powerful AI capabilities through local processing.

The phased implementation approach allows for incremental feature delivery while maintaining system stability and user experience quality. The focus on vision models and local processing ensures privacy and performance while providing the intelligent capabilities users need for collaborative workspace enhancement. 