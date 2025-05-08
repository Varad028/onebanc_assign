import streamlit as st
import re
from onebanc import check_mpin
from datetime import date, timedelta
import streamlit.components.v1 as components



def local_css(file_name):
    """Load local CSS file"""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    """Load remote CSS"""
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def animate_text():
    """Add JS animation for text fade-in"""
    components.html(
        """
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            const headers = document.querySelectorAll('h1, h2, h3, .st-emotion-cache-16idsys p');
            headers.forEach((header, index) => {
                header.style.opacity = "0";
                header.style.animation = `fadeIn 0.5s ease-in-out ${index * 0.2}s forwards`;
            });
        });
        </script>
        <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
        """,
        height=0,
    )

def set_custom_theme():
    """Set custom theme with CSS"""
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #E3620E;
            --primary-light: #E3620E;
            --primary-dark: #CC5500;
            --secondary-color: #FFFFFF;
            --text-color: #E3620E;
            --muted-text: #666666;
            --bg-color: #F8F8F8;
            --card-bg: #FFFFFF;
            --success-color: #4CAF50;
            --error-color: #F44336;
        }
        
        /* Body styles */
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Header and title styles */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-color);
            font-weight: 600;
        }
        
        /* Main title */
        .main-title {
            color: var(--primary-color);
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        /* Subtitle */
        .subtitle {
            color: var(--muted-text);
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        
        /* Card container */
        .card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            border-left: 4px solid var(--primary-color);
        }
        
        /* Form elements */
        .stTextInput > div > div > input, .stDateInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: #FFFFFF !important;
            color: var(--text-color) !important;
            border: 1px solid #E0E0E0 !important;
            border-radius: 6px !important;
        }
        
        .stTextInput > div > div > input:focus, .stDateInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(255, 107, 0, 0.2) !important;
        }
        
        /* Select box */
        .stSelectbox > div > div {
            background-color: #FFFFFF !important;
            color: var(--text-color) !important;
            border: 1px solid #E0E0E0 !important;
            border-radius: 6px !important;
        }
        
        /* Submit button */
        .stButton > button {
            background-color: var(--primary-color) !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.5rem 2rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background-color: var(--primary-light) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(255, 107, 0, 0.3) !important;
        }
        
        .stButton > button:active {
            background-color: var(--primary-dark) !important;
            transform: translateY(0) !important;
        }
        
        /* Divider */
        hr {
            border-color: #E0E0E0 !important;
            margin: 2rem 0 !important;
        }
        
        /* Success message */
        .success-message {
            background-color: rgba(76, 175, 80, 0.1);
            color: #4CAF50;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
            margin: 20px 0;
        }
        
        /* Error message */
        .error-message {
            background-color: rgba(244, 67, 54, 0.1);
            color: #F44336;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid #F44336;
            margin: 20px 0;
        }
        
        /* Warning message */
        .warning-message {
            background-color: rgba(255, 152, 0, 0.1);
            color: #FF9800;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid #FF9800;
            margin: 20px 0;
        }
        
        /* Info message */
        .info-message {
            background-color: rgba(33, 150, 243, 0.1);
            color: #2196F3;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid #2196F3;
            margin: 20px 0;
        }
        
        /* Section headers */
        .section-header {
            background-color: #F9F9F9;
            color: var(--primary-color);
            padding: 8px 16px;
            border-radius: 6px;
            margin: 20px 0 10px 0;
            font-weight: 600;
            border-left: 4px solid var(--primary-color);
        }
        
        /* Progress animation */
        @keyframes progressAnimation {
            0% { width: 0%; }
            100% { width: 100%; }
        }
        
        .progress-bar {
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
            margin-bottom: 20px;
            border-radius: 2px;
            animation: progressAnimation 2s ease-in-out;
        }
        
        /* Form labels */
        .stTextInput label, .stDateInput label, .stTextArea label, .stSelectbox label {
            color: var(--muted-text) !important;
            font-weight: 500 !important;
        }
        
        /* Logo container */
        .logo-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .logo-container img {
            max-height: 150px;
            margin-right: 15px;
        }
        
        /* Field container */
        .field-container {
            margin-bottom: 15px;
        }
        
        /* Guidelines list */
        .guidelines-list {
            background-color: var(--card-bg);
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
        }
        
        .guidelines-list ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .guidelines-list ul li {
            padding: 6px 0;
            padding-left: 24px;
            position: relative;
        }
        
        .guidelines-list ul li:before {
            content: "•";
            color: var(--primary-color);
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #E0E0E0;
            color: var(--muted-text);
            font-size: 0.8rem;
        }
        
        /* Animation for sections */
        .animated-section {
            animation: fadeInUp 0.5s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Error state for inputs */
        .error-border input, .error-border textarea {
            border-color: var(--error-color) !important;
        }
        
        /* Tooltip */
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: var(--secondary-color);
            color: var(--text-color);
            text-align: center;
            border-radius: 6px;
            padding: 8px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.8rem;
            border: 1px solid var(--primary-color);
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Set page config
    
    st.session_state.theme = "light"
    st.set_page_config(
        page_title="OneBanc - MPIN Setup",
        page_icon="onebanc_portrait_logo_png.png",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Apply custom theme
    set_custom_theme()
    
    # Add animation
    animate_text()
    
    # Bank header with logo
    st.markdown("""
    <div class="logo-container">
        <img src="https://static.onebanc.ai/logo/onebanc_text.webp" alt="OneBanc Logo">

    </div>
    <div class="progress-bar"></div>
    """, unsafe_allow_html=True)
    
    # Page title
    st.markdown('<h2 style="color: #FF6B00;">MPIN Setup</h2>', unsafe_allow_html=True)
    
    # Introduction card
    st.markdown("""
    <div class="card animated-section">
        <h3>Welcome to OneBanc MPIN Setup</h3>
        <p>Please complete the form below to set up your secure MPIN for mobile banking access. 
        All fields marked with * are required.</p>
    </div>
    """, unsafe_allow_html=True)

    # Marital status selection outside the form with custom styling
    st.markdown('<div class="section-header">Account Information</div>', unsafe_allow_html=True)
    marital_status = st.selectbox("Marital Status*", ["Single", "Married", "Other"])
    
    # Create styled form
    with st.form("bank_form"):
        st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
        
        # Personal Details in two columns
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name*", placeholder="John Doe")
            today = date.today()
            max_date = today - timedelta(days=18*365)  # Must be at least 18 years old
            min_date = today - timedelta(days=100*365)  # Assuming max age of 100 years
            
            dob_self = st.date_input(
                "Date of Birth*",
                min_value=min_date,
                max_value=max_date,
                value=max_date
            )
            phone = st.text_input("Mobile Number*", placeholder="10 digits")
            
        with col2:
            email = st.text_input("Email Address*", placeholder="john@example.com")
            address = st.text_area("Address*", placeholder="Enter your full address")

        # Show spouse/anniversary fields only if married
        if marital_status == "Married":
            st.markdown('<div class="section-header">Spouse Information</div>', unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            with col3:
                dob_spouse = st.date_input(
                    "Spouse's Date of Birth*",
                    min_value=min_date,
                    max_value=max_date,
                    value=max_date,
                    help="Spouse must be between 18 and 100 years old"
                )
            with col4:
                # Anniversary can't be before either person's birth
                min_anniversary = max(dob_self, dob_spouse)
                anniversary = st.date_input(
                    "Marriage Anniversary*",
                    min_value=min_anniversary,
                    max_value=today,
                    value=today,
                    help="Anniversary date must be after both birth dates"
                )
        else:
            dob_spouse = None
            anniversary = None

        # MPIN Section with improved styling
        st.markdown('<div class="section-header">Security Setup</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-message">
            <strong>MPIN Requirements:</strong> Must be 6 digits and follow security guidelines.
        </div>
        """, unsafe_allow_html=True)
        
        pin = st.text_input("Enter 6-digit MPIN*", type="password", max_chars=6)

        # Submit button with custom styling
        submitted = st.form_submit_button("Validate & Submit")

        if submitted:
            if not all([full_name, dob_self, phone, email, address]):
                st.markdown("""
                <div class="error-message">
                    <strong>Error:</strong> Please fill all required fields marked with *
                </div>
                """, unsafe_allow_html=True)
            elif not re.match(r"^\d{10}$", phone):
                st.markdown("""
                <div class="error-message">
                    <strong>Error:</strong> Please enter a valid 10-digit phone number
                </div>
                """, unsafe_allow_html=True)
            elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                st.markdown("""
                <div class="error-message">
                    <strong>Error:</strong> Please enter a valid email address
                </div>
                """, unsafe_allow_html=True)
            else:
                # Convert dates to YYYYMMDD format
                dob_self_str = dob_self.strftime("%Y%m%d")
                dob_spouse_str = dob_spouse.strftime("%Y%m%d") if dob_spouse else None
                anniversary_str = anniversary.strftime("%Y%m%d") if anniversary else None

                # Check MPIN
                violations = check_mpin(pin, dob_self_str, dob_spouse_str, anniversary_str)

                if not violations:
                    st.markdown("""
                    <div class="success-message animated-section">
                        <strong>✅ Success!</strong> MPIN validated successfully!
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    
                    # Show confirmation animation
                    st.markdown("""
                    <div style="text-align: center; margin: 30px 0;">
                        <svg width="100" height="100" viewBox="0 0 100 100">
                            <circle cx="50" cy="50" r="45" fill="none" stroke="#4CAF50" stroke-width="5">
                                <animate attributeName="stroke-dasharray" from="0 283" to="283 0" dur="1s" fill="freeze" />
                            </circle>
                            <path d="M25,50 L45,70 L75,30" fill="none" stroke="#4CAF50" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
                                <animate attributeName="stroke-dasharray" from="0 120" to="120 0" dur="1s" begin="0.5s" fill="freeze" />
                            </path>
                        </svg>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="error-message animated-section">
                        <strong>❌ Error:</strong> MPIN validation failed
                    </div>
                    <div class="warning-message">
                        <strong>Reason:</strong> {violations[0]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class="guidelines-list">
                        <strong>MPIN Guidelines:</strong>
                        <ul>
                            <li>Must be 6 digits</li>
                            <li>Should not contain repeated or sequential digits</li>
                            <li>Should not form patterns on keypad or keyboard</li>
                            <li>Should not relate to your personal information</li>
                            <li>Should not use only even or only odd digits</li>
                            <li>Should not be a palindrome or have simple repeating patterns</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <p>&copy; 2025 OneBanc. All rights reserved.</p>
        <p>For assistance, please contact our support team at support@onebanc.com</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()