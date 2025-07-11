# Canvus-Local-LLM

**Multitaction Canvus to Local Ollama LLM Interface**

A Windows system tray application that provides real-time AI processing capabilities within Canvus collaborative workspaces using local Ollama vision models.

## 🚀 Features

- **Privacy-First**: All AI processing happens locally using Ollama
- **Real-Time Processing**: Monitors Canvus workspaces via subscription streams
- **System Tray Integration**: Minimal UI footprint with Windows system tray
- **Multiple AI Workflows**: Text analysis, PDF processing, canvas analysis, and OCR
- **Vision Model Support**: Local Ollama vision models for image processing

## 📋 Requirements

- **Operating System**: Windows 10/11 (x64)
- **Python**: 3.8+ 
- **Ollama**: Local Ollama instance with vision models
- **Canvus Server**: Access to a Canvus server instance

## 🛠️ Installation

### Prerequisites

1. **Install Python 3.8+**
   ```powershell
   # Verify Python installation
   python --version
   ```

2. **Install Ollama**
   - Download from [ollama.ai](https://ollama.ai)
   - Install and start the Ollama service
   - Pull a vision model (e.g., `ollama pull gemma3`)

3. **Install Poetry** (recommended)
   ```powershell
   pip install poetry
   ```

### Application Setup

1. **Clone the repository**
   ```powershell
   git clone https://github.com/yourusername/Canvus-Local-LLM.git
   cd Canvus-Local-LLM/app
   ```

2. **Install dependencies**
   ```powershell
   poetry install
   # or
   pip install -r requirements.txt
   ```

3. **Configure the application**
   - Copy `env.template` to `.env`
   - Update configuration with your Canvus server details
   - Set your API key or username/password

4. **Run the application**
   ```powershell
   python -m src.main
   ```

## ⚙️ Configuration

The application uses environment variables for configuration. Create a `.env` file based on `env.template`:

```env
# Canvus Server Configuration
CANVUS_SERVER_URL=http://localhost:3000
CANVUS_API_KEY=your_api_key_here
CANVUS_USERNAME=your_username
CANVUS_PASSWORD=your_password

# Ollama Configuration
OLLAMA_SERVER_URL=http://localhost:11434
OLLAMA_MODEL=gemma3

# Application Configuration
LOG_LEVEL=INFO
MAX_RETRIES=3
RETRY_DELAY=10
```

## 🔧 Development

### Project Structure

```
app/
├── src/                    # Main application code
│   ├── main.py            # Application entry point
│   ├── config.py          # Configuration management
│   └── exceptions.py      # Custom exceptions
├── tests/                 # Test files
├── lib/                   # External libraries
├── config/                # Configuration files
├── assets/                # Application assets
└── logs/                  # Application logs
```

### Running Tests

```powershell
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_config.py -v

# Run with coverage
python -m pytest --cov=src
```

### Code Quality

```powershell
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

## 🤖 AI Workflows

### Text Analysis
- **Trigger**: Notes with `{{ }}` content
- **Process**: Sends text to local Ollama for analysis
- **Response**: Creates response note with 66% transparency

### PDF Analysis
- **Trigger**: Images titled "AI_Icon_PDF_Precis" with PDF parent
- **Process**: Extracts text using PyPDF2, chunks content, processes through Ollama
- **Response**: Creates precis note with document summary

### Canvas Analysis
- **Trigger**: Images titled "AI_Icon_Canvus_Precis" with BackgroundID parent
- **Process**: Gathers all widgets and connectors, analyzes relationships
- **Response**: Creates comprehensive canvas overview

### Snapshot OCR
- **Trigger**: Images titled "Snapshot at ..."
- **Process**: Uses vision model for OCR text extraction
- **Response**: Creates note with extracted text, removes original snapshot

## 🔒 Security & Privacy

- **Local Processing**: All AI processing happens on your local machine
- **No External Calls**: No data is sent to external services
- **Secure Storage**: Credentials stored using Windows Credential Manager
- **Configuration Encryption**: Sensitive data encrypted in configuration files

## 📊 Monitoring

The application provides real-time status through:
- **System Tray Icon**: Visual status indicators
- **Context Menu**: Connection and processing status
- **Log Files**: Detailed logging in `logs/canvus_llm.log`

## 🐛 Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify Canvus server is running and accessible
   - Check API key or username/password
   - Ensure network connectivity

2. **Ollama Errors**
   - Verify Ollama service is running (`ollama serve`)
   - Check model is installed (`ollama list`)
   - Ensure vision model compatibility

3. **Processing Errors**
   - Check log files for detailed error messages
   - Verify file permissions and disk space
   - Ensure sufficient memory for large documents

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env` file.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Canvus-Local-LLM/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/Canvus-Local-LLM/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Canvus-Local-LLM/discussions)

## 🗺️ Roadmap

- [ ] Image generation capabilities
- [ ] Multi-server support
- [ ] Plugin architecture
- [ ] Advanced OCR features
- [ ] Cross-platform support

---

**Version**: 1.0.0  
**Last Updated**: July 2025  
**Status**: In Development 