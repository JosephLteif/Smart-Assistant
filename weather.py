import requests

def weather(location):
    
    #my api key from the openweathermap website
    user_api = ""

    #accessing the json file with this link of a specific location
    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+user_api
    api_link = requests.get(complete_api_link)
    
    #getting the data 
    api_data = api_link.json()
    

    #create variables to store and display data
    temp_city = round(((api_data['main']['temp']) - 273.15),1)
    weather_desc = api_data['weather'][0]['description']
    hmdt = api_data['main']['humidity']
    wind_spd = api_data['wind']['speed']
    
    location_info = {
        "temperature" : temp_city,
        "weather description": weather_desc,
        "humidity" : hmdt,
        "wind speed": wind_spd
    }
    
    return location_info
