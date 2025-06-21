import base64
import streamlit as st
import os
import io
from PIL import Image 

# Add error handling for imports
try:
    import pdf2image
except ImportError as e:
    st.error(f"Error importing pdf2image: {e}")
    st.info("Please ensure pdf2image is properly installed. You may need to install poppler-utils system dependencies.")
    st.stop()

try:
    import google.generativeai as genai
except ImportError as e:
    st.error(f"Error importing google.generativeai: {e}")
    st.info("Please ensure google-generativeai is properly installed.")
    st.stop()

import json

# Initialize Streamlit page - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="IT Consulting Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini AI with better error handling for Streamlit Cloud
api_key = None

# Try to get API key from secrets first (Streamlit Cloud)
try:
    if 'GOOGLE_API_KEY' in st.secrets:
        api_key = st.secrets['GOOGLE_API_KEY']
    elif os.getenv('GOOGLE_API_KEY'):
        api_key = os.getenv('GOOGLE_API_KEY')
    else:
        # For development, allow manual input
        st.sidebar.markdown("### 🔑 API Configuration")
        api_key = st.sidebar.text_input(
            "Enter your Google API Key", 
            type="password",
            help="Get your API key from https://makersuite.google.com/app/apikey"
        )
        
    if api_key and api_key != "your_google_api_key_here":
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ Please configure your Google API Key")
        st.info("""
        **To get your API key:**
        1. Go to https://makersuite.google.com/app/apikey
        2. Create a new API key
        3. Copy it and paste it in the sidebar
        
        **For Streamlit Cloud deployment:**
        - Go to your app Settings → Secrets
        - Add: GOOGLE_API_KEY = "your_actual_api_key_here"
        """)
        st.stop()
        
except Exception as e:
    st.error(f"Error configuring API: {str(e)}")
    st.stop()

# Load and apply custom CSS
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css not found. Some styling may be missing.")

# Custom CSS for card containers
def create_card(title, content):
    st.markdown(f"""
        <div class="css-card">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)

# Load custom CSS
load_css()

def get_gemini_response(context, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([context, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return f"Error: Unable to process the document. Please check your API key and try again. Error details: {str(e)}"

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Reset file pointer to beginning
            uploaded_file.seek(0)
            
            # Convert PDF to images with better error handling
            try:
                # Try to convert PDF to images
                images = pdf2image.convert_from_bytes(uploaded_file.read())
            except Exception as pdf_error:
                st.error(f"PDF processing error: {str(pdf_error)}")
                st.info("""
                **Troubleshooting Steps:**
                1. Ensure the PDF file is not corrupted
                2. Try with a different PDF file
                3. Check if poppler-utils is properly installed
                4. For Streamlit Cloud, ensure packages.txt contains 'poppler-utils'
                """)
                return None
            
            if not images:
                st.warning("No pages found in the PDF. Please check if the PDF file is valid.")
                return None
                
            first_page = images[0]
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()
                }
            ]
            return pdf_parts
        except Exception as e:
            st.error(f"Unexpected error processing PDF: {str(e)}")
            st.info("Please try uploading a different PDF file or contact support if the issue persists.")
            return None
    else:
        raise FileNotFoundError("No file uploaded")

# Main App UI
st.markdown('<h1 style="text-align: center;">💼 IT Consulting Assistant</h1>', unsafe_allow_html=True)

# Introduction Card
create_card(
    "Welcome to IT Consulting Assistant",
    "This AI-powered system helps IT consultants analyze BRD, CRD, and technical documents with precision and efficiency. Upload your documents and get comprehensive insights, technology recommendations, project feasibility analysis, and stakeholder communication tools to accelerate your consulting projects."
)

st.markdown("---")

# How to Use Section
with st.expander("How to Use This System", expanded=True):
    st.markdown("""
    ### System Capabilities
    1. **BRD Analysis**: Upload Business Requirements Documents for comprehensive technology recommendations
    2. **CRD Analysis**: Upload Customer Requirements Documents for solution mapping and gap analysis
    3. **Technical Document Analysis**: Upload technical specifications, architecture documents, or system designs
    4. **Pre-Execution Questions**: Identify critical questions and gaps that need stakeholder clarification
    5. **Project Feasibility**: Assess technical feasibility, resource requirements, and timeline estimates
    6. **Architecture Recommendations**: Get technology stack and architecture recommendations
    7. **Implementation Roadmap**: Detailed project planning with risk assessment
    8. **Stakeholder Communication**: Generate professional emails for stakeholder updates
    
    ### Process Flow
    1. Upload your document (BRD, CRD, or Technical Document)
    2. Add any specific context or focus areas
    3. Choose the type of analysis you need:
       - **Document Analysis**: BRD, CRD, or Technical Document specific analysis
       - **Project Planning**: Feasibility, Architecture, Implementation Roadmap
       - **Stakeholder Communication**: Generate summary emails
    4. Review the AI-generated insights and recommendations
    5. Download or copy results for client presentations and project planning
    """)

# Create two columns for the inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("Document Upload")
    uploaded_file = st.file_uploader("Upload Document (PDF)...", type=["pdf"])
    if uploaded_file is not None:
        st.success("PDF Uploaded Successfully")
    else:
        st.info("Please upload a PDF document to begin analysis")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("Analysis Options")
    analysis_context = st.text_area(
        "Additional Context or Focus Areas (Optional)",
        placeholder="Example:\n- Specific types of information to look for\n- Particular sections to focus on\n- Types of analysis to prioritize\n- Any specific concerns or requirements\n- Technology preferences or constraints",
        help="This context will help guide the analysis of your document"
    )

st.markdown("---")

# Analysis Options Section
st.subheader("Choose Analysis Type")
st.markdown('<div class="analysis-options">', unsafe_allow_html=True)

# Create three columns for better button layout
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    submit1 = st.button("BRD Analysis", use_container_width=True)
    submit2 = st.button("CRD Analysis", use_container_width=True)

with btn_col2:
    submit3 = st.button("Technical Document Analysis", use_container_width=True)
    submit4 = st.button("Pre-Execution Questions", use_container_width=True)

with btn_col3:
    submit5 = st.button("Project Feasibility", use_container_width=True)
    submit6 = st.button("Architecture Recommendations", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Add new section for Implementation Roadmap
st.markdown("---")
st.subheader("Project Planning & Communication")
st.markdown('<div class="analysis-options">', unsafe_allow_html=True)

# Create a dedicated section for project planning
planning_col1, planning_col2 = st.columns(2)

with planning_col1:
    submit_roadmap = st.button("Implementation Roadmap", use_container_width=True, type="primary")

with planning_col2:
    submit_email = st.button("Generate Stakeholder Email", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Results Section
st.markdown("---")
st.subheader("Analysis Results")

# Email generation prompt
input_prompt_email = """
You are an IT Consulting Professional preparing a summary email for stakeholders about project understanding and next steps. Create a professional email that includes:

SUBJECT: IT Project Analysis Summary - [Document Type] Review

Dear [Stakeholder Name],

I hope this email finds you well. I have completed the initial analysis of the [Document Type] and would like to provide you with a comprehensive understanding of the project scope and our recommended next steps.

## Project Understanding Summary:
[Provide a 3-4 line summary of the project scope, objectives, and key deliverables based on the document analysis]

## Key Findings & Recommendations:
[Present the main technical findings, architecture recommendations, and strategic insights in bullet points]

## Critical Questions Requiring Your Input:
[Create a table with the following columns]
| Priority | Question/Clarification Needed | Impact | Recommended Action |
|----------|------------------------------|--------|-------------------|
[Fill with identified gaps and questions that need stakeholder clarification]

## Technical Feasibility Assessment:
- **Overall Feasibility:** [High/Medium/Low]
- **Key Technical Challenges:** [List main technical hurdles]
- **Resource Requirements:** [Skills, team size, timeline estimates]
- **Risk Factors:** [Technical and business risks identified]

## Recommended Implementation Approach:
[Outline the proposed methodology, technology stack, and implementation phases]

## Next Steps & Timeline:
[Provide a clear action plan with specific deliverables and timelines]

## Questions for Your Review:
1. [Specific question about requirements or constraints]
2. [Question about budget or timeline preferences]
3. [Question about stakeholder availability or decision-making process]

Please review the attached detailed analysis and provide your feedback on the above points, particularly regarding [mention 1-2 specific critical decisions needed].

I am available for a detailed discussion at your convenience to address any questions or concerns.

Best regards,
[Your Name]
IT Consulting Team

Note: Please find the detailed technical analysis and recommendations attached to this email.

Format this email professionally and ensure all critical information is clearly presented for stakeholder decision-making.
"""

# Analysis prompts
input_prompt1 = """
You are a Senior IT Consultant specializing in Business Requirements Document (BRD) analysis. Analyze this BRD document and provide comprehensive insights for IT consulting projects.

Please provide a detailed analysis in the following structure:

## 1. BRD Overview & Business Context
- Document type and business domain
- Primary business objectives and goals
- Key stakeholders and end users
- Current pain points or business challenges
- Expected business outcomes and success metrics

## 2. Business Process Analysis
- Identify all major business processes from the BRD
- Map current vs. desired state for each process
- Highlight automation and optimization opportunities
- Identify integration points between processes
- Document process dependencies and workflows

## 3. Functional Requirements Analysis
- Core functional requirements breakdown
- User stories and use cases identification
- Business rules and constraints
- Data requirements and flows
- Reporting and analytics needs

## 4. Non-Functional Requirements
- Performance requirements
- Security and compliance needs
- Scalability considerations
- Usability and accessibility requirements
- Integration requirements

## 5. Technology Implications
- Current technology landscape assessment
- Technology gaps and opportunities
- Recommended technology stack considerations
- Integration requirements with existing systems
- Data migration and conversion needs

## 6. Risk Assessment
- Technical risks and challenges
- Business risks and dependencies
- Resource and timeline risks
- Compliance and regulatory risks
- Mitigation strategies

## 7. Recommendations & Next Steps
- Priority implementation recommendations
- Phased approach suggestions
- Resource requirements estimation
- Timeline recommendations
- Success criteria and KPIs

Present your analysis in a structured format with clear sections, bullet points, and actionable recommendations for IT consulting projects.
"""

input_prompt2 = """
You are a Senior IT Consultant specializing in Customer Requirements Document (CRD) analysis. Analyze this CRD document and provide comprehensive solution mapping and gap analysis for IT consulting projects.

Please provide a detailed analysis in the following structure:

## 1. CRD Overview & Customer Context
- Document type and customer domain
- Primary customer objectives and pain points
- Key customer stakeholders and decision makers
- Current customer challenges and limitations
- Expected customer outcomes and value proposition

## 2. Customer Requirements Analysis
- Functional requirements breakdown
- Non-functional requirements assessment
- User experience requirements
- Integration requirements with customer systems
- Data and reporting requirements

## 3. Solution Mapping
- Current customer solution assessment
- Gap analysis between current and desired state
- Solution architecture recommendations
- Technology stack alignment with customer needs
- Integration strategy with existing customer systems

## 4. Customer Journey & User Experience
- End-user journey mapping
- User interface and experience requirements
- Accessibility and usability considerations
- Training and support requirements
- Change management considerations

## 5. Technical Feasibility Assessment
- Technical complexity evaluation
- Resource requirements estimation
- Timeline feasibility assessment
- Risk factors and mitigation strategies
- Scalability and performance considerations

## 6. Business Value Proposition
- ROI analysis and business case
- Cost-benefit analysis
- Competitive advantages
- Market positioning
- Success metrics and KPIs

## 7. Implementation Strategy
- Phased implementation approach
- Resource allocation recommendations
- Timeline and milestone planning
- Risk management strategies
- Quality assurance and testing approach

Present your analysis with clear recommendations for IT consulting projects, focusing on customer value and successful solution delivery.
"""

input_prompt3 = """
You are a Senior Technical Architect and IT Consultant specializing in technical document analysis. Analyze this technical document and provide comprehensive technical insights and recommendations.

Please provide a detailed analysis in the following structure:

## 1. Technical Document Overview
- Document type and technical domain
- Primary technical objectives
- Target audience and stakeholders
- Current technical challenges
- Expected technical outcomes

## 2. Technical Architecture Analysis
- Current architecture assessment
- Architecture patterns and design principles
- Technology stack evaluation
- Scalability and performance considerations
- Security and compliance requirements

## 3. System Design & Components
- System components and modules
- Data flow and integration points
- API design and specifications
- Database design and data modeling
- Infrastructure requirements

## 4. Technical Requirements Analysis
- Functional technical requirements
- Non-functional technical requirements
- Performance and scalability requirements
- Security and compliance requirements
- Integration and interoperability requirements

## 5. Technology Stack Recommendations
- Programming languages and frameworks
- Database and storage solutions
- Cloud platform recommendations
- DevOps and CI/CD tools
- Monitoring and logging solutions

## 6. Technical Risk Assessment
- Technical complexity risks
- Performance and scalability risks
- Security and compliance risks
- Integration and compatibility risks
- Resource and skill requirements

## 7. Implementation Recommendations
- Development methodology recommendations
- Technical implementation phases
- Resource and skill requirements
- Timeline and milestone planning
- Quality assurance and testing strategy

Present your analysis with technical depth and practical recommendations for IT consulting projects.
"""

input_prompt4 = """
You are a Senior IT Project Manager and Business Analyst specializing in pre-execution project analysis. Analyze this document and identify critical questions, gaps, and clarifications needed before project execution.

Please provide a comprehensive analysis in the following structure:

## 1. Project Scope Analysis
- Current scope understanding
- Scope gaps and ambiguities
- Missing requirements identification
- Scope creep risk assessment
- Scope validation questions

## 2. Stakeholder Analysis & Communication
- Key stakeholder identification
- Stakeholder expectations alignment
- Communication plan requirements
- Decision-making process clarification
- Stakeholder availability and commitment

## 3. Technical Questions & Clarifications
- Technical architecture decisions needed
- Technology stack selection criteria
- Integration requirements clarification
- Performance and scalability requirements
- Security and compliance requirements

## 4. Resource & Timeline Questions
- Team composition and skill requirements
- Resource availability and allocation
- Timeline feasibility and constraints
- Budget allocation and approval process
- External dependencies and vendors

## 5. Risk & Compliance Questions
- Technical risk mitigation strategies
- Business risk assessment
- Compliance and regulatory requirements
- Legal and contractual considerations
- Insurance and liability coverage

## 6. Success Criteria & KPIs
- Project success definition
- Key performance indicators
- Quality assurance criteria
- User acceptance criteria
- Go-live and deployment criteria

## 7. Critical Questions Matrix
Create a detailed table with the following columns:
| Priority | Category | Question/Clarification | Impact | Owner | Timeline |
|----------|----------|------------------------|--------|-------|----------|
[Fill with specific questions that need stakeholder input]

## 8. Recommended Next Steps
- Immediate actions required
- Stakeholder meetings needed
- Documentation requirements
- Approval processes
- Timeline for clarifications

Present your analysis with clear, actionable questions that will help ensure project success and stakeholder alignment.
"""

input_prompt5 = """
You are a Senior IT Project Manager and Technical Architect specializing in project feasibility analysis. Analyze this document and provide comprehensive feasibility assessment for IT consulting projects.

Please provide a detailed analysis in the following structure:

## 1. Technical Feasibility Assessment
- **Overall Technical Feasibility:** [High/Medium/Low]
- Technology maturity and availability
- Technical complexity evaluation
- Integration feasibility with existing systems
- Performance and scalability considerations
- Security and compliance requirements

## 2. Resource Feasibility Analysis
- **Team Requirements:**
  - Required skills and expertise
  - Team size and composition
  - Availability and allocation
  - Training and knowledge transfer needs
- **Infrastructure Requirements:**
  - Hardware and software needs
  - Cloud platform requirements
  - Development and testing environments
  - Production deployment requirements

## 3. Timeline Feasibility Assessment
- **Project Timeline Analysis:**
  - Estimated project duration
  - Critical path identification
  - Milestone planning
  - Dependencies and constraints
- **Risk Factors:**
  - Timeline risks and mitigation
  - Resource availability risks
  - Technical complexity risks
  - External dependency risks

## 4. Budget & Cost Feasibility
- **Cost Breakdown:**
  - Development costs
  - Infrastructure costs
  - Licensing and third-party costs
  - Maintenance and support costs
- **ROI Analysis:**
  - Expected benefits
  - Cost-benefit analysis
  - Payback period
  - Risk-adjusted returns

## 5. Business Feasibility
- **Business Case Validation:**
  - Alignment with business objectives
  - Stakeholder buy-in assessment
  - Market and competitive analysis
  - Regulatory and compliance requirements
- **Change Management:**
  - Organizational readiness
  - User adoption considerations
  - Training and support requirements
  - Resistance and mitigation strategies

## 6. Risk Assessment & Mitigation
- **Technical Risks:**
  - Technology risks and mitigation
  - Integration risks and strategies
  - Performance and scalability risks
  - Security and compliance risks
- **Business Risks:**
  - Market and competitive risks
  - Resource and timeline risks
  - Stakeholder and change management risks
  - Financial and budget risks

## 7. Feasibility Recommendations
- **Go/No-Go Decision Factors:**
  - Critical success factors
  - Deal-breaker conditions
  - Risk tolerance assessment
  - Alternative approaches
- **Implementation Strategy:**
  - Recommended approach
  - Phased implementation plan
  - Risk mitigation strategies
  - Success monitoring plan

Present your analysis with clear feasibility indicators, risk assessments, and actionable recommendations for project decision-making.
"""

input_prompt6 = """
You are a Senior Technical Architect and IT Consultant specializing in architecture and technology stack recommendations. Analyze this document and provide comprehensive architecture and technology recommendations.

Please provide a detailed analysis in the following structure:

## 1. Architecture Assessment & Recommendations
- **Current Architecture Analysis:**
  - Existing system architecture
  - Architecture patterns evaluation
  - Scalability and performance assessment
  - Integration complexity analysis
- **Recommended Architecture:**
  - Architecture pattern selection
  - Component design recommendations
  - Data flow and integration design
  - Security architecture considerations

## 2. Technology Stack Recommendations
- **Frontend Technologies:**
  - Framework recommendations (React, Angular, Vue, etc.)
  - UI/UX libraries and tools
  - Mobile and responsive considerations
  - Performance optimization tools
- **Backend Technologies:**
  - Programming languages (Java, Python, Node.js, etc.)
  - Framework recommendations
  - API design and management
  - Microservices considerations
- **Database & Storage:**
  - Database type recommendations (SQL, NoSQL, etc.)
  - Specific database technologies
  - Data modeling considerations
  - Backup and recovery strategies

## 3. Cloud & Infrastructure Recommendations
- **Cloud Platform:**
  - Platform recommendations (AWS, Azure, GCP)
  - Service selection and optimization
  - Cost optimization strategies
  - Multi-cloud considerations
- **Infrastructure as Code:**
  - IaC tools and practices
  - Containerization strategies
  - Orchestration platforms
  - Monitoring and logging solutions

## 4. Integration & API Strategy
- **Integration Architecture:**
  - API design patterns
  - Integration middleware recommendations
  - Data transformation and mapping
  - Real-time vs. batch processing
- **Third-Party Integrations:**
  - Recommended third-party services
  - API management and governance
  - Security and authentication
  - Rate limiting and throttling

## 5. Security & Compliance Architecture
- **Security Framework:**
  - Authentication and authorization
  - Data encryption and protection
  - Network security considerations
  - Compliance requirements (GDPR, HIPAA, etc.)
- **DevSecOps Integration:**
  - Security scanning and testing
  - Vulnerability management
  - Compliance monitoring
  - Incident response planning

## 6. Performance & Scalability Architecture
- **Performance Optimization:**
  - Caching strategies
  - Load balancing recommendations
  - Database optimization
  - CDN and content delivery
- **Scalability Planning:**
  - Horizontal vs. vertical scaling
  - Auto-scaling strategies
  - Performance monitoring
  - Capacity planning

## 7. Implementation Roadmap
- **Technology Adoption Strategy:**
  - Phased implementation approach
  - Technology migration planning
  - Risk mitigation strategies
  - Success criteria and KPIs
- **Resource Planning:**
  - Skill requirements and training
  - Team composition recommendations
  - Vendor and partner selection
  - Timeline and milestone planning

Present your analysis with specific technology recommendations, architecture diagrams where applicable, and implementation guidance for successful project delivery.
"""

input_prompt_roadmap = """
You are a Senior IT Project Manager and Technical Architect specializing in implementation roadmap development. Analyze this document and provide a comprehensive implementation roadmap with detailed project planning and risk assessment.

Please provide a detailed analysis in the following structure:

## 1. Project Overview & Scope
- **Project Summary:**
  - Project objectives and goals
  - Scope boundaries and deliverables
  - Key stakeholders and decision makers
  - Success criteria and KPIs
- **Business Case:**
  - ROI analysis and business value
  - Cost-benefit justification
  - Risk-adjusted returns
  - Strategic alignment

## 2. Implementation Strategy
- **Approach Selection:**
  - Waterfall vs. Agile vs. Hybrid approach
  - Phased implementation strategy
  - Parallel vs. sequential execution
  - Risk mitigation approach
- **Methodology:**
  - Development methodology (Scrum, Kanban, etc.)
  - Quality assurance approach
  - Testing strategy (Unit, Integration, UAT)
  - Deployment strategy

## 3. Detailed Implementation Roadmap

### Phase 1: Foundation & Setup (Weeks 1-4)
- **Activities:**
  - Project team formation and setup
  - Infrastructure and environment setup
  - Tool selection and configuration
  - Initial architecture design
- **Deliverables:**
  - Project charter and governance
  - Technical architecture document
  - Development environment setup
  - Team training and onboarding
- **Timeline:** 4 weeks
- **Resources:** [List required resources]
- **Risks:** [Identify risks and mitigation]

### Phase 2: Core Development (Weeks 5-16)
- **Activities:**
  - Core system development
  - Database design and implementation
  - API development and integration
  - User interface development
- **Deliverables:**
  - Core system modules
  - Database schema and data
  - API documentation
  - UI/UX components
- **Timeline:** 12 weeks
- **Resources:** [List required resources]
- **Risks:** [Identify risks and mitigation]

### Phase 3: Integration & Testing (Weeks 17-20)
- **Activities:**
  - System integration
  - Comprehensive testing
  - Performance optimization
  - Security testing
- **Deliverables:**
  - Integrated system
  - Test results and reports
  - Performance benchmarks
  - Security assessment
- **Timeline:** 4 weeks
- **Resources:** [List required resources]
- **Risks:** [Identify risks and mitigation]

### Phase 4: Deployment & Go-Live (Weeks 21-24)
- **Activities:**
  - Production deployment
  - User acceptance testing
  - Training and documentation
  - Go-live support
- **Deliverables:**
  - Production system
  - User training materials
  - System documentation
  - Support procedures
- **Timeline:** 4 weeks
- **Resources:** [List required resources]
- **Risks:** [Identify risks and mitigation]

## 4. Resource Planning & Allocation
- **Team Structure:**
  - Project Manager
  - Technical Lead/Architect
  - Developers (Frontend/Backend)
  - QA Engineers
  - DevOps Engineers
  - Business Analysts
- **Skill Requirements:**
  - Technical skills and expertise
  - Domain knowledge requirements
  - Training and certification needs
  - External consultant requirements
- **Resource Timeline:**
  - Resource allocation by phase
  - Ramp-up and ramp-down planning
  - Backup and contingency planning

## 5. Risk Assessment & Mitigation
- **Technical Risks:**
  - Technology complexity risks
  - Integration challenges
  - Performance and scalability issues
  - Security vulnerabilities
- **Project Risks:**
  - Timeline and scope risks
  - Resource availability risks
  - Stakeholder alignment risks
  - Budget and cost risks
- **Mitigation Strategies:**
  - Risk prevention measures
  - Contingency planning
  - Escalation procedures
  - Regular risk reviews

## 6. Quality Assurance & Testing
- **Testing Strategy:**
  - Unit testing approach
  - Integration testing plan
  - User acceptance testing
  - Performance testing
- **Quality Gates:**
  - Definition of Done criteria
  - Quality checkpoints
  - Review and approval processes
  - Go-live readiness criteria

## 7. Communication & Stakeholder Management
- **Communication Plan:**
  - Stakeholder communication matrix
  - Reporting frequency and format
  - Escalation procedures
  - Change management approach
- **Stakeholder Engagement:**
  - Key stakeholder identification
  - Engagement strategies
  - Decision-making processes
  - Conflict resolution procedures

## 8. Budget & Cost Management
- **Cost Breakdown:**
  - Development costs
  - Infrastructure costs
  - Licensing and third-party costs
  - Training and support costs
- **Budget Management:**
  - Cost tracking and monitoring
  - Change request procedures
  - Budget approval processes
  - Cost optimization strategies

## 9. Success Metrics & KPIs
- **Project Success Metrics:**
  - Timeline adherence
  - Budget compliance
  - Quality metrics
  - Stakeholder satisfaction
- **Business Success Metrics:**
  - ROI achievement
  - Business value delivery
  - User adoption rates
  - Performance improvements

## 10. Post-Implementation Support
- **Support Strategy:**
  - Warranty period support
  - Ongoing maintenance
  - Enhancement planning
  - Knowledge transfer
- **Continuous Improvement:**
  - Lessons learned documentation
  - Process improvements
  - Technology updates
  - Future roadmap planning

Present your roadmap with clear timelines, resource requirements, risk assessments, and actionable next steps for successful project execution.
"""

# Add the email generation logic after the existing button handlers
if submit_email:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content is not None:
            with st.spinner("Generating stakeholder email..."):
                response = get_gemini_response(analysis_context, pdf_content, input_prompt_email)
            st.subheader("Stakeholder Email Summary")
            st.markdown("---")
            st.markdown(response)
            
            # Add a copy button for the email
            st.markdown("---")
            st.markdown("##### Copy Email to Clipboard")
            if st.button("Copy Email"):
                st.code(response)
                st.success("Email content copied to clipboard!")
        else:
            st.error("Failed to process the PDF. Please try uploading a different file.")
    else:
        st.write("Please upload a document first")

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content is not None:
            with st.spinner("Analyzing BRD document..."):
                response = get_gemini_response(analysis_context, pdf_content, input_prompt1)
            st.subheader("BRD Analysis & Business Requirements")
            st.markdown("---")
            st.markdown(response)
        else:
            st.error("Failed to process the PDF. Please try uploading a different file.")
    else:
        st.write("Please upload a BRD document first")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content is not None:
            with st.spinner("Analyzing CRD document..."):
                response = get_gemini_response(analysis_context, pdf_content, input_prompt2)
            st.subheader("CRD Analysis & Solution Mapping")
            st.markdown("---")
            st.markdown(response)
        else:
            st.error("Failed to process the PDF. Please try uploading a different file.")
    else:
        st.write("Please upload a CRD document first")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content is not None:
            with st.spinner("Analyzing technical document..."):
                response = get_gemini_response(analysis_context, pdf_content, input_prompt3)
            st.subheader("Technical Document Analysis")
            st.markdown("---")
            st.markdown(response)
        else:
            st.error("Failed to process the PDF. Please try uploading a different file.")
    else:
        st.write("Please upload a technical document first")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content is not None:
            with st.spinner("Identifying pre-execution questions..."):
                response = get_gemini_response(analysis_context, pdf_content, input_prompt4)
            st.subheader("Pre-Execution Questions & Clarifications")
            st.markdown("---")
            st.markdown(response)
        else:
            st.error("Failed to process the PDF. Please try uploading a different file.")
    else:
        st.write("Please upload a document first")

elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content is not None:
            with st.spinner("Assessing project feasibility..."):
                response = get_gemini_response(analysis_context, pdf_content, input_prompt5)
            st.subheader("Project Feasibility Analysis")
            st.markdown("---")
            st.markdown(response)
        else:
            st.error("Failed to process the PDF. Please try uploading a different file.")
    else:
        st.write("Please upload a document first")

elif submit6:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content is not None:
            with st.spinner("Generating architecture recommendations..."):
                response = get_gemini_response(analysis_context, pdf_content, input_prompt6)
            st.subheader("Architecture & Technology Recommendations")
            st.markdown("---")
            st.markdown(response)
        else:
            st.error("Failed to process the PDF. Please try uploading a different file.")
    else:
        st.write("Please upload a document first")

elif submit_roadmap:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content is not None:
            with st.spinner("Creating implementation roadmap..."):
                response = get_gemini_response(analysis_context, pdf_content, input_prompt_roadmap)
            st.subheader("Implementation Roadmap & Project Planning")
            st.markdown("---")
            st.markdown(response)
            
            # Add download option for the roadmap
            st.markdown("---")
            st.markdown("##### Download Implementation Roadmap")
            if st.button("Download as Text"):
                st.download_button(
                    label="Download Implementation Roadmap",
                    data=response,
                    file_name="implementation_roadmap.txt",
                    mime="text/plain"
                )
        else:
            st.error("Failed to process the PDF. Please try uploading a different file.")
    else:
        st.write("Please upload a document first") 