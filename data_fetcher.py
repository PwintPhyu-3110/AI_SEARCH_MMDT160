import json
import time
import requests

# မြန်မာနိုင်ငံ၏ ရှုခင်းလှသော ခရီးစဉ်မြို့များ/ဒေသများ (၄၃ ခု)
CITIES = [
    # Shan State
    "Taunggyi, Myanmar", "Kalaw, Myanmar", "Nyaungshwe, Myanmar", "Pindaya, Myanmar",
    "Hsipaw, Myanmar", "Lashio, Myanmar", "Kengtung, Myanmar",
    
    # Mandalay & Central Region
    "Pyin Oo Lwin, Myanmar", "Mandalay, Myanmar", "Sagaing, Myanmar", 
    "Amarapura, Myanmar", "Bagan, Myanmar", "Magway, Myanmar", 
    "Minbu, Myanmar", "Pakokku, Myanmar",
    
    # Chin State
    "Hakha, Myanmar", "Falam, Myanmar", "Mindat, Myanmar", 
    "Kanpetlet, Myanmar", "Rihkhawdar, Myanmar",
    
    # Kachin State
    "Myitkyina, Myanmar", "Putao, Myanmar", "Bhamo, Myanmar",
    
    # Kayah & Kayin States
    "Loikaw, Myanmar", "Demoso, Myanmar", "Hpa-An, Myanmar", "Thandaunggyi, Myanmar",
    
    # Tanintharyi Region
    "Myeik, Myanmar", "Dawei, Myanmar", "Kawthaung, Myanmar",
    
    # Rakhine State
    "Thandwe, Myanmar", "Mrauk-U, Myanmar", "Kyaukphyu, Myanmar",
    
    # Ayeyarwady Region
    "Chaungtha, Myanmar", "Ngwesaung, Myanmar",
    
    # Mon / Bago / Capital / Main Hubs
    "Kyaikhto, Myanmar", "Mawlamyine, Myanmar", "Katha, Myanmar", 
    "Naypyidaw, Myanmar", "Yangon, Myanmar", "Bago, Myanmar", "Taungoo, Myanmar"
]

# မြို့များကြား ကုန်းလမ်းဆက်သွယ်ထားသော လမ်းကြောင်းများ (Connections)
CONNECTIONS = [
    # Lower Myanmar & Delta Hubs
    ("Yangon, Myanmar", "Bago, Myanmar"),
    ("Yangon, Myanmar", "Chaungtha, Myanmar"),
    ("Chaungtha, Myanmar", "Ngwesaung, Myanmar"),
    ("Bago, Myanmar", "Kyaikhto, Myanmar"),
    ("Bago, Myanmar", "Taungoo, Myanmar"),
    ("Kyaikhto, Myanmar", "Hpa-An, Myanmar"),
    ("Hpa-An, Myanmar", "Mawlamyine, Myanmar"),
    ("Mawlamyine, Myanmar", "Dawei, Myanmar"),
    ("Dawei, Myanmar", "Myeik, Myanmar"),
    ("Myeik, Myanmar", "Kawthaung, Myanmar"),
    
    # Central Trunk (Taungoo -> Naypyidaw -> Mandalay)
    ("Taungoo, Myanmar", "Thandaunggyi, Myanmar"),
    ("Taungoo, Myanmar", "Naypyidaw, Myanmar"),
    ("Naypyidaw, Myanmar", "Magway, Myanmar"),
    ("Naypyidaw, Myanmar", "Loikaw, Myanmar"),
    ("Naypyidaw, Myanmar", "Mandalay, Myanmar"),
    
    # Shan State Network
    ("Loikaw, Myanmar", "Demoso, Myanmar"),
    ("Loikaw, Myanmar", "Taunggyi, Myanmar"),
    ("Taunggyi, Myanmar", "Nyaungshwe, Myanmar"),
    ("Taunggyi, Myanmar", "Kalaw, Myanmar"),
    ("Kalaw, Myanmar", "Pindaya, Myanmar"),
    ("Mandalay, Myanmar", "Pyin Oo Lwin, Myanmar"),
    ("Pyin Oo Lwin, Myanmar", "Hsipaw, Myanmar"),
    ("Hsipaw, Myanmar", "Lashio, Myanmar"),
    ("Taunggyi, Myanmar", "Kengtung, Myanmar"),
    
    # Mandalay, Sagaing & Northern Network
    ("Mandalay, Myanmar", "Amarapura, Myanmar"),
    ("Mandalay, Myanmar", "Sagaing, Myanmar"),
    ("Mandalay, Myanmar", "Bagan, Myanmar"),
    ("Sagaing, Myanmar", "Katha, Myanmar"),
    ("Katha, Myanmar", "Bhamo, Myanmar"),
    ("Bhamo, Myanmar", "Myitkyina, Myanmar"),
    ("Myitkyina, Myanmar", "Putao, Myanmar"),
    
    # Central West & Chin State
    ("Magway, Myanmar", "Minbu, Myanmar"),
    ("Magway, Myanmar", "Bagan, Myanmar"),
    ("Bagan, Myanmar", "Pakokku, Myanmar"),
    ("Pakokku, Myanmar", "Mindat, Myanmar"),
    ("Mindat, Myanmar", "Kanpetlet, Myanmar"),
    ("Pakokku, Myanmar", "Hakha, Myanmar"),
    ("Hakha, Myanmar", "Falam, Myanmar"),
    ("Falam, Myanmar", "Rihkhawdar, Myanmar"),
    
    # Coastal & Rakhine State
    ("Magway, Myanmar", "Thandwe, Myanmar"),
    ("Thandwe, Myanmar", "Kyaukphyu, Myanmar"),
    ("Kyaukphyu, Myanmar", "Mrauk-U, Myanmar")
]

HEADERS = {'User-Agent': 'IntelligentSearchVisualizer/1.0'}

def fetch_coordinates(cities):
    coords = {}
    print("Nominatim API မှ Coordinates ယူနေပါသည်...")
    for city in cities:
        url = "https://nominatim.openstreetmap.org/search"
        params = {'q': city, 'format': 'json', 'limit': 1}
        try:
            res = requests.get(url, params=params, headers=HEADERS, timeout=10)
            data = res.json()
            if data:
                # မြို့နာမည်မှ ", Myanmar" ကို ခွဲထုတ်ပြီး Clean Name အဖြစ်သိမ်းမည်
                clean_name = city.split(',')[0]
                coords[clean_name] = {"lat": float(data[0]['lat']), "lon": float(data[0]['lon'])}
                print(f"  ✓ {clean_name} ရပါပြီ")
            else:
                print(f"  ✗ {city} ကို ရှာမတွေ့ပါ။")
        except Exception as e:
            print(f"  Error {city}: {e}")
        time.sleep(1.2) # Nominatim Rate Limit (1 request/sec) အတွက် စောင့်ခြင်း
    return coords

def fetch_road_distances(connections, coords):
    graph = {city: {} for city in coords}
    print("\nOSRM API မှ လမ်းကြောင်းအကွာအဝေးများ ယူနေပါသည်...")
    for u_full, v_full in connections:
        u = u_full.split(',')[0]
        v = v_full.split(',')[0]
        
        if u not in coords or v not in coords:
            continue
            
        c1, c2 = coords[u], coords[v]
        url = f"http://router.project-osrm.org/route/v1/driving/{c1['lon']},{c1['lat']};{c2['lon']},{c2['lat']}"
        try:
            res = requests.get(url, params={'overview': 'false'}, headers=HEADERS, timeout=10)
            data = res.json()
            if "routes" in data and len(data["routes"]) > 0:
                dist_km = round(data["routes"][0]["distance"] / 1000.0, 2)
                graph[u][v] = dist_km
                graph[v][u] = dist_km
                print(f"  ✓ {u} <-> {v}: {dist_km} km")
            else:
                print(f"  ✗ လမ်းကြောင်းမရှိပါ: {u} - {v}")
        except Exception as e:
            print(f"  Error {u}-{v}: {e}")
        time.sleep(0.5)
    return graph

if __name__ == "__main__":
    coords = fetch_coordinates(CITIES)
    graph = fetch_road_distances(CONNECTIONS, coords)
    map_data = {"nodes": coords, "graph": graph}
    
    with open("map_data.json", "w", encoding="utf-8") as f:
        json.dump(map_data, f, indent=4, ensure_ascii=False)
    print("\n map_data.json ထဲသို့ အချက်အလက်များ အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ!")