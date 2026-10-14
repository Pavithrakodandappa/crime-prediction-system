"""Static reference data: cities, areas, risk scores (same as the frontend)."""

CITIES = [
 ("Bengaluru","Karnataka",2847,["Koramangala","Whitefield","Hebbal","Shivajinagar","Yelahanka","Jayanagar","Rajajinagar","Devanahalli"]),
 ("Mysuru","Karnataka",1642,["Nazarbad","Vijayanagar","Hebbal Kempapura","Kuvempunagar","Lakshmipuram","Bannimantap","Bogadi","Alanahalli"]),
 ("Hubballi","Karnataka",1284,["Vidyanagar","Gokul Road","Navanagar","Kalyan Nagar","Akshay Colony","Tarihal","Unkal","Hosur Road"]),
 ("Mangaluru","Karnataka",1089,["Pandeshwar","Attavar","Bejai","Urva","Balmatta","Kulashekar","Kankanady","Surathkal"]),
 ("Belagavi","Karnataka",987,["Camp Area","Shastri Nagar","Tilakwadi","Angol","Sudhir Colony","Vadgaon","Hindalga","Bhimsen Nagar"]),
 ("Davanagere","Karnataka",754,["PJ Extension","Shamnur Road","4th Main","Nittuvalli","Kondajji","Hadadi","Avaragere","Savalanga"]),
 ("Chennai","Tamil Nadu",3241,["T. Nagar","Adyar","Velachery","Anna Nagar","Tambaram","Perambur","Royapuram","Guindy"]),
 ("Coimbatore","Tamil Nadu",1876,["RS Puram","Gandhipuram","Peelamedu","Singanallur","Saibaba Colony","Ramanathapuram","Kuniyamuthur","Vadavalli"]),
 ("Madurai","Tamil Nadu",1543,["Alanganallur","Tallakulam","Goripalayam","Teppakulam","Anna Nagar","Villapuram","Mattuthavani","Palanganatham"]),
 ("Salem","Tamil Nadu",1123,["Hasthampatti","Kondalampatti","Ammapet","Attur","Omalur","Mettur","Yercaud","Vazhapadi"]),
 ("Visakhapatnam","Andhra Pradesh",2134,["MVP Colony","Gajuwaka","Dwaraka Nagar","Seethammadhara","Asilmetta","Bheemunipatnam","Malkapuram","Rushikonda"]),
 ("Vijayawada","Andhra Pradesh",1876,["Governorpet","Patamata","Benz Circle","Auto Nagar","Krishnalanka","Ajit Singh Nagar","Machavaram","Kandrika"]),
 ("Guntur","Andhra Pradesh",1432,["Arundelpet","Brodipet","Nagarampalem","Pattabhipuram","Gorantla","Tadikonda","Pedakakani","Mangalagiri"]),
 ("Hyderabad","Telangana",3187,["Old City","LB Nagar","Malkajgiri","Saidabad","Balanagar","Rajendranagar","Kukatpally","Miyapur"]),
 ("Mumbai","Maharashtra",4521,["Dharavi","Kurla","Andheri","Bandra","Borivali","Malad","Govandi","Mankhurd"]),
 ("Pune","Maharashtra",2876,["Hadapsar","Kondhwa","Bibwewadi","Kothrud","Pimpri","Chinchwad","Nigdi","Wakad"]),
 ("Nagpur","Maharashtra",1987,["Sitabuldi","Sadar","Gandhibagh","Dharampeth","Manewada","Hingna","Kamptee","Butibori"]),
 ("New Delhi","Delhi",5234,["Rohini","Dwarka","Shahdara","Okhla","Mustafabad","Uttam Nagar","Jahangirpuri","Kirari"]),
 ("Lucknow","Uttar Pradesh",2341,["Hazratganj","Alambagh","Aliganj","Indira Nagar","Chinhat","Kakori","Malihabad","Bakshi Ka Talab"]),
 ("Kanpur","Uttar Pradesh",2187,["Naveen Market","Kidwai Nagar","Arya Nagar","Tilak Nagar","Chakeri","Kalyanpur","Naubasta","Barra"]),
 ("Agra","Uttar Pradesh",1432,["Tajganj","Bodla","Balkeshwar","Kamla Nagar","Sikandra","Khandari","Kalindi Vihar","Shastripuram"]),
 ("Varanasi","Uttar Pradesh",1234,["Godowlia","Assi","Sarnath","Rameshwar","Bhelupur","Shivpur","Chandpur","Mugalsarai"]),
 ("Kolkata","West Bengal",3876,["Howrah","Dum Dum","Behala","Jadavpur","Entally","Jorasanko","Kalighat","Tiljala"]),
 ("Jaipur","Rajasthan",1987,["Mansarovar","Vaishali Nagar","Malviya Nagar","Tonk Road","Durgapura","Murlipura","Sanganer","Bagru"]),
 ("Ahmedabad","Gujarat",2543,["Naroda","Vatva","Odhav","Gomtipur","Behrampura","Kubernagar","Sarkhej","Chandkheda"]),
 ("Surat","Gujarat",2123,["Adajan","Udhna","Katargam","Varachha","Rundh","Puna","Limbayat","Rander"]),
 ("Thiruvananthapuram","Kerala",1123,["Kazhakkoottam","Vattiyoorkavu","Nemom","Attingal","Balaramapuram","Nedumangad","Kattakada","Parassala"]),
 ("Kochi","Kerala",1456,["Ernakulam","Mattancherry","Fort Kochi","Edapally","Kaloor","Kadavanthra","Vyttila","Maradu"]),
 ("Chandigarh","Punjab",876,["Sector 17","Sector 22","Sector 34","Manimajra","Sector 45","Mohali","Panchkula","Zirakpur"]),
 ("Bhopal","Madhya Pradesh",1654,["TT Nagar","Arera Colony","Habibganj","Kolar Road","Berasia","Govindpura","Mandideep","Sehore Road"]),
]

LOCATIONS = {n: dict(name=n, state=s, incidents=i, areas=a) for n, s, i, a in CITIES}

# Base risk per area slot (same order as the frontend map: A..H)
RISK_SCORES = [94, 79, 58, 82, 21, 53, 38, 14]

# Typical crimes, peak time and patrol units per area slot
AREA_META = [
    dict(crime="Theft",         time="10 PM–2 AM", patrol=6),
    dict(crime="Assault",       time="9 PM–1 AM",  patrol=5),
    dict(crime="Burglary",      time="11 PM–3 AM", patrol=3),
    dict(crime="Vandalism",     time="12 AM–4 AM", patrol=4),
    dict(crime="Pickpocketing", time="7 PM–10 PM", patrol=2),
    dict(crime="Fraud",         time="9 AM–5 PM",  patrol=3),
    dict(crime="Drug Offense",  time="8 PM–12 AM", patrol=2),
    dict(crime="Trespass",      time="6 PM–9 PM",  patrol=1),
]

# Crimes each area slot is most likely to see (used to generate training data)
AREA_CRIMES = [
    ["Theft", "Robbery", "Drug Offense"],
    ["Assault", "Robbery", "Vandalism"],
    ["Burglary", "Theft", "Fraud"],
    ["Vandalism", "Drug Offense", "Trespass"],
    ["Pickpocketing", "Vandalism", "Burglary"],
    ["Fraud", "Theft", "Pickpocketing"],
    ["Theft", "Drug Offense", "Pickpocketing"],
    ["Burglary", "Vandalism", "Trespass"],
]

# Real monthly totals for Bengaluru, Jan 2019 -> Dec 2024 (Appendix C of the report)
MONTHLY_HISTORY = [
    210, 195, 230, 220, 240, 260, 280, 270, 255, 245, 220, 200,  # 2019
    205, 182, 177, 185, 190, 210, 230, 250, 240, 228, 210, 198,  # 2020
    215, 200, 235, 225, 248, 268, 288, 278, 262, 252, 228, 208,  # 2021
    218, 204, 242, 232, 258, 278, 298, 285, 268, 258, 232, 216,  # 2022
    225, 208, 248, 238, 262, 282, 304, 290, 274, 262, 235, 216,  # 2023
    225, 208, 248, 242, 265, 285, 310, 295, 278, 262, 240, 215,  # 2024
]


def level(score):
    return "CRITICAL" if score >= 80 else "HIGH" if score >= 60 else "MEDIUM" if score >= 40 else "LOW"
