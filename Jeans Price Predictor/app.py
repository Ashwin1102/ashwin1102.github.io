import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

app = Flask(__name__)

# Load models and encoders
try:
    random_forest = pickle.load(open('models/randomForest.pkl', 'rb'))
    label_encoder_brand = pickle.load(open('models/LabelEncoderBrand.pkl', 'rb'))
    label_encoder_fit = pickle.load(open('models/LabelEncoderFit.pkl', 'rb'))
    preprocessor = pickle.load(open('models/preprocessor.pkl', 'rb'))
except Exception as e:
    print(f"Error loading models: {e}")

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        # Load data
        df = pd.read_csv('data/cleaned_jeans_data.csv')

        # Extract unique values for dropdown options
        brands = df['brand'].unique().tolist()
        distress = df['distress'].unique().tolist()
        waist_rise = df['waist_rise'].unique().tolist()
        length = df['length'].unique().tolist()
        fit = df['fit'].unique().tolist()
        number_of_pockets = df['number_of_pockets'].unique().tolist()
        stretch = df['stretch'].unique().tolist()
        rating = df['rating'].unique().tolist()
        number_of_ratings = df['number_of_ratings'].unique().tolist()

        if request.method == 'POST':
            # Get form inputs
            brands_input = request.form.get('brand')
            distress_input = request.form.get('distress')
            waist_rise_input = request.form.get('waist_rise')
            length_input = request.form.get('length')
            fit_input = request.form.get('fit')
            number_of_pockets_input = request.form.get('number_of_pockets')
            stretch_input = request.form.get('stretch')
            rating_input = float(request.form.get('rating'))
            number_of_ratings_input = float(request.form.get('number_of_ratings'))

            # Create DataFrame for prediction
            new_sample = pd.DataFrame({
                "brand": [brands_input],
                "distress": [distress_input],
                "waist_rise": [waist_rise_input],
                "length": [length_input],
                "fit": [fit_input],
                "number_of_pockets": [number_of_pockets_input],
                "stretch": [stretch_input],
                "rating": [rating_input],
                "number_of_ratings": [number_of_ratings_input]
            })

            # Transform and predict
            new_sample['fit'] = label_encoder_fit.transform(new_sample['fit'])
            new_sample['brand'] = label_encoder_brand.transform(new_sample['brand'])
            new_sample_encoded = preprocessor.transform(new_sample)

            prediction = random_forest.predict(new_sample_encoded)

            return render_template('home.html', brands=brands, distress=distress, waist_rise=waist_rise, length=length, fit=fit, number_of_pockets=number_of_pockets, stretch=stretch, rating=rating, number_of_ratings=number_of_ratings, price=prediction[0])

        return render_template('home.html', brands=brands, distress=distress, waist_rise=waist_rise, length=length, fit=fit, number_of_pockets=number_of_pockets, stretch=stretch, rating=rating, number_of_ratings=number_of_ratings)

    except Exception as e:
        print(f"Error processing request: {e}")
        return "An error occurred. Please try again later."

if __name__ == "__main__":
    app.run(host="0.0.0.0")
