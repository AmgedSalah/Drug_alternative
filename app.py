# import streamlit as st
# import pickle
# import pandas as pd
# import gzip

#                                         ## To Add External CSS ##
# # with open('css/style.css') as f:
# #      st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)




#                                         ## Application Backend ##

#                     # To load medicine-dataframe from pickle in the form of dictionary
# medicines_dict = pickle.load(open('medicine_dict.pkl','rb'))
# medicines = pd.DataFrame(medicines_dict)

#                     # To load similarity-vector-data from pickle in the form of dictionary
# # similarity = pickle.load(open('similarity.pkl','rb'))
# with gzip.open("similarity_compressed.pkl.gz", "rb") as f:
#     similarity = pickle.load(f)

# def recommend(medicine):
#      medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
#      distances = similarity[medicine_index]
#      medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#      recommended_medicines = []
#      for i in medicines_list:
#          recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
#      return recommended_medicines





#                                     ## Appliaction Frontend ##

#                                    # Title of the Application
# st.title('Medicine Recommender System')

#                                         # Searchbox
# selected_medicine_name = st.selectbox(
# 'Type your medicine name whose alternative is to be recommended',
#      medicines['Drug_Name'].values)


#                                    # Recommendation Program
# if st.button('Recommend Medicine'):
#      recommendations = recommend(selected_medicine_name)
#      j=1
#      for i in recommendations:
#           st.write(j,i)                      # Recommended-drug-name
#           # st.write("Click here -> "+" https://www.netmeds.com/catalogsearch/result?q="+i) # Recommnded drug purchase link from netmeds
#           st.write("Click here -> "+" https://pharmeasy.in/search/all?name="+i) # Recommnded-drug purchase link from pharmeasy
#           j+=1


# import streamlit as st
# import pickle
# import pandas as pd

# ## To Add External CSS ##
# with open('css/style.css') as f:
#      st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ## Application Backend ##
# # To load medicine-dataframe from pickle in the form of dictionary
# medicines_dict = pickle.load(open('medicine_dict.pkl','rb'))
# medicines = pd.DataFrame(medicines_dict)

# # To load similarity-vector-data from pickle in the form of dictionary
# similarity = pickle.load(open('similarity.pkl','rb'))

# def recommend(medicine):
#     # التحقق أولاً إذا كان الدواء موجود في البيانات
#     if medicine not in medicines['Drug_Name'].values:
#         st.write("Sorry, the medicine you entered is not found in the database.")
#         return []  # إرجاع قائمة فارغة إذا لم يتم العثور على الدواء
    
#     # إذا تم العثور على الدواء، نكمل البحث
#     medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
#     distances = similarity[medicine_index]
#     medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     recommended_medicines = []
#     for i in medicines_list:
#         recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
#     return recommended_medicines

# ## Application Frontend ##
# # Title of the Application
# st.title('Medicine Recommender System')

# # Text input for writing the medicine name
# selected_medicine_name = st.text_input(
#     'Type your medicine name whose alternative is to be recommended'
# )

# # Recommendation Program
# if st.button('Recommend Medicine') and selected_medicine_name:
#      recommendations = recommend(selected_medicine_name)
#      if recommendations:  # إذا كانت هناك أدوية موصى بها
#          j=1
#          for i in recommendations:
#               st.write(j, i)  # Recommended-drug-name
#               # st.write("Click here -> "+" https://www.netmeds.com/catalogsearch/result?q="+i) # Recommnded drug purchase link from netmeds
#               st.write("Click here -> "+" https://pharmeasy.in/search/all?name="+i)  # Recommended-drug purchase link from pharmeasy
#               j+=1

# ## Image load ##
# from PIL import Image
# image = Image.open('images/medicine-image.jpg')
# st.image(image, caption='Recommended Medicines')








from flask import Flask, request, jsonify
import pickle
import pandas as pd
import gzip

app = Flask(__name__)

# تحميل بيانات الأدوية
medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)

# تحميل بيانات التشابه بين الأدوية
with gzip.open("similarity_compressed.pkl.gz", "rb") as f:
    similarity = pickle.load(f)

def recommend(medicine):
    try:
        medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
        distances = similarity[medicine_index]
        medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_medicines = []
        for i in medicines_list:
            recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
        
        return recommended_medicines
    except IndexError:
        return ["Medicine not found"]

@app.route('/recommend', methods=['POST'])
def recommend_medicine():
    data = request.get_json()
    medicine_name = data.get("medicine")

    if not medicine_name:
        return jsonify({"error": "Please provide a medicine name"}), 400

    recommendations = recommend(medicine_name)
    response = {
        "input_medicine": medicine_name,
        "recommended_medicines": recommendations
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)












from flask import Flask, request, jsonify
import pickle
import pandas as pd
import gzip

app = Flask(__name__)

# تحميل بيانات الأدوية
try:
    medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
    medicines = pd.DataFrame(medicines_dict)

    # تحميل بيانات التشابه بين الأدوية
    with gzip.open("similarity_compressed.pkl.gz", "rb") as f:
        similarity = pickle.load(f)
except FileNotFoundError as e:
    print(f"Error: {e}")
    medicines = None
    similarity = None

def recommend(medicine):
    try:
        medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
        distances = similarity[medicine_index]
        medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_medicines = [medicines.iloc[i[0]].Drug_Name for i in medicines_list]
        return recommended_medicines
    except (IndexError, TypeError):
        return ["Medicine not found"]

# Route للصفحة الرئيسية
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API is running. Use /recommend to get medicine recommendations."})

@app.route('/recommend', methods=['POST'])
def recommend_medicine():
    data = request.get_json()
    medicine_name = data.get("medicine")

    if not medicine_name:
        return jsonify({"error": "Please provide a medicine name"}), 400

    recommendations = recommend(medicine_name)
    response = {
        "input_medicine": medicine_name,
        "recommended_medicines": recommendations
        
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

