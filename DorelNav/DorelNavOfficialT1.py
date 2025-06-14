import streamlit as st
import streamlit.components.v1 as components
import os

# Page configuration and theming
st.set_page_config(
    page_title="Forest Navigation Game",
    page_icon="🌲",
    layout="wide",
)

# Custom CSS for forest theme and center alignment
st.markdown(
    """
    <style>
    .stApp { background-color: #e8f5e9; }
    .stApp .block-container { display: flex; flex-direction: column; align-items: center; }
    iframe, img { margin: auto; }
    h1, h2, h3, .stButton > button { color: #2e7d32; }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
        border: 2px solid #a5d6a7;
        border-radius: 5px;
    }
    .stButton > button {
        background-color: #66bb6a;
        border-radius: 10px;
        padding: 0.5em 1em;
        margin: auto;
    }
    """,
    unsafe_allow_html=True
)

team_riddles = {
    'Team1': {
    543: { # Mizpe Modiin - > HaPagoda
        "description": "**Location 1:** Solve this riddle to find the first clue in the heart of Ben-Shemen forest...",  # longer description
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'49.0%22N+34%C2%B057'24.6%22E",
        "images": ["dorelNavPhoto/514_1.jpeg", "dorelNavPhoto/514_2.jpeg", "dorelNavPhoto/514_3.jpeg"]  # add up to 3 image URLs or file paths here
    },
    514: { # HaPagoda -> Random location 1
        "description": "**Location 2:** A second challenge awaits you among the pine trees...",
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'46.2%22N+34%C2%B057'34.6%22E",
        "images": ["dorelNavPhoto/559_1.jpeg", "dorelNavPhoto/559_2.jpeg"]
    },
    559: { # Random location 1 -> The partisans
        "description": "**Location 3:** The third puzzle is hidden near the old grove...",
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'48.1%22N+34%C2%B057'20.6%22E",
        "images": ["dorelNavPhoto/531_1.jpeg"]
    },
    531: { # The partisans
        "description": "**Location 4:** Almost there—figure this out to proceed to the clearing...",
        "answer": "5",
        "link": None,
        "images": []
    }
},
'Team2':{
    543: { # Mizpe Modiin -> Random location 2
        "description": "**Location 1:** Solve this riddle to find the first clue in the heart of Ben-Shemen forest...",  # longer description
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'52.4%22N+34%C2%B057'33.0%22E",
        "images": ["dorelNavPhoto/572_1.jpeg", "dorelNavPhoto/572_2.jpeg"]  # add up to 3 image URLs or file paths here
    },
    572: { # Random location 2 -> Mahzeba
        "description": "**Location 2:** A second challenge awaits you among the pine trees...",
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'41.1%22N+34%C2%B057'34.7%22E",
        "images": ["dorelNavPhoto/528_1.jpeg", "dorelNavPhoto/528_2.jpeg"]
    },
    528: { # Mahzeba -> HaPagoda
        "description": "**Location 3:** The third puzzle is hidden near the old grove...",
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'49.0%22N+34%C2%B057'24.6%22E",
        "images": ["dorelNavPhoto/514_1.jpeg", "dorelNavPhoto/514_2.jpeg", "dorelNavPhoto/514_3.jpeg"]
    },
    514: { # HaPagoda
        "description": "**Location 4:** Almost there—figure this out to proceed to the clearing...",
        "answer": "5",
        "link": None,
        "images": []
    }
},
'Team3': {
    543: { # Mizpe Modiin -> Box Tombs
        "description": "**Location 1:** Solve this riddle to find the first clue in the heart of Ben-Shemen forest...",  # longer description
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'45.2%22N+34%C2%B057'11.4%22E",
        "images": ["dorelNavPhoto/586_1.jpeg", "dorelNavPhoto/586_2.jpeg"]  # add up to 3 image URLs or file paths here
    },
    586: { # Box Tombs -> Singel Herzel
        "description": "**Location 2:** A second challenge awaits you among the pine trees...",
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'42.8%22N+34%C2%B057'28.3%22E",
        "images": ["dorelNavPhoto/597_1.jpeg"]
    },
    597: { # Singel Herzel -> HaPagoda
        "description": "**Location 3:** The third puzzle is hidden near the old grove...",
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'49.0%22N+34%C2%B057'24.6%22E",
        "images": ["dorelNavPhoto/514_1.jpeg", "dorelNavPhoto/514_2.jpeg", "dorelNavPhoto/514_3.jpeg"]
    },
    514: { # HaPagoda
        "description": "**Location 4:** Almost there—figure this out to proceed to the clearing...",
        "answer": "5",
        "link": None,
        "images": []
    }
}}

gathering_link = "https://www.google.com/maps/place/31%C2%B057'01.4%22N+34%C2%B057'20.0%22E"
gathering_riddle_num = 560

# Reset to home
def go_home():
    st.session_state['stage'] = 'select'

def get_google_maps_link(ggl_link):
    latlon = ggl_link.split("/")[-1]
    embed_url = f"https://maps.google.com/maps?q={latlon}&output=embed"
    return embed_url

# Main app logic
def main(team='Team1', alt_riddles=None):
    global riddles
    if alt_riddles:
        riddles = alt_riddles
    # Initialize session state
    if 'stage' not in st.session_state:
        st.session_state['stage'] = 'select'
    if 'last_riddle' not in st.session_state:
        st.session_state['last_riddle'] = None
    if 'last_location' not in st.session_state:
        st.session_state['last_location'] = None

    # Home / selection page
    if st.session_state['stage'] == 'select':
        st.title(f"Welcome {team} to the Forest Navigation Game! 🌲")
        st.title("🔍 Enter Riddle Number")

        # Show next point if solved
        if st.session_state['last_location']:
            rid = st.session_state['last_riddle']
            st.markdown("---")
            st.subheader("🏁 Next Point to Navigate:")
            st.markdown(f"[Open in Google Maps]({st.session_state['last_location']})")
            components.iframe(get_google_maps_link(st.session_state['last_location']), height=300, scrolling=False)
            imgs = riddles[rid]['images']
            if imgs:
                st.image(imgs, width=200) #, caption=[f"Point {rid} photo {i+1}" for i in range(len(imgs))])
            st.info("Go to the next location and look for the envelop containing the next riddle")
            st.markdown("---")

        # Use a form so text_input updates on submit
        with st.form(key='riddle_form'):
            r_num_str = st.text_input("Riddle Number", key='riddle_input')
            submitted = st.form_submit_button("Go")
        if submitted:
            try:
                r_num = int(r_num_str)
            except ValueError:
                st.error("Please enter a valid riddle number.")
            else:
                if r_num in riddles:
                    st.session_state['current_riddle'] = r_num
                    st.session_state['stage'] = 'answer'
                    st.rerun()
                else:
                    st.error("Riddle number does not exist. Please try again.")

    # Answer page
    else:
        rid = st.session_state['current_riddle']
        solved_key = f"solved_{rid}"
        if solved_key not in st.session_state:
            st.session_state[solved_key] = False

        st.header(f"Riddle {rid}")
        if st.button("🏠 Home"):
            go_home();
            st.rerun()

        st.text_area("Description", value=riddles[rid]['description'], height=200, disabled=True)

        if st.session_state[solved_key]:
            # Completed game or next link
            if riddles[rid]['link'] is None:
                st.balloons(); st.success("🎉 Congratulations! You've completed the game.")
                st.markdown(f"**Gathering Point:** [Open in Google Maps]({gathering_link})")
                components.iframe(get_google_maps_link(gathering_link), height=300, scrolling=False)
            else:
                nxt = riddles[rid]['link']
                st.success("✅ Correct!")
                st.markdown(f"**Next Point:** [Open in Google Maps]({nxt})")

                components.iframe(get_google_maps_link(nxt), height=300, scrolling=False)
                imgs = riddles[rid]['images']
                if imgs:
                    st.image(imgs, width=200) #, caption=[f"Point {rid} photo {i+1}" for i in range(len(imgs))])
                st.info("Go to the next location and look for the envelop containing the next riddle")
        else:
            user_ans = st.text_input("Your Answer", key='answer_input')
            if st.button("Submit"):
                if user_ans.strip().lower() == riddles[rid]['answer']:
                    st.session_state[solved_key] = True
                    nxt = riddles[rid]['link'] or gathering_link
                    st.session_state['last_riddle'], st.session_state['last_location'] = rid, nxt
                    st.success("✅ Correct!")
                    if riddles[rid]['link'] is None:
                        st.balloons(); st.success("🎉 Congratulations! You've completed the game.")
                        st.markdown(f"**Gathering Point:** [Open in Google Maps]({gathering_link})")
                        components.iframe(get_google_maps_link(gathering_link), height=300, scrolling=False)
                    else:
                        st.markdown(f"**Next Point:** [Open in Google Maps]({nxt})")
                        components.iframe(get_google_maps_link(nxt), height=300, scrolling=False)
                        imgs = riddles[rid]['images']
                        if imgs:
                            st.image(imgs, width=200) # , caption=[f"Point {rid} photo {i+1}" for i in range(len(imgs))])
                        st.info("Go to the next location and look for the envelop containing the next riddle")
                else:
                    st.error("❌ Wrong answer. Please try again.")

if __name__ == "__main__":
    selected_team = os.environ.get('SELECTED_TEAM', 'Team1')
    if selected_team not in team_riddles:
        selected_team = 'Team1'
    main(team=selected_team, alt_riddles=team_riddles.get(selected_team))
