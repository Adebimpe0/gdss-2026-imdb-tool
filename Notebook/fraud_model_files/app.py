import streamlit as st
import pandas as pd
import pickle
import numpy as np

# -------- Load model, encoder, scaler --------
@st.cache_resource
def load_assets():
    model = pickle.load(open("Notebook/fraud_model_files/fraud_model.pk", "rb"))
    encoder = pickle.load(open("Notebook/fraud_model_files/fraud_encoder.pk", "rb"))  # for ProductCategory
    scaler = pickle.load(open("Notebook/fraud_model_files/fraud_scaler.pk", "rb"))
    return model, encoder, scaler

model, encoder, scaler = load_assets()

# -------- Constants --------
ALL_FEATURES = ['BatchId', 'AccountId', 'SubscriptionId', 'CustomerId', 'CountryCode',
                'ProviderId', 'ProductId', 'ProductCategory', 'ChannelId',
                'Value', 'PricingStrategy', 'Month', 'Day', 'Credit_or_Debit']

CATEGORICAL_COLS = ['BatchId','AccountId','SubscriptionId','CustomerId','CountryCode', 
                    'ProviderId','ProductId','ChannelId','PricingStrategy']

# -------- Main App --------
def main():
    st.title("Fraud Detection App")

    # -------- Sidebar Input --------
    with st.sidebar:
        st.header("Input Transaction Details")
        value = st.number_input("Transaction Value", min_value=0.0, value=100.0)
        month = st.slider("Transaction Month", 1, 12, 1)
        day = st.slider("Transaction Day", 1, 31, 1)
        credit_or_debit = st.selectbox("Credit or Debit (0 = Credit, 1 = Debit)", (0, 1))

        batch_id = st.selectbox("Batch ID", ['BatchId_36123', 'BatchId_15642'])
        account_id = st.selectbox("Account ID", ['AccountId_3957', 'AccountId_4841'])
        subscription_id = st.selectbox("Subscription ID", ['SubscriptionId_887', 'SubscriptionId_3829'])
        customer_id = st.selectbox("Customer ID", ['CustomerId_4406', 'CustomerId_4683'])
        country_code = st.selectbox("Country Code", [256])
        provider_id = st.selectbox("Provider ID", ['ProviderId_6', 'ProviderId_4'])
        product_id = st.selectbox("Product ID", ['ProductId_10', 'ProductId_6'])
        product_category = st.selectbox("Product Category", ['airtime', 'financial_services'])
        channel_id = st.selectbox("Channel ID", ['ChannelId_3', 'ChannelId_2'])
        pricing_strategy = st.selectbox("Pricing Strategy", (2, 4, 1, 0))

    # -------- Prediction --------
    if st.button("Predict Fraud"):

        input_dict = {
            'BatchId': batch_id,
            'AccountId': account_id,
            'SubscriptionId': subscription_id,
            'CustomerId': customer_id,
            'CountryCode': country_code,
            'ProviderId': provider_id,
            'ProductId': product_id,
            'ProductCategory': product_category,
            'ChannelId': channel_id,
            'Value': value,
            'Month': month,
            'Day': day,
            'Credit_or_Debit': credit_or_debit,
            'PricingStrategy': pricing_strategy
        }

        df_processed = pd.DataFrame([input_dict])

        # -------- Encode ProductCategory safely --------
        df_processed['ProductCategory'] = df_processed['ProductCategory'].apply(
            lambda x: x if x in encoder.classes_ else encoder.classes_[0]
        )
        df_processed['ProductCategory'] = encoder.transform(df_processed['ProductCategory']).astype(float)

        # -------- Convert other categorical columns to numeric safely --------
        for col in CATEGORICAL_COLS:
            if col != 'ProductCategory':  # already encoded
                df_processed[col] = pd.factorize(df_processed[col])[0].astype(float)

        # -------- Ensure all features exist --------
        for col in ALL_FEATURES:
            if col not in df_processed.columns:
                df_processed[col] = 0.0

        # -------- Reorder --------
        all_input = df_processed[ALL_FEATURES]

        # -------- Scale and Predict --------
        scaled_input = scaler.transform(all_input)
        prediction = model.predict(scaled_input)
        prob = model.predict_proba(scaled_input)[0][1]

        # -------- Result --------
        st.subheader("Prediction Result")
        if prediction[0] == 1:
            st.error(f"🚨 Fraudulent Transaction (Risk: {prob:.2%})")
        else:
            st.success(f"✅ Legitimate Transaction (Risk: {prob:.2%})")

# -------- Run App --------
if __name__ == "__main__":
    main()