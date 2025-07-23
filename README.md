# Camp Quest

Camp Quest is an interactive, multi-functional camping assistant designed to make outdoor adventures smarter and more personalized. It integrates AI-powered decision-making with real-time data sources to guide users through every stage of a camping journey—from picking a location to packing the essentials and exploring nature.

## Key Features

- **Personalized Trip Planning**: Vectara API analyzes user responses to suggest glamping, camping, or RVing options.
- **Location Recommendations**: Google Maps API provides ideal nearby sites based on the chosen camping style.
- **Weather Forecasting**: Live weather updates from the Weather API tailored to the chosen location.
- **Nature Scanning**: Identify local plants and wildlife using the iNaturalist API and laptop camera integration.
- **Scavenger Hunt Generator**: Auto-creates an interactive hunt using surrounding flora and fauna data.
- **Smart Packing Assistant**: Custom packing checklist based on factors like age group, weather, and pet presence.
- **Camping Recipes**: Easy outdoor meals recommended using the Vectara API.
- **Entertainment Suggestions**: Activity ideas like stargazing and group games suited to your style of camping.

## App Flow

1. **Greeting Page**  
   - Welcomes the user and introduces app capabilities.
   - Automatically transitions to next step after a short message.

2. **Start Camping Page**  
   - Collects input (group size, budget, pets/infants) using a survey.
   - Vectara API generates a recommendation with context.

3. **Camping Page**  
   - Displays recommended sites with map view and details.

4. **Weather Page**  
   - Shows weather conditions at the selected site.

5. **iNaturalist Page**  
   - Scans and identifies local species.
   - Flags hazards and interesting finds.

6. **Scavenger Hunt Page**  
   - Creates a fun nature hunt using scanned species data.

7. **Packing Page**  
   - Dynamically generates packing checklist.

8. **Games Page**  
   - Displays camping entertainment options tailored to the group.

## Project Structure

camping-app/ ├── app/ │ ├── app.py │ └── models.py ├── static/ │ ├── css/ │ └── js/ ├── templates/ │ ├── index.html │ ├── startCamping.html │ ├── campingPage.html │ ├── weatherPage.html │ ├── iNaturalistPage.html │ ├── scavengerHuntPage.html │ ├── packingPage.html │ └── gamesPage.html ├── data/ │ ├── locations.json │ ├── packing_list.json │ └── recipes.json ├── requirements.txt ├── run.py └── .gitignore


## Setup Instructions

### Prerequisites

- Python 3.11 or compatible version
- Flask
- API credentials for Vectara, Google Maps, Weather, and iNaturalist

### Installation

1. Clone the repository:
git clone https://github.com/YuvaanshKapila/camping-app.git cd camping-app


2. Install dependencies:
pip install -r requirements.txt


3. Set up environment variables with your API keys.

4. Run the app:
python run.py


## License

This project is available under the MIT
