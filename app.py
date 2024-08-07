import streamlit as st
import pandas as pd
import pickle
import os

random_forest_model_path = os.path.join(os.path.dirname(__file__), 'models', 'randomForest.pkl')
label_encoder_brand_model_path = os.path.join(os.path.dirname(__file__), 'models', 'LabelEncoderBrand.pkl')
label_encoder_fit_model_path = os.path.join(os.path.dirname(__file__), 'models', 'LabelEncoderFit.pkl')
preprocessor_model_path = os.path.join(os.path.dirname(__file__), 'models', 'preprocessor.pkl')

random_forest = pickle.load(open(random_forest_model_path, 'rb'))
label_encoder_brand = pickle.load(open(label_encoder_brand_model_path, 'rb'))
label_encoder_fit = pickle.load(open(label_encoder_fit_model_path, 'rb'))
preprocessor = pickle.load(open(preprocessor_model_path, 'rb'))

def main():
    menu = ["Home","Dashboard"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.title("Jeans Price Predictor")
        df = pd.read_csv("data/cleaned_jeans_data.csv")

        with st.form(key="form1"):
            brands = st.selectbox("Please select the brand name", df['brand'].unique().tolist())
            distress = st.selectbox("Please select the distress type", df['distress'].unique().tolist())
            length = st.selectbox("Please select the length type", df['length'].unique().tolist())
            waist_rise = st.selectbox("Please select the waist rise type", df['waist_rise'].unique().tolist())
            fit = st.selectbox("Please select the fit type", df['fit'].unique().tolist())
            number_of_pockets = st.selectbox("Please select the number of pockets", df['number_of_pockets'].unique().tolist())
            stretch = st.selectbox("Please select the stretch of jeans", df['stretch'].unique().tolist())
            rating = st.text_input("Please type the rating of jeans on myntra")
            number_of_ratings = st.text_input("Please type the number of reviews of jeans on myntra")

            submit_button = st.form_submit_button(label='Predict')

            if submit_button:
                st.success("Recommend price for jeans is {:.2f}".format(predict_price(brands, distress, length, waist_rise, fit, number_of_pockets, stretch, rating, number_of_ratings)))

    else:
        st.title("Dashboard")


def predict_price(brands, distress, length, waist_rise, fit, number_of_pockets, stretch, rating, number_of_ratings):
     
    new_sample = pd.DataFrame({
        "brand": [brands],
        "distress": [distress],
        "waist_rise": [waist_rise],
        "length": [length],
        "fit": [fit],
        "number_of_pockets": [number_of_pockets],
        "stretch": [stretch],
        "rating": [rating],
        "number_of_ratings": [number_of_ratings]
    })

    new_sample['fit'] = label_encoder_fit.transform(new_sample['fit'])
    new_sample['brand'] = label_encoder_brand.transform(new_sample['brand'])
    new_sample_encoded = preprocessor.transform(new_sample)

    prediction = random_forest.predict(new_sample_encoded)

    return prediction[0]

if __name__ == '__main__':
    main()