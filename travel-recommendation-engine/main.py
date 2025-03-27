#!/usr/bin/env python3
import requests
import json
import sys
from datetime import datetime

# API Configuration
COUNTRIES_API = "https://restcountries.com/v3.1"
WEATHER_API = "http://api.openweathermap.org/data/2.5/weather"
TELEPORT_API = "https://api.teleport.org/api/urban_areas/"

# You should get your own API key from https://openweathermap.org/api
WEATHER_API_KEY = "fc46e87c6a8c5fa03b2af707b07319c8"  # Replace with your actual key

def get_country_info(country_name):
    """Fetch country information from REST Countries API"""
    try:
        response = requests.get(f"{COUNTRIES_API}/name/{country_name}")
        if response.status_code == 200:
            data = response.json()[0]
            return {
                'name': data.get('name', {}).get('common', 'N/A'),
                'capital': data.get('capital', ['N/A'])[0],
                'region': data.get('region', 'N/A'),
                'subregion': data.get('subregion', 'N/A'),
                'population': f"{data.get('population', 0):,}",
                'languages': ', '.join(data.get('languages', {}).values()),
                'currency': ', '.join([f"{v['name']} ({v['symbol']})" for v in data.get('currencies', {}).values()]),
                'flag': data.get('flags', {}).get('png', 'N/A')
            }
        else:
            return {'error': 'Country not found'}
    except Exception as e:
        return {'error': f'Error fetching country info: {str(e)}'}

def get_weather(city_name):
    """Fetch weather information from OpenWeatherMap API"""
    if city_name == 'N/A':
        return {'error': 'No capital city specified'}
    
    try:
        params = {
            'q': city_name,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_API, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'conditions': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        else:
            return {'error': 'Weather service unavailable'}
    except Exception:
        return {'error': 'Weather service temporarily unavailable'}

def get_city_insights(city_name):
    """Fetch city quality of life data from Teleport API"""
    if city_name == 'N/A':
        return {'error': 'No capital city specified'}
    
    try:
        # First search for the city
        search_url = f"{TELEPORT_API}search/?search={city_name}"
        search_response = requests.get(search_url, timeout=5)
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data['_embedded']['city:search-results']:
                city_link = search_data['_embedded']['city:search-results'][0]['_links']['city:item']['href']
                
                # Now get details
                details_response = requests.get(f"{city_link}scores/", timeout=5)
                if details_response.status_code == 200:
                    details_data = details_response.json()
                    return {
                        'summary': details_data['summary'],
                        'categories': [
                            {'name': cat['name'], 'score': cat['score_out_of_10']}
                            for cat in details_data['categories']
                        ]
                    }
        return {'error': 'Quality of life data not available'}
    except requests.exceptions.Timeout:
        return {'error': 'Service timeout - try again later'}
    except Exception:
        return {'error': 'Service temporarily unavailable'}

def display_country_info(country_info):
    """Display country information in a formatted way"""
    if 'error' in country_info:
        print(f"\n⚠️ {country_info['error']}")
        return
    
    print("\n=== Country Information ===")
    print(f"Name: {country_info['name']}")
    print(f"Capital: {country_info['capital']}")
    print(f"Region: {country_info['region']}", end='')
    if country_info['subregion'] != 'N/A':
        print(f" ({country_info['subregion']})")
    else:
        print()
    print(f"Population: {country_info['population']}")
    print(f"Languages: {country_info['languages']}")
    print(f"Currency: {country_info['currency']}")
    print(f"Flag: {country_info['flag']}")

def display_weather(weather_info, city):
    """Display weather information"""
    print("\n=== Weather Information ===")
    if isinstance(weather_info, dict):
        if 'error' in weather_info:
            print(f"⚠️ {weather_info['error']} for {city}")
        else:
            print(f"Weather in {city}:")
            print(f"Temperature: {weather_info['temperature']}°C")
            print(f"Conditions: {weather_info['conditions'].title()}")
            print(f"Humidity: {weather_info['humidity']}%")
            print(f"Wind Speed: {weather_info['wind_speed']} m/s")
    else:
        print("⚠️ Weather information not available")

def display_city_insights(insights, city):
    """Display city quality of life insights"""
    print("\n=== City Quality of Life ===")
    if isinstance(insights, dict):
        if 'error' in insights:
            print(f"ℹ️ {insights['error']}")
        else:
            print(f"Summary: {insights['summary']}")
            print("\nCategories (Score out of 10):")
            for category in insights['categories']:
                print(f"- {category['name']}: {category['score']}")
    else:
        print(f"ℹ️ Quality of life data not available for {city}")

def get_random_country():
    """Fetch a random country from the API"""
    try:
        response = requests.get(f"{COUNTRIES_API}/all")
        if response.status_code == 200:
            countries = response.json()
            return countries[0]  # For simplicity, just take first
        return None
    except Exception:
        return None

def main():
    print("\n🌍 Travel Recommendation Engine with Cultural Insights 🌏\n")
    
    while True:
        print("\n1. Search by Country")
        print("2. Get Random Country Recommendation")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            country_name = input("Enter country name: ").strip()
            country_info = get_country_info(country_name)
            
            display_country_info(country_info)
            
            if not isinstance(country_info, dict) or 'error' in country_info:
                continue
                
            # Get weather for capital
            capital = country_info['capital']
            weather_info = get_weather(capital)
            display_weather(weather_info, capital)
            
            # Get city insights
            insights = get_city_insights(capital)
            display_city_insights(insights, capital)
                
        elif choice == '2':
            random_country = get_random_country()
            if random_country:
                country_name = random_country['name']['common']
                print(f"\n✨ Random Recommendation: {country_name} ✨")
                
                country_info = {
                    'name': random_country.get('name', {}).get('common', 'N/A'),
                    'capital': random_country.get('capital', ['N/A'])[0],
                    'region': random_country.get('region', 'N/A'),
                    'subregion': random_country.get('subregion', 'N/A'),
                    'population': f"{random_country.get('population', 0):,}",
                    'languages': ', '.join(random_country.get('languages', {}).values()),
                    'currency': ', '.join([f"{v['name']} ({v['symbol']})" for v in random_country.get('currencies', {}).values()]),
                    'flag': random_country.get('flags', {}).get('png', 'N/A')
                }
                
                display_country_info(country_info)
                
                if not isinstance(country_info, dict) or 'error' in country_info:
                    continue
                    
                capital = country_info['capital']
                weather_info = get_weather(capital)
                display_weather(weather_info, capital)
                
                insights = get_city_insights(capital)
                display_city_insights(insights, capital)
            else:
                print("\n⚠️ Error fetching random country. Please try again.")
                
        elif choice == '3':
            print("\nThank you for using the Travel Recommendation Engine. Safe travels! ✈️\n")
            sys.exit()
            
        else:
            print("\n⚠️ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
