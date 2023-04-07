# Spotify Song Popularity Prediction and Recommendation

This project aims to predict the popularity of a song based on its features and create a playlist of songs similar to the given song. The project consists of two main parts: data analysis and model building, and the Streamlit web application. The data analysis and model building part involves the creation of classification and clustering models, which can be found in the `spotify.ipynb` Jupyter Notebook file.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run the Streamlit web application, you'll need to have Python 3 installed on your computer.

### Running the Streamlit Web Application

After installing the prerequisites, you can run the Streamlit web application with the following command:

```bash
streamlit run streamlit_app.py
```

This command will start the web application on your local machine, and you can access it via your web browser.

## Project Overview

### Data Analysis and Model Building

The `spotify.ipynb` Jupyter Notebook contains the data analysis and model building process for both classification and clustering models. The classification model is used to predict the popularity of a song based on its features, while the clustering model is used to group similar songs together.

### Streamlit Web Application

The Streamlit web application (`streamlit_app.py`) allows users to interact with the models built in the `spotify.ipynb` Jupyter Notebook. Users can input a song's features to predict its popularity and create a playlist of similar songs. They can also create a playlist based on the song title and artist name.

## Built With

* [Streamlit](https://www.streamlit.io/) - The web framework used
* [Spotify Web API](https://developer.spotify.com/documentation/web-api/) - The API used to fetch song data and create playlists
* [Scikit-learn](https://scikit-learn.org/) - The library used for building the classification and clustering models
* [Pandas](https://pandas.pydata.org/) - The library used for data manipulation and analysis

## Acknowledgements

* Spotify Web API for providing the song data
* Scikit-learn and Pandas for providing powerful tools for data analysis and model building
* Streamlit for providing an easy-to-use web framework for creating interactive applications

Feel free to explore the project and make any improvements or additions you see fit. Enjoy!
