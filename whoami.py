import streamlit as st
import numpy as np
import pandas as pd
import math
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import euclidean_distances

st.title("Who am I?")
st.subheader("Answer this questionnaire and find out which character you resemble the most.")
#st.markdown("How long do you want the questionnaire to be?")
#lenght = st.radio(" ", ("Short: 10 questions","Medium: 35 questions (Recommended)", "Long: 70 questions"),index=1, label_visibility="collapsed")

st.markdown("Select the :red[movie] or :red[TV show] from which you want to find your most similar character.")
option = st.selectbox("**Movie or show**", ("All","How I met your Mother","Friends","The Office","Arcane"), label_visibility="collapsed")


st.header("Survey")

st.markdown("Slide the bar to the value that best describes you. ")

st.subheader("I'm more of an :green[Introvert **(0)**],  or an :green[Extrovert **(100)**]")
q1 = st.slider("q1", 0, 100, 50, label_visibility="collapsed" )

st.subheader(":green[Thinker],  or a :green[Doer]")
q2 = st.slider("q2", 0, 100, 50, format='%.0f', label_visibility="collapsed")

st.subheader(":green[Hard worker],  or :green[Lazy]")
q3 = st.slider("q3", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Logical],  or :green[Emotional]")
q4 = st.slider("q4", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Organized],  or :green[Chaotic]")
q5 = st.slider("q5", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Peaceful],  or :green[Confrontational]")
q6 = st.slider("q6", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Optimistic],  or :green[Pessimistic]")
q7 = st.slider("q7", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Uptight],  or :green[Free spirit]")
q8 = st.slider("q8", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Practical],  or :green[Imaginative]")
q9 = st.slider("q9", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Leader],  or :green[Follower]")
q10 = st.slider("q10", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Selfish],  or :green[Generous]")
q11 = st.slider("q11", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Confident],  or :green[Insecure]")
q12 = st.slider("q12", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Nerd],  or :green[Cool]")
q13 = st.slider("q13", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Rough],  or :green[Sweetheart]")
q14 = st.slider("q14", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Brave],  or :green[Coward]")
q15 = st.slider("q15", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Good],  or :green[Evil]")
q16 = st.slider("q16", 0, 100, 50, label_visibility="collapsed")

st.subheader(":green[Feminine],  or :green[Masculine] (for your own sex)")
q17 = st.slider("q17", 0, 100, 50, label_visibility="collapsed")




if st.button("Submit"):
    
    #MODE = 0 (USER) or 1 (ADD CHARACTER)
    MODE = 0
    #if option is how i met your mother
    
    if  option == "How I met your Mother":
        path = "characters/himym/characters.csv"
        df = pd.read_csv(path)

    elif option == "The Office":
        path = "characters/office/characters.csv"
        df = pd.read_csv(path)

    elif option == "Arcane":
        path = "characters/arcane/characters.csv"
        df = pd.read_csv(path)

    elif option == "Friends":
        path = "characters/friends/characters.csv"
        df = pd.read_csv(path)

    elif option == "All":
        path = "characters/characters_all.csv"
        df = pd.read_csv(path)

    results = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17]

    #CODE FOR THE USER
    if MODE==0:
        #Classification
        names = df["name"]
        if option == "All":
            numbers = df.drop(["name","from"], axis=1)
        else:
            numbers = df.drop(["name"], axis=1)

        numbers_norm = (numbers - numbers.mean()) / numbers.std()

        new_row = pd.DataFrame([results], columns=numbers.columns)
        new_row_norm = (new_row - numbers.mean()) / numbers.std()

        knn = KNeighborsClassifier(n_neighbors=1)
        knn.fit(numbers_norm, names)
        prediction = knn.predict(new_row_norm)

        assigned_character = prediction[0]
        #Path to image
        image_path = "characters/images/" + assigned_character + ".jpg"
        st.header("You are most similar to: ")
        st.image(image_path, width=500)

        if option == "All":
            st.subheader(assigned_character + " from " + df[df["name"]==assigned_character]["from"].values[0])
        else:
            st.subheader(assigned_character)

        # extract the actual point, the predicted point
        df_all = pd.read_csv("characters/characters_all.csv")
        actual_point_norm = new_row_norm.values[0]
        actual_point = actual_point_norm * numbers.std() + numbers.mean()
        predicted_row = df_all.loc[df_all['name'] == assigned_character]
        predicted_point = predicted_row.drop(["name","from"], axis=1).values[0]

        euclidean_distance = np.linalg.norm(actual_point - predicted_point)
        similarity = 100 - euclidean_distance/math.sqrt(17)

        st.subheader("With a similarity of :orange[{:.2f}%]".format(similarity))

    #CODE TO ADD CHARACTERS TO THE DATAFRAME
    elif MODE==1: 
        name = "Creed Bratton"
        show = "The Office"
        if option != "All":
            df.loc[len(df)] = [name] + results
            df.to_csv(path, index=False)
            st.header("Added to the database")

        else:
            df.loc[len(df)] = [name] + [show] + results
            df.to_csv(path, index=False)
            st.header("Added to the database")

    


