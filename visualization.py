import streamlit as st
from utils import prepare_plotly_data, MetricBubbleMapPlots

# Page configuration for wider layout
st.set_page_config(layout="wide")

# Load and preprocess the data
df = prepare_plotly_data("compiled_data.csv")

# Societal Metrics
SocietalMetrics = MetricBubbleMapPlots(df,
            animation_speed=200,
            default_size=2.5,
            time_var="Year",
            unit_var="Country Code",
            class_var="Region",
            x_var="Women with Secondary Education (%)",
            y_var="Labor, Women in Industry & Services (%)",
            z_var="Legislative Representation (%)",
            unit_label="Country Name",
            x_label="% of Women aged 15+ with at least Secondary Education",
            y_label="% of total Labor Force: Women aged 15+ in Industry & Services",
            z_label="% of Legislative seats for Women",
            title="Women's Educational, Economic & Political Representation",
            x_range=[0, 100],
            y_range=[0, 60],
            z_range=[0, 100],
            plot_height=800,
            map_height=450
    )
societal_bubble_chart = SocietalMetrics.bubble_chart()
education_map, labor_map, parliament_map = SocietalMetrics.map_plots()

# Health Metrics
HealthMetrics = MetricBubbleMapPlots(df,
            animation_speed=200,
            default_size=2.5,
            time_var="Year",
            unit_var="Country Code",
            class_var="Region",
            x_var="Maternal Deaths per 100k pregnancies",
            y_var="Births attended by medical staff (%)",
            z_var="Child Deaths per 100k pregnancies",
            unit_label="Country Name",
            x_label="Maternal Deaths per 100k pregnancies",
            y_label="% of total births attended by medical staff",
            z_label="Child Deaths (< 5 years) per 100k pregnancies",
            title="Women's Maternal Health",
            x_range=[0, 1000],
            y_range=[0, 120],
            z_range=[0, 200],
            plot_height=800,
            map_height=450
    )
health_bubble_chart = HealthMetrics.bubble_chart()
maternal_deaths_map, attended_births_map, child_deaths_map = HealthMetrics.map_plots()

# Streamlit app
def main():
    # Dropdown to toggle between the two datasets
    data_type = st.selectbox("Select Data Type", ["Societal Indicators", "Maternal Health Indicators"])

    if data_type == "Societal Indicators":

        col1, col2 = st.columns([2, 3])

        with col1:
            st.plotly_chart(education_map, use_container_width=False)
            st.plotly_chart(labor_map, use_container_width=False)
            st.plotly_chart(parliament_map, use_container_width=False)

        with col2:
            st.plotly_chart(societal_bubble_chart, use_container_width=False)

    elif data_type == "Maternal Health Indicators":

        col1, col2 = st.columns([2, 3])

        with col1:
            st.plotly_chart(maternal_deaths_map, use_container_width=False)
            st.plotly_chart(attended_births_map, use_container_width=False)
            st.plotly_chart(child_deaths_map, use_container_width=False)

        with col2:
            st.plotly_chart(health_bubble_chart, use_container_width=False)

if __name__ == "__main__":
    main()

