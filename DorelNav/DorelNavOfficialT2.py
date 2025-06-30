import streamlit as st
import streamlit.components.v1 as components
import os
from twilio.rest import Client

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

# in your <style> block (once at the top):
st.markdown("""
<style>
.description-box {
    direction: rtl;
    text-align: right;
    max-width: 600px;
    margin: 1.5em auto;
    background: #fff;
    border: 1px solid #a5d6a7;
    border-radius: 8px;
    padding: 1.2em 1.5em;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 18px;
    line-height: 1.6;
    text-align: justify;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

descriptions = {
    543: """
    מצפה מודיעין, הניצב על גבעה נקדמת בלב יער בן שמן, מציע תצפית פנורמית על מישור יהודה והרי ירושלים.
     נקודת התצפית משמשת זה דורות אתר מנוחה לדרך המלך העתיקה שחיברה בין שפלת החוף למרכז הארץ. 
     במאה ה־19 ביקר כאן חוקר הנופים אלברט בואן, שתיאר את נוף ההרים והגבעות סביב כ“ימין גן העדן העתיק”. 
     היום, המטיילים עוצרים במקום כדי לחוש את רוח ההיסטוריה, לתצפת על שקיעות צבעוניות וליהנות מקפה חם לצד מצפור העץ הפשוט.
    """,
    514: """
    בלב יער בן שמן, סמוך למצפה מודיעין, ניצבת הפגודה התאילנדית – ביתן מסורתי עשוי עץ ושיש בגווני זהב, אדום ולבן, המעוטר בסמלים מקודשים של התרבות התאילנדית.
     המבנה נתרם במתנה לעם ישראל על ידי העם התאילנדי לציון 50 שנות עצמאות מדינת ישראל ו-50 שנות מלכותו של המלך בומיבל אדוליידי, ומהווה סמל לידידות בין שני העמים.
      הפגודה מוקפת גדר ומונגשת לצפייה מחוץ לה, ומשקיפה על גבעות היער הצפוניות, יוצרת שילוב קסום של אדריכלות מזרחית ואווירת טבע פסטורלית.
    """,
    559: """
    יער בן־שמן הוא אחד הפרויקטים הראשונים של קק״ל בארץ: כבר ב-1905 החלו חלוצי העלייה השנייה לשתול עצי חרוב, אלון וארז בעזרת מועקות ופרדות. 
    העבודה התבצעה בעזרת מזחלות עץ ושטח בלתי סלול, כדי להיאבק בסחף ולייצב את הקרקע. 
    במשך עשרות שנים ניטעו בעצי היער מאות אלפי עצים, והפכו את השטח המדברי שאפיין פעם את שפלת יהודה לחורש ירוק ומוצל.
    """,
    531: """
    בתחילת מלחמת העצמאות באביב 1948 הפך יער בן שמן למבצע פלמ״ח מסתורי: לוחמים הסתתרו בסבך, ערכו מארבים לשיירות על כביש ירושלים, ושחררו נתיבי אספקה קריטיים. 
    ב־12 באפריל, במסגרת מבצע נחשון, חוליית יפת״ח פוצצה מחסום ערביי סמוך וליוותה מעבר מטעני תרופות למוססים בעיר המצור. 
    קרבות הקצרים אך העזים זיכו ללוחמים את הכינוי “פרטיזני השפלה” והדגימו את חשיבות היער בלוחמת גרילה על רקע מצבו המסוכן של היישוב.
    """,
    572: """
    בין שבילי היער חובקים חובבי הציפורים: יותר מ-170 מיני עופות נצפים כאן במהלך השנה, בהם עיטים, שלדגים נדירים וציפורי חורף נודדות. 
    כל עונה מביאה איתה תצפיות חדשות – מפרפרי כחול־זנב בחורף ועד נקרי סלע בסתיו. 
    היער מהווה מוקד צפרות ותצפית, עם ציוד תצפית מוקצים במספר תחנות לאורך השבילים.
    """,
    528: """
    בתל חדיד, בגובה 147 מ', שוכנים שרידי מחצבות עתיקות חצובות בגיר, ששימשו לדורות לבניית מבני היישובים הסמוכים. 
    לצד המחצבות מצויים בורות מים, מערות, גת לדריכת ענבים ובתי בד עתיקים. 
    חפירות משנת 1955 חשפו ריצפת פסיפס מהמאה השישית ובה תיאור ספינה על הנילוס והכתובת “איגיפטוס”, שהוצאה לאור ומוצגת כיום במוזיאון הימי בחיפה. 
    המקום מעיד על עושרה ההיסטורי והכלכלי של האזור ומעניק הצצה לחיי היום־יום ולמסחר העתיקים ביער בן שמן.
    """,
    586: """
    על מצלע גבעה בשפלת יער בן שמן, מתחבאים “קברי ארגז” – תשעה קברים מלבניים חצובים בסלע, עם אבני גולל רחבות שהשמשו לסגירתם. 
    עוד במאה ה־19 זוהו כמקום קבורתם של החשמונאים, על סמך שמם הערבי “קובור אל־יהוד”, ומצבת אבן גדולה הוקמה לכבודם. 
    חפירות ובדיקות ארכיאולוגיות חשפו סמוך אליהם שרידי כנסייה ביזנטית ומקווה רומאי, אך עתה יודעים שהקברים עצמם שייכים לתקופה הרומית. 
    האתר משלב מסתורין ומגע היסטוריה עמוק באזור פסטורלי. 
    """,
    597: """
    סינגל הרצל, המכונה “הכחול”, הוא מסלול רכיבה מעגלי בן כ-10.5 ק"מ ביער בן שמן שהוסדר על ידי קק"ל וקבוצות מתנדבים כחלק ממערכת שבילי היער. 
    המסלול מציע טיפוס מתון של כ-250 מ' וירידות מהנות, ומקשר בין מצפה מודיעין לחלקים הפנימיים של היער. 
    השביל מספק פיסת טבע פסטורלית במרחק קצר ממרכז הארץ ומשמש מפלט לרוכבי שטח בכל העונות.
    """
}


team_riddles = {
    'Team1': {
    543: { # Mizpe Modiin - > HaPagoda
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'49.0%22N+34%C2%B057'24.6%22E",
        "images": ["DorelNav/dorelNavPhoto/514_1.jpeg", "DorelNav/dorelNavPhoto/514_2.jpeg", "DorelNav/dorelNavPhoto/514_3.jpeg"]  # add up to 3 image URLs or file paths here
    },
    514: { # HaPagoda -> Random location 1
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'46.2%22N+34%C2%B057'34.6%22E",
        "images": ["DorelNav/dorelNavPhoto/559_1.jpeg", "DorelNav/dorelNavPhoto/559_2.jpeg"]
    },
    559: { # Random location 1 -> The partisans
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'48.1%22N+34%C2%B057'20.6%22E",
        "images": ["DorelNav/dorelNavPhoto/531_1.jpeg"]
    },
    531: { # The partisans
        "answer": "5",
        "link": None,
        "images": []
    }
},
'Team2':{
    543: { # Mizpe Modiin -> Random location 2
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'52.4%22N+34%C2%B057'33.0%22E",
        "images": ["DorelNav/dorelNavPhoto/572_1.jpeg", "DorelNav/dorelNavPhoto/572_2.jpeg"]  # add up to 3 image URLs or file paths here
    },
    572: { # Random location 2 -> Mahzeba
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'41.1%22N+34%C2%B057'34.7%22E",
        "images": ["DorelNav/dorelNavPhoto/528_1.jpeg", "DorelNav/dorelNavPhoto/528_2.jpeg"]
    },
    528: { # Mahzeba -> HaPagoda
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'49.0%22N+34%C2%B057'24.6%22E",
        "images": ["DorelNav/dorelNavPhoto/514_1.jpeg", "DorelNav/dorelNavPhoto/514_2.jpeg", "DorelNav/dorelNavPhoto/514_3.jpeg"]
    },
    514: { # HaPagoda
        "answer": "5",
        "link": None,
        "images": []
    }
},
'Team3': {
    543: { # Mizpe Modiin -> Box Tombs
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'45.2%22N+34%C2%B057'11.4%22E",
        "images": ["DorelNav/dorelNavPhoto/586_1.jpeg", "DorelNav/dorelNavPhoto/586_2.jpeg"]  # add up to 3 image URLs or file paths here
    },
    586: { # Box Tombs -> Singel Herzel
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'42.8%22N+34%C2%B057'28.3%22E",
        "images": ["DorelNav/dorelNavPhoto/597_1.jpeg"]
    },
    597: { # Singel Herzel -> HaPagoda
        "answer": "5",
        "link": "https://www.google.com/maps/place/31%C2%B056'49.0%22N+34%C2%B057'24.6%22E",
        "images": ["DorelNav/dorelNavPhoto/514_1.jpeg", "DorelNav/dorelNavPhoto/514_2.jpeg", "DorelNav/dorelNavPhoto/514_3.jpeg"]
    },
    514: { # HaPagoda
        "answer": "5",
        "link": None,
        "images": []
    }
}}

gathering_link = "https://www.google.com/maps/place/31%C2%B057'01.4%22N+34%C2%B057'20.0%22E"
gathering_riddle_num = 560

# Whatsapp configuration
auth_token = ''
account_sid = ''
FROM_WHATSAPP = 'whatsapp:+14155238886'  # your Twilio Sandbox WhatsApp number
TO_WHATSAPP = 'whatsapp:+972522957309'  # e.g. whatsapp:+972512345678

# Function to send WhatsApp message using Twilio
def send_whatsapp_message(body):
    try:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_=FROM_WHATSAPP,          # your Twilio Sandbox WhatsApp number
            to=TO_WHATSAPP,  # e.g. whatsapp:+972512345678
            body=body
        )
        return message.sid
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
        # st.error(f"Failed to send WhatsApp message: {e}")


# Reset to home
def go_home():
    st.session_state['stage'] = 'select'

def get_google_maps_link(ggl_link):
    latlon = ggl_link.split("/")[-1]
    embed_url = f"https://maps.google.com/maps?q={latlon}&output=embed"
    return embed_url

# Main app logic
def main(team='Team2', alt_riddles=None):
    global riddles, account_sid, auth_token
    if alt_riddles:
        riddles = alt_riddles
    # Initialize session state
    if 'stage' not in st.session_state:
        st.session_state['stage'] = 'select'
    if 'last_riddle' not in st.session_state:
        st.session_state['last_riddle'] = None
    if 'last_location' not in st.session_state:
        st.session_state['last_location'] = None

    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')

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

        st.markdown(f"<div class='description-box'>{descriptions[rid]}</div>", unsafe_allow_html=True)

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
                    # Correct answer
                    st.session_state[solved_key] = True
                    nxt = riddles[rid]['link'] or gathering_link
                    send_whatsapp_message(f'{team} solved riddle {rid} correctly!\nNext location: {nxt}')
                    st.session_state['last_riddle'], st.session_state['last_location'] = rid, nxt
                    st.success("✅ Correct!")
                    if riddles[rid]['link'] is None:
                        st.balloons(); st.success("🎉 Congratulations! You've completed the game.")
                        send_whatsapp_message(f'{team} completed the game! Gathering point: {gathering_link}')
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
                    # Wrong answer
                    send_whatsapp_message(f'{team} answered riddle {rid} incorrectly: "{user_ans}" - expected "{riddles[rid]["answer"]}"')
                    st.error("❌ Wrong answer. Please try again.")

if __name__ == "__main__":
    selected_team = os.environ.get('SELECTED_TEAM', 'Team2')
    if selected_team not in team_riddles:
        selected_team = 'Team2'
    main(team=selected_team, alt_riddles=team_riddles.get(selected_team))
