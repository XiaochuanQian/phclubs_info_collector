import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import datetime
import os
import base64
from PIL import Image
import io
import uuid

# Email configuration from Streamlit secrets
def get_email_config():
    EMAIL_USER = st.secrets["EMAIL_USER"] if "EMAIL_USER" in st.secrets else None
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"] if "EMAIL_PASSWORD" in st.secrets else None
    RECIPIENT_EMAIL = st.secrets["RECIPIENT_EMAIL"] if "RECIPIENT_EMAIL" in st.secrets else "default_recipient@example.com"
    return EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL

SMTP_SERVER = "smtp.2925.com"
SMTP_PORT = 25

# Club categories
CLUB_CATEGORIES = [
    "Academic clubs",
    "Arts and creative clubs",
    "Community Service & Volunteering clubs",
    "Cultural & Diversity clubs",
    "Sport & fitness clubs",
    "Language clubs",
    "School Teams",
    "Test Catgory"
]

# Maximum file size (30 MB)
MAX_FILE_SIZE = 30 * 1024 * 1024  # 30 MB in bytes

# Example club data
EXAMPLE_CLUB = {
    "club_name": "Coding Club",
    "club_emoji": "💻",
    "club_category": "Academic clubs",
    "establishment_date": "September 15, 2022",
    "presidents": [
        {
            "chinese_name": "张明",
            "english_name": "Ming Zhang",
            "class": "G12.1",
            "email": "ming.zhang@example.com",
            "wechat": "mingz2022"
        }
    ],
    "vice_presidents": [
        {
            "chinese_name": "李华",
            "english_name": "Hua Li",
            "class": "G11.1",
            "email": "hua.li@example.com",
            "wechat": "huali_code"
        }
    ],
    "meeting_frequency": "Weekly",
    "meeting_day_time": "Wednesday P8",
    "meeting_location": "Computer Lab 2",
    "requirements": [
        "Basic programming knowledge is helpful but not required",
        "Interest in learning to code",
        "Commitment to attend regular meetings"
    ],
    "learning_objectives": [
        "Learn programming fundamentals in Python and JavaScript",
        "Build web applications and games",
        "Understand software development principles"
    ],
    "for_whom": [
        "Students interested in computer science and programming",
        "Those who want to pursue careers in technology",
        "Creative problem solvers who enjoy logical thinking"
    ],
    "past_activities": [
        "Developed a school event management app",
        "Participated in the regional coding competition",
        "Hosted a workshop on building personal websites"
    ],
    "benefits": [
        "Gain valuable programming skills relevant to many careers",
        "Build an impressive portfolio of coding projects",
        "Connect with like-minded peers and industry professionals"
    ]
}

def send_email(subject, body, image_data=None):
    """Send email with the collected information and optional image"""
    EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL = get_email_config()
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        
        # Attach plain text content
        msg.attach(MIMEText(body, 'plain'))
        
        # If there's an image, add it to the email
        if image_data:
            # Attach the image
            img = MIMEImage(image_data)
            img.add_header('Content-Disposition', 'attachment', filename='club_background.jpg')
            msg.attach(img)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def format_club_info(form_data):
    """Format the collected club information into plain text"""
    text = f"""
CLUB INFORMATION

Name: {form_data['club_name']} {form_data['club_emoji']}
Category: {form_data['club_category']}
Date of Establishment: {form_data['establishment_date']}

LEADERSHIP
"""
    
    # Add presidents
    for i, president in enumerate(form_data['presidents']):
        text += f"""
President {i+1}:
- Chinese Name: {president['chinese_name']}
- English Name: {president['english_name']}
- Class: {president['class']}
- Email: {president['email']}
- WeChat ID: {president['wechat']}
"""
    
    # Add vice-presidents
    for i, vp in enumerate(form_data['vice_presidents']):
        text += f"""
Vice-President {i+1}:
- Chinese Name: {vp['chinese_name']}
- English Name: {vp['english_name']}
- Class: {vp['class']}
- Email: {vp['email']}
- WeChat ID: {vp['wechat']}
"""
    
    # Meeting information
    text += f"""
MEETING SCHEDULE
- Frequency: {form_data['meeting_frequency']}
- Day and Time: {form_data['meeting_day_time']}
- Location: {form_data['meeting_location']}

REQUIREMENTS
"""
    
    for i, req in enumerate(form_data['requirements']):
        if req.strip():
            text += f"- {req}\n"
    
    text += f"""
LEARNING OBJECTIVES
"""
    
    for i, obj in enumerate(form_data['learning_objectives']):
        if obj.strip():
            text += f"- {obj}\n"
    
    text += f"""
FOR WHOM
"""
    
    for i, whom in enumerate(form_data['for_whom']):
        if whom.strip():
            text += f"- {whom}\n"
    
    text += f"""
EXAMPLES OF PAST ACTIVITIES/PROJECTS
"""
    
    for i, activity in enumerate(form_data['past_activities']):
        if activity.strip():
            text += f"- {activity}\n"
    
    text += f"""
BENEFITS OF JOINING
"""
    
    for i, benefit in enumerate(form_data['benefits']):
        if benefit.strip():
            text += f"{i+1}. {benefit}\n"
    
    return text

def format_update_info(club_identifier, update_data):
    """Format the update information for email body."""
    text = f"""
CLUB UPDATE REQUEST

Club Identifier: {club_identifier}

Updated Fields:
"""
    for key, value in update_data.items():
        if key == "background_image":
            text += f"- Background Image: [Attached if present]\n"
        elif key == "presidents":
            text += "- Presidents:\n"
            for i, president in enumerate(value):
                text += f"  President {i+1}:\n"
                for k, v in president.items():
                    text += f"    {k.replace('_', ' ').title()}: {v}\n"
        elif key == "vice_presidents":
            text += "- Vice-Presidents:\n"
            for i, vp in enumerate(value):
                text += f"  Vice-President {i+1}:\n"
                for k, v in vp.items():
                    text += f"    {k.replace('_', ' ').title()}: {v}\n"
        elif isinstance(value, list):
            text += f"- {key.replace('_', ' ').title()}:\n"
            for i, item in enumerate(value):
                text += f"    {i+1}. {item}\n"
        else:
            text += f"- {key.replace('_', ' ').title()}: {value}\n"
    return text

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
        # Initialize data lists
        st.session_state.requirements = [""]
        st.session_state.learning_objectives = [""]
        st.session_state.for_whom = [""]
        st.session_state.past_activities = [""]
        st.session_state.benefits = [""]
        
        # Initialize leadership counts
        st.session_state.num_presidents = 1
        st.session_state.num_vps = 1
        
        # Initialize example state
        st.session_state.show_example = False

def update_dynamic_list(key, count):
    """Update a dynamic list based on the new count"""
    current_len = len(st.session_state[key])
    
    if count > current_len:
        # Add new empty items
        st.session_state[key].extend([""] * (count - current_len))
    elif count < current_len:
        # Remove items
        st.session_state[key] = st.session_state[key][:count]

def render_dynamic_inputs(title, key_prefix, help_text=None):
    """Render text area inputs for a dynamic section"""
    data_key = key_prefix
    items = []
    
    for i in range(len(st.session_state[data_key])):
        item = st.text_area(
            f"{title} {i+1}", 
            value=st.session_state[data_key][i],
            key=f"{key_prefix}_{i}",
            help=help_text
        )
        # Update the value in session state
        st.session_state[data_key][i] = item
        items.append(item)
    
    return items

def load_example():
    """Load example data into the form"""
    # Update session state with example data
    st.session_state.num_presidents = len(EXAMPLE_CLUB["presidents"])
    st.session_state.num_vps = len(EXAMPLE_CLUB["vice_presidents"])
    
    # Update dynamic lists
    st.session_state.requirements = EXAMPLE_CLUB["requirements"]
    st.session_state.learning_objectives = EXAMPLE_CLUB["learning_objectives"]
    st.session_state.for_whom = EXAMPLE_CLUB["for_whom"]
    st.session_state.past_activities = EXAMPLE_CLUB["past_activities"]
    st.session_state.benefits = EXAMPLE_CLUB["benefits"]
    
    # Set example flag
    st.session_state.show_example = True

def clear_example():
    """Clear example data and return to empty form"""
    # Reset example flag
    st.session_state.show_example = False
    
    # Reset all fields
    st.session_state.num_presidents = 1
    st.session_state.num_vps = 1
    st.session_state.requirements = [""]
    st.session_state.learning_objectives = [""]
    st.session_state.for_whom = [""]
    st.session_state.past_activities = [""]
    st.session_state.benefits = [""]
    
    # Force rerun to update the UI immediately
    st.rerun()

def main():
    st.set_page_config(
        page_title="Club Information Collector", 
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Add page navigation state
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'

    # Navigation logic
    def go_to(page):
        st.session_state.page = page
        st.rerun()

    # Landing page
    if st.session_state.page == 'landing':
        st.title("Club Information Collector")
        st.markdown("Please choose an action:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Club", use_container_width=True):
                go_to('new_club')
        with col2:
            if st.button("Update Old Club", use_container_width=True):
                go_to('update_club')
        st.stop()

    # Update Old Club page
    if st.session_state.page == 'update_club':
        st.title("Update Old Club Information")
        st.markdown("""
        To update an existing club, please enter the club's name or unique identifier below.
        Select which sections you want to update. Only the selected sections will be included in the update.
        """)
        club_identifier = st.text_input("Club Name or Unique Identifier")
        st.divider()
        st.subheader("Select Sections to Update")
        update_sections = {
            "club_name": st.checkbox("Club Name"),
            "club_emoji": st.checkbox("Club Emoji"),
            "club_category": st.checkbox("Club Category"),
            "establishment_date": st.checkbox("Date of Establishment"),
            "presidents": st.checkbox("Presidents"),
            "vice_presidents": st.checkbox("Vice-Presidents"),
            "meeting_schedule": st.checkbox("Meeting Schedule"),
            "requirements": st.checkbox("Requirements"),
            "learning_objectives": st.checkbox("Learning Objectives"),
            "for_whom": st.checkbox("For Whom"),
            "past_activities": st.checkbox("Past Activities/Projects"),
            "benefits": st.checkbox("Benefits of Joining"),
            "background_image": st.checkbox("Background Picture")
        }
        st.divider()
        update_data = {}
        # Render input fields for checked sections
        if update_sections["club_name"]:
            update_data["club_name"] = st.text_input("New Club Name (leave blank to keep unchanged)")
        if update_sections["club_emoji"]:
            update_data["club_emoji"] = st.text_input("New Club Emoji (leave blank to keep unchanged)")
        if update_sections["club_category"]:
            update_data["club_category"] = st.selectbox("New Club Category", options=CLUB_CATEGORIES)
        if update_sections["establishment_date"]:
            update_data["establishment_date"] = st.date_input("New Date of Establishment", datetime.date.today(), format="YYYY-MM-DD")
        if update_sections["presidents"]:
            num_presidents = st.number_input("Number of Presidents to Update", min_value=1, max_value=5, value=1, key="update_num_presidents")
            presidents = []
            for i in range(num_presidents):
                st.markdown(f"#### President {i+1}")
                p_col1, p_col2 = st.columns(2)
                with p_col1:
                    p_chinese_name = st.text_input(f"Chinese Name (President {i+1})", key=f"update_president_cn_{i}")
                    p_english_name = st.text_input(f"English Name (President {i+1})", key=f"update_president_en_{i}")
                    p_class = st.text_input(f"Class [Grade/Class] (President {i+1})", key=f"update_president_class_{i}")
                with p_col2:
                    p_email = st.text_input(f"Email Address (President {i+1})", key=f"update_president_email_{i}")
                    p_wechat = st.text_input(f"WeChat ID (President {i+1})", key=f"update_president_wechat_{i}")
                presidents.append({
                    "chinese_name": p_chinese_name,
                    "english_name": p_english_name,
                    "class": p_class,
                    "email": p_email,
                    "wechat": p_wechat
                })
            update_data["presidents"] = presidents
        if update_sections["vice_presidents"]:
            num_vps = st.number_input("Number of Vice-Presidents to Update", min_value=1, max_value=5, value=1, key="update_num_vps")
            vice_presidents = []
            for i in range(num_vps):
                st.markdown(f"#### Vice-President {i+1}")
                vp_col1, vp_col2 = st.columns(2)
                with vp_col1:
                    vp_chinese_name = st.text_input(f"Chinese Name (VP {i+1})", key=f"update_vp_cn_{i}")
                    vp_english_name = st.text_input(f"English Name (VP {i+1})", key=f"update_vp_en_{i}")
                    vp_class = st.text_input(f"Class [Grade/Class] (VP {i+1})", key=f"update_vp_class_{i}")
                with vp_col2:
                    vp_email = st.text_input(f"Email Address (VP {i+1})", key=f"update_vp_email_{i}")
                    vp_wechat = st.text_input(f"WeChat ID (VP {i+1})", key=f"update_vp_wechat_{i}")
                vice_presidents.append({
                    "chinese_name": vp_chinese_name,
                    "english_name": vp_english_name,
                    "class": vp_class,
                    "email": vp_email,
                    "wechat": vp_wechat
                })
            update_data["vice_presidents"] = vice_presidents
        if update_sections["meeting_schedule"]:
            meeting_frequency = st.text_input("New Frequency of Meetings (leave blank to keep unchanged)")
            meeting_day_time = st.text_input("New Day and Time of Meetings (leave blank to keep unchanged)")
            meeting_location = st.text_input("New Location of Meetings (leave blank to keep unchanged)")
            update_data["meeting_frequency"] = meeting_frequency
            update_data["meeting_day_time"] = meeting_day_time
            update_data["meeting_location"] = meeting_location
        if update_sections["requirements"]:
            req_count = st.number_input("Number of Requirements to Update", min_value=1, max_value=10, value=1, key="update_req_count")
            requirements = []
            for i in range(req_count):
                requirements.append(st.text_area(f"Requirement {i+1}", key=f"update_req_{i}"))
            update_data["requirements"] = requirements
        if update_sections["learning_objectives"]:
            obj_count = st.number_input("Number of Learning Objectives to Update", min_value=1, max_value=10, value=1, key="update_obj_count")
            learning_objectives = []
            for i in range(obj_count):
                learning_objectives.append(st.text_area(f"Learning Objective {i+1}", key=f"update_obj_{i}"))
            update_data["learning_objectives"] = learning_objectives
        if update_sections["for_whom"]:
            whom_count = st.number_input("Number of For Whom Items to Update", min_value=1, max_value=5, value=1, key="update_whom_count")
            for_whom = []
            for i in range(whom_count):
                for_whom.append(st.text_area(f"For Whom {i+1}", key=f"update_whom_{i}"))
            update_data["for_whom"] = for_whom
        if update_sections["past_activities"]:
            act_count = st.number_input("Number of Past Activities to Update", min_value=1, max_value=10, value=1, key="update_act_count")
            past_activities = []
            for i in range(act_count):
                past_activities.append(st.text_area(f"Activity {i+1}", key=f"update_act_{i}"))
            update_data["past_activities"] = past_activities
        if update_sections["benefits"]:
            ben_count = st.number_input("Number of Benefits to Update", min_value=1, max_value=10, value=1, key="update_ben_count")
            benefits = []
            for i in range(ben_count):
                benefits.append(st.text_area(f"Benefit {i+1}", key=f"update_ben_{i}"))
            update_data["benefits"] = benefits
        if update_sections["background_image"]:
            st.info(f"Maximum file size: 30 MB")
            background_image = st.file_uploader("Upload a new background picture", type=["jpg", "jpeg", "png"], key="update_bg_img")
            update_data["background_image"] = background_image
        st.divider()
        col_submit, col_back = st.columns([2,1])
        with col_submit:
            if st.button("Submit Update", use_container_width=True):
                if not club_identifier.strip():
                    st.error("Please enter the club's name or unique identifier.")
                elif not any(update_sections.values()):
                    st.error("Please select at least one section to update.")
                else:
                    # Only collect non-empty fields
                    filtered_update = {k: v for k, v in update_data.items() if v}
                    email_body = format_update_info(club_identifier, filtered_update)
                    email_subject = f"Club Update Request: {club_identifier}"
                    # Handle background image
                    image_data = None
                    if filtered_update.get("background_image") is not None:
                        bg_file = filtered_update["background_image"]
                        if bg_file is not None:
                            image_data = bg_file.getvalue()
                    EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL = get_email_config()
                    if EMAIL_USER and EMAIL_PASSWORD:
                        with st.spinner("Sending update email..."):
                            success, message = send_email(email_subject, email_body, image_data)
                            if success:
                                st.success(f"Update submitted for club: {club_identifier}. Email sent!")
                            else:
                                st.error(message)
                    else:
                        st.warning("Email credentials not found. Please set EMAIL_USER and EMAIL_PASSWORD in Streamlit secrets.")
                        st.info("Preview of the update email content:")
                        st.code(email_body)
                        if image_data is not None:
                            st.info("Background image would be included in the email as an attachment.")
                    # For demo: show the JSON as well
                    st.json(filtered_update)
        with col_back:
            if st.button("Back", use_container_width=True, key="update_back_btn"):
                go_to('landing')
        st.stop()

    # New Club page (existing form logic)
    if st.session_state.page == 'new_club':
        # Sidebar controls - cannot be collapsed
        st.sidebar.title("Form Controls")
        
        # Example button in sidebar - correct logic
        if st.session_state.show_example:
            if st.sidebar.button("Clear Example", key="clear_example", use_container_width=True):
                clear_example()
            st.sidebar.warning("⚠️ Submit button is disabled in example mode. Clear example data to enable submission.")
        else:
            if st.sidebar.button("Load Example", key="load_example", use_container_width=True):
                load_example()
                st.success("Example data loaded! Scroll down to see the form filled with example data.")
                st.rerun()  # Force a rerun to update the UI immediately after loading example
        
        # Leadership controls in sidebar
        with st.sidebar.expander("Leadership", expanded=True):
            num_presidents = st.number_input(
                "Number of Presidents", 
                min_value=1, 
                max_value=5, 
                value=st.session_state.num_presidents,
                key="sidebar_num_presidents"
            )
            st.session_state.num_presidents = num_presidents
            
            num_vps = st.number_input(
                "Number of Vice-Presidents", 
                min_value=0, 
                max_value=5, 
                value=st.session_state.num_vps,
                key="sidebar_num_vps"
            )
            st.session_state.num_vps = num_vps
        
        # Dynamic sections management in sidebar
        with st.sidebar.expander("Requirements", expanded=True):
            req_count = st.number_input(
                "Number of Requirements", 
                min_value=1, 
                max_value=10, 
                value=len(st.session_state.requirements),
                key="req_count"
            )
            update_dynamic_list("requirements", req_count)
        
        with st.sidebar.expander("Learning Objectives", expanded=True):
            obj_count = st.number_input(
                "Number of Learning Objectives", 
                min_value=1, 
                max_value=10, 
                value=len(st.session_state.learning_objectives),
                key="obj_count"
            )
            update_dynamic_list("learning_objectives", obj_count)
        
        with st.sidebar.expander("For Whom", expanded=True):
            whom_count = st.number_input(
                "Number of For Whom Items", 
                min_value=1, 
                max_value=5, 
                value=len(st.session_state.for_whom),
                key="whom_count"
            )
            update_dynamic_list("for_whom", whom_count)
        
        with st.sidebar.expander("Past Activities", expanded=True):
            act_count = st.number_input(
                "Number of Past Activities", 
                min_value=1, 
                max_value=10, 
                value=len(st.session_state.past_activities),
                key="act_count"
            )
            update_dynamic_list("past_activities", act_count)
        
        with st.sidebar.expander("Benefits", expanded=True):
            ben_count = st.number_input(
                "Number of Benefits", 
                min_value=1, 
                max_value=10, 
                value=len(st.session_state.benefits),
                key="ben_count"
            )
            update_dynamic_list("benefits", ben_count)
        
        # Main content area
        st.title("Club Information Collector")
        st.markdown("Fill in the form below to submit information about your club.")
        st.info("Use the sidebar to control the number of fields for each section")
        
        # Example data preview
        if st.session_state.show_example:
            with st.expander("Example Data Preview", expanded=True):
                st.markdown(f"### {EXAMPLE_CLUB['club_name']} {EXAMPLE_CLUB['club_emoji']}")
                st.markdown(f"**Category:** {EXAMPLE_CLUB['club_category']}")
                st.markdown(f"**Established:** {EXAMPLE_CLUB['establishment_date']}")
                st.markdown("This is an example of a completed club form. The form below has been pre-filled with this example data.")
                st.warning("⚠️ You are in example mode. The submit button is disabled. To submit your own club information, click 'Clear Example' in the sidebar first.")
        
        # Main form
        with st.form("club_info_form"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                club_name = st.text_input("Club Name", value=EXAMPLE_CLUB["club_name"] if st.session_state.show_example else "")
            
            with col2:
                club_emoji = st.text_input("Club Emoji", value=EXAMPLE_CLUB["club_emoji"] if st.session_state.show_example else "")
            
            club_category = st.selectbox(
                "Club Category", 
                options=CLUB_CATEGORIES,
                index=CLUB_CATEGORIES.index(EXAMPLE_CLUB["club_category"]) if st.session_state.show_example else 0
            )
            
            # Date selector for establishment date
            default_date = datetime.date.today()
            if st.session_state.show_example:
                try:
                    # Try to parse the example date
                    default_date = datetime.datetime.strptime(EXAMPLE_CLUB["establishment_date"], "%B %d, %Y").date()
                except:
                    pass
                    
            establishment_date = st.date_input(
                "Date of Establishment",
                default_date,
                format="YYYY-MM-DD"
            )
            
            st.subheader("Leadership")
            
            # Presidents - using count from sidebar
            presidents = []
            for i in range(st.session_state.num_presidents):
                st.markdown(f"#### President {i+1}")
                p_col1, p_col2 = st.columns(2)
                
                # Get example data if available
                example_president = {}
                if st.session_state.show_example and i < len(EXAMPLE_CLUB["presidents"]):
                    example_president = EXAMPLE_CLUB["presidents"][i]
                
                with p_col1:
                    p_chinese_name = st.text_input(
                        f"Chinese Name (President {i+1})",
                        value=example_president.get("chinese_name", "") if st.session_state.show_example else ""
                    )
                    p_english_name = st.text_input(
                        f"English Name (President {i+1})",
                        value=example_president.get("english_name", "") if st.session_state.show_example else ""
                    )
                    p_class = st.text_input(
                        f"Class [Grade/Class] (President {i+1})",
                        value=example_president.get("class", "") if st.session_state.show_example else ""
                    )
                
                with p_col2:
                    p_email = st.text_input(
                        f"Email Address (President {i+1})",
                        value=example_president.get("email", "") if st.session_state.show_example else ""
                    )
                    p_wechat = st.text_input(
                        f"WeChat ID (President {i+1})",
                        value=example_president.get("wechat", "") if st.session_state.show_example else ""
                    )
                
                presidents.append({
                    "chinese_name": p_chinese_name,
                    "english_name": p_english_name,
                    "class": p_class,
                    "email": p_email,
                    "wechat": p_wechat
                })
            
            # Vice Presidents - using count from sidebar
            vice_presidents = []
            for i in range(st.session_state.num_vps):
                st.markdown(f"#### Vice-President {i+1}")
                vp_col1, vp_col2 = st.columns(2)
                
                # Get example data if available
                example_vp = {}
                if st.session_state.show_example and i < len(EXAMPLE_CLUB["vice_presidents"]):
                    example_vp = EXAMPLE_CLUB["vice_presidents"][i]
                
                with vp_col1:
                    vp_chinese_name = st.text_input(
                        f"Chinese Name (VP {i+1})",
                        value=example_vp.get("chinese_name", "") if st.session_state.show_example else ""
                    )
                    vp_english_name = st.text_input(
                        f"English Name (VP {i+1})",
                        value=example_vp.get("english_name", "") if st.session_state.show_example else ""
                    )
                    vp_class = st.text_input(
                        f"Class [Grade/Class] (VP {i+1})",
                        value=example_vp.get("class", "") if st.session_state.show_example else ""
                    )
                
                with vp_col2:
                    vp_email = st.text_input(
                        f"Email Address (VP {i+1})",
                        value=example_vp.get("email", "") if st.session_state.show_example else ""
                    )
                    vp_wechat = st.text_input(
                        f"WeChat ID (VP {i+1})",
                        value=example_vp.get("wechat", "") if st.session_state.show_example else ""
                    )
                
                vice_presidents.append({
                    "chinese_name": vp_chinese_name,
                    "english_name": vp_english_name,
                    "class": vp_class,
                    "email": vp_email,
                    "wechat": vp_wechat
                })
            
            st.subheader("Meeting Schedule")
            meeting_frequency = st.text_input(
                "Frequency of Meetings (e.g. Weekly, Bi-weekly, Monthly)",
                value=EXAMPLE_CLUB["meeting_frequency"] if st.session_state.show_example else ""
            )
            meeting_day_time = st.text_input(
                "Day and Time of Meetings (e.g. Tuesday P10)",
                value=EXAMPLE_CLUB["meeting_day_time"] if st.session_state.show_example else ""
            )
            meeting_location = st.text_input(
                "Location of Meetings (e.g. Room 213)",
                value=EXAMPLE_CLUB["meeting_location"] if st.session_state.show_example else ""
            )
            
            # Dynamic sections rendering (inside the form)
            st.subheader("Requirements")
            requirements = render_dynamic_inputs(
                "Requirement", 
                "requirements", 
                help_text="e.g. No prerequisite / all students can join / Students with a GPA of > 3.8"
            )
            
            st.subheader("Learning Objectives")
            learning_objectives = render_dynamic_inputs(
                "Learning Objective", 
                "learning_objectives", 
                help_text="e.g. Learn about image processing"
            )
            
            st.subheader("For Whom")
            for_whom = render_dynamic_inputs(
                "For Whom", 
                "for_whom", 
                help_text="Ideal for students who: (e.g. love math, are passionate about art, enjoy outdoor activities, etc.)"
            )
            
            st.subheader("Examples of Past Activities/Projects")
            past_activities = render_dynamic_inputs(
                "Activity", 
                "past_activities", 
                help_text="Please write in full sentences."
            )
            
            st.subheader("Benefits of Joining")
            benefits = render_dynamic_inputs(
                "Benefit", 
                "benefits", 
                help_text="Please write in full sentences."
            )
            
            st.subheader("Background Picture")
            st.info(f"Maximum file size: 30 MB")
            background_image = st.file_uploader("Upload a background picture", type=["jpg", "jpeg", "png"])
            
            # Submit button - disabled in example mode
            if st.session_state.show_example:
                st.warning("⚠️ You are in example mode. Please click 'Clear Example' in the sidebar to enable submission.")
                submitted = st.form_submit_button("Submit", disabled=True)
                submitted = False  # Ensure it's always False in example mode
            else:
                submitted = st.form_submit_button("Submit")
            
            if submitted:
                if not club_name:
                    st.error("Club Name is required.")
                elif background_image is not None and background_image.size > MAX_FILE_SIZE:
                    st.error(f"File size exceeds the maximum limit of 30 MB. Please upload a smaller file.")
                else:
                    # Format the establishment date as a string
                    establishment_date_str = establishment_date.strftime("%B %d, %Y")
                    
                    # Collect all form data
                    form_data = {
                        "club_name": club_name,
                        "club_emoji": club_emoji,
                        "club_category": club_category,
                        "establishment_date": establishment_date_str,
                        "presidents": presidents,
                        "vice_presidents": vice_presidents,
                        "meeting_frequency": meeting_frequency,
                        "meeting_day_time": meeting_day_time,
                        "meeting_location": meeting_location,
                        "requirements": requirements,
                        "learning_objectives": learning_objectives,
                        "for_whom": for_whom,
                        "past_activities": past_activities,
                        "benefits": benefits
                    }
                    
                    # Format the email content
                    email_body = format_club_info(form_data)
                    email_subject = f"New Club Information: {club_name}"
                    
                    # Process background image if uploaded
                    image_data = None
                    if background_image is not None:
                        image_bytes = background_image.getvalue()
                        image_data = image_bytes
                        
                        # Display the image in the app
                        st.image(image_bytes, caption="Uploaded Background Image", use_column_width=True)
                    
                    EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL = get_email_config()
                    if EMAIL_USER and EMAIL_PASSWORD:
                        with st.spinner("Sending email..."):
                            success, message = send_email(email_subject, email_body, image_data)
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
                    else:
                        st.warning("Email credentials not found. Please set EMAIL_USER and EMAIL_PASSWORD in Streamlit secrets.")
                        st.info("Preview of the email content:")
                        st.code(email_body)
                        
                        if background_image is not None:
                            st.info("Background image would be included in the email as an attachment.")
            # Add a Back button
            if st.form_submit_button("Back", use_container_width=True):
                go_to('landing')

if __name__ == "__main__":
    main()
