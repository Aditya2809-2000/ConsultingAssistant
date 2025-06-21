# 💼 IT Consulting Assistant

An AI-powered IT consulting assistant built with Streamlit and Google's Gemini AI. This application helps IT consultants analyze BRD, CRD, and technical documents with comprehensive insights, technology recommendations, project feasibility analysis, and stakeholder communication tools to accelerate consulting projects.

## 🚀 Features

- **BRD Analysis**: Comprehensive Business Requirements Document analysis with technology recommendations
- **CRD Analysis**: Customer Requirements Document analysis with solution mapping and gap analysis
- **Technical Document Analysis**: Technical specifications, architecture documents, and system design analysis
- **Pre-Execution Questions**: Identify critical questions and gaps that need stakeholder clarification
- **Project Feasibility**: Assess technical feasibility, resource requirements, and timeline estimates
- **Architecture Recommendations**: Get technology stack and architecture recommendations
- **Implementation Roadmap**: Detailed project planning with risk assessment
- **Stakeholder Communication**: Generate professional emails for stakeholder updates

## 📋 Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini AI
- Poppler-utils (for PDF processing)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd it-consulting-assistant
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Install System Dependencies

**Windows:**
- Download and install Poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
- Add Poppler to your system PATH

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

## 🔑 API Configuration

### Option 1: Using Streamlit Secrets (Recommended for Production)

Create a `.streamlit/secrets.toml` file in your project directory:

```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

### Option 2: Environment Variable

Set the environment variable:

**Windows:**
```bash
set GOOGLE_API_KEY=your_actual_api_key_here
```

**macOS/Linux:**
```bash
export GOOGLE_API_KEY=your_actual_api_key_here
```

### Option 3: Manual Input (Development)

The application will prompt you to enter the API key in the sidebar if not found in secrets or environment variables.

## 🔑 Getting Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Use it in one of the configuration methods above

## 🚀 Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📖 Usage Guide

### Document Analysis
1. **Upload Document**: Upload a BRD, CRD, or technical document (PDF format)
2. **Add Context**: Optionally provide additional context or focus areas
3. **Choose Analysis**: Select the type of analysis you need:
   - **BRD Analysis**: For Business Requirements Documents
   - **CRD Analysis**: For Customer Requirements Documents
   - **Technical Document Analysis**: For technical specifications and architecture documents
   - **Pre-Execution Questions**: To identify gaps and clarifications needed
   - **Project Feasibility**: To assess technical and business feasibility
   - **Architecture Recommendations**: For technology stack and architecture guidance
   - **Implementation Roadmap**: For detailed project planning
4. **Review Results**: Examine the AI-generated insights and recommendations
5. **Generate Stakeholder Email**: Create professional emails for stakeholder communication

### Analysis Types

#### BRD Analysis
- Business process analysis and optimization opportunities
- Functional and non-functional requirements breakdown
- Technology implications and recommendations
- Risk assessment and mitigation strategies

#### CRD Analysis
- Customer requirements mapping and gap analysis
- Solution architecture recommendations
- User experience and journey mapping
- Business value proposition and ROI analysis

#### Technical Document Analysis
- Technical architecture assessment
- System design and component analysis
- Technology stack recommendations
- Implementation strategy and risk assessment

#### Pre-Execution Questions
- Project scope validation and gaps
- Stakeholder alignment and communication needs
- Technical and resource requirements clarification
- Risk identification and mitigation planning

#### Project Feasibility
- Technical feasibility assessment
- Resource and timeline feasibility
- Budget and cost analysis
- Business case validation

#### Architecture Recommendations
- Technology stack selection
- Cloud and infrastructure recommendations
- Security and compliance architecture
- Performance and scalability planning

#### Implementation Roadmap
- Detailed project phases and timelines
- Resource planning and allocation
- Risk assessment and mitigation
- Quality assurance and testing strategy

## 🎨 Customization

### Styling
Modify `style.css` to customize the application's appearance.

### Prompts
Edit the analysis prompts in `app.py` to tailor the AI responses to your specific consulting needs.

## 🔧 Troubleshooting

### Common Issues

1. **"No secrets files found" Error**
   - Create the `.streamlit/secrets.toml` file as described above
   - Or use environment variables
   - Or enter the API key manually in the sidebar

2. **PDF Processing Errors**
   - Ensure Poppler-utils is properly installed
   - Check that the PDF file is not corrupted
   - Try with a different PDF file

3. **API Key Issues**
   - Verify your Google API key is valid
   - Check your API quota and billing status
   - Ensure the key has access to Gemini AI

4. **Import Errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Verify you're using the correct Python version

### Streamlit Cloud Deployment Issues

If you encounter deployment errors on Streamlit Cloud:

1. **Dependency Installation Errors**
   - Ensure `packages.txt` contains `poppler-utils`
   - Check that `requirements.txt` has compatible versions
   - Verify `runtime.txt` specifies a supported Python version

2. **PDF Processing Failures**
   - The app includes fallback error handling for PDF processing
   - Check the error messages for specific troubleshooting steps
   - Ensure uploaded PDFs are valid and not corrupted

3. **Testing Deployment**
   - Run `python test_deployment.py` locally to verify dependencies
   - Check Streamlit Cloud logs for specific error messages
   - Ensure all files are committed to your repository

### Error Messages and Solutions

- **"Please set up the GOOGLE_API_KEY"**: Configure your API key using one of the methods above
- **"Error processing PDF"**: Check PDF file validity and Poppler installation
- **"Error generating response"**: Verify API key and internet connection
- **"installer returned a non-zero exit code"**: Check dependencies and system requirements

## 📁 Project Structure

```
it-consulting-assistant/
├── app.py                 # Main application file
├── style.css             # Custom styling
├── requirements.txt      # Python dependencies
├── packages.txt          # System dependencies
├── .streamlit/
│   └── secrets.toml     # API configuration (create this)
├── static/              # Static assets
└── README.md           # This file
```

## 🔒 Security Notes

- Never commit your API key to version control
- Use environment variables or Streamlit secrets for production
- Regularly rotate your API keys
- Monitor your API usage and costs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the error messages in the application
3. Ensure all dependencies are properly installed
4. Verify your API key configuration

## 🔄 Updates

To update the application:

1. Pull the latest changes: `git pull`
2. Update dependencies: `pip install -r requirements.txt --upgrade`
3. Restart the application: `streamlit run app.py` 