import streamlit as st
import pandas as pd
import pickle
import joblib
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

random_forest = joblib.load("models/randomForest.sav")
label_encoder_brand = joblib.load("models/LabelEncoderBrand.sav")
label_encoder_fit = joblib.load("models/LabelEncoderFit.sav")
preprocessor = joblib.load("models/preprocessor.sav")

def main():
    menu = ["Home","Dashboard"]
    choice = st.sidebar.selectbox("Menu",menu)
    df = pd.read_csv("data/cleaned_jeans_data.csv")

    if choice == "Home":
        st.title("Jeans Price Predictor")
        

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

        # Pie Chart
        top_n = st.text_input("Please enter a number to get the appropriate chart", "10")
        if top_n.isdigit():
            brand_counts = df['brand'].value_counts()
            labels = brand_counts.head(int(top_n)).index
            sizes = brand_counts.head(int(top_n)).values

            # Create a pie chart
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the pie chart in Streamlit
            st.pyplot(fig)
        else:
            st.error("Please enter a valid integer.")


        st.write("")
        st.write("")
        st.write("")

        # Scatter Plot
        brands_list = df['brand'].unique().tolist()
        brand1 = st.selectbox("Please select the first brand", brands_list)
        brands_list.remove(brand1)
        brand2 = st.selectbox("Please select the second brand", brands_list)

        df_group = df[(df["brand"] == brand1) | (df["brand"] == brand2)]

        # Scatter plot
        fig = px.scatter(
            df_group,
            x="price",
            y="number_of_ratings",
            color="brand",
            size="rating"
        )

        st.plotly_chart(fig, key="jeans")

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