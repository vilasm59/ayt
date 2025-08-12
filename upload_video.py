import os
import google.auth.transport.requests
import googleapiclient.discovery
import googleapiclient.errors
import google.oauth2.credentials
import requests

# Load environment variables
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Function to refresh access token
def get_access_token():
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to refresh access token")

# Function to upload a video
def upload_video(video_file, title="श्री हनुमान चालीसा 1 Hour loop Series | Shree Hanuman Chalisa Video", description="""श्री हनुमान चालीसा 1 Hour loop Series | Shree Hanuman Chalisa Video

दोहा
श्रीगुरु चरन सरोज रज, निजमन मुकुरु सुधारि। बरनउं रघुबर बिमल जसु, जो दायक फल चारि।।
बुद्धिहीन तनु जानिके, सुमिरौं पवन-कुमार। बल बुधि बिद्या देहु मोहिं, हरहु कलेस बिकार।।

चौपाई
जय हनुमान ज्ञान गुन सागर। जय कपीस तिहुं लोक उजागर।।
राम दूत अतुलित बल धामा। अंजनि-पुत्र पवनसुत नामा।।
महाबीर बिक्रम बजरंगी। कुमति निवार सुमति के संगी।।
कंचन बरन बिराज सुबेसा। कानन कुण्डल कुँचित केसा।।
हाथ बज्र औ ध्वजा बिराजे। कांधे मूंज जनेउ साजे।।
शंकर सुवन केसरी नंदन। तेज प्रताप महा जग वंदन।।
बिद्यावान गुनी अति चातुर। राम काज करिबे को आतुर।।
प्रभु चरित्र सुनिबे को रसिया। राम लखन सीता मन बसिया।।
सूक्ष्म रूप धरि सियहिं दिखावा। बिकट रूप धरि लंक जरावा।।
भीम रूप धरि असुर संहारे। रामचन्द्र के काज संवारे।।
लाय सजीवन लखन जियाये। श्री रघुबीर हरषि उर लाये।।
रघुपति कीन्ही बहुत बड़ाई। तुम मम प्रिय भरतहि सम भाई।।
सहस बदन तुम्हरो जस गावैं। अस कहि श्रीपति कण्ठ लगावैं।।
सनकादिक ब्रह्मादि मुनीसा। नारद सारद सहित अहीसा।।
जम कुबेर दिगपाल जहां ते। कबि कोबिद कहि सके कहां ते।।
तुम उपकार सुग्रीवहिं कीन्हा। राम मिलाय राज पद दीन्हा।।
तुम्हरो मंत्र बिभीषन माना। लंकेश्वर भए सब जग जाना।।
जुग सहस्र जोजन पर भानु। लील्यो ताहि मधुर फल जानू।।
प्रभु मुद्रिका मेलि मुख माहीं। जलधि लांघि गये अचरज नाहीं।।
दुर्गम काज जगत के जेते। सुगम अनुग्रह तुम्हरे तेते।।
राम दुआरे तुम रखवारे। होत न आज्ञा बिनु पैसारे।।
सब सुख लहै तुम्हारी सरना। तुम रच्छक काहू को डर ना।।
आपन तेज सम्हारो आपै। तीनों लोक हांक तें कांपै।।
भूत पिसाच निकट नहिं आवै। महाबीर जब नाम सुनावै।।
नासै रोग हरे सब पीरा। जपत निरन्तर हनुमत बीरा।।
संकट तें हनुमान छुड़ावै। मन क्रम बचन ध्यान जो लावै।।
सब पर राम तपस्वी राजा। तिन के काज सकल तुम साजा।।
और मनोरथ जो कोई लावै। सोई अमित जीवन फल पावै।।
चारों जुग परताप तुम्हारा। है परसिद्ध जगत उजियारा।।
साधु संत के तुम रखवारे।। असुर निकन्दन राम दुलारे।।
अष्टसिद्धि नौ निधि के दाता। अस बर दीन जानकी माता।।
राम रसायन तुम्हरे पासा। सदा रहो रघुपति के दासा।।
तुह्मरे भजन राम को पावै। जनम जनम के दुख बिसरावै।।
अंत काल रघुबर पुर जाई। जहां जन्म हरिभक्त कहाई।।
और देवता चित्त न धरई। हनुमत सेइ सर्ब सुख करई।।
सङ्कट कटै मिटै सब पीरा। जो सुमिरै हनुमत बलबीरा।।
जय जय जय हनुमान गोसाईं। कृपा करहु गुरुदेव की नाईं।।
जो सत बार पाठ कर कोई। छूटहि बन्दि महा सुख होई।।
जो यह पढ़ै हनुमान चालीसा। होय सिद्धि साखी गौरीसा।।
तुलसीदास सदा हरि चेरा। कीजै नाथ हृदय महं डेरा।।

Copyright Disclaimer: - Under section 107 of the copyright Act 1976, allowance is mad for FAIR USE for purpose such a as criticism, comment, news reporting, teaching, scholarship and research. Fair use is a use permitted by copyright statues that might otherwise be infringing. Non- Profit, educational or personal use tips the balance in favor of FAIR USE.""", category_id="24", privacy_status="public"):
    access_token = get_access_token()
    
    credentials = google.oauth2.credentials.Credentials(access_token)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["hanuman chalisa", "हनुमान चालीसा", "shree hanuman chalisa", "shri hanuman chalisa", "श्री हनुमान चालीसा", "hanuman chalisa fast", "hanuman chalisa lyrics", "hanuman chalisa gulshan kumar", "hanuman chalisa original", "hanuman chalisa full", "jai hanuman gyan gun sagar", "gulshan kumar hanuman chalisa", "chalisa hanuman", "hanuman chalisa hariharan", "lord hanuman", "hanuman", "hanuman chalisa song", "hanuman jayanti", "हनुमान चालीसा फास्ट", "hanuman chalisa super fast", "hanuman chalisa fast 7 times"],
            "categoryId": category_id,
        },
        "status": {"privacyStatus": privacy_status},
    }
    
    with open(video_file, "rb") as file:
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=googleapiclient.http.MediaIoBaseUpload(file, mimetype="video/mp4", chunksize=-1, resumable=True),
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")
        
    print("Upload complete!")
    return response

if __name__ == "__main__":
    video_path = "video.mp4"
    
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found!")
        exit(1)
    
    upload_video(video_path)
