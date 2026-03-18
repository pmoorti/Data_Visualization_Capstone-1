#Loading appropriate libraries
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#load Covid data
@st.cache_data
def load_data():
    df = pd.read_csv('/Users/payalmoorti/Documents/Data Visualization /Capstone/cleaned_data.csv')
    return df

df=load_data()

# Streamlit app

#page configuration
st.set_page_config(
    layout="wide",
    page_icon=":bar_chart:",
    page_title="Student Performance Analysis",)

st.title("Student Performance Data Explorer")
st.write("This app provides an interactive exploration of student performance data, and what factors influence student exam scores.")

# Sidebar for user input and filters
st.sidebar.header("Filter Data")

#slider for selecting range of exam scores
score_range = st.sidebar.slider("Select Exam Score Range", min_value=df['exam_score'].min(), max_value=df['exam_score'].max(), value=(df['exam_score'].min(), df['exam_score'].max()),step=1)

#filter data based on tutoring sessions
Attendance_Percentage = st.sidebar.multiselect("Attendance_Percentage (select multiple)", 
                                          options=sorted(df['Attendance_Percentage'].unique())
                                          )
#set default value for tutoring sessions to all if no selection is made
if not Attendance_Percentage:
    Attendance_Percentage = df['Attendance_Percentage'].unique()

#filtered data only on score range and tutoring sessions
filtered_df = df[(df['exam_score'] >= score_range[0]) & (df['exam_score'] <= score_range[1]) & (df['Attendance_Percentage'].isin(Attendance_Percentage))]

#Scatter Plot Exam Score vs. Attendance Percentage
st.subheader("Scatter Plot: Exam Score vs. Hours Studied Per Week (%)")
fig1 = px.scatter(filtered_df, 
                  x='hours_studied_per_week',
                   y='exam_score', 
                   color='Attendance_Percentage',
                   color_continuous_scale='viridis',
                   hover_data={'exam_score': ':,', 'Attendance_Percentage': ':,', 'Attendance_Percentage': ':,', 'hours_studied_per_week': ':,'},
                   title='Exam Score vs. Attendance (%)',
                 labels={'Attendance_Percentage': 'Attendance (%)', 'exam_score': 'Exam Score', 'hours_studied_per_week': 'Hours Studied Per Week'}
                  )

st.plotly_chart(fig1, use_container_width=True)

bar_data = filtered_df.groupby('gender')['exam_score'].mean().sort_values(ascending=False).reset_index()

# Bar chart for mean exam scores by gender
st.subheader("Bar Chart: Mean Exam Score by Gender")
fig2 = px.bar(bar_data, 
                x='gender',
                 y='exam_score', 
                 hover_data={'exam_score': ':,'},
                 title='Mean Exam Score by Gender',
                 color='gender',
                 color_discrete_sequence=['#636EFA', '#FFA15A'],
                 labels={'gender': 'Gender', 'exam_score': 'Mean Exam Score'}
                )
st.plotly_chart(fig2, use_container_width=True)

# Brief code explanantion:
st.write(
    "The scatter plot above shows the relationship between hours studied per week and exam scores, "
    "with different colors representing different attendance percentages. The bar chart displays the mean exam scores for each gender, "
    "providing insights into performance differences based on gender. These visualizations help in understanding how attendance and amount of study hours impact exam scores, "
    "as well as gender-based performance differences. It can be observed that students with higher attendance percentages and higher hours studied per week tend to have higher exam scores. "
    "The average exam scores between genders are also similar, indicating that gender may not be a significant factor in exam performance. "
    "This dashboard was built using Streamlit and Plotly for interactive data visualization. "
    "The two interactive elements, the score range slider and attendance percentage multiselect, allow users to filter the data on the scatter plot and explore different subsets interactively. "
    "The data shown when hovering over each gender provides a concise summary of the mean exam scores for that gender."
)

