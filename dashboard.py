import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title='Healthcare Dashboard', layout='wide')

# Hide Streamlit default elements
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {
                padding-top: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title('🩺 Healthcare Dashboard')

# Helper function to clean long diagnosis labels
def clean_label(label):
    if len(label) > 20:
        return label[:17] + "..."  
    return label

@st.cache_data
def get_data():
    df = pd.read_csv('df_sample.csv')
    
    # Create Age Group column if it doesn't exist
    if 'Age Group' not in df.columns:
        # Define age groups
        bins = [0, 12, 19, 39, 59, 100]
        labels = ['Child', 'Teen', 'Young Adult', 'Adult', 'Senior']
        df['Age Group'] = pd.cut(df['AGE'], bins=bins, labels=labels, right=False)
    
    return df

df = get_data()

# Calculate top 15 diagnoses once for all tabs
top_15_diagnoses = df['label_text'].value_counts().head(15).reset_index()
top_15_diagnoses.columns = ['Diagnosis', 'Count']
top_15_diagnoses['Diagnosis'] = top_15_diagnoses['Diagnosis'].apply(clean_label)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    'Overall Diagnosis', 
    'Diagnosis by Gender', 
    'Diagnosis by Age',
    'Diagnosis by Age and Gender'
])

with tab1:
    st.subheader("Overall Diagnosis")

    fig1 = px.bar(top_15_diagnoses, 
                x='Diagnosis', 
                y='Count', 
                title='Top 15 Most Common Diagnoses (Sampled Data)', 
                labels={'Diagnosis': 'Diagnosis', 'Count': 'Count'},
                color='Count',  
                color_continuous_scale='Viridis')

    fig1.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig1)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: This visualization identifies the most prevalent health conditions in our dataset, with the top diagnoses requiring prioritized attention.
        
        **Strategic Value**: Healthcare administrators can use this data to:
        - Allocate resources more effectively toward high-volume conditions
        - Design targeted intervention programs for the most common diagnoses
        - Plan staff training focused on managing frequent conditions
        - Optimize medication and equipment inventory based on actual diagnostic trends
        """)

    diagnoses_gender = df[df['label_text'].isin(top_15_diagnoses['Diagnosis'])]
    diagnoses_gender = diagnoses_gender.groupby(['label_text', 'SEX']).size().reset_index(name='Count')

    fig2 = px.bar(diagnoses_gender, 
                x='label_text', 
                y='Count', 
                color='SEX', 
                title='Distribution of Diagnoses by Gender',
                labels={'label_text': 'Diagnosis', 'Count': 'Count'},
                color_discrete_map={'M': 'blue', 'F': 'pink'},  
                barmode='stack')

    fig2.update_layout(xaxis_tickangle=-45, showlegend=True)

    st.plotly_chart(fig2)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: The gender distribution across diagnoses reveals important patterns that may indicate biological differences, lifestyle factors, or diagnostic biases.
        
        **Clinical Implications**:
        - Diagnoses with significant gender disparities may require tailored treatment protocols
        - Gender-specific risk factors should be incorporated into preventive screening guidelines
        - Patient education materials can be customized to address gender-specific concerns
        - Research funding could be directed toward understanding conditions with notable gender disparities
        """)

    age_diagnoses = df[df['label_text'].isin(top_15_diagnoses['Diagnosis'])]

    fig3 = px.box(age_diagnoses, 
                x='label_text', 
                y='AGE', 
                title='Age Distribution by Diagnosis',
                labels={'label_text': 'Diagnosis', 'AGE': 'Age'},
                color='label_text',  
                color_discrete_sequence=px.colors.qualitative.Set3)

    fig3.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig3)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: This visualization shows the age distribution for major diagnoses, revealing which conditions affect specific age demographics and helping identify outliers.
        
        **Clinical Applications**:
        - Conditions with tight age clustering suggest strong age-related risk factors
        - Wide age distributions indicate conditions that require universal screening approaches
        - Outliers may represent unusual presentations requiring specialized attention
        - Age-specific clinical guidelines can be developed based on the median age for each condition
        - Early onset cases (shown as lower outliers) may benefit from genetic counseling or additional workup
        """)
        
with tab2:
    st.subheader("Diagnosis by Gender")

    gender_diagnoses_count = df[df['label_text'].isin(top_15_diagnoses['Diagnosis'])]
    gender_diagnoses_count = gender_diagnoses_count.groupby(['label_text', 'SEX']).size().reset_index(name='Count')

    gender_diagnoses_count['label_text'] = gender_diagnoses_count['label_text'].apply(clean_label)

    fig4 = px.bar(gender_diagnoses_count, 
                x='label_text', 
                y='Count', 
                color='SEX', 
                title='Gender Distribution for Top 15 Diagnoses', 
                labels={'label_text': 'Diagnosis', 'Count': 'Count'},
                color_discrete_sequence=px.colors.qualitative.Set1, 
                barmode='stack')

    fig4.update_layout(xaxis_tickangle=-45, showlegend=True)

    st.plotly_chart(fig4)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: This visualization quantifies the gender breakdown for each major diagnosis, revealing conditions with significant gender predominance.
        
        **Healthcare Delivery Implications**:
        - Conditions heavily skewed toward one gender may benefit from specialized clinics
        - Provider training should emphasize gender differences in disease presentation
        - Screening programs could be optimized by gender-specific targeting
        - Community outreach efforts could be tailored to address gender-specific health literacy needs
        - Equal representation in clinical trials should be prioritized for conditions affecting both genders
        """)

    age_diagnosis_dist = df.groupby('Age Group').size().reset_index(name='Count')

    fig5 = px.bar(age_diagnosis_dist, 
                x='Age Group', 
                y='Count', 
                title='Age Distribution of Diagnoses', 
                labels={'Age Group': 'Age Group', 'Count': 'Count'},
                color_discrete_sequence=px.colors.qualitative.Set2)

    fig5.update_layout(xaxis_tickangle=-45, showlegend=False)

    st.plotly_chart(fig5)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: This chart reveals the overall health burden across age groups, showing which demographic segments generate the most diagnoses.
        
        **Healthcare Planning Implications**:
        - Age groups with high diagnosis counts indicate populations requiring greater healthcare resources
        - Workforce planning should account for specialties needed to serve the most affected age groups
        - Facility design and accessibility features should prioritize needs of high-volume age demographics
        - Prevention programs can be strategically targeted to address conditions before they peak in higher-risk age groups
        - Healthcare budgeting can be more accurately forecasted based on population age trends
        """)

    gender_diagnosis_dist = df.groupby('SEX').size().reset_index(name='Count')

    fig6 = px.bar(gender_diagnosis_dist, 
                x='SEX', 
                y='Count', 
                title='Gender Distribution of Diagnoses', 
                labels={'SEX': 'Gender', 'Count': 'Count'},
                color='SEX',
                color_discrete_map={'M': '#636EFA', 'F': '#EF553B'})  # Distinct blue for male, red-orange for female

    fig6.update_layout(showlegend=True)

    st.plotly_chart(fig6)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: This visualization shows the overall gender composition of the patient population, providing essential context for interpreting all other gender-related patterns.
        
        **Data Interpretation Value**:
        - Helps distinguish true gender-specific health trends from sampling bias
        - Establishes a baseline for evaluating whether specific conditions are truly overrepresented in a particular gender
        - Informs appropriate statistical adjustments when comparing gender-based outcomes
        - Validates whether the dataset appropriately represents the general population gender distribution
        - Guides recruitment strategies if clinical research will be based on this patient population
        """)

with tab3:
    st.subheader("Diagnosis by Age")

    age_group_diagnoses = df[df['label_text'].isin(top_15_diagnoses['Diagnosis'])]
    age_group_diagnoses = age_group_diagnoses.groupby(['Age Group', 'label_text']).size().reset_index(name='Count')

    age_group_diagnoses['label_text'] = age_group_diagnoses['label_text'].apply(clean_label)

    fig7 = px.bar(age_group_diagnoses, 
                x='Age Group', 
                y='Count', 
                color='label_text', 
                title='Top Diagnoses in Relation to Age Group', 
                labels={'Age Group': 'Age Group', 'Count': 'Count'},
                color_discrete_sequence=px.colors.qualitative.Set3, 
                barmode='stack')

    fig7.update_layout(xaxis_tickangle=-45, showlegend=True)

    st.plotly_chart(fig7)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: This visualization breaks down which specific diagnoses are driving health issues in each age group, revealing the unique health profiles across different life stages.
        
        **Population Health Management Applications**:
        - Each age group shows a distinct diagnostic signature that requires tailored intervention strategies
        - Age-transition points where diagnoses change significantly represent critical intervention opportunities
        - Public health campaigns can be precisely targeted based on age-specific condition prevalence
        - Healthcare facilities serving specific age demographics can optimize their services accordingly
        - Longitudinal tracking of these patterns may reveal emerging health trends in specific age cohorts
        """)

    age_gender_diagnoses = df[df['label_text'].isin(top_15_diagnoses['Diagnosis'])]
    age_gender_diagnoses = age_gender_diagnoses.groupby(['Age Group', 'SEX', 'label_text']).size().reset_index(name='Count')

    age_gender_diagnoses['label_text'] = age_gender_diagnoses['label_text'].apply(clean_label)

    fig8 = px.bar(age_gender_diagnoses, 
                x='Age Group', 
                y='Count', 
                color='SEX', 
                facet_col='label_text', 
                title='Age and Gender Breakdown for Top Diagnoses', 
                labels={'Age Group': 'Age Group', 'Count': 'Count'},
                color_discrete_sequence=px.colors.qualitative.Set1, 
                barmode='stack', 
                facet_col_wrap=3)

    fig8.update_layout(xaxis_tickangle=-45, showlegend=True)

    st.plotly_chart(fig8)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: This detailed breakdown of diagnoses by both age and gender reveals complex demographic patterns that may indicate biological, social, or environmental factors affecting health outcomes.
        
        **Research & Clinical Value**:
        - Conditions showing different age distributions between genders may suggest hormonal influences
        - Similar patterns across multiple conditions could indicate shared risk factors or comorbidities
        - Unexpected patterns may reveal gaps in current screening recommendations
        - Clinical algorithms for disease risk assessment could be refined using these multi-dimensional patterns
        - Unusual distributions warrant targeted epidemiological studies to identify causal factors
        """)

    fig9 = px.histogram(df, 
                    x='AGE', 
                    color='SEX', 
                    title='Age vs Gender Distribution', 
                    labels={'AGE': 'Age', 'SEX': 'Gender'},
                    color_discrete_sequence=px.colors.qualitative.Set1, 
                    nbins=30)

    fig9.update_layout(showlegend=True)

    st.plotly_chart(fig9)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: This histogram reveals the underlying age-gender demographic profile of the entire patient population, which is essential for contextualizing all other analyses.
        
        **Analytical Implications**:
        - Peaks in specific age-gender combinations highlight demographic segments with higher healthcare utilization
        - Gaps or underrepresented groups may indicate access barriers requiring targeted outreach
        - Differences in age distribution between genders may reflect different healthcare-seeking behaviors
        - Life expectancy differences may be reflected in the older age distributions
        - Understanding this baseline demographic is crucial for proper risk adjustment in outcomes research
        """)
    
with tab4:
    st.subheader("Diagnosis by Age and Gender")
    
    # Grouping data by Age Group and Diagnosis
    age_diagnosis = df[df['label_text'].isin(top_15_diagnoses['Diagnosis'])]
    age_diagnosis = age_diagnosis.groupby(['Age Group', 'label_text']).size().reset_index(name='Count')

    # Clean the diagnosis labels for display
    age_diagnosis['label_text'] = age_diagnosis['label_text'].apply(clean_label)

    fig11 = px.box(age_diagnosis, 
               x='label_text', 
               y='Age Group', 
               title='Age Distribution for the Top 15 Diagnoses', 
               labels={'label_text': 'Diagnosis', 'Age Group': 'Age Group'},
               color='label_text', 
               color_discrete_sequence=px.colors.qualitative.Set2)

    fig11.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig11)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: This box plot reveals which age groups are most affected by each diagnosis, showing both typical patterns and exceptions.
        
        **Clinical Decision Support Value**:
        - The median age for each diagnosis provides a critical reference point for clinical suspicion
        - Narrow IQR (box width) indicates strong age correlation that should influence diagnostic reasoning
        - Wide IQR suggests conditions that present across multiple life stages, requiring broader screening
        - Outliers represent atypical presentations that may benefit from more extensive workup
        - This visualization can help clinicians contextualize patient demographics within expected patterns
        """)

    # Grouping data by Gender and Diagnosis
    gender_diagnoses = df[df['label_text'].isin(top_15_diagnoses['Diagnosis'])]
    gender_diagnoses = gender_diagnoses.groupby(['SEX', 'label_text']).size().reset_index(name='Count')

    # Clean the diagnosis labels for display
    gender_diagnoses['label_text'] = gender_diagnoses['label_text'].apply(clean_label)

    fig10 = px.bar(gender_diagnoses, 
               x='label_text', 
               y='Count', 
               color='SEX', 
               title='Top Diagnoses for Each Gender', 
               labels={'label_text': 'Diagnosis', 'Count': 'Count'},
               color_discrete_sequence=px.colors.qualitative.Set1, 
               barmode='group')

    fig10.update_layout(xaxis_tickangle=-45, showlegend=True)

    st.plotly_chart(fig10)

    with st.expander("**Insight**"):
        st.markdown("""
        **Key Finding**: This grouped comparison highlights which conditions show the most significant gender differences, potentially revealing biological vulnerabilities, behavioral factors, or diagnostic biases.
        
        **Healthcare Quality Implications**:
        - Conditions with extreme gender disparities may warrant specialized protocols or facilities
        - Similar rates between genders for typically gender-associated conditions may indicate diagnostic issues
        - Provider education should emphasize awareness of gender differences in disease presentation
        - Screening guidelines should account for demonstrated gender-specific risk profiles
        - Quality metrics may need gender-specific benchmarking for conditions with established biological differences
        """)