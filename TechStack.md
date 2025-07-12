# TechStack.md
## Multitaction Canvus to Local Ollama LLM Interface

**Version:** 1.0  
**Date:** July 2025  
**Project:** Canvus-Local-LLM  

---

## 0. Executive Summary

This document defines the technical stack and architecture for the Multitaction Canvus to Local Ollama LLM Interface, a Windows system tray application that provides real-time AI processing capabilities within Canvus collaborative workspaces.

### Core Technology Stack
- **Platform**: Windows 10/11 with PowerShell
- **Language**: Python 3.8+
- **Architecture**: System tray application with async processing
- **AI Engine**: Local Ollama with vision models
- **Integration**: Canvus API via existing Python client library

---

## 1. Core Technology Stack

### 1.1 Platform & Runtime
- **Operating System**: Windows 10/11 (x64)
- **Python Version**: 3.8+ (compatible with existing CanvusPythonAPI)
- **Shell Environment**: PowerShell 7+ (as per user environment)
- **Architecture**: x64 (64-bit)

### 1.2 Core Dependencies

#### 1.2.1 Primary Libraries
```toml
# Core Application Dependencies
python = ">=3.8"
httpx = ">=0.24.0"          # HTTP client (from CanvusPythonAPI)
pydantic = ">=2.0.0"        # Data validation (from CanvusPythonAPI)
aiohttp = ">=3.8.0"         # Async HTTP client
asyncio = ">=3.8.0"         # Async programming support

# System Tray & UI
infi.systray = ">=0.1.5"    # Windows system tray integration (Windows-specific)
Pillow = ">=9.0.0"          # Image processing for tray icons

# AI & Vision Processing
ollama = ">=0.1.0"          # Ollama Python client (existing library)
PyPDF2 = ">=3.0.0"          # PDF text extraction (pure Python)
opencv-python = ">=4.8.0"   # Image processing for vision models

# Configuration & Logging
pydantic-settings = ">=2.0.0"  # Configuration management
loguru = ">=0.7.0"             # Advanced logging
poetry = ">=1.7.0"             # Dependency management (development)
```

#### 1.2.2 Development Dependencies
```toml
# Testing
pytest = ">=7.0.0"
pytest-asyncio = ">=0.21.0"
pytest-mock = ">=3.10.0"

# Code Quality
black = ">=23.0.0"
isort = ">=5.12.0"
flake8 = ">=6.0.0"
mypy = ">=1.0.0"

# Documentation
sphinx = ">=7.0.0"
sphinx-rtd-theme = ">=1.3.0"
```

### 1.3 External Services & APIs

#### 1.3.1 Canvus API Integration
- **Library**: Existing `CanvusPythonAPI` (lib/CanvusPythonAPI/)
- **Authentication**: API Key (preferred) or Username/Password
- **Streaming**: Real-time subscription endpoints with `?subscribe=true`
- **Endpoints**: 
  - `/clients` - Client management
  - `/canvases/{id}?subscribe` - Canvas real-time updates
  - `/widgets` - Widget CRUD operations
  - `/notes`, `/images`, `/pdfs` - Specific widget types

#### 1.3.2 Ollama Local AI Engine
- **Service**: Local Ollama instance
- **Library**: Existing `ollama-python` library (lib/ollama-python/)
- **Models**: Vision-capable models (Gemma3 default)
- **API**: HTTP REST API (localhost:11434)
- **Capabilities**: Text generation, vision processing, OCR
- **Model Download**: Hybrid approach with user choice at installation
- **Model Source**: https://ollama.com/search?c=vision

---

## 2. Architecture Components

### 2.1 System Tray Application

#### 2.1.1 Core Structure
```python
# Main application class
class CanvusLLMInterface:
    def __init__(self):
        self.tray_icon = None
        self.config = Config()
        self.canvus_client = None
        self.ollama_client = None
        self.processing_queue = asyncio.Queue()
        self.active_subscriptions = {}
```

#### 2.1.2 System Tray Features
- **Icon**: Custom application icon with status indicators
- **Context Menu**: Right-click hierarchical menu (system tray menu only)
- **Status Display**: Visual connection and processing status
- **Settings Access**: Configuration management through system tray menu
- **Library**: `infi.systray` for Windows-specific system tray integration

### 2.2 Real-Time Processing Engine

#### 2.2.1 Subscription Management
```python
class SubscriptionManager:
    async def subscribe_to_clients(self):
        """Subscribe to client updates"""
        
    async def subscribe_to_canvas(self, canvas_id: str):
        """Subscribe to canvas widget updates"""
        
    async def process_widget_update(self, widget_data: dict):
        """Process incoming widget updates"""
```

#### 2.2.2 Event Processing Pipeline
1. **Event Detection**: Monitor widget changes (Title, Text, ParentID)
2. **Trigger Validation**: Check for AI processing triggers
3. **Duplicate Prevention**: Track processed widget IDs
4. **Queue Management**: Async processing queue
5. **Response Generation**: Create response widgets

### 2.3 AI Processing Workflows

#### 2.3.1 Text Analysis Workflow
```python
class TextAnalysisWorkflow:
    async def process_text_trigger(self, note: Note) -> Note:
        """Process {{ }} text triggers"""
        
    async def create_response_note(self, content: str, original: Note) -> Note:
        """Create response note with 66% alpha"""
```

#### 2.3.2 PDF Analysis Workflow
```python
class PDFAnalysisWorkflow:
    async def process_pdf_trigger(self, image: Image, pdf: PDF) -> Note:
        """Process PDF analysis triggers"""
        
    async def extract_pdf_text(self, pdf_bytes: bytes) -> str:
        """Extract text using PyPDF2"""
        
    async def chunk_text(self, text: str) -> List[str]:
        """Chunk text based on strategy from Summarizing_long_documents.ipynb"""
```

#### 2.3.3 Canvas Analysis Workflow
```python
class CanvasAnalysisWorkflow:
    async def process_canvas_trigger(self, image: Image, canvas_id: str) -> Note:
        """Process canvas analysis triggers"""
        
    async def gather_canvas_data(self, canvas_id: str) -> dict:
        """Gather all widgets and connectors"""
```

#### 2.3.4 Snapshot Analysis Workflow
```python
class SnapshotAnalysisWorkflow:
    async def process_snapshot_trigger(self, image: Image) -> Note:
        """Process snapshot OCR triggers"""
        
    async def perform_ocr_analysis(self, image_bytes: bytes) -> str:
        """Perform OCR using vision model"""
```

### 2.4 Configuration Management

#### 2.4.1 Configuration Structure
```python
class Config(BaseSettings):
    # Canvus Server Configuration
    canvus_server_url: str = "http://localhost:3000"
    canvus_api_key: Optional[str] = None
    canvus_username: Optional[str] = None
    canvus_password: Optional[str] = None
    
    # Ollama Configuration
    ollama_server_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3"
    
    # Application Configuration
    log_level: str = "INFO"
    max_retries: int = 3
    retry_delay: int = 10
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

#### 2.4.2 Configuration Storage
- **Format**: JSON configuration file
- **Location**: `%APPDATA%/CanvusLLM/config.json`
- **Encryption**: Easiest to implement credential storage method
- **Backup**: Automatic backup on changes
- **UI**: System tray menu only for configuration management

---

## 3. Data Models & Schemas

### 3.1 Core Data Models

#### 3.1.1 Widget Processing Models
```python
class WidgetUpdate(BaseModel):
    widget_id: str
    widget_type: str
    canvas_id: str
    title: Optional[str] = None
    text: Optional[str] = None
    parent_id: Optional[str] = None
    timestamp: datetime
    
class ProcessingTrigger(BaseModel):
    trigger_type: str  # "text", "pdf", "canvas", "snapshot"
    widget_id: str
    canvas_id: str
    trigger_data: dict
    created_at: datetime
```

#### 3.1.2 AI Response Models
```python
class AIResponse(BaseModel):
    response_type: str  # "note", "image", "analysis"
    content: str
    metadata: dict
    processing_time: float
    
class ProcessingStatus(BaseModel):
    status: str  # "pending", "processing", "completed", "error"
    progress: int  # 0-100
    message: str
    error_details: Optional[str] = None
```

### 3.2 API Integration Models

#### 3.2.1 Canvus API Models
- **Reuse**: Existing models from `CanvusPythonAPI`
- **Extension**: Add processing-specific models
- **Validation**: Pydantic model validation

#### 3.2.2 Ollama API Models
```python
class OllamaRequest(BaseModel):
    model: str
    prompt: str
    images: Optional[List[str]] = None
    stream: bool = False
    
class OllamaResponse(BaseModel):
    response: str
    done: bool
    model: str
    created_at: datetime
```

---

## 4. Security & Privacy

### 4.1 Authentication & Authorization

#### 4.1.1 Canvus Authentication
- **Primary**: API Key authentication
- **Fallback**: Username/Password authentication
- **Token Management**: Automatic token refresh
- **Security**: Encrypted credential storage

#### 4.1.2 Local Processing Security
- **No External Calls**: All AI processing local
- **Data Privacy**: No data sent to external services
- **Model Validation**: Ensure vision model compatibility
- **Access Control**: Local file system permissions

### 4.2 Data Protection

#### 4.2.1 Configuration Security
- **Encryption**: AES-256 for sensitive data
- **Key Management**: Windows Credential Manager
- **Access Control**: User-specific configuration files

#### 4.2.2 Processing Security
- **Temporary Files**: Immediate deletion after use
- **Memory Management**: Secure memory clearing
- **Log Security**: No sensitive data in logs

---

## 5. Performance & Scalability

### 5.1 Performance Requirements

#### 5.1.1 Response Times
- **Text Processing**: < 30 seconds
- **PDF Analysis**: < 2 minutes (depending on size)
- **Canvas Analysis**: < 5 minutes
- **Snapshot OCR**: < 1 minute

#### 5.1.2 Resource Usage
- **Memory**: < 500MB baseline
- **CPU**: < 50% during processing
- **Disk**: < 100MB temporary storage (temporary file storage approach)
- **Network**: Minimal (local processing)
- **Concurrent Tasks**: Fixed limit of 5 concurrent processing tasks

### 5.2 Scalability Considerations

#### 5.2.1 Concurrent Processing
- **Async Processing**: Non-blocking operations
- **Queue Management**: Priority-based processing
- **Resource Limits**: Configurable processing limits
- **Error Isolation**: Individual widget processing

#### 5.2.2 Memory Management
- **Streaming**: Large file streaming
- **Chunking**: Text chunking for large documents
- **Cleanup**: Automatic resource cleanup
- **Monitoring**: Memory usage monitoring

---

## 6. Error Handling & Resilience

### 6.1 Error Categories

#### 6.1.1 Network Errors
- **Connection Loss**: Automatic reconnection
- **Timeout Handling**: Configurable timeouts
- **Retry Logic**: Exponential backoff (current plan)
- **Circuit Breaker**: Prevent cascading failures

#### 6.1.2 Processing Errors
- **Model Errors**: Ollama model issues
- **API Errors**: Canvus API failures
- **File Errors**: PDF/image processing issues
- **Validation Errors**: Data validation failures

### 6.2 Recovery Strategies

#### 6.2.1 Automatic Recovery
- **Reconnection**: Automatic API reconnection
- **Model Reload**: Automatic model reloading
- **Queue Recovery**: In-memory processing queue (simpler)
- **State Recovery**: In-memory only state persistence

#### 6.2.2 User Feedback
- **Status Updates**: Real-time status updates
- **Error Messages**: Clear error communication
- **Retry Options**: Manual retry capabilities
- **Log Access**: Debug log access

---

## 7. Monitoring & Observability

### 7.1 Logging Strategy

#### 7.1.1 Log Levels
- **DEBUG**: Detailed processing information
- **INFO**: General application events
- **WARNING**: Non-critical issues
- **ERROR**: Processing failures
- **CRITICAL**: Application failures

#### 7.1.2 Log Structure
```python
class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    component: str
    message: str
    context: dict
    trace_id: str
```

### 7.2 Metrics & Monitoring

#### 7.2.1 Performance Metrics
- **Processing Time**: Average processing times
- **Success Rate**: Processing success rates
- **Error Rates**: Error frequency by type
- **Resource Usage**: Memory and CPU usage

#### 7.2.2 Business Metrics
- **Trigger Frequency**: Processing trigger counts
- **User Activity**: Active canvas monitoring
- **Model Usage**: Ollama model usage patterns
- **Feature Usage**: Workflow usage statistics

---

## 8. Development & Deployment

### 8.1 Development Environment

#### 8.1.1 Local Development
- **Python Environment**: Virtual environment setup
- **Dependencies**: Poetry for dependency management (modern, better resolution)
- **Testing**: pytest with async support
- **Linting**: black, isort, flake8, mypy

#### 8.1.2 Development Tools
- **IDE**: VS Code with Python extensions
- **Debugging**: pdb and logging
- **Testing**: pytest with coverage
- **Documentation**: Sphinx documentation

### 8.2 Deployment Strategy

#### 8.2.1 Installation
- **Distribution**: Easy and simple installation without virus flags
- **Python Distribution**: PyInstaller executable
- **Dependencies**: Bundled with application
- **Updates**: Manual updates only

#### 8.2.2 Configuration
- **First Run**: Guided setup wizard
- **Configuration**: System tray settings
- **Updates**: Automatic configuration migration
- **Backup**: Configuration backup/restore

---

## 9. Testing Strategy

### 9.1 Test Categories

#### 9.1.1 Unit Tests
- **Component Tests**: Individual class testing
- **Model Tests**: Data model validation
- **Utility Tests**: Helper function testing
- **Live Testing**: API-driven workflow testing on live test server

#### 9.1.2 Integration Tests
- **API Tests**: Canvus API integration with live test server
- **Ollama Tests**: AI processing integration
- **Workflow Tests**: End-to-end processing with triggering widget creation
- **UI Tests**: System tray interaction

### 9.2 Test Infrastructure

#### 9.2.1 Test Environment
- **Mock Services**: Mock Canvus and Ollama APIs
- **Test Data**: Synthetic test data
- **CI/CD**: Automated testing pipeline
- **Coverage**: Code coverage reporting

---

## 10. Documentation & Support

### 10.1 Technical Documentation

#### 10.1.1 API Documentation
- **Integration Guide**: Canvus API integration
- **Configuration Guide**: Setup and configuration
- **Troubleshooting**: Common issues and solutions
- **Development Guide**: Contributing guidelines

#### 10.1.2 User Documentation
- **Installation Guide**: Step-by-step installation
- **User Manual**: Feature usage guide
- **FAQ**: Frequently asked questions
- **Support**: Contact and support information

### 10.2 Maintenance & Updates

#### 10.2.1 Version Management
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Changelog**: Detailed change documentation
- **Migration Guide**: Version upgrade instructions
- **Deprecation**: Feature deprecation notices

---

## 11. Future Considerations

### 11.1 Technology Evolution

#### 11.1.1 AI Model Evolution
- **New Models**: Support for new Ollama models
- **Model Switching**: Dynamic model selection
- **Performance**: Model performance optimization
- **Capabilities**: New AI capabilities integration

#### 11.1.2 Platform Evolution
- **Windows Updates**: Windows 12 compatibility
- **Python Updates**: Python 3.12+ support
- **Dependency Updates**: Security and performance updates
- **API Evolution**: Canvus API version updates

### 11.2 Scalability Planning

#### 11.2.1 Multi-Server Support
- **Multiple Canvus Servers**: Support for multiple instances
- **Load Balancing**: Intelligent server selection
- **Failover**: Automatic failover between servers
- **Configuration**: Multi-server configuration

#### 11.2.2 Advanced Features
- **Plugin Architecture**: Extensible processing workflows
- **Custom Models**: User-defined AI models
- **Advanced Analytics**: Canvas relationship analysis
- **Collaboration**: Multi-user processing coordination

---

## 12. Conclusion

The TechStack.md document provides a comprehensive technical foundation for the Multitaction Canvus to Local Ollama LLM Interface. The architecture prioritizes:

- **Privacy**: Local processing with no external dependencies
- **Performance**: Async processing with efficient resource usage
- **Reliability**: Robust error handling and recovery mechanisms
- **Usability**: Minimal UI footprint with system tray integration
- **Extensibility**: Modular design for future enhancements

The technology stack leverages existing investments in the CanvusPythonAPI while providing a solid foundation for real-time AI processing capabilities within Canvus collaborative workspaces. 